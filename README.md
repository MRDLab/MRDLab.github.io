# Medical Robotics and Devices Lab — Website

Website for the Medical Robotics and Devices Lab, Department of Mechanical
Engineering, University of Minnesota. Static HTML/CSS/JS, built to be hosted on
GitHub Pages. No build step, no frameworks — edit a file, commit, done.

Colors and typography follow the previous site (`mrd.umn.edu`, UMN "Folwell"
theme): maroon `#7a0019`, gold `#ffcc33`, Open Sans.

---

## Pages

| Nav item | File | What's on it |
|----------|------|--------------|
| Home | `index.html` | Who we are, research focus areas, project summary |
| People | `people.html` | Lead faculty, current members, alumni |
| Projects | `projects.html` | Current and past research projects |
| Publications | — | Links straight out to Dr. Kowalewski's Google Scholar profile |
| Contact | `contact.html` | Directs all inquiries to `timk@umn.edu` |

Publications is an external link, not a page — it opens
[Google Scholar](https://scholar.google.com/citations?user=cNrTOccAAAAJ&hl=en&view_op=list_works&sortby=pubdate)
in a new tab, sorted newest-first so the UMN-era work leads. Note that a
Scholar profile covers an author's whole career, so a handful of pre-2012
papers from his UW PhD appear at the bottom of the list; Scholar has no URL
parameter to filter those out.

---

## Repository layout

```
.
├── index.html              Home
├── people.html             People   (content from js/people-data.js)
├── projects.html           Projects (content from the projects/ folder)
├── contact.html            Contact
├── css/
│   └── style.css           All styling, including the maroon/gold palette
├── js/
│   ├── site.js             Mobile nav + automatic photo fallbacks
│   ├── people-data.js      <-- THE ROSTER. Edit to update People.
│   ├── people-render.js    Builds the People page from the roster
│   └── projects-render.js  Builds the Projects page from projects/
├── projects/               <-- ONE FOLDER PER PROJECT
│   ├── README.md           How to add or edit a project
│   ├── index.json          Project order and active/past status
│   └── <slug>/
│       ├── project.json    That project's text, media list, publications
│       └── *.jpg *.png *.mp4
├── images/
│   ├── README.md           Image conventions
│   ├── shared/             Logo (used on every page)
│   ├── home/               Home page imagery
│   └── people/             Headshots
└── .nojekyll               Tells GitHub Pages to serve files as-is
```

---

## Common edits

### Update the people roster

Edit **`js/people-data.js`** only. Each person is one object:

```js
{
  name:  'Jane Doe',
  role:  'Doctoral Student',
  photo: 'jane-doe.jpg',        // file in images/people/ — or '' for none
  email: 'doe0001@umn.edu',     // optional
  blurb: 'Works on soft catheter robots.'   // optional
}
```

Add the photo to `images/people/`, add the entry, commit. If the photo is
missing or the filename is wrong, the card falls back to a maroon tile with the
person's initials — the layout never breaks.

Entries currently marked `// TODO` are placeholders for the current roster.
Everyone previously listed as a current member has been moved to the `alumni`
array; their degrees and graduation years still need filling in.

### Update a project, or mark one active/past

Everything for a project lives in `projects/<slug>/` — its text in
`project.json`, its pictures and videos alongside it. Edit that file; no HTML
involved. To flip a project between Current and Past, change its `status` in
`projects/index.json`.

All six projects are currently marked `"past"`, so the Projects page shows
them under **Past Projects** with a "Completed" badge. The **Current Projects**
section hides itself entirely until something is marked `"active"`.

Full instructions, including how to add media and new projects, are in
**`projects/README.md`**.

### Add people photos

See `images/README.md` and the README inside each image folder — they list the
exact filenames each page is looking for. Project media does *not* go in
`images/`; it goes in that project's own folder.

### Change the contact email

It appears in several places. To change them all at once:

```bash
grep -rl 'timk@umn.edu' . --include='*.html' | xargs sed -i '' 's/timk@umn.edu/NEW@umn.edu/g'
```

---

## Previewing locally

```bash
cd labmrdwebsite
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

The People and Projects pages **require** the local server — they load their
content with `fetch`, which browsers block on `file://` URLs. Opening the HTML
files directly will show those pages empty.

---

## Publishing

**Live at <https://labmrd.github.io>**

This is a GitHub Pages *user site*, which means:

- The repository is named exactly **`labmrd.github.io`** — that name is what
  produces the root URL. Renaming the repo changes the site's address.
- It must stay **public** (a private user site needs a paid GitHub plan).
- **Settings → Pages** is set to deploy from branch `main`, folder `/ (root)`.

### Updating the live site

```bash
git add -A
git commit -m "Describe the change"
git push
```

Pages rebuilds automatically; the change is live in about a minute. If you
don't see it, hard-reload (`Cmd+Shift+R`) — browsers cache CSS and JS
aggressively.

### Using a custom domain

Add a file named `CNAME` at the repo root containing just the domain (e.g.
`mrd.umn.edu`), then point a DNS CNAME record at `labmrd.github.io`. UMN's IT
group has to make the DNS change for a `umn.edu` domain.

### Using a custom domain

Add a file named `CNAME` at the repo root containing just the domain (e.g.
`mrd.umn.edu`), then point a DNS CNAME record at `labmrd.github.io`. UMN's IT
group has to make the DNS change for a `umn.edu` domain.

---

## Notes

- `.nojekyll` is required. Without it GitHub Pages runs Jekyll, which ignores
  files and folders beginning with an underscore.
- The site uses no external JavaScript. The only third-party request is the
  Open Sans webfont from Google Fonts; it degrades to Helvetica if blocked.
- Headshots on the old site were hosted on Discord links that have since
  expired, so no student photos carried over — they need to be re-collected.
- Project figures and videos *were* recovered from the old site. The three
  animated GIFs (15–56 MB each) were converted to MP4, taking 95 MB down to
  472 KB. Don't commit GIFs — see `projects/README.md` for the command.
- Publication PDFs are linked to their original `me.umn.edu` URLs rather than
  mirrored. Those links worked as of October 2026; if that host is retired,
  they'll need replacing with copies or DOIs.
- Alumni degrees were supplied from memory and still need graduation years.
  The master's and undergraduate degrees in particular were given tentatively —
  confirm them before treating the list as authoritative.
