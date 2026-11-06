import re
from stylometry import words, sentences
from scenarios import HUMAN, AI

for i, human in enumerate(HUMAN, 1):
    print("human", i, "words:", len(words(human)), "sentences:", len(sentences(human)))

for i, ai in enumerate(AI, 1):
    print("ai", i, "words:", len(words(ai)), "sentences:", len(sentences(ai)))