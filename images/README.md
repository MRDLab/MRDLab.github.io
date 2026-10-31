# Image resources

One folder per page, so it's always obvious where a picture belongs.

| Folder       | Used by        | What goes here |
|--------------|----------------|----------------|
| `shared/`    | every page     | The lab logo and anything else reused site-wide |
| `home/`      | `index.html`   | Hero and research-overview imagery |
| `people/`    | `people.html`  | Headshots, one file per person |
| `projects/`  | `projects.html`| One photo/figure per research project |

Each folder has its own README with naming rules and sizes.

## General rules

- Use lowercase filenames with hyphens: `tim-kowalewski.jpg`, not `Tim K Photo.JPG`.
- Prefer `.jpg` for photographs, `.png` for diagrams, screenshots, and logos.
- Keep files under ~500 KB. Resize before committing — GitHub Pages serves
  these to every visitor. On a Mac you can resize in Terminal:

      sips -Z 1200 big-photo.jpg --out resized.jpg

- Only commit images the lab has the right to publish.
