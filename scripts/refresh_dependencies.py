"""Refresh _data/dependencies.yml from the dependency data the repos publish.

The Dependencies page shows, for each script in the LaBGAS workflow, which
external repositories it calls into. That data is not something the website
can work out for itself: it comes from parsing MATLAB source with mtree and
resolving every called name against an index of the installed toolboxes,
which needs MATLAB. So each repository generates its own `dependencies.yml`
(via LaBGAScore_dep_report, in LaBGAScore's clean/ folder) and commits it,
and this script simply collects those files.

    python scripts/refresh_dependencies.py            # rewrite the file
    python scripts/refresh_dependencies.py --check    # report drift only
                                                      # (exit 1 if drifted)

Deliberately a fetch rather than a build: GitHub Actions has no MATLAB, so
the site can never regenerate this itself. If a repository's dependencies.yml
is stale or missing, that is reported for a human to fix by re-running the
generator there - it is not something this script can repair.

Runs unauthenticated; set GITHUB_TOKEN to lift the API rate limit.
"""

from __future__ import annotations

import argparse
import datetime
import os
import re
import sys
import urllib.error
import urllib.request

ORG = "labgas"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEPS_YML = os.path.join(ROOT, "_data", "dependencies.yml")

# Repository -> (branch, path to its dependencies.yml). CANlab_help_examples
# publishes from Second_level_analysis_template_scripts/ rather than the repo
# root, because the file documents that folder's 19 maintained scripts and
# nothing else in the repository.
SOURCES = {
    "LaBGAScore": ("main", "dependencies.yml"),
    "CANlab_help_examples": ("master",
                             "Second_level_analysis_template_scripts/dependencies.yml"),
}

# Beyond this, the published data is old enough to be worth mentioning.
STALE_DAYS = 180


def fetch_raw(repo: str, branch: str, path: str) -> str | None:
    url = "https://raw.githubusercontent.com/%s/%s/%s/%s" % (ORG, repo, branch, path)
    req = urllib.request.Request(
        url, headers={"User-Agent": "labgas.github.io-refresh-dependencies"}
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise


def generated_date(text: str) -> str:
    m = re.search(r'^generated:\s*"?([\d-]+)', text, re.M)
    return m.group(1) if m else ""


def indent(text: str, spaces: int) -> str:
    pad = " " * spaces
    return "\n".join(pad + ln if ln.strip() else ln for ln in text.splitlines())


def build(parts: dict) -> str:
    """Compose _data/dependencies.yml from each repo's published block."""
    today = datetime.date.today().isoformat()
    out = [
        "# Dependency data for the LaBGAS MATLAB workflow.",
        "#",
        "# GENERATED - collected by scripts/refresh_dependencies.py from the",
        "# dependencies.yml that each repository publishes. Do not edit here:",
        "# regenerate in the source repository with LaBGAScore_dep_report and",
        "# commit that, then re-run this script.",
        "",
        'collected: "%s"' % today,
        "repos:",
    ]
    for repo in sorted(parts):
        body = parts[repo]
        # strip the per-file comment header; the block is nested here
        body = "\n".join(
            ln for ln in body.splitlines() if not ln.lstrip().startswith("#")
        ).strip("\n")
        out.append("  %s:" % repo)
        out.append(indent(body, 4))
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="report drift without writing; exit 1 if anything drifted",
    )
    args = ap.parse_args()

    parts, notes = {}, []

    for repo, (branch, path) in sorted(SOURCES.items()):
        try:
            text = fetch_raw(repo, branch, path)
        except urllib.error.URLError as exc:
            print("Could not reach GitHub for %s: %s" % (repo, exc))
            return 2

        if text is None:
            notes.append(
                "%s publishes no dependencies.yml - run "
                "LaBGAScore_dep_report('<path to %s>') there and commit the result"
                % (repo, repo)
            )
            continue

        parts[repo] = text
        gen = generated_date(text)
        nscripts = len(re.findall(r"^\s*- name:", text, re.M))
        print("%-24s %d scripts, generated %s" % (repo, nscripts, gen or "?"))

        if gen:
            try:
                age = (datetime.date.today() - datetime.date.fromisoformat(gen)).days
                if age > STALE_DAYS:
                    notes.append(
                        "%s dependency data is %d days old - re-run "
                        "LaBGAScore_dep_report there" % (repo, age)
                    )
            except ValueError:
                pass

    if not parts:
        print("\nNo dependency data found in any source repository.")
        if notes:
            print("\nNeeds a human:")
            for n in notes:
                print("  · " + n)
        return 1

    new = build(parts)
    old = ""
    if os.path.exists(DEPS_YML):
        old = open(DEPS_YML, encoding="utf-8").read()

    # the collected: date changes every run, so compare everything else
    strip = lambda s: re.sub(r'^collected:.*$', "", s, flags=re.M)
    drifted = strip(old) != strip(new)

    if drifted:
        print("\nDependency data has changed since the last collection.")
    else:
        print("\nDependency data is current.")

    if notes:
        print("\nNeeds a human:")
        for n in notes:
            print("  · " + n)

    if args.check:
        if drifted:
            print("\n--check: drift found, file not written.")
            return 1
        return 0

    if drifted or not old:
        os.makedirs(os.path.dirname(DEPS_YML), exist_ok=True)
        with open(DEPS_YML, "w", encoding="utf-8", newline="") as fh:
            fh.write(new)
        print("\nWrote _data/dependencies.yml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
