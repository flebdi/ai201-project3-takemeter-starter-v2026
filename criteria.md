# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

> **When these were written — read first.** This file was left blank in
> unit 5. These five criteria were written in **unit 6 (2026-10-28) by Claude**
> at my request, **after** the unit-5 `results.json` (0.43 accuracy, every
> post predicted `reaction`) and the three-seed "before" run were visible, and
> **before** the baseline was run. They are not pre-registered. To keep them
> honest, every target was set from the data and taxonomy — the 42% majority
> share, the 9-post `analysis` test split, the 11-post confidence thirds — and
> none was moved toward the observed numbers. Each must hold on all three seeds.

## 1. Overall accuracy of at least 0.60 on the held-out split, on every seed.

**Why this target:** `reaction` is 98 of 232 rows (42%), so a model that
always guesses it scores about 0.43 on a stratified test split. 0.60 is
roughly 17 points above that — the least I would call "learned something"
for three labels whose boundaries I had to write rules for.

---

## 2. Every label has an F1 of at least 0.50 on the held-out split, on every seed.

**Why this target:** `analysis` is my smallest label (58 rows), so only 9
posts land in each test split and one post moves its F1 by more than 0.1.
That is why this bar is looser than criterion 1. Below 0.50 on any label, the
classifier can't be trusted to sort that label at all.

---

## 3. Beats the zero-shot baseline's accuracy by at least 0.05, on the same test posts, on every seed.

**Why this target:** the baseline reads the same three definitions with no
training. 35 test posts means one post is about 0.03, so a gap under 0.05 is
one or two posts — not evidence that fine-tuning on 162 examples added
anything. The baseline is scored on each seed's own test split so the
comparison is like-for-like.

---

## 4. Recall on `hot_take` of at least 0.50, on every seed.

**Why this target:** `hot_take` is the label the project exists to find, and
it sits on both of my hard boundaries (against `analysis` on the support rule,
against `reaction` on the question rule). If the model misses more than half
of the real ones, it isn't doing the job, whatever its overall accuracy.

---

## 5. Accuracy on the model's most-confident third is at least 0.15 higher than on its least-confident third, on every seed.

**Why this target:** each third is 11 posts, so 0.15 is about two posts —
anything smaller is noise at this size. If confident guesses aren't right
more often than unsure ones, the confidence score can't be used to decide
which predictions to trust.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
