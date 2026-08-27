"""Static checks on the site source, without needing Jekyll or Ruby.

Verifies that:
  * every _data/*.yml file parses as YAML;
  * every page, doc and post has valid YAML front matter;
  * every internal link points at a permalink that actually exists;
  * data files referenced by templates have the fields those templates expect.

Run:  python scripts/validate_site.py
Exits non-zero if anything fails, so it can be used as a pre-push check.
"""

from __future__ import annotations

import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
# {{ '/docs/setup/' | relative_url }}
LIQUID_LINK = re.compile(r"\{\{\s*'([^']+)'\s*\|\s*relative_url\s*\}\}")
# Plain markdown links to absolute site paths
MD_LINK = re.compile(r"\]\((/[^)\s]*)\)")

problems: "list[str]" = []
notes: "list[str]" = []


def fail(msg: str) -> None:
    problems.append(msg)


def rel(path: str) -> str:
    return os.path.relpath(path, ROOT).replace("\\", "/")


def content_files() -> "list[str]":
    out = []
    for sub in ("_pages", "_docs", "_posts"):
        d = os.path.join(ROOT, sub)
        if os.path.isdir(d):
            for name in sorted(os.listdir(d)):
                if name.endswith((".md", ".markdown", ".html")):
                    out.append(os.path.join(d, name))
    idx = os.path.join(ROOT, "index.md")
    if os.path.isfile(idx):
        out.append(idx)
    return out


def check_data() -> dict:
    data = {}
    d = os.path.join(ROOT, "_data")
    if not os.path.isdir(d):
        fail("_data/ is missing")
        return data
    for name in sorted(os.listdir(d)):
        if not name.endswith((".yml", ".yaml")):
            continue
        path = os.path.join(d, name)
        try:
            with open(path, encoding="utf-8") as fh:
                data[os.path.splitext(name)[0]] = yaml.safe_load(fh)
        except yaml.YAMLError as exc:
            fail(f"{rel(path)}: invalid YAML — {exc}")
    return data


def check_front_matter(files: "list[str]") -> "tuple[set, dict]":
    permalinks, meta = set(), {}
    for path in files:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        m = FRONT_MATTER.match(text)
        if not m:
            fail(f"{rel(path)}: no YAML front matter")
            continue
        try:
            fm = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError as exc:
            fail(f"{rel(path)}: invalid front matter — {exc}")
            continue
        meta[path] = fm
        if not fm.get("title") and "404" not in path:
            fail(f"{rel(path)}: front matter has no title")
        pl = fm.get("permalink")
        if pl:
            permalinks.add(pl if pl.endswith("/") or "." in os.path.basename(pl) else pl + "/")
        elif path.endswith(("index.md",)):
            permalinks.add("/")
        elif "_posts" in path:
            # Posts get a generated permalink; record the file so links to it
            # are not reported, but they are rarely linked directly.
            pass
    return permalinks, meta


def check_links(files: "list[str]", permalinks: set) -> None:
    # Anchors on a page are not resolvable statically; strip them.
    known = {p.rstrip("/") or "/" for p in permalinks}
    known.add("/")
    for path in files:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        targets = set(LIQUID_LINK.findall(text)) | set(MD_LINK.findall(text))
        for t in targets:
            if t.startswith("//") or t.startswith("http"):
                continue
            base = t.split("#", 1)[0].split("?", 1)[0]
            if base in ("", "/"):
                continue
            # Asset and file references resolve to real files on disk.
            if re.search(r"\.\w{2,5}$", base):
                if not os.path.isfile(os.path.join(ROOT, base.lstrip("/"))):
                    fail(f"{rel(path)}: link to missing file {t}")
                continue
            if base.rstrip("/") not in known:
                fail(f"{rel(path)}: link to unknown page {t}")


def check_expected_fields(data: dict) -> None:
    team = data.get("team") or {}
    groups = {g.get("id") for g in team.get("groups", [])}
    members = team.get("members", [])
    if not members:
        fail("_data/team.yml: no members")
    for m in members:
        if not m.get("name"):
            fail("_data/team.yml: a member has no name")
        if m.get("group") not in groups:
            fail(f"_data/team.yml: {m.get('name')} has unknown group {m.get('group')!r}")
        photo = m.get("photo")
        if photo and not os.path.isfile(os.path.join(ROOT, "assets", "images", "team", photo)):
            fail(f"_data/team.yml: {m.get('name')} references missing photo {photo}")
    notes.append(f"team: {len(members)} members across {len(groups)} groups")

    projects = (data.get("projects") or {}).get("projects", [])
    valid_lines = {"symptoms", "appetite", "microbiota"}
    for p in projects:
        if p.get("line") not in valid_lines:
            fail(f"_data/projects.yml: {p.get('name')} has unknown line {p.get('line')!r}")
    notes.append(f"projects: {len(projects)}")

    repos = (data.get("repos") or {}).get("repos", [])
    for r in repos:
        if r.get("category") not in {"methods", "study"}:
            fail(f"_data/repos.yml: {r.get('name')} has unknown category {r.get('category')!r}")
    notes.append(f"repos: {len(repos)}")

    pubs = data.get("publications") or {}
    items = pubs.get("items", [])
    line_ids = {l.get("id") for l in pubs.get("lines", [])}
    unverified = [p for p in items if not p.get("verified")]
    no_doi = [p for p in items if not p.get("doi")]
    for p in items:
        if p.get("line") not in line_ids:
            fail(f"_data/publications.yml: unknown line {p.get('line')!r}")
    if unverified:
        fail(f"_data/publications.yml: {len(unverified)} unverified entries — re-run enrich_publications.py")
    notes.append(f"publications: {len(items)} items, {len(no_doi)} without DOI")

    nav = data.get("navigation") or {}
    if not nav.get("main"):
        fail("_data/navigation.yml: no main navigation")


def main() -> int:
    data = check_data()
    files = content_files()
    if not files:
        fail("no content files found")
    permalinks, _ = check_front_matter(files)

    # Navigation targets must resolve too.
    nav = (data.get("navigation") or {})
    known = {p.rstrip("/") or "/" for p in permalinks} | {"/"}
    for section in nav.values():
        for entry in section or []:
            for item in [entry] + (entry.get("children") or []):
                url = item.get("url")
                if url and not url.startswith("http") and url.rstrip("/") not in known:
                    fail(f"_data/navigation.yml: '{item.get('title')}' points at unknown page {url}")

    check_links(files, permalinks)
    check_expected_fields(data)

    print(f"Checked {len(files)} content files and {len(data)} data files.")
    for n in notes:
        print(f"  · {n}")
    if problems:
        print(f"\n{len(problems)} problem(s):")
        for p in problems:
            print(f"  ✗ {p}")
        return 1
    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
