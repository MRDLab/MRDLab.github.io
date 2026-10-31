# home/

Images for the home page (`index.html`).

| Path | Purpose |
|------|---------|
| `research/*.jpg`, `research/skill-evaluation.png` | The four "Research at a glance" panels |

The original `research-banner.png` was a single image with the four section
labels baked into the pixels, which fails **WCAG 1.4.5 (Images of Text)**. It
was split into four panels; the labels are real text in `index.html`. If you
replace a panel, keep its label as HTML text rather than burning it into the
image.

## Adding a hero photo

The hero currently uses a textured maroon gradient (no image needed). To use a
real lab photo instead, drop a wide shot here — e.g. `hero.jpg`, about
2000x900, under 500 KB — and in `css/style.css` add to the `.hero` rule:

    background-image:
      linear-gradient(rgba(77, 0, 16, .78), rgba(77, 0, 16, .78)),
      url('../images/home/hero.jpg');
    background-size: cover;
    background-position: center;

The dark maroon overlay in the first line keeps the white headline readable.
