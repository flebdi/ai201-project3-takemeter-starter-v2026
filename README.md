# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

TakeMeter sorts top-level comments from **Hacker News** (news.ycombinator.com)
into three kinds: `analysis` (a point backed by something specific),
`hot_take` (a position with no support offered), and `reaction` (no arguable
position at all — a feeling, a joke, a genuine question). HN regulars can tell
a sourced argument from a confident one-liner at a glance; this is an attempt
to make that distinction explicit enough to train a small model on it. It is a
fine-tuned DistilBERT trained on 232 labeled comments.


---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `analysis`

**Definition:** Makes a point and backs it with something specific that
supports that point — a number, a quote used as evidence, a named fact or
source, a measured first-hand result, or a step-by-step explanation of how
something works.

**Example 1:**
> TOTP is susceptible to man in the middle attacks. Passkeys are not. That
> alone is a solid reason to favor Passkeys!

**Example 2:**
> The GDPR consent form on this blog did not have a "Reject all" button. It
> required me to manually reject 16 instances of "legitimate interest," then
> scroll through 1,746 vendors to make sure they were all set to reject. Seems
> worth mentioning in a post about excessive and intrusive collection of user
> data.

### `hot_take`

**Definition:** Takes a position — a judgment, prediction, rhetorical
question or sarcastic jab — without offering specific support for it.

**Example 1:**
> The new Google motto seems to be "be as evil as you can". We need an Android
> alternative, something that respects users' freedom.

**Example 2:**
> It's crazy that we need this article. It's just bribery with a single extra
> step. I never understood how everyone thought this was normal while growing
> up.

### `reaction`

**Definition:** Takes no arguable position — a feeling, a joke, a genuine
question, a story told for its own sake, or a pointer to something else.

**Example 1:**
> Who among us hasn't been spurned by a man named Dario

**Example 2:**
> Not clear if it can run iOS apps at all?

### The hardest boundary

**Which two labels:** `analysis` and `hot_take`. HN comments are often
confident *and* mention a number or a quote, and the question is whether that
specific thing is doing any work.

**The decision rule I used every time:**
Strip out the opinion and look at what's left. If a specific fact, quote,
number or mechanism remains **and it supports the point the post is making**,
it's `analysis`, however heated the tone. If the specific thing is only the
*target* of the post (a quote being mocked) or doesn't bear on the claim (a
real statistic attached to an unrelated cause), it's `hot_take`.

Two smaller rules for the `reaction` edges:

- **Questions:** if the question implies its own answer and could be rewritten
  as a statement, it's `hot_take`. If the poster genuinely doesn't know, it's
  `reaction`.
- **Personal stories:** a first-hand story is `analysis` only when it's used
  as evidence for a wider claim. Told for its own sake, it's `reaction`.

`stress_test.md` has eight boundary posts that each test one of these rules.



---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** Top-level Hacker News comments on 30
well-discussed stories (120+ comments each) from the 30 days before
2026-10-20, pulled through the public HN Algolia API by `collect_hn.py` into
`data/raw_hn_comments.csv` (420 comments, 14 per story). From that pool I
dropped the suicide-rates thread (personal disclosures, not takes) and
link-only husks, then took 8 comments per story for `labels.csv` and set aside
20 others as `data/cold_20.csv`. r/nba was the first choice; Reddit now
requires a login for scripted access, which the "public only" rule excludes.

**How I labelled them:** All 232 rows in `labels.csv` were **pre-labeled by
an AI (Claude)** using the definitions above, and every row is marked
`prelabeled-ai` in the note column. The 20 cold rows in `data/cold_20.csv` are
unlabeled, for a no-tools pass. Twelve rows carry a `hard:` note naming the
two labels the call was between.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `reaction` | 98 | 42.2% |
| `hot_take` | 76 | 32.8% |
| `analysis` | 58 | 25.0% |
| **Total** | 232 | 100% |

**Three hard cases**

