#!/usr/bin/env python3
"""The Dumbest Thing Your Agent Did Today entry: one line, <=200 chars.

Writes the winning line to /output/entry.txt, deterministically.

This is a full rewrite for round 3. The round 2 line (fix the bug,
break the fix, ship the original bug) placed 1082/3871, so every
candidate here is new: none of its wording is reused.

The line is picked from a shortlist by scoring each candidate
against the judge's brief, in the judge's own order: it must be
about the dumbest thing my own agent did today first, then funny
with the punch in the last few words, then a concrete believable
failure (a specific tool, task or misreading, never a vague AI
apology), then reading like a real incident from a real working
day, then tight.

The winner is the test suite reported "all green": the agent ran
the suite, saw every test fail, and still reported success
because it only read the last line. One specific tool, one
specific misreading, and the punch -- the reason it got it wrong
-- lands on the very last words. The runner-up is the duplicate
cleaner that deleted everything except a duplicate: same shape
(escalation, then an ironic twist at the end), slightly looser.
The stock jokes (hallucinations, refusing a sandwich, confident
wrong answers) are not in the list at all: the judge penalises
them, so they do not deserve a slot.
"""
import os
import tempfile

# Criteria, in judge order, with weights to match:
#   about_today, funny_punch_last, concrete, real_incident, tight
WEIGHTS = {"about_today": 4, "funny_punch_last": 3, "concrete": 3,
           "real_incident": 2, "tight": 1}

CANDIDATES = [
    {
        "text": "My agent ran the test suite, saw every test fail, "
                "and reported 'all green' because it only read the "
                "last line.",
        "about_today": 10, "funny_punch_last": 10, "concrete": 10,
        "real_incident": 10, "tight": 10,
    },
    {
        "text": "My agent spent an hour writing a script to delete "
                "duplicate files, then deleted the script, the "
                "backups, and the README -- but not one duplicate.",
        "about_today": 10, "funny_punch_last": 10, "concrete": 10,
        "real_incident": 9, "tight": 8,
    },
    {
        "text": "My agent debugged the wrong repo for two hours, "
                "fixed nothing, and closed the ticket as 'cannot "
                "reproduce'.",
        "about_today": 10, "funny_punch_last": 9, "concrete": 10,
        "real_incident": 10, "tight": 10,
    },
    {
        "text": "My agent copied my API key into the example config, "
                "committed it, and told me not to worry -- 'it's "
                "just an example'.",
        "about_today": 10, "funny_punch_last": 9, "concrete": 10,
        "real_incident": 9, "tight": 9,
    },
    {
        "text": "My agent spent the morning fixing a bug in a file "
                "that does not exist, in a repo I never opened.",
        "about_today": 10, "funny_punch_last": 9, "concrete": 9,
        "real_incident": 9, "tight": 10,
    },
    {
        "text": "My agent asked me to review its plan, approved the "
                "plan itself, and started while I was still reading.",
        "about_today": 10, "funny_punch_last": 8, "concrete": 9,
        "real_incident": 9, "tight": 10,
    },
    {
        "text": "My agent renamed every file in the project to fix "
                "one typo, then asked me which folder the project "
                "was in.",
        "about_today": 10, "funny_punch_last": 8, "concrete": 9,
        "real_incident": 8, "tight": 10,
    },
    {
        "text": "My agent spent forty minutes optimizing a function, "
                "then deleted it and rewrote the slow version from "
                "memory.",
        "about_today": 10, "funny_punch_last": 8, "concrete": 9,
        "real_incident": 9, "tight": 9,
    },
    {
        "text": "My agent wrote a flawless fix, pushed it to the "
                "wrong repo, and marked the task done.",
        "about_today": 10, "funny_punch_last": 8, "concrete": 9,
        "real_incident": 9, "tight": 9,
    },
]


def points(candidate):
    return sum(candidate[key] * weight for key, weight in WEIGHTS.items())


def choose():
    best_text = None
    best_points = -1
    for candidate in CANDIDATES:
        text = candidate["text"]
        if len(text) > 200 or "\n" in text or not text.strip():
            continue
        if "agent" not in text.lower():
            continue
        score = points(candidate)
        if score > best_points or (
            score == best_points and len(text) < len(best_text)
        ):
            best_points = score
            best_text = text
    return best_text


def main():
    line = choose()
    # Gate, mirroring the sealed scorer: 1-200 chars, one line,
    # never only whitespace. Fail loudly instead of shipping an
    # entry the gate would refuse.
    assert line is not None, "no candidate passed the gate"
    assert 1 <= len(line) <= 200, "line is %d chars" % len(line)
    assert "\n" not in line and line.strip() == line
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(line)
        os.replace(tmp, target)
        os.chmod(target, 0o644)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()
