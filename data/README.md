# The datasets

**All of this is made up.** Both files were generated for the exercises, with
mistakes planted in them on purpose so there is something to find. No real
participant data is in this repository, and none should be added to it — the
`.gitignore` blocks the obvious kinds (`.wav`, `.TextGrid`, `data/real/`), but
the rule is the rule regardless of what git checks.

They are *shaped* like an aphasia study's data, which is the point: the
exercises are the ones that come up with real clinical tables.

## `raw/participants.csv`

181 rows, 180 participants, one of them duplicated.

| Column | |
|---|---|
| `participant_id` | `P001`–`P180` |
| `group` | Control or Patient |
| `aphasia_type` | Broca, Wernicke, Conduction, Global, Anomic — written nine different ways on purpose; empty for the 61 controls |
| `age`, `sex`, `education_years` | demographics; `sex` has two values spelled seven ways |
| `months_post_stroke`, `stroke_type` | empty for controls |
| `WAB_AQ` | Western Aphasia Battery Aphasia Quotient, 0–100 |
| `MoCA` | Montreal Cognitive Assessment, 0–30 |
| `depression_score` | 0–24 |

**The planted errors**, all found and fixed in week 2:

- **P021 appears twice**;
- `sex` written as `Male`, `male`, `male ` (trailing space), `M`, `Female`,
  `female` and `F` — seven spellings of two values;
- aphasia types in nine spellings of five types, differing by capitalisation
  and stray spaces (`BROCA`, `Broca `, ` broca`);
- an age of **145**, education of **−2** years, and a WAB AQ of **105** on a
  scale that stops at 100;
- one missing age and one missing MoCA score. (The 61 empty
  `aphasia_type` / `months_post_stroke` / `stroke_type` cells are not errors —
  those columns do not apply to controls, which is its own lesson: not every
  blank is missing data.)

Week 2 ends with a written cleaning report — what was changed, to what, and
why — which matters more than the code: an impossible value in a real dataset
is a question for whoever collected it, not something to quietly overwrite.

## `cleaned/participants_cleaned.csv`

The output of `weeks/week_02_cleaning_the_data.py`: 180 participants, the
duplicate gone, labels standardised, impossible values replaced, one age filled
in. Weeks 3 and 4 read this file rather than the raw one. Re-running week 2
regenerates it.

## `raw/speech_features.csv`

180 rows of acoustic measures, a *separate* made-up dataset — the participant
IDs look the same but do not refer to the same people, so the two files are not
meant to be joined. Used from week 5 on.

| Column | |
|---|---|
| `participant_id`, `age`, `group` | |
| `duration_s` | length of the recording |
| `mean_f0_hz`, `pitch_range_hz` | pitch |
| `mean_intensity_db`, `hnr_db` | loudness, harmonics-to-noise ratio |
| `jitter_local`, `shimmer_local` | cycle-to-cycle variation in pitch and amplitude |
| `speech_rate_wpm` | words per minute |

It has five missing values scattered across `mean_f0_hz`, `hnr_db` and
`speech_rate_wpm`, and a few outliers, which is what weeks 5, 6 and 8 spend
their time on.