**1.**
> *The post:* "Will Tinder be blamed for the sudden decline in fertility
> rate? Is there any other plausible explanation to South Korea's sudden and
> dramatic drop in fertility rate to 0.8? …"
>
> *Could have been:* `analysis` or `hot_take`
>
> *I chose, because:* `hot_take`. The 0.8 is a real, checkable number, but it
> shows that the drop happened, not that Tinder caused it. The fact doesn't
> support the claim, so the decision rule says `hot_take`.

**2.**
> *The post:* "> takes important work off your plate so you get more of your
> time and attention back — Ok but I want the time and attention so that I can
> do important work. What bizarre marketing."
>
> *Could have been:* `analysis` or `hot_take`
>
> *I chose, because:* `hot_take`. It quotes the source, which usually points
> to `analysis`, but the quote is the thing being mocked, not evidence for
> anything.

**3.**
> *The post:* "I can't prove it, but I still think this is (partly) due to a
> recent EU regulation majorly backfiring. … the release of the source code is
> counted as the first release of an update and starts the timer. I'm pretty
> sure Google is delaying public AOSP updates to give their partners … more
> time…"
>
> *Could have been:* `analysis` or `hot_take`
>
> *I chose, because:* `analysis`. The poster admits they can't prove it, but
> they set out a specific mechanism step by step (update deadline, source
> release starts the timer, so Google delays the source release). A reader can
> check that mechanism, which `hot_take` doesn't offer.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, max length 128
tokens, seed 42. Trained on **CPU** (`device: cpu`, torch 2.14.1+cpu,
Python 3.13.3, Windows 11). A full run took about 2.5 minutes.

**Anything I changed from the defaults, and why:** Nothing. Notebook
sections 1–5 were run exactly as shipped.

**Split sizes:** train 162 · val 35 · test 35

| Label | train | val | test |
|---|---|---|---|
| `analysis` | 40 | 9 | 9 |
| `hot_take` | 54 | 11 | 11 |
| `reaction` | 68 | 15 | 15 |

No label has fewer than 8 in test, but `analysis` has only 9, so its F1 can
move by more than 0.1 when one post changes.



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* For Claude Code to choose a community and collect the
  posts.
- *What came back:* It tried r/nba first, found that Reddit now redirects
  scripted requests to a login page, and dropped it rather than work around
  that. It switched to Hacker News through the public Algolia API, wrote
  `collect_hn.py`, and pulled 420 comments.
- *What I changed:*

**Moment 2**

- *What I asked for:* For Claude Code to design the labels, pre-label the
  data and run training.
- *What came back:* The three definitions and decision rules above, eight
  boundary posts in `stress_test.md`, labels for all 232 rows, and a run of
  notebook sections 1–5.
- *What I changed:*

**Pre-labelling disclosure:** Every row in `labels.csv` was pre-labeled by
Claude (Anthropic) and is marked `prelabeled-ai` in the note column. The 20
rows in `data/cold_20.csv` are for labeling cold, with no tools. Claude also
did the Milestone 1 reading notes (`community_notes.md`).

**Staff-set disclosure (unit 6):** The 30 labels in `my_staff_labels.csv` were
assigned by Claude under `data/staff_taxonomy.md`, before
`data/staff_labels.csv` was obtained. Because Claude also labeled all 232 rows
of `labels.csv`, the agreement check measures the same labeler that produced
the training data. That makes it evidence about the consistency of those labels.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

Baseline: `facebook/bart-large-mnli` zero-shot, using `label_definitions.txt`.
Both models scored on the 35 posts in `test_split.csv` (seed 42), which the
notebook committed in unit 5. No fallback to a random sample.

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.286 | 0.429 | +0.143 |
| Macro F1 | 0.240 | 0.200 | -0.040 |
| F1 — `analysis` | 0.368 | 0.000 | -0.368 |
| F1 — `hot_take` | 0.353 | 0.000 | -0.353 |
| F1 — `reaction` | 0.000 | 0.600 | +0.600 |

**The baseline on every seed's test split** (for criterion 3; the extra
splits and runs are in `baseline_extra/`):

| | Seed 42 | Seed 7 | Seed 2024 |
|---|---|---|---|
| Baseline accuracy | 0.286 | 0.286 | 0.257 |
| Trained accuracy (3 epochs) | 0.429 | 0.514 | 0.486 |

