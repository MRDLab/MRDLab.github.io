# people/

Headshots for the People page (`people.html`).

## How to add someone's photo

1. Save the photo here as `firstname-lastname.jpg` (all lowercase, hyphenated).
2. Open `js/people-data.js` and set that person's `photo:` field to the
   filename, e.g. `photo: 'tim-kowalewski.jpg'`.

That's it — the page builds itself from that file.

## If there's no photo yet

Leave `photo: ''`. The card shows a maroon tile with the person's initials
instead, so the page still looks finished. The same tile appears automatically
if a filename is wrong or the file is missing, so a typo never breaks the layout.

## Format

- **Square crops**, roughly 600x600. Non-square images get center-cropped.
- Head and shoulders, face in the upper-middle of the frame.
- JPEG, under ~300 KB. Resize with:

      sips -Z 600 original.jpg --out firstname-lastname.jpg

## Expected filenames

`js/people-data.js` currently refers to:

- `tim-kowalewski.jpg` — lead faculty

Everyone else is a placeholder awaiting the current roster.
