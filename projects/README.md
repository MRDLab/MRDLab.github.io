# projects/

Everything about each research project lives here — its description, its
figures, and its videos — one subdirectory per project.

```
projects/
├── index.json                     which projects exist, their order and status
├── bioprinting/
│   ├── project.json               title, description, media list, publications
│   ├── bioprinting.jpg
│   └── ...
├── soft-catheter-robots/
└── ...
```

The Projects page builds itself from these files (`js/projects-render.js`).
You never need to edit HTML to change a project.

---

## Changing a project's text

Open that project's `project.json` and edit it. The fields:

| Field | What it does |
|-------|--------------|
| `title` | Heading on the Projects page |
| `tagline` | Small maroon line above the title |
| `summary` | One-line version, used on the home page cards |
| `body` | Array of paragraphs. Each string is one `<p>`. |
| `researchers` | Credit line under the text |
| `media` | Images and videos — see below |
| `publications` | Array of `{ "label": "...", "url": "..." }` |

## Adding a picture or video

Put the file in the project's folder, then add an entry to its `media` array.

**Image**
```json
{ "type": "image", "file": "rig-photo.jpg",
  "alt": "Description for screen readers", "caption": "Shown under the image" }
```

**Video file** (`.mp4` — autoplays muted and loops, like a GIF)
```json
{ "type": "video", "file": "demo.mp4", "poster": "demo-poster.jpg",
  "alt": "Description", "caption": "Shown under the video" }
```

**YouTube**
```json
{ "type": "youtube", "id": "6VrozlyELdw", "title": "Video title" }
```
The `id` is the part after `watch?v=` in the URL. Embeds use
`youtube-nocookie.com`, so viewers aren't tracked until they press play.

`alt` is required on images for accessibility. `caption` and `poster` are
optional.

## Marking a project active or past

Edit `index.json`. Each entry is `{ "slug": "folder-name", "status": "past" }`.

- `"status": "active"` → appears under **Current Projects**
- `"status": "past"` → appears under **Past Projects** with a "Completed" badge

The Current Projects section hides itself entirely while nothing is marked
active, so the page never shows an empty heading. The order of the array is the
order on the page.

## Adding a whole new project

1. Make a folder: `projects/my-new-project/`
2. Add a `project.json` — copy one from an existing project and edit it.
3. Drop in the images/videos it references.
4. Add `{ "slug": "my-new-project", "status": "active" }` to `index.json`.

Use lowercase-hyphenated folder names; the slug also becomes the page anchor
(`projects.html#my-new-project`).

---

## Media conventions

- **Images**: JPEG for photographs, PNG for diagrams and plots. Max ~1400px
  wide, under ~400 KB. Resize with `sips -Z 1400 big.jpg --out small.jpg`.
- **Video**: MP4 (H.264, `yuv420p`). Keep clips short and under ~1 MB.
  **Never commit animated GIFs** — the three originally on this site were
  15–56 MB each. Convert them:

      ffmpeg -i clip.gif -movflags +faststart -pix_fmt yuv420p \
             -vf "scale='min(900,trunc(iw/2)*2)':-2" -crf 30 -an clip.mp4
      ffmpeg -i clip.gif -vframes 1 clip-poster.jpg

  That took the three clips here from 95 MB to 472 KB combined.

## Where this media came from

The images and videos in these folders were taken from the previous site at
`mrd.umn.edu` in October 2026. The two YouTube videos are embedded from the
lab's existing uploads rather than copied. Publication PDFs are linked to their
original `me.umn.edu` URLs, not mirrored here — if that host ever goes away,
those links will need replacing with copies or DOIs.
