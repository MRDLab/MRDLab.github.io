# home/

Images for the home page (`index.html`).

| File | Purpose |
|------|---------|
| `research-banner.png` | The "Research at a glance" strip, carried over from the previous site. |

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
