# collaborators/

Logos for the Collaborators strip at the bottom of the home page.

| File | Collaborator | Source |
|---|---|---|
| `visible-heart-laboratory.jpg` | Visible Heart® Laboratories (UMN) | their site's banner photo |
| `rpm-lab.jpg` | Robotics: Perception and Manipulation Lab (MnRI) | their Fall 2025 group photo |
| `medtronic.png` *(not present)* | Medtronic | — wordmark shown instead |

**Why photos and not logos:** neither UMN lab publishes a standalone logo —
the RPM Lab has only a 32x32 favicon and Visible Heart uses the University
wordmark — so their cards use a picture from their own home page. Medtronic's
site blocks automated requests and their logo is a corporate trademark, so
that card shows a wordmark until someone supplies an approved file.

A card marked `class="logo photo"` in `index.html` crops its image to fill the
plate; a plain `class="logo"` fits a logo inside it with padding. Switch the
class if you swap a photo for a real logo.

Drop a file in with the matching name and it appears automatically. Until then
the card shows a clean wordmark instead, so the section looks finished either
way — nothing breaks while you gather logos.

## Format

- **PNG with a transparent background** is ideal; the plate behind the logo is
  white so coloured marks keep their own colours.
- Roughly 400–600px wide, under ~100 KB. Landscape marks sit better than tall
  ones; the plate is 110px high and the logo is scaled to fit inside it.
- `sips -Z 600 original.png --out rpm-lab.png` to resize.

## Before you add a logo — please check permission

These are other organisations' trademarks, not ours. Displaying a partner's
logo normally needs their okay, and most companies publish brand guidelines
covering third-party use:

- **Medtronic** — a corporate trademark. Confirm with the professor that there
  is a current relationship, and check Medtronic's brand/trademark guidelines
  (or ask your contact there) before publishing their mark.
- **Visible Heart® Laboratories** and the **RPM Lab** — both UMN groups, so
  this is usually a quick email to them. Note "Visible Heart" is a registered
  trademark; keep the ® in the name.
- UMN's own marks are governed by University Relations' brand policy.

If in doubt, leave the file out. The wordmark fallback is perfectly
presentable, and naming a collaborator in text carries none of the same
trademark questions that reproducing their logo does.

## Changing who is listed

The three cards are written directly in `index.html` — search for
`collaborators`. Each is one `<a class="collab">` block: copy one to add a
partner, delete one to remove a partner.
