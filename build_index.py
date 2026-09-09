#!/usr/bin/env python3
"""Propagate the workshop Introduction page outward: Home, the collateral narrative, and each
lab/overview page's Executive outcome.

DIRECTION OF TRUTH (reversed 2026-07-29): the hand-authored source is the workshop's
Introduction page,

    content/workshops/<slug>/00-introduction.md

and everything else is generated from it:

  1. content/_index.md (Home)          — Home's `+++` front matter (hero, CTAs) is site UI and is
                                         PRESERVED verbatim. The body is a LANDING PAGE, not the
                                         whole narrative: the italic descriptor plus the opening
                                         section ("The Problem") and nothing after it.
  2. ../collateral/1 - narrative.md    — the narrative export for decks/collateral. Home's front
                                         matter supplies the title block (`# `, `### `, pillars);
                                         the Executive-outcome notice callouts are unwrapped back
                                         to bare paragraphs and `/images/image-NN.png` paths go
                                         back to relative.
  3. the five lab/overview pages       — each page's full Executive outcome is written between
                                         `<!-- exec-outcome:start -->` / `<!-- exec-outcome:end -->`
                                         markers, so it never drifts from the Introduction.

Edit 00-introduction.md, then run:

    python3 build_index.py

Do NOT hand-edit content/_index.md's body, 1 - narrative.md, or the text between the
exec-outcome markers — those are outputs and the next run overwrites them. Home's front matter
IS hand-maintained (it is the only place the hero title, eyebrow, pillars line, and CTAs live).

Override the narrative output path with an argument or NARRATIVE_MD; select the vertical with
WORKSHOP_SLUG (each verticalized workshop is its own section under content/workshops/):

    WORKSHOP_SLUG=agentic-observability-<variant> python3 build_index.py "/path/to/1 - narrative.md"
"""
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_NARRATIVE = HERE.parent / "collateral" / "1 - narrative.md"

narrative_path = Path(
    sys.argv[1] if len(sys.argv) > 1 else os.environ.get("NARRATIVE_MD", DEFAULT_NARRATIVE)
)
# Slug of the vertical being built. Each verticalized workshop is its own section under
# content/workshops/ (ai-trust-healthcare, ai-trust-finserv, …) so the URLs stay
# distinct; override with WORKSHOP_SLUG when generating a different vertical.
WORKSHOP_SLUG = os.environ.get("WORKSHOP_SLUG", "agentic-observability-nvidia")
WORKSHOP_DIR = HERE / "content" / "workshops" / WORKSHOP_SLUG
INTRO = WORKSHOP_DIR / "00-introduction.md"
HOME = HERE / "content" / "_index.md"

OUTCOME_TITLE = "Executive outcome"
NOTICE_CLOSE = "{{% /notice %}}"
MARK_START = "<!-- exec-outcome:start -->"
MARK_END = "<!-- exec-outcome:end -->"

for required in (INTRO, HOME):
    if not required.exists():
        sys.exit(f"not found: {required}")


