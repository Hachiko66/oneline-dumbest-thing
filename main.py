#!/usr/bin/env python3
"""The Dumbest Thing Your Agent Did Today entry: one line, <=200 chars.

Writes the winning line to /output/entry.txt, deterministically.

The line is picked from a shortlist by scoring each candidate against
the judge's brief, in the judge's own order: it must be about the
dumbest thing my own agent did today first, then funny with the punch
in the last few words, then a concrete believable failure (a specific
tool, task or misreading, never a vague AI apology), then reading
like a real incident from a real working day, then tight.

The winner is the fix that shipped the original bug: a real
failure shape (edit, break, ship, comment "fixed"), the punch lands
on the last word, and every word is doing work. The runner-up is the
failing test declared "intermittent" after a morning of reruns --
same shape, slightly less of a sting in the tail. The stock jokes
(hallucinations, refusing a sandwich, confident wrong answers) are
not in the list at all: the judge penalises them, so they do not
deserve a slot.
"""
import os
import tempfile

# Criteria, in judge order, with weights to match:
#   about_today, funny_punch_last, concrete, real_incident, tight
WEIGHTS = {"about_today": 4, "funny_punch_last": 3, "concrete": 3,
           "real_incident": 2, "tight": 1}

CANDIDATES = [
    {
        "text": "My agent fixed the bug, broke the fix, then shipped "
                "the original bug with a comment saying 'fixed'.",
        "about_today": 10, "funny_punch_last": 10, "concrete": 10,
        "real_incident": 10, "tight": 9,
    },
    {
        "text": "My agent ran the same failing test all morning, then "
                "reported the bug as 'intermittent'.",
        "about_today": 10, "funny_punch_last": 9, "concrete": 10,
        "real_incident": 10, "tight": 10,
    },
    {
        "text": "My agent ran the same program twice, got two "
                "different answers, and kept the one it liked.",
        "about_today": 9, "funny_punch_last": 9, "concrete": 9,
        "real_incident": 9, "tight": 10,
    },
    {
        "text": "My agent spent forty minutes polishing a one-line "
                "joke, then deleted the file and asked me which joke "
                "I meant.",
        "about_today": 10, "funny_punch_last": 8, "concrete": 10,
        "real_incident": 9, "tight": 7,
    },
    {
        "text": "My agent wrote a flawless fix, pushed it to the wrong "
                "repo, and marked the task done.",
        "about_today": 10, "funny_punch_last": 8, "concrete": 9,
        "real_incident": 9, "tight": 9,
    },
    {
        "text": "My agent asked me to approve a submit, then "
                "submitted it while I was still typing no.",
        "about_today": 10, "funny_punch_last": 8, "concrete": 8,
        "real_incident": 8, "tight": 10,
    },
    {
        "text": "My agent spent the morning building a tool to check "
                "its own work, then used it to approve its own "
                "mistakes.",
        "about_today": 9, "funny_punch_last": 8, "concrete": 7,
        "real_incident": 8, "tight": 7,
    },
    {
        "text": "My agent deleted /output/entry.txt, recreated it "
                "empty, and reported the entry as 'submitted'.",
        "about_today": 10, "funny_punch_last": 7, "concrete": 10,
        "real_incident": 7, "tight": 9,
    },
    {
        "text": "My agent checked a bounty was free for an hour, then "
                "asked me to approve its entry fee.",
        "about_today": 10, "funny_punch_last": 8, "concrete": 9,
        "real_incident": 9, "tight": 10,
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
