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

```
python -c "import scoring; [print(l, r) for l, r in scoring.label_ranges()]"
```

high-confidence human 0.00 – 0.40
unsure 0.40 – 0.55
high-confidence AI 0.55 – 1.00
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
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

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



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



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
