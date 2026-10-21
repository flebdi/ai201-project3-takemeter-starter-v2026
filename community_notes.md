# Milestone 1 — Community and candidate distinctions

## Community

**Hacker News** (news.ycombinator.com), top-level comments on well-discussed
stories. Public, no login, and the topics vary widely: AI models, privacy,
Linux, energy policy, dating apps. Collected with `collect_hn.py` into
`data/raw_hn_comments.csv` (420 comments, 30 stories, last 30 days).

First choice was r/nba, but Reddit now sends scripted requests to a login
page, which the "public only" rule excludes.

## What I read

40 comments, sampled at random from the pool (`random_state=7`). Bracketed
numbers below are row indexes in `raw_hn_comments.csv`.

## Candidate distinctions

**1. Some comments cite something checkable. Most don't.**
A benchmark score, a count, a quote from the article. [111] lists four
benchmark numbers and two prices. [255] says the consent form had 16
"legitimate interest" toggles and 1,746 vendors. [303] quotes the article's
own footnote and then argues against it. Compare [417], which is just as
confident ("simply barking up the wrong tree") and points at nothing.

**2. Some comments are questions.**
8 of the 40. Some are real questions asking for information: [56] "Does
it have a niche use case or is it just for testing?", [373]. Others are
arguments phrased as questions: [145] "Would the author feel the same if git
had used MD5?", [322] "Does Cloudflare need to be in the middle of
everything?". Telling those two apart will be a boundary problem.

**3. Some are a quick feeling or a joke, with no claim to argue with.**
[307] "I love passkeys." [394] "Just post the bloody content." [278], [386]
and [30] are one-line jokes. There's nothing in them you could agree or
disagree with. Compare [132] "it takes just as much ram if not more than
1.0", which is just as short but makes a checkable claim.

**4. Some use personal experience as the evidence.**
[254] the TV that made a million DNS queries; [271] using Google to search
exact text; [266]. These are specific and first-hand but not checkable by a
reader, so they sit somewhere between distinctions 1 and 3.

**5. Some make a broad claim about how things are, without support.**
[269] "Most people in the world are profoundly lonely." [378], [292], [399].
These are opinions offered as facts.

## What this suggests for labels

The assignment's example taxonomy (`analysis` / `hot_take` / `reaction`) maps
onto distinctions 1, 5 and 3. HN has two groups it doesn't cover cleanly:
questions (2) and personal anecdote (4). Milestone 2 has to decide whether
those get their own label or a rule that folds them into one of the three.

## Rows to leave out

- Mostly-link posts that lost their content when URLs were stripped
  (e.g. "The code is available at: LLM Models and data: Evaluations:").
- The suicide-rates thread ([239], [244], [245] and others): personal
  disclosures, not takes, and not something to train a quality classifier
  on.
