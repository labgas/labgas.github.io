"""Refresh the repo-derived facts in _data/repos.yml from the GitHub API.

The Tools page indexes every repository in the github.com/labgas organisation.
Two fields on each entry are facts GitHub already knows and that go stale on
every push — `updated` and `lang` — so they are refreshed from the API rather
than maintained by hand. `category` and `desc` are editorial and are never
touched: GitHub's own descriptions are terser and less useful than the ones
written for the site.

    python scripts/refresh_repos.py            # rewrite the file in place
    python scripts/refresh_repos.py --check    # report drift, change nothing
                                               # (exit 1 if anything drifted)

It also reports what it cannot fix on its own:

  * repositories in the organisation with no entry on the site, and entries
    whose repository has gone. Adding one needs a category and a description,
    which is a judgement call, so it is flagged rather than guessed.
  * LaBGAScore file names cited in _docs/ and _pages/ that no longer exist in
    the repository. The site deliberately names very few scripts and links out
    for the rest, but the ones it does name should resolve.

Editing is line-based rather than a YAML round-trip, because the file carries
comments and folded block scalars that a load/dump cycle would flatten.

Runs unauthenticated; set GITHUB_TOKEN to lift the API rate limit.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

ORG = "labgas"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPOS_YML = os.path.join(ROOT, "_data", "repos.yml")

# The repository whose file names the documentation cites.
DOCS_REPO = "LaBGAScore"

# This repository is the website itself; it is not part of the index.
EXCLUDE = {"labgas.github.io"}


def api(path: str):
    req = urllib.request.Request(
        "https://api.github.com/" + path,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "labgas.github.io-refresh-repos",
        },
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def fetch_repos() -> dict:
    """name -> {pushed, lang, default_branch}, for every repo in the org."""
    out, page = {}, 1
    while True:
        batch = api("orgs/%s/repos?per_page=100&page=%d" % (ORG, page))
        if not batch:
            break
        for r in batch:
            if r["name"] in EXCLUDE:
                continue
            out[r["name"]] = {
                "pushed": r["pushed_at"][:10],
                # A repo of only data files reports no language; keep whatever
                # the site already says rather than blanking the column.
                "lang": r.get("language"),
                "default_branch": r.get("default_branch", "main"),
            }
        page += 1
    return out


def fetch_tree(repo: str, branch: str) -> set:
    data = api("repos/%s/%s/git/trees/%s?recursive=1" % (ORG, repo, branch))
    return {n["path"] for n in data.get("tree", []) if n.get("type") == "blob"}


def cited_filenames() -> dict:
    """File names the site mentions -> the pages mentioning them."""
    pattern = re.compile(r"(?:LaBGAScore_[A-Za-z0-9_]+\.m|README_[A-Za-z0-9_]+\.md)")
    found = {}
    for sub in ("_docs", "_pages"):
        d = os.path.join(ROOT, sub)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".md"):
                continue
            text = open(os.path.join(d, fn), encoding="utf-8").read()
            for name in pattern.findall(text):
                found.setdefault(name, set()).add("%s/%s" % (sub, fn))
    return found


def rewrite(lines: list, live: dict, today: str) -> "tuple[list, list]":
    """Return (new lines, list of human-readable changes)."""
    out, changes, current = [], [], None
    for line in lines:
        m = re.match(r"^(\s*-\s+name:\s*)(\S+)\s*$", line)
        if m:
            current = m.group(2)
            out.append(line)
            continue

        if current and current in live:
            m = re.match(r'^(\s*updated:\s*)"?([\d-]+)"?\s*$', line)
            if m:
                new = live[current]["pushed"]
                if new != m.group(2):
                    changes.append("%s  updated %s -> %s" % (current, m.group(2), new))
                    line = '%s"%s"\n' % (m.group(1), new)
                out.append(line)
                continue

            m = re.match(r"^(\s*lang:\s*)(.+?)\s*$", line)
            if m:
                new = live[current]["lang"]
                old = m.group(2).strip('"')
                if new and new != old:
                    changes.append("%s  lang %s -> %s" % (current, old, new))
                    line = "%s%s\n" % (m.group(1), new)
                out.append(line)
                continue

        m = re.match(r'^(compiled:\s*)"?([\d-]+)"?\s*$', line)
        if m:
            if m.group(2) != today:
                changes.append("compiled  %s -> %s" % (m.group(2), today))
                line = '%s"%s"\n' % (m.group(1), today)
            out.append(line)
            continue

        out.append(line)
    return out, changes


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="report drift without writing; exit 1 if anything drifted")
    args = ap.parse_args()

    try:
        live = fetch_repos()
    except urllib.error.URLError as exc:
        print("Could not reach the GitHub API: %s" % exc)
        return 2

    lines = open(REPOS_YML, encoding="utf-8").readlines()
    indexed = set(re.findall(r"^\s*-\s+name:\s*(\S+)\s*$", "".join(lines), re.M))

    # The newest push across the org is a more honest "compiled" date than
    # today: it says how current the data is, not when the script last ran.
    today = max((r["pushed"] for r in live.values()), default="")

    new_lines, changes = rewrite(lines, live, today)

    print("%d repositories in the organisation, %d indexed on the site."
          % (len(live), len(indexed)))

    if changes:
        print("\n%d field(s) drifted:" % len(changes))
        for c in changes:
            print("  " + c)
    else:
        print("\nAll `updated` and `lang` fields are current.")

    notes = []
    for name in sorted(set(live) - indexed):
        notes.append("in the organisation but not on the site: %s "
                     "(needs a category and a description)" % name)
    for name in sorted(indexed - set(live)):
        notes.append("on the site but no longer in the organisation: %s" % name)

    # Script names the docs cite must still exist upstream.
    if DOCS_REPO in live:
        try:
            paths = fetch_tree(DOCS_REPO, live[DOCS_REPO]["default_branch"])
            basenames = {os.path.basename(p) for p in paths}
            for name, pages in sorted(cited_filenames().items()):
                if name not in basenames:
                    notes.append("%s is cited in %s but no longer exists in %s"
                                 % (name, ", ".join(sorted(pages)), DOCS_REPO))
        except urllib.error.URLError as exc:
            notes.append("could not check cited file names: %s" % exc)

    if notes:
        print("\nNeeds a human:")
        for n in notes:
            print("  · " + n)

    if args.check:
        if changes:
            print("\n--check: drift found, file not written.")
            return 1
        return 0

    if changes:
        with open(REPOS_YML, "w", encoding="utf-8", newline="") as fh:
            fh.writelines(new_lines)
        print("\nWrote _data/repos.yml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
