"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics

MIN_WORDS = 40          # less then 40 words -> not enough signal, return 0.5
MIN_SENTENCES = 4       # same as above
TTR_WINDOW = 50         # TTR only count first 50 words to avoid the impact of long paragraph
CV_HUMAN, CV_AI = 0.70, 0.20     # coefficient of variance of length of sentence:>=0.70 human,<=0.20 AI
TTR_HUMAN, TTR_AI = 0.90, 0.60   # TTR:>=0.90 humna,<=0.60 AI
PUNCT_AI = 3.0                   # every qoo words, more than 3 em dash, colon, semicolon, more like AI
WEIGHTS = {"spread": 0.4, "ttr": 0.3, "punct": 0.3}


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())

def clamp(x: float) -> float:
    return max(0.0, min(1.0, x))

# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

#  Scale: 0 and up. HIGHER = more human-like.
#  Fewer than 2 sentences: returns 0.0 as a placeholder, NOT a real measurement.
def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies. ← TODO

    Returns:
        A float. Decide yourself what scale it's on and which direction means
        "more human" — then write that down, because your combining rule
        depends on knowing it.

    A hint on what you're reaching for: the standard deviation of sentence
    lengths, probably divided by the mean so a long text and a short one are
    comparable. `statistics.stdev` is imported for you.

    Watch the edge case: a one-sentence submission has no spread at all, and
    `stdev` raises on fewer than two values. Decide what that should return
    before the attack set decides for you.
    """
    lengths = [len(words(s)) for s in sentences(text)]

    # statistics.stdev need at least two numbers
    if len(lengths) < 2:
        return 0.0

    mean = statistics.mean(lengths)
    if mean == 0:
        return 0.0

    return statistics.stdev(lengths) / mean

# Unique words / total words, measured on the first TTR_WINDOW words
# so texts of different lengths are comparable.
# Scale: 0 to 1. HIGHER = more varied vocabulary = more human-like.
def type_token_ratio(text: str) -> float:
    """
    Unique words over total words. ← TODO

    Returns:
        A float between 0 and 1. Higher means more varied vocabulary.

    Worth knowing before you rely on it: this measure falls as text gets
    longer, because common words repeat. Two texts of different lengths aren't
    directly comparable on it, and if your test inputs vary a lot in length,
    that alone can look like a signal.
    """
    words_window = words(text)[:TTR_WINDOW]

    if not words_window:
        return 0.0
  
    return len(set(words_window)) / len(words_window)

# Em/en dashes, colons and semicolons per 100 words.
# Scale: 0 and up. HIGHER = more AI-like
def punctuation_density(text: str) -> float:
    """
    How much punctuation, relative to length. ← TODO

    Returns:
        A float. Whether you count all punctuation or only some kinds — commas,
        semicolons, dashes — is a real choice. Semicolons and em dashes are
        more interesting than full stops, because they vary more between
        writers.
    """
    n_words = len(words(text))
    if n_words == 0:
        return 0.0
    
    marks = len(re.findall(r"[—–:;]|--", text))

    return marks / n_words * 100


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.** ← TODO
    Returns 0.5 when the text is too short to measure.

    Combine your three measures into one number. Same direction as
    `detector.model_signal`, so that `scoring.combine_signals` can treat them
    the same way — if one of your signals runs backwards, everything above it
    is wrong in a way that's hard to see.

    Two things to decide and write down:

      1. Which direction each measure points. Low spread means more AI-ish, so
         it needs flipping. Work out which of your three need that.
      2. How to get each onto a comparable scale. A raw type-token ratio sits
         between 0 and 1; a raw punctuation count doesn't. Adding them
         unscaled means whichever has the bigger numbers wins by default.

    Test it on the four calibration inputs from Milestone 4 — clearly AI,
    clearly human, plain conventional human writing, lightly-edited AI — before
    you trust it. Plain and ordinary, not formal: formal prose reads as *human*
    to signal one, and it is plain writing that gets accused.
    """
    if len(words(text)) < MIN_WORDS or len(sentences(text)) < MIN_SENTENCES:
        return 0.5
    
    spread_ai = clamp((CV_HUMAN - sentence_length_spread(text)) / (CV_HUMAN - CV_AI))
    ttr_ai = clamp((TTR_HUMAN - type_token_ratio(text)) / (TTR_HUMAN - TTR_AI))
    punct_ai = clamp(punctuation_density(text) / PUNCT_AI)

    return (WEIGHTS["spread"] * spread_ai
            + WEIGHTS["ttr"] * ttr_ai
            + WEIGHTS["punct"] * punct_ai)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
    print("\nAll zeros? These are stubs — Milestone 4 is where you build them.")
