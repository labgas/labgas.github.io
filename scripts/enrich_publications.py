"""Resolve the curated publication titles against PubMed and write _data/publications.yml.

Reads scripts/curated_titles.yml (title strings grouped by research line) and, for
each title, queries the NCBI E-utilities API for the matching PubMed record. Writes
authors, journal, year, PMID and DOI so the Publications page never has to carry
hand-transcribed citation metadata.

Every hit is checked for "Van Oudenhove" in the author list. This guards against the
well-known namesake problem: a bare PubMed search for "Van Oudenhove L" also returns
work by an unrelated entomologist. Titles that do not resolve, or that resolve to a
record without him as an author, are reported and written with `verified: false` so
they are visible rather than silently wrong.

Usage:  python scripts/enrich_publications.py
No third-party dependencies; stdlib only.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = os.path.join(HERE, "curated_titles.yml")
OUT = os.path.join(ROOT, "_data", "publications.yml")

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
# NCBI asks for identification and <=3 requests/second without an API key.
TOOL = "labgas-github-io"
EMAIL = "lukas.vanoudenhove@kuleuven.be"
DELAY = 0.4

LINE_ORDER = ["symptoms", "appetite", "microbiota", "methods"]
LINE_LABELS = {
    "symptoms": "Gastrointestinal symptom, pain, and fatigue perception",
    "appetite": "Appetite, food intake & reward",
    "microbiota": "Microbiota-gut-brain signalling, stress & affect",
    "methods": "Neuroimaging methods & brain representations",
}


# Dutch/Flemish and other surname particles. PubMed keeps them as part of the
# surname ("Van Den Houte M"), so they must be kept when building the match key
# and used to find where the surname starts.
PARTICLES = {
    "van", "de", "den", "der", "det", "ten", "ter", "te", "vande", "vanden",
    "op", "'t", "in", "di", "da", "del", "della", "dos", "du", "la", "le", "el",
}


def _surname_key(tokens: "list[str]") -> str:
    return re.sub(r"[^a-z]", "", "".join(tokens).lower())


def load_lab_members() -> "list[tuple[str, str]]":
    """(surname key, first initial) for every current lab member.

    Read straight out of _data/team.yml with a regex rather than a YAML parser to
    keep this script dependency-free.
    """
    path = os.path.join(ROOT, "_data", "team.yml")
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        return []
    out = []
    for name in re.findall(r'^\s*- name: "(.+)"\s*$', text, re.M):
        tokens = name.split()
        if len(tokens) < 2:
            continue
        # The surname starts at the first particle, or at the last token.
        start = len(tokens) - 1
        for i, t in enumerate(tokens[1:], start=1):
            if t.lower().strip(".") in PARTICLES:
                start = i
                break
        surname, given = tokens[start:], tokens[:start]
        if not given:
            continue
        out.append((_surname_key(surname), given[0][0].upper()))
    return out


def lab_authors(authors: "list[str]", members: "list[tuple[str, str]]") -> "list[str]":
    """Which of a paper's PubMed author strings are lab members.

    PubMed formats authors as "Surname II". Match on the surname and require the
    member's first initial to appear in the initials, so "Johansson EM" matches
    Elin Marie Johansson while a different Johansson does not.
    """
    hits = []
    for a in authors:
        parts = a.split()
        if len(parts) < 2:
            continue
        initials = parts[-1]
        if not initials.isupper() or len(initials) > 3:
            continue
        key = _surname_key(parts[:-1])
        for m_key, m_initial in members:
            if key == m_key and m_initial in initials:
                hits.append(a)
                break
    return hits


def _get(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": f"{TOOL} ({EMAIL})"})
    with urllib.request.urlopen(req, timeout=60) as fh:
        return json.loads(fh.read().decode("utf-8", "replace"))


def read_seed(path: str) -> "list[tuple[str, str]]":
    """Minimal reader for the seed file: `key:` lines followed by `- "title"` items."""
    out, line = [], None
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            s = raw.rstrip("\n")
            if not s.strip() or s.lstrip().startswith("#"):
                continue
            m = re.match(r"^([A-Za-z_]+):\s*$", s)
            if m:
                line = m.group(1)
                continue
            m = re.match(r'^\s*-\s*"(.*)"\s*$', s)
            if m and line:
                out.append((line, m.group(1)))
    return out


def _esearch(term: str) -> "list[str]":
    url = (
        f"{EUTILS}/esearch.fcgi?db=pubmed&retmode=json&retmax=5"
        f"&tool={TOOL}&email={EMAIL}&term={urllib.parse.quote(term)}"
    )
    return _get(url).get("esearchresult", {}).get("idlist", [])


STOP = {"a", "an", "the", "of", "in", "on", "for", "and", "or", "to", "with", "is", "are"}


def _tokens(s: str) -> "set[str]":
    return {w for w in re.sub(r"[^\w\s]", " ", s.lower()).split() if w not in STOP and len(w) > 2}


def candidates(title: str) -> "list[str]":
    """Collect plausible PubMed IDs for a title, best-guess queries first.

    Parentheses and other punctuation break PubMed's phrase index, and its
    full-title phrase entries are incomplete, so several query shapes are tried
    and their results pooled. Author filtering happens in `resolve`, not here:
    constraining the query by author proved unreliable, whereas checking the
    retrieved author list is exact.
    """
    clean = re.sub(r"[^\w\s-]", " ", title)
    clean = re.sub(r"\s+", " ", clean).strip()
    words = clean.split()

    # PubMed frequently stores a shorter title than FRIS does — it drops long
    # subtitles — so an unquoted [Title] search on the full string ANDs words
    # that are simply not in its record and returns nothing. Walking down to
    # progressively shorter leading fragments is what actually finds these.
    terms = [f'"{title}"[Title]', f'"{clean}"[Title]', f"{clean}[Title]"]
    for n in (8, 6, 5, 4, 3):
        if len(words) >= n:
            terms.append(f'{" ".join(words[:n])}[Title] AND Oudenhove[Author]')
    terms.append(clean)

    seen, out = set(), []
    for term in terms:
        try:
            ids = _esearch(term)
        except Exception:
            ids = []
        time.sleep(DELAY)
        for pmid in ids:
            if pmid not in seen:
                seen.add(pmid)
                out.append(pmid)
        if len(out) >= 12:
            break
    return out[:12]


def resolve(title: str) -> "tuple[str, dict] | tuple[None, None]":
    """Return the first candidate that has Van Oudenhove as an author and a
    title that actually overlaps the one we asked for."""
    want = _tokens(title)
    best_pmid, best_rec, best_score = None, None, 0.0
    for pmid in candidates(title):
        d = summary(pmid)
        time.sleep(DELAY)
        authors = [a.get("name", "") for a in d.get("authors", []) if a.get("authtype") == "Author"]
        if not any("oudenhove" in a.lower() for a in authors):
            continue
        got = _tokens(d.get("title", ""))
        if not got:
            continue
        shared = len(want & got)
        # Symmetric overlap penalises a candidate that merely shares some words
        # with a longer, different title. Taking the *best* scoring candidate
        # rather than the first one over a threshold matters: a same-topic paper
        # by the same author can clear a threshold while the real match sits
        # further down the candidate list.
        symmetric = shared / len(want | got)
        # Containment rescues the opposite case — PubMed often stores only the
        # main clause of a title, so a correct match legitimately scores low on
        # symmetric overlap while being fully contained in what we asked for.
        containment = shared / min(len(want), len(got))
        score = symmetric
        if containment >= 0.9 and min(len(want), len(got)) >= 5:
            score = max(score, containment)
        if score > best_score:
            best_pmid, best_rec, best_score = pmid, d, score
    if best_score >= 0.55:
        return best_pmid, best_rec
    return None, None


def summary(pmid: str) -> dict:
    url = f"{EUTILS}/esummary.fcgi?db=pubmed&retmode=json&tool={TOOL}&email={EMAIL}&id={pmid}"
    return _get(url).get("result", {}).get(pmid, {})


def yq(s: str) -> str:
    """Quote a value for YAML output."""
    return json.dumps("" if s is None else str(s))


def main() -> int:
    members = load_lab_members()
    print(f"Matching authors against {len(members)} lab members\n")
    seeds = read_seed(SEED)
    if not seeds:
        print("No titles found in seed file", file=sys.stderr)
        return 1

    by_line: "dict[str, list[dict]]" = {k: [] for k in LINE_ORDER}
    problems = []

    for i, (line, title) in enumerate(seeds, 1):
        print(f"[{i:>2}/{len(seeds)}] {title[:70]}...", flush=True)
        rec = {"title": title, "line": line, "verified": False}
        try:
            pmid, d = resolve(title)
            if pmid:
                authors = [a.get("name", "") for a in d.get("authors", []) if a.get("authtype") == "Author"]
                doi = ""
                for aid in d.get("articleids", []):
                    if aid.get("idtype") == "doi":
                        doi = aid.get("value", "")
                year = (d.get("pubdate", "") or "").split(" ")[0]
                rec.update(
                    {
                        "title": d.get("title", title).rstrip("."),
                        "authors": authors,
                        "journal": d.get("fulljournalname") or d.get("source", ""),
                        "year": year,
                        "volume": d.get("volume", ""),
                        "issue": d.get("issue", ""),
                        "pages": d.get("pages", ""),
                        "pmid": pmid,
                        "doi": doi,
                        "verified": any("oudenhove" in a.lower() for a in authors),
                        "lab_authors": lab_authors(authors, members),
                    }
                )
                if not rec["verified"]:
                    problems.append((title, f"PMID {pmid} has no Van Oudenhove in author list"))
            else:
                problems.append((title, "no PubMed match"))
        except Exception as exc:  # network hiccup, malformed record, ...
            problems.append((title, f"{type(exc).__name__}: {exc}"))
        by_line.setdefault(line, []).append(rec)

    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Curated publication highlights — GENERATED FILE, do not edit by hand.\n")
        fh.write("# Regenerate with: python scripts/enrich_publications.py\n")
        fh.write("# Source titles: scripts/curated_titles.yml; metadata: NCBI PubMed E-utilities.\n")
        fh.write("# `verified: true` means Van Oudenhove appears in the PubMed author list.\n\n")
        fh.write("lines:\n")
        for key in LINE_ORDER:
            fh.write(f"  - id: {key}\n    label: {yq(LINE_LABELS[key])}\n")
        fh.write("\nitems:\n")
        for key in LINE_ORDER:
            for r in sorted(by_line.get(key, []), key=lambda x: str(x.get("year", "")), reverse=True):
                fh.write(f"  - line: {key}\n")
                fh.write(f"    title: {yq(r.get('title'))}\n")
                fh.write(f"    journal: {yq(r.get('journal'))}\n")
                fh.write(f"    year: {yq(r.get('year'))}\n")
                fh.write(f"    volume: {yq(r.get('volume'))}\n")
                fh.write(f"    issue: {yq(r.get('issue'))}\n")
                fh.write(f"    pages: {yq(r.get('pages'))}\n")
                fh.write(f"    pmid: {yq(r.get('pmid'))}\n")
                fh.write(f"    doi: {yq(r.get('doi'))}\n")
                fh.write(f"    verified: {'true' if r.get('verified') else 'false'}\n")
                authors = r.get("authors") or []
                fh.write("    authors:\n")
                for a in authors:
                    fh.write(f"      - {yq(a)}\n")
                # Author strings belonging to lab members, so the Publications
                # page can bold them without re-deriving the match in Liquid.
                marked = r.get("lab_authors") or []
                if marked:
                    fh.write("    lab_authors:\n")
                    for a in marked:
                        fh.write(f"      - {yq(a)}\n")

    print(f"\nWrote {OUT} ({sum(len(v) for v in by_line.values())} records)")
    if problems:
        print(f"\n{len(problems)} need attention:")
        for t, why in problems:
            print(f"  - {t[:60]}... -> {why}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
