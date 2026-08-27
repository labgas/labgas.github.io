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
| Projects on the Research page | `_data/projects.yml` |
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
    group: phd          # pi | guest | coordinator | postdoc | phd | students | alumni
    title: "PhD student"
    focus: >-
      One or two sentences. Optional.
    photo: given-family.jpg     # optional; drop the file in assets/images/team/
    kuleuven: "https://..."     # optional
    orcid: "0000-0000-0000-0000"  # optional
```

Without a `photo`, the page renders an initials avatar — so you can add people now and photos
later.

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
