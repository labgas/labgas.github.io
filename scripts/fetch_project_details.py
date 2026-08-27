"""RETIRED — kept as a record of where the project detail came from. Do not run.

This harvested full project descriptions, funding, investigators and team members from
the LaBGAS project pages on gbiomed.kuleuven.be. That site is being taken offline, and
_data/projects.yml is now the source of truth: edit the `detail:` block there directly
(see the README).

Running this against a dead or moved site would be destructive — it rewrites `detail:`
wholesale.

Note that SLUG_ALIASES below is still imported by fetch_team_bios.py, so this module
must remain importable even though neither script should be executed.

Stdlib only.
"""

from __future__ import annotations

import argparse
import html
import os
import re
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECTS = os.path.join(ROOT, "_data", "projects.yml")
BASE = "https://gbiomed.kuleuven.be/english/research/50000625/50000628/labgas/projects"
UA = {"User-Agent": "Mozilla/5.0 (compatible; labgas.github.io site build)"}
DELAY = 0.3

# Source page slug -> the project name we use on the Research page.
#
# Keyed on the URL slug rather than the page title: two of these have nearly
# identical titles but are different studies (the anorexia SCFA project versus
# GUTSIE), so matching on text would silently mis-link them. Imported by
# fetch_team_bios.py so the two harvests cannot drift apart.
SLUG_ALIASES = {
    "Moodbugs": "MoodBugs",
    "moodbugs": "MoodBugs",
    "discoverie": "DISCOvERIE",
    "inbody": "INBODY",
    "erythritol-project": "Erythritol: satiation and reward without the calories?",
    "pavlov-visceroception": "From Pavlov to visceroception",
    "CFS": "Biopsychosocial mechanisms of chronic fatigue syndrome",
    "the-effects-of-gut-bacterial-metabolites-short-chain-fatty-acids-on-stress-"
    "induced-impairment-in-core-executive-functions": "GUTSIE",
    "unraveling-the-neurobiological-mechanisms-underlying-the-bidirectional-"
    "sleep-pain-relationship-in-people-with-non-specific-chronic-low-back-pain": "SY-NAPS",
    "gut-brain-mechanisms-mediating-the-effect-of-bariatric-surgery-on-food-reward-1":
        "Food reward after bariatric surgery",
    "a-neuropsychobiological-approach-to-optimize-patient-selection-for-glp-1-based-"
    "pharmacotherapy-for-weight-management-across-the-binge-eating-spectrum":
        "GLP-1 pharmacotherapy optimisation",
    "the-effects-of-gut-bacterial-metabolites-short-chain-fatty-acids-scfas-on-regulating-"
    "stress-responses-eating-behavior-and-nutritional-state-in-anorexia-nervosa":
        "Short-chain fatty acids in anorexia nervosa",
    "copy_of_the-effects-of-gut-bacterial-metabolites-short-chain-fatty-acids-scfas-on-"
    "regulating-stress-responses-eating-behavior-and-nutritional-state-in-anorexia-nervosa":
        "Gut-immune-brain axis in IBD fatigue",
}

# Wording the lab has asked us to change; re-applied on every run.
SUBSTITUTIONS = [
    ("gastrointestinal symptom perception", "gastrointestinal symptom, pain, and fatigue perception"),
    ("Gastrointestinal symptom perception", "Gastrointestinal symptom, pain, and fatigue perception"),
]

# Labels in the PROJECT INFORMATION block -> field name in projects.yml.
INFO_FIELDS = {
    "duration": "duration",
    "funding": "funding",
    "principal investigator": "investigators",
    "principal investigators": "investigators",
    "promotor": "investigators",
    "promotors": "investigators",
    "team member": "team",
    "team members": "team",
    "collaborators": "collaborators",
    "collaborator": "collaborators",
    "phd student": "team",
    "phd students": "team",
}

NOISE = re.compile(r"^\s*(>|Follow @|Comments on the content|Last update:|Log in\b)", re.I)

# Some pages end with a key-publications list rendered in the same markup as the
# prose. These are references, not description — surface them separately.
CITATION = re.compile(r"\bdoi:\s*10\.|\bdoi\.org/10\.", re.I)


