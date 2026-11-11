# python-refresher

Pretty self-explanatory repo that keeps my baby Python skills alive.

Eight weeks of working through pandas, matplotlib and statistics on a synthetic
clinical dataset: load a CSV, clean it, describe it, plot it, then pick the
right statistical test, run it, and check whether its assumptions actually
hold. Plus a regex exercise on a speech transcript.

Every script is standalone and prints what it finds. The questions and the
answers are in the comments, because the point was to learn rather than to
build a package.

## The weeks

| | Script | What it covers |
|---|---|---|
| 1 | [`weeks/week_01_loading_and_inspecting.py`](weeks/week_01_loading_and_inspecting.py) | reading a CSV with pandas; `head`, `shape`, `columns`, `info`, `describe` |
| 2 | [`weeks/week_02_cleaning_the_data.py`](weeks/week_02_cleaning_the_data.py) | copy before you edit; duplicates, inconsistent category labels, impossible values, missing data — ends with a cleaning log and writes `data/cleaned/` |
| 3 | [`weeks/week_03_descriptives.py`](weeks/week_03_descriptives.py) | counts and means by group, `groupby` with aggregation, a derived `age_group` column, sorting and ranking |
| 4 | [`weeks/week_04_first_plots.py`](weeks/week_04_first_plots.py) | histogram, bar plot, scatter, grouped comparison; saving figures at 300 dpi |
| 5 | [`weeks/week_05_second_dataset.py`](weeks/week_05_second_dataset.py) | a second dataset met cold: what's in it, what's missing, which feature varies most |
| 6 | [`weeks/week_06_group_comparison.py`](weeks/week_06_group_comparison.py) | do patients and controls differ in speech rate? an independent-samples t-test, and correlation against age |
| 7 | [`weeks/week_07_choosing_a_test.py`](weeks/week_07_choosing_a_test.py) | notes: which test for which design, and why correlation isn't a group comparison |
| 8 | [`weeks/week_08_checking_assumptions.py`](weeks/week_08_checking_assumptions.py) | normality and equal variance — Q-Q plots, Shapiro–Wilk, Levene, and what to use when they fail |

Alongside those:

- [`notebooks/functions.ipynb`](notebooks/functions.ipynb) — the running list of
  every pandas function learned so far, as a cheat sheet.
- [`notebooks/notes.ipynb`](notebooks/notes.ipynb) — the decision tree for
  getting from a research question to a test.
- [`transcript_cleaning/`](transcript_cleaning/) — a regex exercise:
  `cleaning_transcript.py` strips filler words `(eeh)`, `(uuh)`, `(uhm)` from a
  short picture-description transcript and reformats each utterance with its
  timestamp in front. The comments explain the regex piece by piece.

## The data is made up

`data/` holds two synthetic datasets with errors planted in them on purpose —
impossible ages, negative education years, out-of-range clinical scores, a
duplicated participant ID. Cleaning those is the week 2 exercise.

No real participant data is in this repository, and none should ever be added
to it. See [`data/README.md`](data/README.md).

## Running it

```bash
pip install -r requirements.txt
```

Then any week, from anywhere:

```bash
python3 weeks/week_01_loading_and_inspecting.py
```

Paths inside the scripts are built from each file's own location
(`Path(__file__).resolve().parents[1]`), not from an absolute home-folder path,
so they work after a clone and from whatever directory you happen to be in.

Weeks 2, 4, 5 and 6 write files — the cleaned CSV and the figures. Re-running
them overwrites what's already committed, which is the intended behaviour.

## License

MIT, see [`LICENSE`](LICENSE).
