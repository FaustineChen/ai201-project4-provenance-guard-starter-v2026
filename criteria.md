# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1.False positives

<!-- Your criterion. It must name a number. -->
 Of 10 human-written pieces I wrote myself:
   - at most 1 is labeled high-confidence AI (false accusation)
   - at least 6 are labeled high-confidence human, so at most 3 can be unsure.


**Why this target:**
No detector is perfect, so I allow one miss, but a wrong accusation costs a writer more than a missed detection.
"Unsure" is the safe failure, but a system that says unsure about everything is useless.


---

## 2.Score spread

<!-- Your criterion. -->
Pair each of my 10 AI-generated texts with each of my 10 human-written texts (100 pairs).
In at least 80% of pairs, the AI text gets the higher combined score.


**Why this target:**
50% is random guessing, so 80% means the signals really separate the groups.
It does not depend on guessing where scores will land.


---

## 3.Label coverage

<!-- Your criterion. -->
Feed scores 0.00 to 1.00 in steps of 0.01 (101 values) into the score-to-label function.
Every score returns exactly one of the three labels (no errors, no empty values), and all three labels appear.


**Why this target:**
this checks the thresholds for gaps or an empty "unsure" range. It needs no text, so it cannot be gamed. Must pass 101 of 101.


---

## 4.The appeal path

<!-- Your criterion. -->
Send an appeal for 10 different valid content_ids. All 10 change to under_review and the reasoning can be read back afterwards. An appeal for a nonexistent content_id returns 404 and creates no record.


**Why this target:**
the appeal is the only way out for a wrongly accused writer, so it must work every time, not 90% of the time.


---

## 5.Bad input

<!-- Your criterion. -->
Missing text, empty text, missing creator_id, and text over 10,000 characters
each return a clear 4xx error (no 500, no crash), and /ping still answers afterwards.


**Why this target:**
Bad input will arrive by accident or on purpose, and the service must stay up.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
