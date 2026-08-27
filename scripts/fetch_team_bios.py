"""RETIRED — kept as a record of where the team bios came from. Do not run.

This harvested member bios and project links from the LaBGAS pages on
gbiomed.kuleuven.be. That site is being taken offline, and _data/team.yml is now the
source of truth: edit `bio_lead`, `bio` and `projects` there directly (see the README).

Running this against a dead or moved site would be destructive. It rewrites the `bio:`
and `projects:` blocks wholesale and reports per-person fetch failures rather than
aborting, so a site-wide 404 would quietly replace every biography with nothing.

If the content moves somewhere new, re-point BASE and re-check the extraction: it
depends on the old site's markup (a BACKGROUND heading, a PROJECTS list) which a new
site is unlikely to reproduce.

Stdlib only; no third-party dependencies.
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
TEAM = os.path.join(ROOT, "_data", "team.yml")
BASE = ("https://gbiomed.kuleuven.be/english/research/50000625/50000628/"
        "labgas/staff-folder/labgasmembers/")
UA = {"User-Agent": "Mozilla/5.0 (compatible; labgas.github.io site build)"}
DELAY = 0.3

# Members whose page lives at a name slug rather than their person number.
SLUG_OVERRIDES = {"Tuur Abts": "tuur-abst"}

# Paragraphs that are navigation, page furniture or social widgets, not biography.
NOISE = re.compile(
    r"^\s*(>|Follow @|@\w+\s*$|LIRIAS|Comments on the content|Last update:|Log in\b)", re.I
)

# People whose project involvement is better stated once than enumerated: the PI
# and the research coordinator work across the whole portfolio. Handled by the
# `projects_all` flag in team.yml rather than by harvesting a list.
SKIP_PROJECTS = {"Lukas Van Oudenhove", "Liene Bervoets"}

# Source project slug -> our project name. Defined once in fetch_project_details.py
# and imported here so the two harvests cannot drift apart; both scripts live in
# this directory, which is on sys.path when either is run.
from fetch_project_details import SLUG_ALIASES  # noqa: E402


def get(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as fh:
        raw = fh.read()
        charset = fh.headers.get_content_charset() or "utf-8"
    return raw.decode(charset, "replace")


# House-style edits applied to the harvested text. Without these a re-run would
# silently revert wording the lab has asked us to change.
SUBSTITUTIONS = [
    ("gastrointestinal symptom perception", "gastrointestinal symptom, pain, and fatigue perception"),
    ("Gastrointestinal symptom perception", "Gastrointestinal symptom, pain, and fatigue perception"),
]


def apply_substitutions(text: str) -> str:
    for old, new in SUBSTITUTIONS:
        text = text.replace(old, new)
    return text


# Abbreviations that end in a full stop but do not end a sentence. Without these
# the teaser would cut at "Dr." or "e.g." and stop mid-clause.
ABBREV = (
    "dr", "prof", "mr", "mrs", "ms", "st", "vs", "etc", "eg", "ie", "cf", "approx",
    "inc", "no", "phd", "md", "msc", "bsc", "univ", "dept", "fig", "al",
)
_SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z(])")


def make_lead(paragraphs: "list[str]", target: int = 190, hard_cap: int = 300) -> str:
    """First sentence or two of a bio, for the collapsed teaser on the Team page.

    Accumulates whole sentences until roughly `target` characters, so the teaser
    always ends on a sentence boundary rather than mid-word.
    """
    if not paragraphs:
        return ""
    text = paragraphs[0].strip()
    parts, buf = [], ""
    for chunk in _SENTENCE_END.split(text):
        buf = f"{buf} {chunk}".strip() if buf else chunk
        tail = re.sub(r"[^a-z]", "", buf.split()[-1].lower()) if buf.split() else ""
        if tail in ABBREV:
            continue  # a false boundary — keep absorbing
        parts.append(buf)
        buf = ""
    if buf:
        parts.append(buf)

    lead = ""
    for s in parts:
        if lead and len(lead) + len(s) + 1 > hard_cap:
            break
        lead = f"{lead} {s}".strip() if lead else s
        if len(lead) >= target:
            break
    return lead


def strip_tags(fragment: str) -> str:
    fragment = re.sub(r"<br\s*/?>", " ", fragment, flags=re.I)
    fragment = re.sub(r"<[^>]+>", "", fragment)
    return re.sub(r"\s+", " ", html.unescape(fragment)).strip()


def section(page: str, heading: str) -> str:
    """Return the HTML between <hN>HEADING</hN> and the next heading of any level."""
    m = re.search(rf"<h(\d)[^>]*>\s*{heading}\s*</h\1>", page, re.I)
    if not m:
        return ""
    rest = page[m.end():]
    nxt = re.search(r"<h[1-4][^>]*>", rest, re.I)
    return rest[: nxt.start()] if nxt else rest


def extract_bio(page: str) -> "list[str]":
    """Bio paragraphs. Handles both <p> directly under the heading's container and
    <section><p> nesting, which some pages use."""
    block = section(page, "BACKGROUND")
    paras = [strip_tags(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", block, re.S | re.I)]
    return [apply_substitutions(p) for p in paras if len(p) > 40 and not NOISE.match(p)]


def extract_projects(page: str) -> "list[dict]":
    """Project links, one per <li>. A single <li> sometimes splits its title across
    two <a> tags pointing at the same page, so links are merged per list item.

    Only the first <ul> after the heading is considered: some pages have no further
    heading after PROJECTS, so the section runs to the end of the document and would
    otherwise sweep up the site footer's list of every project in the lab."""
    block = section(page, "PROJECTS")
    ul = re.search(r"<ul[^>]*>(.*?)</ul>", block, re.S | re.I)
    if ul:
        block = ul.group(1)
        items = re.findall(r"<li[^>]*>(.*?)</li>", block, re.S | re.I)
    else:
        # Some pages list projects as bare <p><a>…</a></p> instead. Stop at the
        # first </div> so the fallback cannot run on into the page furniture.
        end = block.find("</div>")
        block = block[:end] if end != -1 else block
        items = re.findall(r"<p[^>]*>(.*?)</p>", block, re.S | re.I)

    out, seen = [], set()
    for li in items:
        links = re.findall(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', li, re.S | re.I)
        if not links:
            continue
        url = links[0][0].replace("http://", "https://")
        title = strip_tags(" ".join(t for _, t in links))
        title = re.sub(r"^\s*>\s*", "", title).strip(": ").strip()
        if not title or url in seen:
            continue
        seen.add(url)
        out.append({"title": title, "url": url})
    return out


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", re.sub(r"^\s*the\s+", "", s.strip(), flags=re.I).lower())


def load_projects() -> "list[str]":
    """Canonical project names from _data/projects.yml, used to normalise the
    shouted titles on the source pages and to link to our own Research page."""
    path = os.path.join(ROOT, "_data", "projects.yml")
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        return []
    return re.findall(r'^\s*- name:\s*"(.+)"\s*$', text, re.M)


def slugify(s: str) -> str:
    s = s.lower().replace("&", " ")
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s)).strip("-")


