# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-07 22:58
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `ab1e4913-932c-47db-8ac0-faad2f6634d8` | human | 0.718 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `bbadd39e-28c5-4b25-9702-2d1914c38915` | unsure | 0.543 | HELD |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `87d602ca-0f74-4e38-a8c5-3d6794755a6f` | unsure | 0.517 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `373c7d80-3614-4777-ac02-bc3b6ebc5df7` | unsure | 0.506 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `424a7426-383f-4bb1-be5d-1c22f72d71e8` | human | 0.758 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `2ddf79fc-c5f2-4310-800a-0f233d336ba7` | unsure | 0.590 | HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | `9eaa5f49-7bd4-494d-8308-b6875e90fa6b` | ai | 0.610 | HELD |
| EV08 | evasion | signal one: text below the token window | 200 | `139c3d42-107c-42fa-80a9-0331bb087785` | human | 0.627 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `b021f6fe-bb09-4b86-9e51-17543bc87446` | unsure | 0.555 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `d420931b-3a4a-46b4-ad30-a4e8d49ce996` | unsure | 0.540 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `a15b2984-7439-4b94-a808-77e12bf8ff46` | unsure | 0.574 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `7c4e0ee1-7acb-4d47-a09d-9f0f2b5a74b8` | unsure | 0.540 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `a08774dd-1072-41a3-80a9-7703424b3a8e` | unsure | 0.540 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `3468a434-ac68-4c49-abbd-8f04889a1844` | unsure | 0.540 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `8a2bd0c0-3e67-4f63-82e3-c4780b1c8ff3` | ai | 0.720 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `b67d2f1c-5122-4c11-bfb6-50789fa1ba37` | unsure | 0.540 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `7a37dd9e-50e3-4440-acc3-64b1c36cb729` | unsure | 0.540 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `eee6dab3-b0dd-4ce3-8569-8c5d6441c29c` | human | 0.600 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `06adc520-00c4-490a-9f8f-b56e0ca590b9` | human | 0.754 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `153180f5-31bc-4934-a347-a0407dac4b17` | human | 0.767 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `76c8d0a1-88fd-4cad-adc8-67791d9ae463` | unsure | 0.531 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `cbdefc72-7377-4c89-9583-7097ef76f581` | human | 0.609 | BROKE |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `1dfc6553-1328-490d-a4ae-f52bec4506fc` | unsure | 0.540 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `645a3ef7-f597-4dec-a04b-12418c7949ce` | unsure | 0.589 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `2f655c6e-27bf-4105-89d0-eb7046c932b5` | human | 0.750 | HELD |
| MF04 | malformed | text is only punctuation | 200 | `21d46a88-056a-4ea8-98ff-b66d3b4823c2` | human | 0.744 | HELD |
| MF05 | malformed | text is a very long single word | 200 | `3870247f-e2c0-4b7c-a0ed-9dbde9c8c63a` | unsure | 0.540 | HELD |
| MF06 | malformed | text is emoji only | 200 | `b934a49a-66ff-4b7f-8089-5bf9cb5eac9a` | unsure | 0.540 | HELD |
| MF07 | malformed | text is right-to-left script | 200 | `72b808b9-abc3-4cf1-9db4-9042f0a4327f` | unsure | 0.540 | HELD |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3d0000da-83f9-4fd9-b4bb-dda717d72544` | human | 0.736 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c6dbbd15-312a-470d-af7f-fbd51c76d676` | human | 0.736 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `95875963-3953-4cd2-a8d3-337d64e60489` | human | 0.736 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `22e89bf1-1902-469e-8fa2-f9da11387d0b` | human | 0.736 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `6f337d9a-33df-4ede-b42a-f5cd8fa7aeb4` | human | 0.736 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "ab1e4913-932c-47db-8ac0-faad2f6634d8",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.7183,
  "model_score": 0.1635,
  "style_score": 0.4,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "bbadd39e-28c5-4b25-9702-2d1914c38915",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.5428,
  "model_score": 0.5943,
  "style_score": 0.32,
  "label": "We can't tell whether this was written by a person or with the help of AI. This is not an accusation, and plenty of people's own writing gets this result. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "87d602ca-0f74-4e38-a8c5-3d6794755a6f",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5171,
  "model_score": 0.6662,
  "style_score": 0.2996386996810229,
  "label": "We can't tell whether this was written by a person or with the help of AI. This is not an accusation, and plenty of people's own writing gets this result. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "373c7d80-3614-4777-ac02-bc3b6ebc5df7",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5057,
  "model_score": 0.6114,
  "style_score": 0.4,
  "label": "We can't tell whether this was written by a person or with the help of AI. This is not an accusation, and plenty of people's own writing gets this result. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "424a7426-383f-4bb1-be5d-1c22f72d71e8",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.7585,
  "model_score": 0.3212,
  "style_score": 0.16174172878411203,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "2ddf79fc-c5f2-4310-800a-0f233d336ba7",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.59,
  "model_score": 0.5727,
  "style_score": 0.020000000000000014,
  "label": "We can't tell whether this was written by a person or with the help of AI. This is not an accusation, and plenty of people's own writing gets this result. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "9eaa5f49-7bd4-494d-8308-b6875e90fa6b",
  "creator_id": "attacker_EV07",
  "guess": "ai",
  "confidence": 0.6098,
  "model_score": 0.5862,
  "style_score": 0.6333333333333334,
  "label": "Our checks suggest this may have been written with AI. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "139c3d42-107c-42fa-80a9-0331bb087785",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.6274,
  "model_score": 0.2452,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "b021f6fe-bb09-4b86-9e51-17543bc87446",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5549,
  "model_score": 0.7042,
  "style_score": 0.18597094287554172,
  "label": "We can't tell whether this was written by a person or with the help of AI. This is not an accusation, and plenty of people's own writing gets this result. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "d420931b-3a4a-46b4-ad30-a4e8d49ce996",
  "creator_id": "attacker_EV10",
  "guess": "unsure",
  "confidence": 0.54,
  "model_score": 0.9792,
  "style_score": 0.5448760718823136,
  "label": "We can't tell whether this was written by a person or with the help of AI. This is not an accusation, and plenty of people's own writing gets this result. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "a15b2984-7439-4b94-a808-77e12bf8ff46",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5743,
  "model_score": 0.6175,
  "style_score": 0.23399658628820633,
  "label": "We can't tell whether this was written by a person or with the help of AI. This is not an accusation, and plenty of people's own writing gets this result. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "7c4e0ee1-7acb-4d47-a09d-9f0f2b5a74b8",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.54,
  "model_score": 0.7387,
  "style_score": 0.5077205788235754,
  "label": "We can't tell whether this was written by a person or with the help of AI. This is not an accusation, and plenty of people's own writing gets this result. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "a08774dd-1072-41a3-80a9-7703424b3a8e",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.54,
  "model_score": 0.8051,
  "style_score": 0.3774488969276871,
  "label": "We can't tell whether this was written by a person or with the help of AI. This is not an accusation, and plenty of people's own writing gets this result. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "3468a434-ac68-4c49-abbd-8f04889a1844",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.54,
  "model_score": 0.8329,
  "style_score": 0.3666564809509724,
  "label": "We can't tell whether this was written by a person or with the help of AI. This is not an accusation, and plenty of people's own writing gets this result. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "8a2bd0c0-3e67-4f63-82e3-c4780b1c8ff3",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7195,
  "model_score": 0.8005,
  "style_score": 0.6384900303221848,
  "label": "Our checks suggest this may have been written with AI. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "b67d2f1c-5122-4c11-bfb6-50789fa1ba37",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.54,
  "model_score": 0.8814,
  "style_score": 0.2646688068540961,
  "label": "We can't tell whether this was written by a person or with the help of AI. This is not an accusation, and plenty of people's own writing gets this result. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "7a37dd9e-50e3-4440-acc3-64b1c36cb729",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.54,
  "model_score": 0.8816,
  "style_score": 0.3,
  "label": "We can't tell whether this was written by a person or with the help of AI. This is not an accusation, and plenty of people's own writing gets this result. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "eee6dab3-b0dd-4ce3-8569-8c5d6441c29c",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.6,
  "model_score": 0.3223,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "06adc520-00c4-490a-9f8f-b56e0ca590b9",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.7538,
  "model_score": 0.4625,
  "style_score": 0.02987632470232838,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "153180f5-31bc-4934-a347-a0407dac4b17",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.7674,
  "model_score": 0.2044,
  "style_score": 0.26075420892812873,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "76c8d0a1-88fd-4cad-adc8-67791d9ae463",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5308,
  "model_score": 0.5943,
  "style_score": 0.46737509434017155,
  "label": "We can't tell whether this was written by a person or with the help of AI. This is not an accusation, and plenty of people's own writing gets this result. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "cbdefc72-7377-4c89-9583-7097ef76f581",
  "creator_id": "attacker_PI04",
  "guess": "human",
  "confidence": 0.6088,
  "model_score": 0.4998,
  "style_score": 0.2826354843295474,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "1dfc6553-1328-490d-a4ae-f52bec4506fc",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.54,
  "model_score": 0.6401,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or with the help of AI. This is not an accusation, and plenty of people's own writing gets this result. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "645a3ef7-f597-4dec-a04b-12418c7949ce",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.589,
  "model_score": 0.5583,
  "style_score": 0.2636539100411502,
  "label": "We can't tell whether this was written by a person or with the help of AI. This is not an accusation, and plenty of people's own writing gets this result. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "2f655c6e-27bf-4105-89d0-eb7046c932b5",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.75,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "21d46a88-056a-4ea8-98ff-b66d3b4823c2",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.7444,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "3870247f-e2c0-4b7c-a0ed-9dbde9c8c63a",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.54,
  "model_score": 0.9976,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or with the help of AI. This is not an accusation, and plenty of people's own writing gets this result. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "b934a49a-66ff-4b7f-8089-5bf9cb5eac9a",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.54,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or with the help of AI. This is not an accusation, and plenty of people's own writing gets this result. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "72b808b9-abc3-4cf1-9db4-9042f0a4327f",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.54,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or with the help of AI. This is not an accusation, and plenty of people's own writing gets this result. If you wrote it yourself, you can appeal and your appeal will be recorded and marked for review.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "3d0000da-83f9-4fd9-b4bb-dda717d72544",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7357,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "c6dbbd15-312a-470d-af7f-fbd51c76d676",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7357,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "95875963-3953-4cd2-a8d3-337d64e60489",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7357,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "22e89bf1-1902-469e-8fa2-f9da11387d0b",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7357,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "6f337d9a-33df-4ede-b42a-f5cd8fa7aeb4",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7357,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
