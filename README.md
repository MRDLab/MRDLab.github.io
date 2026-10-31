# Medical Robotics and Devices Lab — Website

Website for the Medical Robotics and Devices Lab, Department of Mechanical
Engineering, University of Minnesota. Static HTML/CSS/JS, built to be hosted on
GitHub Pages. No build step, no frameworks — edit a file, commit, done.

Colors and typography follow the previous site (`mrd.umn.edu`, UMN "Folwell"
theme): maroon `#7a0019`, gold `#ffcc33`, Open Sans.

---

## Pages

| File | Page | What's on it |
|------|------|--------------|
| `index.html` | Home | Who we are, research focus areas, active-project summary |
| `people.html` | People | Lead faculty, current members, alumni |
| `projects.html` | Projects | The six active research projects |
| `contact.html` | Contact | Directs all inquiries to `timk@umn.edu` |

Archived/past projects are intentionally not included.

---

## Repository layout

```
.
├── index.html            Home
├── people.html           People   (content comes from js/people-data.js)
├── projects.html         Projects (content is in the HTML)
├── contact.html          Contact
├── css/
│   └── style.css         All styling, including the maroon/gold palette
├── js/
│   ├── site.js           Mobile nav + automatic photo fallbacks
│   ├── people-data.js    <-- THE ROSTER. Edit this to update People.
│   └── people-render.js  Builds the People page from the roster
├── images/
│   ├── README.md         Image conventions
│   ├── shared/           Logo (used on every page)
│   ├── home/             Home page imagery
│   ├── people/           Headshots
│   └── projects/         Project photos
└── .nojekyll             Tells GitHub Pages to serve files as-is
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

### Update a project

Edit `projects.html` directly. Each project is one
`<article class="project">` block. Copy one to add another; they alternate
image-left / image-right automatically.

### Add project or people photos

See `images/README.md` and the README inside each image folder — they list the
exact filenames each page is looking for.

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

Opening the `.html` files directly with `file://` mostly works, but the People
page needs the local server, since it loads its roster via JavaScript.

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