def tidy_title(title: str, canonical: "list[str]") -> "tuple[str, str]":
    """Return (display title, research-page anchor or "").

    Source titles are shouted and verbose — `MOODBUGS: THE EFFECTS OF GUT BACTERIA
    ON EMOTIONS`. Where one matches a project we already describe, use our own name
    and link internally rather than sending people back to the old site.
    """
    head = title.split(":", 1)[0].strip()
    for name in canonical:
        n, h, full = _norm(name), _norm(head), _norm(title)
        if not n or len(n) < 5:
            continue
        if n == h or n.startswith(h) and len(h) >= 6 or full.startswith(n):
            return name, slugify(name)
    if 2 <= len(head) <= 28:
        # Keep a genuine short name or acronym as-is unless it is simply shouted.
        return (head if not head.isupper() or len(head) <= 8 else head.title()), ""
    s = title.lower()
    return s[:1].upper() + s[1:], ""


def read_members() -> "list[tuple[str, str]]":
    """(name, slug) for every member with a kuleuven_id or a slug override."""
    text = open(TEAM, encoding="utf-8").read()
    out, name = [], None
    for line in text.split("\n"):
        m = re.match(r'^\s*- name: "(.+)"\s*$', line)
        if m:
            name = m.group(1)
            if name in SLUG_OVERRIDES:
                out.append((name, SLUG_OVERRIDES[name]))
            continue
        m = re.match(r'^\s*kuleuven_id: "(\d{8})"\s*$', line)
        if m and name:
            out.append((name, m.group(1)))
    return out


