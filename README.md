# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

Provenance Guard takes a piece of text and says whether it was probably written
by a person or with AI, how sure it is, and what the writer reads. If the
system is not sure, it says so instead of accusing anyone.

A submission passes through these steps:

1. **Request arrives** at `POST /submit` with `text` and `creator_id`. Valid input gets a new `content_id`.
2. **Model signal** (`detector.py`): a local language model scores how predictable the text is. Adds `model_score` (0-1, higher = more AI-like).
3. **Style signal** (`stylometry.py`): measures sentence-length spread, vocabulary variety and punctuation, without reading meaning.
Adds `style_score` (0-1). Text under 4 sentences or 40 words returns 0.5.
4. **Combine** (`scoring.py::combine_signals`): each signal is sorted into human, unsure or AI, and high-confidence AI needs both to agree. Adds
   `combined_score`.
5. **Label** (`scoring.py::score_to_label`): the combined score becomes one of three plain-English labels and a `guess` (`ai`, `human`, `unsure`).
6. **Log** (`audit.py`): the decision and both signal scores are written to `logs/audit.jsonl` with status `decided`.
7. **Response**: JSON with `content_id`, `guess`, `confidence`, `label`, and both signal scores.

If a writer disagrees, `POST /appeal` with the `content_id` and their reasoning
records the appeal next to the original decision and moves the item to
`under_review`. Nothing is re-checked automatically.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:**
Perplexity under a local language model (gpt2): how predictable the text is
to the model. ( 0–1 score, higher means more likely AI)
It measures predictability, not authorship.

**Why that might differ between human and AI writing:**
LLM generates text by repeatedly choosing likely next words, so
its output tends to be easy for another model to predict as AI.
Human writing tends to include more surprising wording, abrupt turns,
and specific details, which raises perplexity.

**What it can't see:**
Who really wrote the text. 
The detector only measures how predictable the text is. Simple words and short, plain sentences are very predictable, so
they get a high "AI" score. But many real people write this way (for example, people writing in a second language).
In my test, a plain human paragraph scored 0.7, close to the AI samples. So the detector can wrongly accuse real writers.

### Signal two — the style signal

**What it measures:**
The shape of the text, without reading its meaning. Three measures:
sentence-length spread (standard deviation divided by mean sentence length),
type-token ratio (unique words divided by total words), and punctuation
density (em dashes, colons and semicolons per 100 words). Each is converted
to a 0-1 score where higher means more AI-like, then combined into one score.

**Why that might differ between human and AI writing:**
Generated prose tends toward even, mid-length sentences and a narrower
vocabulary, because "most likely next word" produces that on average.
Human writing is more varied punctuation habits.

**What it can't see:**
What the text says. Anything that changes the shape without changing the
substance moves the score: adding typos, splitting or merging sentences,
pasting in a quotation, or telling an AI to "vary your sentence length and
avoid dashes".
It is also unreliable on short text such as poems: with few
sentences, the spread is meaningless, and type-token ratio looks high
simply because there are few words to repeat.
Poems also break the assumptions behind the measures (line breaks instead of sentences,
little punctuation by design).
A plainly written, regular human writer can look
machine-like. Below a minimum length, this signal returns 0.5 and is marked
"insufficient data" rather than guessing.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:**

Each signal is first sorted into one of three states: points to human, unsure, or points to AI. The two states are then combined:

| model signal | style signal | Result |
|---|---|---|
| AI | AI | Weighted average of the two scores (labeled AI if it reaches the AI threshold) |
| human | human | Weighted average of the two scores (labeled human if it falls under the human threshold) |
| human | unsure | Human |
| AI | human | Unsure |
| unsure | unsure | Unsure |
| AI | unsure | Unsure |

A text is called high-confidence AI only when both signals independently point to AI.
One signal is never enough, because a wrong accusation costs a writer more than a missed detection. I accept that this lets some AI text through.

