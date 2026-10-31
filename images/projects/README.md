# projects/

One image per research project on `projects.html`.

## Expected filenames

The page already points at these. Drop a file in with the matching name and it
appears; until then a maroon placeholder tile shows the filename it's waiting for.

| File | Project |
|------|---------|
| `bioprinting.jpg` | 3D Bioprinting Directly Onto Moving Human Anatomy |
| `soft-catheter-robots.jpg` | Soft Catheter Robots |
| `shared-control.jpg` | Shared Control |
| `surgical-skill-evaluation.jpg` | Surgical Skill Evaluation |
| `tissue-identification.jpg` | Tissue Identification |
| `tissue-characterization.jpg` | In-vivo and Ex-vivo Tissue Characterization |

## Format

- **Landscape**, roughly 1200x800. Images are center-cropped to fill the panel.
- Photos of hardware and experiments read better than text-heavy figures —
  the panel is fairly small.
- JPEG, under ~400 KB:

      sips -Z 1200 original.jpg --out bioprinting.jpg

## Adding a new project

In `projects.html`, copy one whole `<article class="project">...</article>`
block, change the `id`, title, text, and the image filename. Projects alternate
image-left / image-right automatically.