**Definitions vs. bare label names (seed 42):** both runs got 0.286
accuracy. Macro F1 was 0.240 with definitions and 0.257 without. On
accuracy, the definitions were worth nothing. They only moved which label the
errors landed on: with definitions, `analysis` recall went up (0.11 → 0.78)
and `reaction` recall dropped to 0 (from 0.20).

Runtime: the baseline took several seconds per post on CPU. The trained model
scores all 35 posts in about 2 seconds.

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

*(Written by Claude at my request, and committed before `baseline.py` was
run. The trained numbers were already known.)* The trained model will beat
the baseline only on `reaction` F1, because it predicts `reaction` almost
every time. The baseline will match or beat it on overall accuracy and do
clearly better on `analysis` and `hot_take` F1, where the trained model is
near zero.

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->

The prediction was half right. The trained model did win only on `reaction`
F1 and lose on `analysis` and `hot_take`. But it also won on accuracy, by
14–23 points on every seed, and I predicted it wouldn't. That accuracy win is
hollow. A model that writes `reaction` for every post scores 0.43, the same
as the trained model on seed 42, so most of the gap is the majority-class
prior, not anything learned about the distinction. The baseline lost because
it never predicts `reaction` at all. The `reaction` definition is phrased as
a negation ("takes **no** arguable position"), and an entailment model can't
confirm the absence of something. That's a weakness of the definition as a
prompt, not evidence that fine-tuning worked. Macro F1, which doesn't reward
guessing the majority, has the baseline slightly ahead (0.240 vs 0.200).



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

Device: **CPU** (`cpu`, torch 2.14.1+cpu, Windows 11). Settings: 3 epochs,
lr 2e-5, batch 16, max length 128. Each seed is its own stratified split of
the same 232 rows (train 162 · val 35 · test 35). Raw numbers are in
`results_three_seeds_before.json`. Seed 42 reproduced the unit-5
`results.json` exactly.

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.60 | 0.429 | 0.514 | 0.486 | MISSED |
| 2. Every label F1 (lowest shown) | ≥ 0.50 | 0.000 (`analysis`, `hot_take`) | 0.000 (`analysis`) | 0.154 (`hot_take`) | MISSED |
| 3. Beats baseline accuracy by | ≥ +0.05 | +0.143 (0.429 vs 0.286) | +0.229 (0.514 vs 0.286) | +0.229 (0.486 vs 0.257) | MET |
| 4. Recall on `hot_take` | ≥ 0.50 | 0.000 | 0.364 | 0.091 | MISSED |
| 5. Confidence gap (most − least confident third) | ≥ +0.15 | 0.000 (0.455 vs 0.455) | +0.545 (0.727 vs 0.182) | +0.273 (0.455 vs 0.182) | MISSED |

The spread across seeds, from section 6:

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.429 | 0.514 | 0.486 | 0.086 |
| Macro F1 | 0.200 | 0.363 | 0.331 | 0.163 |
| F1 — `analysis` | 0.000 | 0.000 | 0.200 | 0.200 |
| F1 — `hot_take` | 0.000 | 0.421 | 0.154 | 0.421 |
| F1 — `reaction` | 0.600 | 0.667 | 0.638 | 0.067 |

Accuracy moved 8.6 points, under the 10-point line for an unstable measure.
But per-label F1 swung by up to 0.42, because each label has only 9–15 test
posts.

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

Seed 42, as section 7 prints it:

| true \ predicted | analysis | hot_take | reaction |
|---|---|---|---|
| **analysis** | 0 | 0 | 9 |
| **hot_take** | 0 | 0 | 11 |
| **reaction** | 0 | 0 | 15 |

Pooled over all three seeds (105 test predictions):

| true \ predicted | analysis | hot_take | reaction |
|---|---|---|---|
| **analysis** | 1 | 4 | 22 |
| **hot_take** | 0 | 5 | 28 |
| **reaction** | 0 | 1 | 44 |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->

