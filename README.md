# labgas.github.io

Source for the [Laboratory for Brain-Gut Axis Studies](https://labgas.github.io) website —
KU Leuven, TARGID.

Built with [Jekyll](https://jekyllrb.com/) and the
[Minimal Mistakes](https://mmistakes.github.io/minimal-mistakes/) theme, pulled in at build time
via `remote_theme`. GitHub Pages builds and deploys the site automatically on every push to
`main`; there is no build step to run yourself and no theme copy to maintain.

## Editing content

Almost everything that changes over time lives in `_data/`, so routine updates never touch
layout or HTML.

| To change | Edit |
|---|---|
| A team member — add, remove, update, add a photo | `_data/team.yml` |
| Team bios and project links | the KU Leuven page, then re-run the harvest (below) |
| Projects on the Research page — name, tagline, summary | `_data/projects.yml` |
| Project descriptions, funding, people | the KU Leuven project page, then re-run the harvest (below) |
| The repository index on the Tools page | `_data/repos.yml` |
| Publication highlights | `scripts/curated_titles.yml`, then re-run the script (below) |
| Masthead and docs sidebar navigation | `_data/navigation.yml` |
| Site title, description, social links | `_config.yml` |

Page prose lives in `_pages/`, the pipeline documentation in `_docs/`, and news posts in
`_posts/`.

### Adding a team member

Append to the `members:` list in `_data/team.yml`:

```yaml
  - name: "Given Family"
    kuleuven_id: "00123456"     # optional; 8-digit KU Leuven person number
    group: phd          # pi | guest | coordinator | postdoc | phd | students | alumni
    title: "PhD student"
    focus: >-
      One or two sentences. Optional.
    photo: given-family.jpg     # optional; see "Adding a photo" below
    orcid: "0000-0000-0000-0000"  # optional
    scholar: "https://scholar.google.com/citations?user=..."  # optional
    email: "given.family@kuleuven.be"   # optional
```

`kuleuven_id` becomes a link to `https://www.kuleuven.be/wieiswie/en/person/<id>` — the
university's public profile with publications, memberships and contact details. Find the number
in the URL of that person's entry on the LaBGAS members page or in any who's who link.

Without a `photo`, the page renders an initials avatar — so you can add people now and photos
later.

### Refreshing bios and project links

Biographies and project lists are not written here — they are pulled from each person's page on
the KU Leuven site so there is a single place to keep them current:

```bash
python scripts/fetch_team_bios.py
```

This rewrites the `bio:` and `projects:` blocks in `_data/team.yml` for everyone with a
`kuleuven_id`, leaving all other fields alone. **Hand-edits to those two fields will not survive
a re-run** — change the source page instead. Use `--dry-run` to see what would change.

Two behaviours worth knowing:

- **House-style wording** lives in `SUBSTITUTIONS` at the top of the script, so edits the lab
  has asked for are re-applied on every run instead of being silently reverted.
- **Project links point at our own Research page**, not back at the KU Leuven site. Source
  titles are matched to `_data/projects.yml`, with an explicit `SLUG_ALIASES` table for the
  ones whose long official titles do not resemble our short names. The table is keyed on the
  source URL slug rather than the title, because two projects have nearly identical titles but
  are different studies. Add an entry there when a new project appears.

People whose project involvement spans the whole portfolio — the PI and the research
coordinator — are marked `projects_all: true` in `_data/team.yml` instead, and listed in
`SKIP_PROJECTS` so the harvest leaves them alone. Add `projects_link: false` to show that
without a link.

### Refreshing project details

Each project on the Research page expands to show its full description, duration, funding,
investigators, team and key publications. That content is harvested from the project pages on
the KU Leuven site:

```bash
python scripts/fetch_project_details.py
```

This rewrites only the `detail:` block of each project in `_data/projects.yml`; the
hand-written `name`, `line`, `tagline` and `summary` — the index-level copy shown when the
project is collapsed — are left alone. Use `--dry-run` to preview.

Where a project has harvested `detail.duration` or `detail.funding`, those take precedence over
the `period` and `funder` fields for the summary line, because the project pages name the actual
funding body where our own summary often only had the category.

`SLUG_ALIASES` in this script is the single mapping from source page slug to our project name.
`fetch_team_bios.py` imports it, so a new project only needs adding in one place. It is keyed on
the URL slug rather than the page title on purpose: the anorexia SCFA project and GUTSIE have
nearly identical titles but are different studies.

### Adding a photo

Put the original in the shared Drive folder
(`LaBGAS/LaBGAS_GENERAL/LaBGAS_website/Profile photos/`), add it to the `PORTRAITS` map in
`scripts/prepare_images.py`, then:

```bash
python scripts/prepare_images.py
```

That crops it square, resizes to 480px and writes it to `assets/images/team/`. Sources are never
committed — some are over 20 MB. If the automatic crop misses the face (full-length shots,
mainly), add a `(centre_x, centre_y, side)` entry to `CROP_OVERRIDES` instead of editing the
photo. `--greyscale` renders all portraits in black and white, if you would rather they were
uniform than true to the originals.

### Adding a publication

Add the title under the appropriate research line in `scripts/curated_titles.yml`, then:

```bash
python scripts/enrich_publications.py
```

The script resolves each title against the PubMed API and regenerates `_data/publications.yml`
with authors, journal, year, volume, pages, PMID and DOI. Do not edit that file by hand — it is
overwritten on every run.

It checks that Van Oudenhove actually appears in the author list of each match and reports
anything it could not resolve. This matters: a plain PubMed search for `Van Oudenhove L` also
returns work by an unrelated researcher in entomology, so unverified matches are a real risk.

### Adding a news post

Create `_posts/YYYY-MM-DD-slug.md` with front matter:

```yaml
---
title: "Headline"
date: 2026-08-27
categories: [research]
tags: [publications]
excerpt: "One sentence shown in listings."
---
```

Posts dated in the future are not built (`future: false`).

### Adding a documentation page

Create a file in `_docs/`, set an explicit `permalink`, and add it to the `docs:` list in
`_data/navigation.yml` so it appears in the sidebar.

## Previewing locally

The site does not need to be built locally to deploy, but previewing before pushing is worth it.

**With Docker** (no Ruby installation required):

```bash
docker run --rm -v "$PWD:/site" -v labgas_gems:/usr/local/bundle -w /site -p 4000:4000 ruby:3.3 bash -c "bundle install && bundle exec jekyll serve --host 0.0.0.0"
```

**With a local Ruby** (3.3 recommended — the `github-pages` gem expects stdlib gems that 3.4
dropped):

```bash
bundle install
bundle exec jekyll serve --livereload
```

Then open <http://localhost:4000>.

> **Note for KU Leuven managed Windows machines:** AppLocker blocks executables outside
> `C:\Program Files` and `C:\Windows`, so a RubyInstaller installation to `C:\Ruby33-x64` will
> not run. Use the Docker route above, which is unaffected because `docker.exe` lives in an
> allowed path.

## Deploying

Push to `main`. GitHub Pages builds the site and publishes it at
<https://labgas.github.io>. Build errors appear under the repository's **Actions** tab.

Repository settings must have **Pages → Source** set to *Deploy from a branch*, branch `main`,
folder `/`.

## Structure

```
_config.yml         site configuration
index.md            home page
_pages/             research, team, publications, tools, docs, join, search, 404, news
_docs/              pipeline documentation (a Jekyll collection)
_posts/             news
_data/              team, projects, repos, publications, navigation
_sass/              custom skin and components
_includes/head/     favicon and theme-colour tags
assets/images/      logo, social image, team photos
scripts/            publication enrichment
```

## Licence

Site content is CC BY 4.0; see [LICENSE](LICENSE). Software referenced from this site is
licensed separately in its own repository — LaBGAScore is GPL-3.0.