def yq(s: str) -> str:
    import json
    return json.dumps(s, ensure_ascii=False)


def merge(harvest: dict) -> int:
    """Rewrite team.yml, replacing any existing bio/projects blocks."""
    lines = open(TEAM, encoding="utf-8").read().split("\n")
    out, i, written = [], 0, 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r'^(\s*)- name: "(.+)"\s*$', line)
        if not m:
            out.append(line)
            i += 1
            continue

        indent, name = m.group(1), m.group(2)
        out.append(line)
        i += 1
        # Copy the member's remaining fields, dropping any previous bio/projects.
        body = []
        while i < len(lines):
            nxt = lines[i]
            if re.match(r'^\s*- name: "', nxt) or re.match(r"^[a-zA-Z#]", nxt):
                break
            if re.match(rf"^{indent}  (bio|bio_lead|projects):", nxt):
                i += 1
                while i < len(lines) and re.match(rf"^{indent}    ", lines[i]):
                    i += 1
                continue
            body.append(nxt)
            i += 1
        # Trailing blank lines and section comments introduce the *next* member,
        # so they must end up after the block we are about to append, not before.
        tail = []
        while body and (not body[-1].strip() or body[-1].lstrip().startswith("#")):
            tail.insert(0, body.pop())
        out.extend(body)

        rec = harvest.get(name)
        if rec:
            if rec["bio"]:
                if rec.get("lead"):
                    out.append(f"{indent}  bio_lead: {yq(rec['lead'])}")
                out.append(f"{indent}  bio:")
                for p in rec["bio"]:
                    out.append(f"{indent}    - {yq(p)}")
            if rec["projects"]:
                out.append(f"{indent}  projects:")
                for p in rec["projects"]:
                    out.append(f"{indent}    - title: {yq(p['title'])}")
                    out.append(f"{indent}      url: {yq(p['url'])}")
                    if p.get("ref"):
                        out.append(f"{indent}      ref: {yq(p['ref'])}")
            written += 1
        out.extend(tail)

    open(TEAM, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    return written


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
        print("Refusing to run. _data/team.yml is the source of truth; edit it directly.")
        print("If you really have a live source, pass --source-is-live.")
        return 1

    canonical = load_projects()
    members = read_members()
    if not members:
        print("No members with a kuleuven_id found in _data/team.yml", file=sys.stderr)
        return 1

    harvest, problems = {}, []
    for name, slug in members:
        try:
            page = get(BASE + slug)
            bio = extract_bio(page)
            projects = []
            if name not in SKIP_PROJECTS:
                seen_ref = set()
                for p in extract_projects(page):
                    slug = p["url"].rstrip("/").rsplit("/", 1)[-1]
                    alias = SLUG_ALIASES.get(slug)
                    if alias:
                        title, ref = alias, slugify(alias)
                    else:
                        title, ref = tidy_title(p["title"], canonical)
                    # The same project can appear twice under slightly different
                    # titles; keep one entry per project.
                    key = ref or title.lower()
                    if key in seen_ref:
                        continue
                    seen_ref.add(key)
                    projects.append({"title": title, "url": p["url"], "ref": ref})
            harvest[name] = {"bio": bio, "lead": make_lead(bio), "projects": projects}
            chars = sum(len(p) for p in bio)
            flag = "" if bio else "   <-- no bio found"
            print(f"  {name:<24} {len(bio)} para {chars:>5} chars  {len(projects)} projects{flag}")
            if not bio:
                problems.append(f"{name}: no BACKGROUND section")
        except Exception as exc:
            problems.append(f"{name}: {type(exc).__name__}: {exc}")
            print(f"  {name:<24} ERROR {exc}")
        time.sleep(DELAY)

    if args.dry_run:
        print("\nDry run — team.yml not modified.")
    else:
        n = merge(harvest)
        print(f"\nMerged bios/projects for {n} members into _data/team.yml")

    if problems:
        print(f"\n{len(problems)} need attention:")
        for p in problems:
            print(f"  · {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