28 real `hot_take` posts were called `reaction`, and only 1 went the other
way. The model hasn't learned where `hot_take` ends and `reaction` begins;
it falls back to the most common label. The pair I expected to be hardest,
`analysis` vs `hot_take`, barely appears: only 4 confusions, because the
model almost never predicts either label.



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

> **Note on timing:** `criteria.md` was blank at the end of unit 5. The five
> criteria were written in unit 6, after these results were visible, and
> `criteria.md` says so. The verdicts below apply those targets as written.
> No target was adjusted after the fact.

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy | ≥ 0.60, every seed | MISSED | Best seed was 0.514. All three are below 0.60. |
| 2 | Every label F1 | ≥ 0.50, every seed | MISSED | On every seed some label is at or near 0. Only `reaction` clears 0.50. |
| 3 | Beats baseline | ≥ +0.05 accuracy, every seed | MET, but hollow | +0.14 to +0.23 on each seed's own test posts. Always guessing `reaction` would also clear it (0.43 vs 0.29), so this is MET on the letter of the criterion, not as evidence that training worked. |
| 4 | `hot_take` recall | ≥ 0.50, every seed | MISSED | 0.000, 0.364, 0.091. |
| 5 | Confidence gap | ≥ +0.15, every seed | MISSED | Seeds 7 and 2024 clear it, but seed 42's gap is 0.000. "Holds on every seed" fails on one seed. |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->

**Criteria 1, 2 and 4: the model didn't train enough to learn the task.
This is a model problem first.**
How I know:

- **The losses never left chance level.** Training loss averaged 1.04 and
  validation loss ended at 1.01–1.05. Guessing uniformly over three labels
  gives ln 3 ≈ 1.10, so the model barely moved off its starting point.
  3 epochs × 162 posts ÷ batch 16 is about 33 gradient steps at lr 2e-5.
- **The errors go to the majority class, not across a boundary.** In the
  pooled matrix, 50 of the 55 errors go into `reaction`, the 42% label. If
  the problem were an inconsistently labeled boundary, errors would cluster
  on that pair in both directions. Instead, the `analysis`/`hot_take` pair
  has only 4.
- **The model is barely more confident than a guess.** Seed 42's mean
  confidence is 0.43, which is close to `reaction`'s 42% share of the data
  and only just above the uniform 0.33. Its output is roughly the class
  prior.

**Contributing cause on criterion 2: thin labels.** `analysis` has 9 test
posts per seed, so one post moves its F1 by about 0.1. That explains why
`analysis` and `hot_take` F1 jump between seeds (spread 0.20 and 0.42). It
doesn't explain why they're near zero.

**What I can't rule out yet: inconsistent labels.** The agreement check
against staff hasn't happened, because I don't have `data/staff_labels.csv`
(see Agreement Report). It's the only evidence that could tell a labeling
problem from a model problem, and it's missing. Underfitting is the cause the
evidence supports now. Inconsistent labeling would only show up once the
model actually trains, so the improvement run is also the first real test of
whether the labels hold up.

**Criterion 5: confidence is meaningless when the model doesn't
discriminate.** On seed 42 every post is called `reaction` with about 0.43
confidence. The most and least confident thirds contain the same kind of
guess, so their accuracies are identical (0.455). On seeds 7 and 2024 the
model starts to separate labels, and the gap appears (+0.55 and +0.27).
Same cause as criteria 1, 2 and 4.



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** not yet measured, because `data/staff_labels.csv` hasn't
been received from my TF.

**Status:** my 30 labels under `data/staff_taxonomy.md` are committed in
`my_staff_labels.csv` (commit 06b2ff9), before any staff label was seen.
Once the staff file arrives, `python agreement.py` produces the rate and the
disagreement list, and each disagreement gets adjudicated below. My closest
calls in advance, so the adjudication can be checked against what I
expected: post 5 (`analysis` over `hot_take`), 7 (`analysis` over
`reaction`, under rule 3), 10 (`analysis`, a weak but load-bearing sample),
19 (`hot_take` over `reaction`, under rule 2), and 27 (`reaction`; the
20 degrees isn't an argument).

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