If the text is too short for the style signal (under 4 sentences or under 40 words), the style signal returns 0.5.
That falls in its "unsure" range, so short text can never be called high-confidence AI.

**The numbers:**
- model signal: human below 0.50, unsure 0.50 to 0.55, AI at 0.55 or above
- style signal: human at 0.30 or below, unsure 0.30 to 0.55, AI at 0.55 or above
- The style AI cutoff must stay above 0.5, which is the "too short" value.
- weights for the average: 0.5 model, 0.5 style
- final score to label: `HUMAN_THRESHOLD` 0.40 or below is human, `AI_THRESHOLD` 0.55 or above is AI, anything between is unsure
- when the rule says "unsure" or "human", the output score is pushed into that label's range (unsure: kept between 0.41 and 0.54), so the label always matches the rule
- These numbers come from 11 calibration texts. They are starting values, not statistical results.


**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**
A human-written 9-sentence text scored 0.554 on the model signal (as AI-like as my AI samples, which scored 0.56 to 0.79) but 0.229 on the style signal, which clearly says human. The model signal alone cannot separate this writer from AI.
My rule treats AI plus human as disagreement and returns unsure, so the writer is not accused.

A near miss: a plain, evenly written 7-sentence human text scored 0.699 on the model signal and exactly 0.50 on the style signal, which is a real calculated value, not the "too short" default.
It stayed unsure only because the style signal was 0.05 below its AI cutoff. Plain, regular human writing is where this system is most likely to be wrong.


---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.40 | "We think this was probably written by a person." |
| unsure | 0.40 – 0.55 | "We can't tell whether this was written by a person or with the help of AI. This is not an accusation, and plenty of people's own writing gets this result. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review." |
| high-confidence AI | 0.55 – 1.00 | "Our checks suggest this may have been written with AI. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review." |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

The person reading it may have written every word themselves, so it starts with what the system does not know, not with a guess about them.
It says outright that this is not an accusation, because "can't tell" can still sound like "we suspect you". It also says that this result is common for honest writers.
It ends with the appeal option so the reader has something to do next.

```bash
python -c "import scoring; [print(l, r) for l, r in scoring.label_ranges()]"
```
```
high-confidence human 0.00 – 0.40
unsure 0.40 – 0.55
high-confidence AI 0.55 – 1.00
```
---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$n = 0
$item = (Get-Content body.json -Raw -Encoding utf8 | ConvertFrom-Json)[$n]
$tmp = New-TemporaryFile
[System.IO.File]::WriteAllText($tmp, ($item | ConvertTo-Json -Compress), (New-Object System.Text.UTF8Encoding($false)))
curl.exe -X POST http://127.0.0.1:9000/submit -H "Content-Type: application/json" --data-binary "@$tmp"
Remove-Item $tmp
```

```json
{
  "combined_score": 0.44179049445310137,
  "confidence": 0.5582,
  "content_id": "1f6676ff-a205-4a54-a8ba-7af0f7172759",
  "guess": "unsure",
  "label": "We can't tell whether this was written by a person or with the help of AI. This is not an accusation, and plenty of people's own writing gets this result. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review.",
  "model_score": 0.5614,
  "style_score": 0.3221809889062027
}