def split_front_matter(path: Path) -> tuple[str, str]:
    """Return (front_matter_including_delimiters, body) for a `+++`-fenced page."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("+++"):
        sys.exit(f"{path} does not start with a '+++' front-matter block")
    end = text.find("\n+++", 3)
    if end == -1:
        sys.exit(f"{path} has an unterminated '+++' front-matter block")
    close = end + len("\n+++")
    return text[:close], text[close:].strip("\n")


def fm_value(front: str, key: str) -> str:
    """Pull a quoted scalar out of a TOML front-matter block."""
    m = re.search(rf'^{re.escape(key)}\s*=\s*"((?:[^"\\]|\\.)*)"', front, re.M)
    if not m:
        sys.exit(f"content/_index.md front matter has no '{key}' — layout changed?")
    return m.group(1).replace('\\"', '"').replace("\\\\", "\\")


intro_front, body = split_front_matter(INTRO)
home_front, _ = split_front_matter(HOME)

# The narrative's title block is the hero, flattened back into Markdown; everything from the
# first '## ' heading on is the body. Any preamble before that first heading (the italic
# descriptor) belongs above the '---' in the narrative, which is where it came from.
body_lines = body.split("\n")
try:
    first_h2 = next(i for i, ln in enumerate(body_lines) if ln.startswith("## "))
except StopIteration:
    sys.exit(f"{INTRO} has no '## ' heading — layout changed?")

preamble = [ln for ln in body_lines[:first_h2] if ln.strip()]
rest = body_lines[first_h2:]

# --- 1. Home: preserved front matter (hero + CTAs) + preamble + the FIRST section only ------
# Home is a landing page, not the whole narrative: it carries the hero, the italic descriptor,
# and the opening section ("The Problem") — then stops and hands off to the CTAs. The full
# narrative lives on the Introduction page and in the collateral export. The section ends at
# the next horizontal rule or '## ' heading, whichever comes first.
first_section_end = next(
    (i for i, ln in enumerate(rest[1:], start=1)
     if ln.strip() == "---" or ln.startswith("## ")),
    len(rest),
)
home_body = "\n".join(preamble + [""] + rest[:first_section_end]).strip("\n")
HOME.write_text(home_front + "\n\n" + home_body + "\n", encoding="utf-8")
print(f"wrote {HOME} (front matter preserved; body = descriptor + "
      f"{rest[0].lstrip('# ').strip()!r})")

# Flatten every notice callout: the narrative is plain Markdown for decks and collateral, so
# no Hugo shortcode may survive into it. Executive outcomes already open with their own bold
# lead ("**Executive outcome — …**"), so they need no label; any other callout keeps its title
# as a bold lead line so the label is not lost.
unwrapped = []
in_notice = False
for ln in rest:
    if ln.startswith("{{% notice"):
        if in_notice:
            sys.exit(f"{INTRO} nests notice callouts — cannot flatten them for the narrative")
        in_notice = True
        title = re.search(r'title="([^"]*)"', ln)
        if title and title.group(1) != OUTCOME_TITLE:
            unwrapped.extend(["", f"**{title.group(1)}**", ""])
        continue
    if in_notice and ln.strip() == NOTICE_CLOSE:
        in_notice = False
        continue
    unwrapped.append(ln.replace("](/images/image", "](image"))
if in_notice:
    sys.exit(f"{INTRO} has an unclosed notice callout")

narrative_lines = [
    f"# {fm_value(home_front, 'title')}",
    "",
    f"### {fm_value(home_front, 'eyebrow')}",
    "",
    f"**{fm_value(home_front, 'description')}**",
    "",
    *(preamble + [""] if preamble else []),
    "---",
    "",
    *unwrapped,
]
narrative = re.sub(r"\n{3,}", "\n\n", "\n".join(narrative_lines)).strip("\n") + "\n"

if narrative_path.exists():
    previous = narrative_path.read_text(encoding="utf-8")
    if previous == narrative:
        print(f"{narrative_path} already current — left untouched")
    else:
        # Single rolling backup: the narrative is collateral the user also edits by hand, so
        # never overwrite it without leaving the prior version recoverable.
        backup = narrative_path.with_suffix(narrative_path.suffix + ".bak")
        backup.write_text(previous, encoding="utf-8")
        narrative_path.write_text(narrative, encoding="utf-8")
        print(f"wrote {narrative_path} (previous version saved to {backup.name})")
else:
    narrative_path.write_text(narrative, encoding="utf-8")
    print(f"wrote {narrative_path}")

# --- 3. Sync each lab/overview page's full Executive outcome from the Introduction ----------
# The Introduction has exactly five "**Executive outcome …**" paragraphs, in this order:
# Overview, Part 1, Part 2, Part 3, Part 4 — mapped positionally to the pages below. Each page
# carries its outcome as a notice callout between sentinel markers, so the text stays
# verbatim-identical to the Introduction and Home.
OUTCOME_PAGES = [
    "02-overview.md",        # Overview / one architecture, one trace
    "03-lab-1-deploy.md",    # Lab 1 — Run the blueprint as shipped
    "04-lab-2-observe.md",   # Lab 2 — Observe (Splunk Agent Observability)
    "05-lab-3-secure.md",    # Lab 3 — Secure (Cisco AI Defense)
    "06-lab-4-govern.md",    # Lab 4 — Govern (Splunk Core)
]

outcomes = [ln for ln in body_lines if ln.startswith("**Executive outcome")]
if len(outcomes) != len(OUTCOME_PAGES):
    sys.exit(f"expected {len(OUTCOME_PAGES)} '**Executive outcome' paragraphs in "
             f"{INTRO.name}, found {len(outcomes)} — cannot sync lab pages safely.")

synced = 0
for page_name, outcome in zip(OUTCOME_PAGES, outcomes):
    page = WORKSHOP_DIR / page_name
    if not page.exists():
        print(f"  skip {page_name}: not found")
        continue
    page_lines = page.read_text(encoding="utf-8").split("\n")
    try:
        s = page_lines.index(MARK_START)
        e = page_lines.index(MARK_END)
    except ValueError:
        print(f"  skip {page_name}: missing exec-outcome markers")
        continue
    block = [MARK_START, "",
             '{{% notice style="info" title="Executive outcome" icon="star" %}}',
             outcome,
             NOTICE_CLOSE,
             "", MARK_END]
    page_lines[s:e + 1] = block
    page.write_text("\n".join(page_lines), encoding="utf-8")
    synced += 1

print(f"synced {synced}/{len(OUTCOME_PAGES)} lab/overview executive outcomes from {INTRO.name}")
