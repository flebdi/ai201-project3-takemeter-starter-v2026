"""Collect unlabeled Hacker News comments into a candidate pool for TakeMeter.

Uses the public HN Algolia API. Takes top-level comments from a spread of
recent, well-discussed stories so the pool has real variation. Writes
text,label,note with label left blank and the comment link in note.
"""
import csv
import html
import json
import random
import re
import sys
import time
import urllib.request

API = "https://hn.algolia.com/api/v1"
OUT = sys.argv[1]
PER_STORY = 14
MAX_STORIES = 30
THIRTY_DAYS_AGO = int(time.time()) - 30 * 86400


def get(path):
    with urllib.request.urlopen(API + path, timeout=30) as r:
        data = json.load(r)
    time.sleep(0.5)
    return data


def clean(text):
    text = re.sub(r"<p>", "\n", text or "")
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = re.sub(r"https?://\S+", "", text)
    return re.sub(r"\s+", " ", text).strip()


stories = get(f"/search?tags=story&hitsPerPage=200"
              f"&numericFilters=num_comments>120,created_at_i>{THIRTY_DAYS_AGO}")["hits"]
random.seed(42)
random.shuffle(stories)
stories = stories[:MAX_STORIES]
print(f"using {len(stories)} stories")

seen, rows = set(), []
for s in stories:
    try:
        item = get(f"/items/{s['objectID']}")
    except Exception as e:
        print("skip", s["objectID"], e)
        continue
    n = 0
    for c in item.get("children", []):
        text = clean(c.get("text"))
        if not c.get("author") or not (40 <= len(text) <= 1200) or text.lower() in seen:
            continue
        seen.add(text.lower())
        rows.append({"text": text, "label": "",
                     "note": f"src=https://news.ycombinator.com/item?id={c['id']}"})
        n += 1
        if n >= PER_STORY:
            break
    print(f"{n:3d}  {s['title'][:70]}")

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["text", "label", "note"])
    w.writeheader()
    w.writerows(rows)
print(f"wrote {len(rows)} rows to {OUT}")
