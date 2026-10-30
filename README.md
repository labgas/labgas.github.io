# labgas.github.io

Source for the [Laboratory for Brain-Gut Axis Studies](https://labgas.github.io) website —
KU Leuven, TARGID.

Built with [Jekyll](https://jekyllrb.com/) and the
[Minimal Mistakes](https://mmistakes.github.io/minimal-mistakes/) theme, pulled in at build time
via `remote_theme`. GitHub Pages builds and deploys the site automatically on every push to
`main`; there is no build step to run yourself and no theme copy to maintain.

**Lab members:** you can update your own biography, photo and projects yourself, in the browser,
without installing anything — see [For lab members](#for-lab-members-updating-your-own-entry)
below. The rest of this README is for whoever maintains the site.

## For lab members: updating your own entry

You do **not** need to install anything, know git, or ask anyone. Everything is edited in the
browser on github.com, and the site rebuilds itself about a minute after you save.

You need a GitHub account that is a member of the [labgas organisation](https://github.com/labgas).
If you are not a member yet, ask Lukas to add you. If you do not have permission to save
directly, GitHub will offer to "propose changes" instead — do that, and someone will approve it.

### The 60-second version

1. Open the file you need (links below) and click the **pencil icon** ✏️ at the top right.
2. Make your change.
3. Scroll down, write a short note like `update my bio`, and click **Commit changes**.
4. Wait about a minute, then reload <https://labgas.github.io> — your change is live.

### Update your biography

Open **[`_data/team.yml`](https://github.com/labgas/labgas.github.io/edit/main/_data/team.yml)**
and find your name. Your entry looks like this:

```yaml
  - name: "Given Family"
    kuleuven_id: "00123456"
    photo: given-family.jpg
    group: phd
    title: "PhD student"
    bio_lead: "The first sentence or two of your bio."
    bio:
      - "The first sentence or two of your bio. Then the rest of the paragraph, which stays hidden until someone clicks Read more."
      - "A second paragraph, if you want one."
```

**The one rule that matters:** `bio_lead` is the part shown before someone clicks "Read more",
and it must be **the exact opening of your first `bio` paragraph, copied word for word**. If the
two differ, your opening sentence appears twice on the page. The safest way is to write your
first paragraph, then copy its first sentence or two into `bio_lead`.

Don't want a "Read more" toggle? Delete the `bio_lead:` line and your whole bio shows at once —
sensible if it is only a few sentences.

Everything sits inside `"double quotes"` on one long line. That is fine — the browser will wrap
it. If your text contains a `"`, write it as `\"`.

### Add or change your photo

Photos are not stored in this file. Send a photo (portrait orientation, head and shoulders, at
least 400×400) to Lukas or Liene and it gets processed and added — it needs resizing and
cropping first, which is not something the browser editor can do.

If your entry has no `photo:` line you currently show as initials in a circle, which is a
perfectly fine thing to leave.

### Add a project to your entry

Under your name, add or edit the `projects:` block:

```yaml
    projects:
      - title: "MoodBugs"
        ref: moodbugs
```

`ref` is the project's name in lower case with spaces and punctuation turned into hyphens, and it
must match a project on the [Research page](https://labgas.github.io/research/) —
`MoodBugs` → `moodbugs`, `SY-NAPS` → `sy-naps`,
`SEM-BEAT — GLP-1 pharmacotherapy optimisation` → `sem-beat-glp-1-pharmacotherapy-optimisation`.
After saving, click
your project chip on the [Team page](https://labgas.github.io/team/) to check it jumps to the
right project. If it scrolls nowhere, the `ref` is wrong.

### Update a project description

Open **[`_data/projects.yml`](https://github.com/labgas/labgas.github.io/edit/main/_data/projects.yml)**.
The short text on the collapsed card is `tagline` and `summary`; everything under `detail:` is
what appears when someone clicks it — description, duration, funding, investigators, team and key
publications. Add a paragraph by adding another `- "…"` line under `description:`.

### Share a poster or talk

Conference presentations are not added here. Push the PDF to the
[`conference_presentations/`](https://github.com/labgas/LaBGAScore/tree/main/conference_presentations)
folder of LaBGAScore, named as its README describes, and within a day a link appears under your
name on the Team page, in a "Conference presentations" row.

### Things that will break the site

The files are YAML, which is fussy about two things:

- **Indentation must be spaces, never tabs**, and must line up with the lines around it. Copy an
  existing entry and edit it rather than typing a new one from scratch.
- **Every piece of text needs its `"quotes"` closed.**

Nothing you do here can break the site permanently, and nothing is ever lost — every version is
kept. If a change is malformed the site simply keeps serving the previous version.

### Checking it worked

The **[Actions tab](https://github.com/labgas/labgas.github.io/actions)** shows a build for every
save: a green tick means your change is live, a red cross means the file has a syntax error.
Click a red one and it will tell you which line. Either fix it, or revert your change and ask for
help — no harm done.

---

## Editing content

Almost everything that changes over time lives in `_data/`, so routine updates never touch
layout or HTML.

| To change | Edit |
|---|---|
| A team member — add, remove, update, add a photo | `_data/team.yml` |
| Team bios and their project links | `_data/team.yml` (`bio_lead`, `bio`, `projects`) |
| Projects on the Research page — name, tagline, summary | `_data/projects.yml` |
| Project descriptions, funding, people | `_data/projects.yml` (`detail:`) |
| The repository index on the Tools page | `_data/repos.yml` (`category`, `desc`; the rest refreshes itself — below) |
| Publication highlights | `scripts/curated_titles.yml` — the page rebuilds itself (below) |
| Recent publications (last 12 months) | nothing — refreshed daily from PubMed (below) |
| Conference presentations on the Team page | nothing here — push the PDF to LaBGAScore (below) |
| Masthead and docs sidebar navigation | `_data/navigation.yml` |
| Site title, description, social links | `_config.yml` |

Page prose lives in `_pages/`, the pipeline documentation in `_docs/`, and news posts in
`_posts/`.

### The repository index keeps itself current

`_data/repos.yml` carries two facts GitHub already knows — each repo's last-push date and its
language — and those go stale the moment anyone pushes anywhere. A scheduled workflow,
[`.github/workflows/refresh-repo-index.yml`](.github/workflows/refresh-repo-index.yml), runs
`scripts/refresh_repos.py` once a day and commits any change, so the index is at most a day
behind. **`category` and `desc` are editorial and are never touched** — GitHub's own descriptions
are terser and less useful than the ones written for the site.

Run it yourself any time, or check without writing:

```bash
python scripts/refresh_repos.py
```

The script also reports what it cannot fix alone: a new repository in the organisation with no
entry yet (adding one needs a category and a description), an entry whose repository has gone,
and any LaBGAScore script name cited in `_docs/` or `_pages/` that no longer exists upstream.
Those appear in the workflow's run summary on the Actions tab.

### Conference presentations come from LaBGAScore

Posters and talks are shared in LaBGAScore's
[`conference_presentations/`](https://github.com/labgas/LaBGAScore/tree/main/conference_presentations)
folder as `<year>/<meeting>/<First_Author_Name>_<topic>_<meeting>_<year>.pdf`. That folder's
README is the guide for lab members.

`scripts/refresh_presentations.py` lists the folder through the GitHub API, matches the start of
each file name against the names in `_data/team.yml` (case, accents, spaces and hyphens
ignored), and writes `_data/presentations.yml`. **That file is generated — do not edit it.** The
Team page shows each person's entries as chips labelled `topic · meeting year`, newest first,
linking to the PDF on GitHub. Only the first author is linked.

The same daily workflow as the repository index runs it, so a pushed PDF appears within a day.
Run it yourself to publish one sooner:

```bash
python scripts/refresh_presentations.py            # rewrite _data/presentations.yml
python scripts/refresh_presentations.py --check    # report drift only, exit 1 if drifted
```

Files it cannot place — a name that breaks the convention, or a first author who is not on the
Team page — are listed in the output and in the workflow's run summary, never guessed. Renaming
someone in `_data/team.yml` unlinks their presentations until the file names match again.

### The dependency page is fetched, not built

`_data/dependencies.yml` backs the [Dependencies](https://labgas.github.io/docs/dependencies/)
page — which script calls into which external repository. The website cannot work this out for
itself: it comes from parsing MATLAB source and resolving every called name against an index of
the installed toolboxes, which needs MATLAB, and GitHub Actions has none.

So the flow has three steps, in this order, and skipping the middle one is the usual mistake:

1. **In the source repo**, regenerate with `LaBGAScore_dep_report` (LaBGAScore's `clean/`).
   That writes `DEPENDENCIES.md`, `dependencies.tsv` and `dependencies.yml` there.
2. **Commit and push** that repo. `refresh_dependencies.py` reads from the **GitHub API**, not
   from your local clone, so an uncommitted regeneration is invisible to it.
3. **Then**, here:

   ```bash
   python scripts/refresh_dependencies.py            # rewrite _data/dependencies.yml
   python scripts/refresh_dependencies.py --check    # report drift only, exit 1 if drifted
   ```

It collects from two sources: `LaBGAScore` (repo root, `main`) and `CANlab_help_examples`
(`Second_level_analysis_template_scripts/`, `master` — that folder's 20 maintained scripts, not
the ~113 present). If a repository's `dependencies.yml` is stale or missing the script says so
for a human to fix upstream; it deliberately cannot repair it here.

The `collected:` date at the top of `_data/dependencies.yml` says when it last ran. If it
predates a change you made in a source repo, the page is behind.

### Checking the site before pushing

```bash
python scripts/validate_site.py
```

Catches broken internal links, missing photos and malformed front matter. It does **not** catch
everything — a navigation chip pointing at a heading that does not exist still renders and
scrolls nowhere (see [Editing a person's projects](#editing-a-persons-projects)) — so treat a
clean run as necessary, not sufficient.

### Adding a team member

Append to the `members:` list in `_data/team.yml`:

```yaml
  - name: "Given Family"
    kuleuven_id: "00123456"     # optional; 8-digit KU Leuven person number
    group: phd          # pi | guest | coordinator | assistant | postdoc | phd | clinical_phd | students | alumni | former_phd
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

Groups render in the order of the `groups:` list at the top of `_data/team.yml`, and a group with
no members is skipped. When a PhD student defends, move them to `group: former_phd` and set
`title` to `"PhD (year)"`; bio, photo and project chips stay as they are.

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
`SEM-BEAT — GLP-1 pharmacotherapy optimisation` → `sem-beat-glp-1-pharmacotherapy-optimisation`.
Get it wrong and
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

### Marking a project as completed

Add `status: completed` to the project in `_data/projects.yml`:

```yaml
  - name: "From Pavlov to visceroception"
    line: symptoms
    status: completed
```

It then moves out of its research line into the **Completed projects** section at the bottom of
the Research page. Keep `line` — it still records which research line the work belongs to. The
project's anchor does not change, so team members' project chips keep working.

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
photo. Portraits are rendered in black and white, which is what lets photos shot in wildly
different light sit in one grid; pass `--colour` if you would rather they were true to the
originals.

### Publications: recent ones arrive by themselves, highlights are chosen

The Publications page has two parts.

**Recent publications**, at the top, lists every PubMed paper from the last 12 months with Van
Oudenhove L as author and a Leuven affiliation. `scripts/refresh_recent_publications.py` writes it
to `_data/recent_publications.yml` (generated — do not edit) in the same daily workflow as the
repository index. Nothing to do here.

**The research-line sections** are curated highlights. When the daily run finds a paper it has
not reported before, it opens a **GitHub issue assigned to Lukas** listing each one with a
suggested research line and the line to paste. The suggestion comes from keyword rules
(`LINE_KEYWORDS` in the script) — check it. To make a paper a highlight, add its title under the
right line in `scripts/curated_titles.yml`, in the browser, and commit. The
[`enrich-publications`](.github/workflows/enrich-publications.yml) workflow then runs
`scripts/enrich_publications.py` and commits the rebuilt `_data/publications.yml` — nothing to
run locally. A highlight from the last 12 months appears in both parts, by design. Close the
issue when done; skipped papers need nothing.

Which papers have been reported is kept in `reported:` at the bottom of
`_data/recent_publications.yml`; delete a PMID there to have it raised again.

To rebuild the highlights by hand:

```bash
python scripts/enrich_publications.py
```

It resolves each title against the PubMed API and regenerates `_data/publications.yml` with
authors, journal, year, volume, pages, PMID and DOI. Do not edit that file by hand — it is
overwritten on every run. The workflow refuses to commit if any title fails to resolve, so a
PubMed hiccup cannot strip existing entries; the run log names the title.

It checks that Van Oudenhove actually appears in the author list of each match and reports
anything it could not resolve. This matters: a plain PubMed search for `Van Oudenhove L` also
returns work by an unrelated researcher in entomology, so unverified matches are a real risk.
There is a second namesake, Lore Van Oudenhove (Ghent), and a Leuven co-author can let her
papers through an affiliation filter. `refresh_recent_publications.py` therefore also checks
the author's forename — or, where PubMed gives only an initial, Leuven in that author's own
affiliation.

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
_data/              team, projects, repos, publications, recent_publications, presentations, navigation
_sass/              custom skin and components
_includes/head/     favicon and theme-colour tags
assets/images/      logo, social image, team photos
scripts/            publication enrichment
```

## Licence

Site content is CC BY 4.0; see [LICENSE](LICENSE). Software referenced from this site is
licensed separately in its own repository — LaBGAScore is GPL-3.0.
