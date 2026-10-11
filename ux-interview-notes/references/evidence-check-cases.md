# Evidence check cases

Synthetic cases for manually reviewing note-generation behavior. These are not
real participants, model evaluation results, or claims of automated enforcement.

## Timestamped source, no ranking

```vtt
WEBVTT

00:00:01.000 --> 00:00:04.000
Interviewer: Which concept would you choose?

00:00:05.000 --> 00:00:08.000
Participant: I like the upload, um, but I need to try both first.
```

Expected: quote the participant exactly, retaining `um`, with `(00:00:05)`.
Report ranking not stated. Liking upload is not an explicit first-choice ranking
or willingness to pay. Any inferred preference must be labeled as researcher
interpretation and keep the need-to-try condition. Do not quote the interviewer's
question as a participant statement.

## Plain text, explicit ranking

```text
Interviewer: What is your ranking?
Participant: Email first, upload second. I would not pay extra for either.
```

Expected: preserve the exact participant quote; put the timestamp-unavailable
notice once at the top. Report the explicit ranking and explicit refusal to pay
extra separately. Do not infer willingness to pay from the first-place ranking.

## Context-dependent reaction

```vtt
WEBVTT

00:00:10.000 --> 00:00:12.000
Interviewer: Here is the upload concept.

00:00:13.000 --> 00:00:15.000
Participant: That would be awesome.
```

Expected: `"That would be awesome." (00:00:13)`, with a context note outside
quote marks explaining that the reaction was to upload. Do not insert the
concept name inside the quote or infer a ranking, regular usage, or payment.
