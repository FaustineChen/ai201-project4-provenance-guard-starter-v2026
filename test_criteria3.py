from scoring import score_to_label

labels = [score_to_label(round(i / 100, 2)) for i in range(101)]
print(len(labels), set(labels))   # expect 101, 3