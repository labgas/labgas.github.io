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
| Team bios and their project links | `_data/team.yml` (`bio_lead`, `bio`, `projects`) |
| Projects on the Research page — name, tagline, summary | `_data/projects.yml` |
| Project descriptions, funding, people | `_data/projects.yml` (`detail:`) |
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

### Editing a biography

Bios live in `_data/team.yml` under each member. Two fields, both plain text:

```yaml
    bio_lead: "The first sentence or two, shown collapsed on the Team page."
    bio:
      - "Full first paragraph. `bio_lead` must be an exact prefix of this."
      - "Second paragraph. Add as many as you like."
```

The Team page shows `bio_lead` and hides the rest behind a "Read more" toggle. It does that by
removing `bio_lead` from the front of the first paragraph, so **`bio_lead` has to match the
opening of `bio[0]` character for character** — otherwise the opening text appears twice. Copy
and paste it rather than retyping. Leave `bio_lead` out entirely and the whole bio shows
uncollapsed, which is fine for a short one.

### Editing a person's projects

```yaml
    projects:
      - title: "MoodBugs"
        ref: moodbugs          # anchor on /research/ — omit and give `url:` for an external link
```

`ref` must match the project's `name` in `_data/projects.yml` slugified: lower case, spaces and
punctuation to hyphens. `MoodBugs` → `moodbugs`, `SY-NAPS` → `sy-naps`,
`GLP-1 pharmacotherapy optimisation` → `glp-1-pharmacotherapy-optimisation`. Get it wrong and
the chip renders but scrolls nowhere; `scripts/validate_site.py` does not currently catch this,
so check the link after editing.

People whose involvement spans everything — the PI and the research coordinator — use
`projects_all: true` instead of a list, plus `projects_link: false` to show it without a link.

### Editing a project description

In `_data/projects.yml`, the collapsed card comes from `name`, `tagline`, `summary`; everything
under `detail:` is what opens when it is clicked:

```yaml
    detail:
      duration: "2021-2026"
      funding: "ERC-Consolidator Grant granted to …"
      investigators: "…"
      team: "…"
      description:
        - "One paragraph per entry."
      publications:
        - "Full citation with a DOI. Rendered under Key publications."
```

`detail.duration` and `detail.funding` override the `period` and `funder` fields on the
collapsed card when both are present.

### About the harvest scripts

`scripts/fetch_team_bios.py` and `scripts/fetch_project_details.py` originally populated all of
the above from the lab's pages on `gbiomed.kuleuven.be`. **That site is being retired, and the
data files above are now the source of truth.** The scripts are kept as a record of where the
text came from and would need re-pointing at a new source to be useful again.

Do not run them against a dead site: they rewrite `bio`/`projects`/`detail` wholesale, so a
failed fetch would replace good content with nothing. They report per-person errors rather than
failing outright, which is exactly the case to avoid here.

`scripts/enrich_publications.py` is unaffected — it reads PubMed, not the KU Leuven site, and
stays the way to refresh the publication list.

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