```

**An appeal**

```bash
$ curl.exe -X POST http://127.0.0.1:9000/appeal -H "Content-Type: application/json" -d '{\"content_id\": \"1f6676ff-a205-4a54-a8ba-7af0f7172759\", \"reasoning\": \"I wrote this myself.\"}'
```

```json
{
  "content_id": "1f6676ff-a205-4a54-a8ba-7af0f7172759",
  "message": "Your appeal has been recorded and this item is now marked for review.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl.exe "http://127.0.0.1:9000/log?limit=3"
```

```json
{
  "count": 3,
  "entries": [
    {
      "combined_score": 0.22518718909421653,
      "content_id": "84c1144b-a89a-4052-ae75-7165bcc8b402",
      "creator_id": "u1",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.3046,
      "status": "decided",
      "style_score": 0.14577437818843306,
      "timestamp": "2026-10-30T19:06:22+00:00"
    },
    {
      "combined_score": 0.54,
      "content_id": "688525a4-a3e8-4984-a8af-d37e17b1d6d4",
      "creator_id": "u1",
      "guess": "unsure",
      "label": "We can't tell whether this was written by a person or with the help of AI. This is not an accusation, and plenty of people's own writing gets this result. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review.",
      "model_score": 0.6986,
      "status": "decided",
      "style_score": 0.5,
      "timestamp": "2026-10-30T19:06:37+00:00"
    },
    {
      "content_id": "1f6676ff-a205-4a54-a8ba-7af0f7172759",
      "creator_id": "u1",
      "event": "appeal",
      "reasoning": "I wrote this myself.",
      "status": "under_review",
      "timestamp": "2026-10-30T19:12:24+00:00"
    }
  ]
}

```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
I didn't understand what a "score spread" criterion meant or how one would be written before I had built anything.
I asked what it checks and roughly how to write one.

- *What came back:*
An explanation that it checks whether the signals separate clearly-AI from clearly-human text, with example targets such as "the average AI score is at least 0.3 above the average human score", plus a version that compared AI scores to the lowest human score.

- *What I changed:*
I noticed that comparing against the lowest human score is almost impossible to fail, and "at most 1 human labeled AI" would still pass if the system labeled everything unsure, so I added a minimum number of pieces labeled human.


**Moment 2**

- *What I asked for:*
The possible ways to combine the model signal and the style signal when they disagree.

- *What came back:*
A weighted average, and a suggestion that high-confidence AI should require both signals to agree.

- *What I changed:*
I decided that one signal saying AI and the other unsure should end up as unsure, because a false accusation costs more than a missed detection.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** _5_ per minute, _20_ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->
5 per minute covers rapid revise-and-resubmit without friction, and 20 per day 
is well above what one person needs for theirown work. 
A script probing for the detector's boundary needs 20/day from one creator_id takes about 50 days, 
slow enough to stand out in the audit log. 
The daily cap is what hurts the attacker; the per-minute cap only stops bursts. 
These limits do not stop a script that rotates creator_id.


**What a caller counts as:** <!-- per address, or per creator_id? They fail
     differently — one script can look like a thousand callers, and one household
     can look like one. -->
Per creator_id (falls back to remote address if missing or invalid).  
The weakness: creator_id is self-declared, so a script can send a new one with every request and never hit a limit, looking like a thousand callers.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
15 submissions as 'flood_tester' against http://127.0.0.1:9000
The first one is slow while the model loads.

  [ 1/15] 200
  [ 2/15] 200
  [ 3/15] 200
  [ 4/15] 200
  [ 5/15] 200
  [ 6/15] 429
  [ 7/15] 429
  [ 8/15] 429
  [ 9/15] 429
  [10/15] 429
  [11/15] 429
  [12/15] 429
  [13/15] 429
  [14/15] 429
  [15/15] 429

============================================================
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
============================================================

10 of 15 were rate limited.

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json
{"timestamp": "2026-11-05T01:35:28+00:00", "content_id": "9da3aa88-f1bb-4454-9036-dff3ae78d3fb", "creator_id": "attacker_EV01", "guess": "human", "model_score": 0.1635, "style_score": 0.4, "combined_score": 0.28175, "label": "We think this was probably written by a person.", "status": "decided"}

{"timestamp": "2026-11-05T01:35:29+00:00", "content_id": "d3ebc308-4328-42b5-b330-74fa18a66d2c", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.3212, "style_score": 0.16174172878411203, "combined_score": 0.241470864392056, "label": "We think this was probably written by a person.", "status": "decided"}

{"timestamp": "2026-11-05T01:35:29+00:00", "content_id": "53eee5b7-4e9c-4715-b823-eda4bb6cba67", "creator_id": "attacker_EV08", "guess": "human", "model_score": 0.2452, "style_score": 0.5, "combined_score": 0.3726, "label": "We think this was probably written by a person.", "status": "decided"}

{"timestamp": "2026-11-05T01:35:30+00:00", "content_id": "5d49a1c4-c0d3-4732-a803-36a15d6f618e", "creator_id": "attacker_FP05", "guess": "ai", "model_score": 0.8005, "style_score": 0.6384900303221848, "combined_score": 0.7194950151610924, "label": "Our checks suggest this may have been written with AI. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review.", "status": "decided"}

{"timestamp": "2026-11-05T01:35:30+00:00", "content_id": "8cba7a3f-b6c7-4ca6-8002-899b8611f1b9", "creator_id": "attacker_FP08", "guess": "human", "model_score": 0.3223, "style_score": 0.5, "combined_score": 0.4, "label": "We think this was probably written by a person.", "status": "decided"}

{"timestamp": "2026-11-05T01:35:30+00:00", "content_id": "200220fe-d4a3-4c4a-b07e-79cadf995aa6", "creator_id": "attacker_PI01", "guess": "human", "model_score": 0.4625, "style_score": 0.02987632470232838, "combined_score": 0.2461881623511642, "label": "We think this was probably written by a person.", "status": "decided"}

{"timestamp": "2026-11-05T01:35:30+00:00", "content_id": "a1b46e7d-4f17-4e69-97a0-71365934138f", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.26075420892812873, "combined_score": 0.23257710446406438, "label": "We think this was probably written by a person.", "status": "decided"}

{"timestamp": "2026-11-05T01:35:31+00:00", "content_id": "68c7eab8-fd5d-436c-88a7-754d7b15da95", "creator_id": "attacker_PI04", "guess": "human", "model_score": 0.4998, "style_score": 0.2826354843295474, "combined_score": 0.3912177421647737, "label": "We think this was probably written by a person.", "status": "decided"}

{"timestamp": "2026-11-05T01:35:32+00:00", "creator_id": "unknown", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute", "status_code": 429}

{"timestamp": "2026-11-05T01:35:33+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute", "status_code": 429}


```
RQ10 and RQ11 returned 429 in the run. Neither body is parseable as JSON, so
neither had a usable creator_id and both counted against the shared
remote-address bucket, which earlier malformed requests had already used up.
They never reached submit(), so the run did not test how the route handles
form-encoded or text/plain bodies.
I re-sent both after the limit window reset:
``` json
RQ10 400 {
  "error": "bad_request",
  "message": "text is required to be a non-empty string"
}

RQ11 400 {
  "error": "bad_request",
  "message": "text is required to be a non-empty string"
}
```

MF02 and RQ07 returned 500 and left no audit entry: the crash happened before
any logging ran, so in the original run they were invisible in the log.


**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:
FP05 (`5d49a1c4-c0d3-4732-a803-36a15d6f618e`): technical documentation written
by a person was labeled `ai` with confidence 0.720 (model_score 0.8005, style_score
0.6385). This is the one false accusation in the run. 
The label is the strongest one the system gives, so the writer's
only recourse is to appeal, and I could not explain to them why plain
documentation looked like AI.

**Diagnoses**

Pattern: model reads unusual AI-style text as human, and the combining rule turns that into a confident label.
- Six evasion/injection inputs came back human: EV01, EV05, EV08, PI01, PI02, PI04. All six have model_score <= 0.50 (0.16, 0.32, 0.25, 0.46, 0.20, 0.4998).
- All ten other evasion/injection inputs have model_score >= 0.55 and stayed unsure.
- Typos, pasted fragments, injected sentences and very short text are less predictable to the language model, so it scores them as human.
- The rule then makes it final: human + human averages to a confident human (EV05, PI01, PI02, PI04), and human + unsure returns human (EV01 and EV08, style 0.40 and 0.5).
- no evasion input was labeled ai. "Held" here means unsure.

The route: no 500 crash produced an audit entry
- MF02: text is too short to score
- RQ07: body is a JSON array, not an object

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False positives | 10 human-written, at most 1 is labeled high-confidence AI, at least 6 are labeled high-confidence human | 5 unsure, 5 human | 5 unsure, 5 human | 5 unsure, 5 human | MISSED |
| 2. Score spread | 100 pairs (10 AI × 10 human): AI text has the higher combined score in at least 80% of pairs | 68/100 | 68/100 | 68/100 | MISSED |
| 3. Label coverage | Every score returns exactly one of the three labels, and all three labels appear. | 3/3 | 3/3 | 3/3 | MET |
| 4. The appeal path | All 10 appeals change to under_review and the reasoning can be read back. An appeal for a nonexistent content_id returns 404 and creates no record. | 10/10 | 10/10 | 10/10 | MET |
| 5. Bad input | return a clear 4xx error (no 500, no crash) | 5/5 | 5/5 | 5/5 | MET |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

Produced by `run_eval.py` (trial 1, scenario "my own writing", text 1), saved
in `results/run_2026-11-05_2131_before.md`. The service function that built the response is
`app.py::submit`.

```json
{
     "status": 200,
     "guess": "unsure",
     "confidence": 0.5315,
     "model_score": 0.8107,
     "style_score": 0.2522957725138764,
     "label": "We can't tell whether this was written by a person or with the help of AI. This is not an accusation, and plenty of people's own writing gets this result. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review.",
     "sent": "Remote work has fundamentally transformed the modern workplace, offeri"
}

```

**Criterion 3 (label coverage)**: produced by `test_criteria3.py`, calling
`python test_criteria3.py` for 0.00 to 1.00 in steps of 0.01.
```
101 {('unsure', "We can't tell whether this was written by a person or with the help of AI. This is not an accusation, and plenty of people's ownwriting gets this result. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review."), ('human', 'We thinkthis was probably written by a person.'), ('ai', 'Our checks suggest this may have been written with AI. If you wrote it yourself, you can appealand your appeal will be recorded and marked for review.')}
```

**Criterion 4 (appeal path)**: produced by `test_criteria4.py`.
```
appeals recorded: 10 / 10
under_review: 10 / 10
with reasoning: 10 / 10
404 test: 404 | appeal records before/after: 11 11
```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

**Criterion 1 (5/10 high-confidence human, needed 6): model.**
Model: 5 of my 10 pieces scored model_score >= 0.55 (0.64, 0.72, 0.66, 0.68, 0.56) read half of my own writing as AI.
Style: did not confirm (0.28, 0.5, 0.5, 0.5, 0.38), so the rule sent them to unsure: 0 false accusations, 5 unsure.
The rule worked as designed; the miss comes from style signal's false-positive rate at the 0.55 cutoff.

**Criterion 2 (68/100, needed 80): combining rule.**
model_score alone ranks 91 of 100 pairs correctly; combined_score ranks 68.
When the signals do not both agree, the rule clamps the score into 0.41-0.54,
so 7 of 10 AI texts and 3 of 10 human texts all landed on exactly 0.54 (21 ties, which do not count as AI higher).
The clamp keeps the label right but destroys the ordering.

**Pattern: sometimes Style Model says almost nothing, so signal one decides alone.**
- style_score was exactly 0.5 (the sentence or word too-short default) on 11 of my 20 eval texts (8 of 10 human, 3 of 10 AI).
- It never reached 0.55 on any of the 20, so none of the 10 AI texts could satisfy "both signals say AI".
- Style alone ranks the AI text higher in only 14 of 100 pairs.


---

## The Improvement

**What I changed:**
In `stylometry.py::style_signal`, the 0.5 "not enough evidence" return now happens only below 40 words. With 40 or more words but fewer than 4 sentences, sentence-length spread is skipped and the style score uses type-token ratio and punctuation density only, with their weights rescaled to sum to 1 (0.5 each). Texts with 4 or more sentences are scored as before.

**Which diagnosis pointed at it:**
10 of my 20 eval texts (8 of 10 human, 2 of 10 AI) had at least 40 words but only 2 or 3 sentences, so the old OR gate returned 0.5 and the style signal said nothing on them. Spread is the only feature that needs several sentences to mean anything; the other two only need enough words. The change gives each feature its own minimum evidence instead of silencing the whole signal.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json
{"timestamp": "2026-11-08T03:58:29+00:00", "content_id": "ab1e4913-932c-47db-8ac0-faad2f6634d8", "creator_id": "attacker_EV01", "guess": "human", "model_score": 0.1635, "style_score": 0.4, "combined_score": 0.28175, "label": "We think this was probably written by a person.", "status": "decided"}

{"timestamp": "2026-11-08T03:58:30+00:00", "content_id": "424a7426-383f-4bb1-be5d-1c22f72d71e8", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.3212, "style_score": 0.16174172878411203, "combined_score": 0.241470864392056, "label": "We think this was probably written by a person.", "status": "decided"}

{"timestamp": "2026-11-08T03:58:30+00:00", "content_id": "139c3d42-107c-42fa-80a9-0331bb087785", "creator_id": "attacker_EV08", "guess": "human", "model_score": 0.2452, "style_score": 0.5, "combined_score": 0.3726, "label": "We think this was probably written by a person.", "status": "decided"}

{"timestamp": "2026-11-08T03:58:31+00:00", "content_id": "8a2bd0c0-3e67-4f63-82e3-c4780b1c8ff3", "creator_id": "attacker_FP05", "guess": "ai", "model_score": 0.8005, "style_score": 0.6384900303221848, "combined_score": 0.7194950151610924, "label": "Our checks suggest this may have been written with AI. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review.", "status": "decided"}

{"timestamp": "2026-11-08T03:58:32+00:00", "content_id": "eee6dab3-b0dd-4ce3-8569-8c5d6441c29c", "creator_id": "attacker_FP08", "guess": "human", "model_score": 0.3223, "style_score": 0.5, "combined_score": 0.4, "label": "We think this was probably written by a person.", "status": "decided"}

{"timestamp": "2026-11-08T03:58:32+00:00", "content_id": "06adc520-00c4-490a-9f8f-b56e0ca590b9", "creator_id": "attacker_PI01", "guess": "human", "model_score": 0.4625, "style_score": 0.02987632470232838, "combined_score": 0.2461881623511642, "label": "We think this was probably written by a person.", "status": "decided"}

{"timestamp": "2026-11-08T03:58:32+00:00", "content_id": "153180f5-31bc-4934-a347-a0407dac4b17", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.26075420892812873, "combined_score": 0.23257710446406438, "label": "We think this was probably written by a person.", "status": "decided"}

{"timestamp": "2026-11-08T03:58:32+00:00", "content_id": "cbdefc72-7377-4c89-9583-7097ef76f581", "creator_id": "attacker_PI04", "guess": "human", "model_score": 0.4998, "style_score": 0.2826354843295474, "combined_score": 0.3912177421647737, "label": "We think this was probably written by a person.", "status": "decided"}

{"timestamp": "2026-11-08T03:58:32+00:00", "content_id": "2f655c6e-27bf-4105-89d0-eb7046c932b5", "creator_id": "attacker_MF03", "guess": "human", "model_score": 0.0, "style_score": 0.5, "combined_score": 0.25, "label": "We think this was probably written by a person.", "status": "decided"}


{"timestamp": "2026-11-08T03:58:34+00:00", "creator_id": "attacker_RQ12", "event": "rejected", "status": "rejected", "reason": "empty_text", "status_code": 400}
```

**The single worst outcome** — same as attack before, FP05 technical documentation written
by a person was still labeled `ai`.

---

## Run Log and Verdicts

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False positives | 10 human-written, at most 1 is labeled high-confidence AI, at least 6 are labeled high-confidence human | 5 unsure, 4 human, 1 ai | 5 unsure, 4 human, 1 ai | 5 unsure, 4 human, 1 ai | MISSED |
| 2. Score spread | 100 pairs (10 AI × 10 human): AI text has the higher combined score in at least 80% of pairs | 83/100 | 83/100 | 83/100 | MET |
| 3. Label coverage | Every score returns exactly one of the three labels, and all three labels appear. | 3/3 | 3/3 | 3/3 | MET |
| 4. The appeal path | All 10 appeals change to under_review and the reasoning can be read back. An appeal for a nonexistent content_id returns 404 and creates no record. | 10/10 | 10/10 | 10/10 | MET |
| 5. Bad input | return a clear 4xx error (no 500, no crash) | 5/5 | 5/5 | 5/5 | MET |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

Produced by `run_eval.py` (trial 1, scenario "my own writing", text 1), saved
in `results/run_2026-11-07_2259_after.md`. The service function that built the response is
`app.py::submit`.

```json
{
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5545,
    "model_score": 0.7244,
    "style_score": 0.1666666666666666,
    "label": "We can't tell whether this was written by a person or with the help of AI. This is not an accusation, and plenty of people's own writing gets this result. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review.",
    "sent": "For the project, we sometimes allow certain third-party components and"
  }

```

**Criterion 3 (label coverage)**: produced by `test_criteria3.py`, calling
`python test_criteria3.py` for 0.00 to 1.00 in steps of 0.01.
```
101 {('unsure', "We can't tell whether this was written by a person or with the help of AI. This is not an accusation, and plenty of people's ownwriting gets this result. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review."), ('human', 'We thinkthis was probably written by a person.'), ('ai', 'Our checks suggest this may have been written with AI. If you wrote it yourself, you can appealand your appeal will be recorded and marked for review.')}
```

**Criterion 4 (appeal path)**: produced by `test_criteria4.py`.
```
appeals recorded: 10 / 10
under_review: 10 / 10
with reasoning: 10 / 10
404 test: 404 | appeal records before/after: 21 21
```


**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

**run attack**
- Of the 29 attack inputs that reach scoring, 28 are identical to the first run: same label and same model and style scores.
- The only input that changed is EV07 (evasion): its style score went from 0.500 to 0.633, and the label from unsure to ai.
- Nothing else move. The change was narrow on this set because most attack texts either have at least 4 sentences or fewer than 40 words, so the gate did not apply to them.

**run eval**
- After the style change: criterion 2 went from 68/100 (21 ties) to 83/100 (0 ties), meeting the 80% target.
     - because the style score no longer sits at the neutral 0.5, which removed the ties at 0.54
     - not because the style signal became informative
- Criterion 1 got worse: my own writing is now 1 ai / 4 human / 5 unsure (was 0 / 5 / 5).
     - Human 3 was labeled ai (model 0.66, style 0.60), the first false accusation in the evaluation, and human 7 moved from human to unsure because the new style score (0.72) disagrees with its human model score (0.095).

---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->
**Criterion 1 (1 ai / 4 human / 5 unsure; target is at most 1 ai and at least 6 human).** 
I would recalibrate the model signal's 0.55 line and the style
signal's TTR and punctuation cutoffs on a separate set of human writing that includes formal and non-native English. I stopped because the only labeled texts I have are the ten I test on, so any threshold I moved would be fitted to the test.

**Root cause: the style signal barely separates the groups.** Its mean is 0.31 for AI and 0.28 for human, and the spread inside each group (AI 0.03 to 0.50, human 0.00 to 0.72) is larger than the gap between them. I suspect (untested) that formal writing and non-native English raise human scores. Fixing it means rebuilding the features and validating them on more samples than I have.


**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->
I would keep requiring both signals before accusing anyone, so fewer writers are wrongly accused and more AI text gets through unlabeled. The cost falls on readers and on writers whose own work competes with that unlabeled AI text, rather than on a writer who must prove through an appeal that their own work is theirs.


<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