def get(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as fh:
        raw = fh.read()
        charset = fh.headers.get_content_charset() or "utf-8"
    return raw.decode(charset, "replace")


def clean(fragment: str) -> str:
    fragment = re.sub(r"<br\s*/?>", " ", fragment, flags=re.I)
    fragment = re.sub(r"<[^>]+>", "", fragment)
    text = re.sub(r"\s+", " ", html.unescape(fragment)).strip()
    for old, new in SUBSTITUTIONS:
        text = text.replace(old, new)
    return text


def body(page: str) -> str:
    """The main content container, excluding page furniture."""
    m = re.search(r'id="parent-fieldname-text"[^>]*>(.*)', page, re.S)
    return m.group(1) if m else page


def blocks(fragment: str) -> "list[tuple[str, str]]":
    """(tag, text) for every <p> and <h2>/<h4> in document order."""
    out = []
    for m in re.finditer(r"<(p|h2|h3|h4)\b[^>]*>(.*?)</\1>", fragment, re.S | re.I):
        text = clean(m.group(2))
        if text and not NOISE.match(text):
            out.append((m.group(1).lower(), text))
    return out


def parse_page(page: str) -> dict:
    items = blocks(body(page))
    info, description, publications, section = {}, [], [], None

    for tag, text in items:
        upper = text.upper().strip(": ")
        if tag in ("h2", "h3") and "PROJECT INFORMATION" in upper:
            section = "info"
            continue
        if tag in ("h2", "h3") and ("PROJECT DESCRIPTION" in upper or "DESCRIPTION" == upper):
            section = "desc"
            continue
        if tag in ("h2", "h3") and upper and len(upper) < 60:
            # Any other heading ends the structured part (PUBLICATIONS, TEAM, ...).
            section = None if section == "info" else section
            continue

        if CITATION.search(text):
            publications.append(text)
            continue

        if section == "info":
            m = re.match(r"([A-Za-z /()]{3,40}?)\s*:\s*(.+)", text)
            if m:
                key = INFO_FIELDS.get(m.group(1).strip().lower())
                if key:
                    info[key] = (info.get(key, "") + "; " + m.group(2).strip()).strip("; ")
                    continue
            if len(text) > 120:
                description.append(text)
        elif section == "desc":
            if len(text) > 60:
                description.append(text)
        elif section is None and len(text) > 120:
            # Pages without the structured headings: keep substantial prose.
            description.append(text)

    return {"info": info, "description": description, "publications": publications}


def yq(s: str) -> str:
    import json
    return json.dumps(s, ensure_ascii=False)


def merge(details: dict, dry: bool) -> "tuple[int, list]":
    lines = open(PROJECTS, encoding="utf-8").read().split("\n")
    out, i, written, unmatched = [], 0, 0, []
    names_seen = set()

    while i < len(lines):
        line = lines[i]
        m = re.match(r'^(\s*)- name: "(.+)"\s*$', line)
        if not m:
            out.append(line)
            i += 1
            continue

        indent, name = m.group(1), m.group(2)
        names_seen.add(name)
        out.append(line)
        i += 1

        block = []
        while i < len(lines):
            nxt = lines[i]
            if re.match(r'^\s*- name: "', nxt) or re.match(r"^[a-zA-Z#]", nxt):
                break
            if re.match(rf"^{indent}  detail:", nxt):
                i += 1
                while i < len(lines) and (
                    re.match(rf"^{indent}    ", lines[i]) or not lines[i].strip()
                ) and not re.match(r'^\s*- name: "', lines[i]):
                    if not lines[i].strip() and i + 1 < len(lines) and re.match(
                        r'^\s*- name: "', lines[i + 1]
                    ):
                        break
                    i += 1
                continue
            block.append(nxt)
            i += 1

        tail = []
        while block and (not block[-1].strip() or block[-1].lstrip().startswith("#")):
            tail.insert(0, block.pop())
        out.extend(block)

        rec = details.get(name)
        if rec and (rec["description"] or rec["info"]):
            out.append(f"{indent}  detail:")
            for key in ("duration", "funding", "investigators", "team", "collaborators"):
                if rec["info"].get(key):
                    out.append(f"{indent}    {key}: {yq(rec['info'][key])}")
            if rec.get("source"):
                out.append(f"{indent}    source: {yq(rec['source'])}")
            if rec["description"]:
                out.append(f"{indent}    description:")
                for p in rec["description"]:
                    out.append(f"{indent}      - {yq(p)}")
            if rec.get("publications"):
                out.append(f"{indent}    publications:")
                for p in rec["publications"]:
                    out.append(f"{indent}      - {yq(p)}")
            written += 1
        out.extend(tail)

    for name in details:
        if name not in names_seen:
            unmatched.append(name)

    if not dry:
        open(PROJECTS, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    return written, unmatched


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--source-is-live",
        action="store_true",
        help="confirm the source site is reachable and still has the expected markup",
    )
    args = ap.parse_args()

    if not args.source_is_live:
        print(__doc__)
        print("Refusing to run. _data/projects.yml is the source of truth; edit it directly.")
        print("If you really have a live source, pass --source-is-live.")
        return 1

    try:
        idx = get(BASE)
    except Exception as exc:
        print(f"Could not load the project index: {exc}", file=sys.stderr)
        return 1

    urls, seen = [], set()
    for href in re.findall(r'href="([^"]*/labgas/projects/[^"#?]+)"', idx):
        href = href.replace("http://", "https://").rstrip("/")
        if href.endswith("/projects") or href in seen:
            continue
        seen.add(href)
        urls.append(href)

    details, problems = {}, []
    for url in urls:
        slug = url.rsplit("/", 1)[-1]
        name = SLUG_ALIASES.get(slug)
        if not name:
            problems.append(f"{slug}: no mapping in SLUG_ALIASES")
            continue
        try:
            rec = parse_page(get(url))
            rec["source"] = url
            details[name] = rec
            chars = sum(len(p) for p in rec["description"])
            fields = ", ".join(rec["info"]) or "no info fields"
            pubs = f"  {len(rec['publications'])} refs" if rec["publications"] else ""
            print(
                f"  {name[:38]:<38} {chars:>5} chars  {len(rec['description'])} para{pubs}  [{fields}]"
            )
            if not rec["description"]:
                problems.append(f"{name}: no description text found")
        except Exception as exc:
            problems.append(f"{name}: {type(exc).__name__}: {exc}")
        time.sleep(DELAY)

    written, unmatched = merge(details, args.dry_run)
    print(f"\n{'Would merge' if args.dry_run else 'Merged'} detail for {written} projects")
    for u in unmatched:
        problems.append(f"{u}: harvested but no project of that name in projects.yml")
    if problems:
        print(f"\n{len(problems)} need attention:")
        for p in problems:
            print(f"  · {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
