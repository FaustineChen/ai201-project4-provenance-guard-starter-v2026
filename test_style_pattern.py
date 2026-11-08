import re
import stylometry as s
# from stylometry import words, sentences
from scenarios import HUMAN, AI

# for i, human in enumerate(HUMAN, 1):
#     print("human", i, "words:", len(s.words(human)), "sentences:", len(s.sentences(human)))

# for i, ai in enumerate(AI, 1):
#     print("ai", i, "words:", len(s.words(ai)), "sentences:", len(s.sentences(ai)))


def raw(t):
    spread = s.clamp((s.CV_HUMAN - s.sentence_length_spread(t)) / (s.CV_HUMAN - s.CV_AI))
    ttr    = s.clamp((s.TTR_HUMAN - s.type_token_ratio(t)) / (s.TTR_HUMAN - s.TTR_AI))
    punct  = s.clamp(s.punctuation_density(t) / s.PUNCT_AI)
    print("spread:", round(spread, 3), "ttr: ", round(ttr, 3), "punct", round(punct, 3))
    return s.WEIGHTS["spread"] * spread + s.WEIGHTS["ttr"] * ttr + s.WEIGHTS["punct"] * punct

for i, human in enumerate(HUMAN, 1):
    r = round(raw(human), 3)

    print("human", i,
          "words:", len(s.words(human)),
          "sentences:", len(s.sentences(human)), 
          "gated:", round(s.style_signal(human), 3), "raw:", r)

for i, ai in enumerate(AI, 1):
    r = round(raw(ai), 3)

    print("ai", i,
          "words:", len(s.words(ai)),
          "sentences:", len(s.sentences(ai)), 
          "gated:", round(s.style_signal(ai), 3), "raw:", r)

