# People/

Everything about each lab member lives here — one folder per person, holding
their `info.txt` and their photo. The People page is generated from these
folders.

```
People/
├── Professor/
│   └── Tim Kowalewski/
│       ├── info.txt
│       └── tim-kowalewski.jpg
├── PhD_Students/
│   ├── Ethan Foley/info.txt
│   └── Rolando Gonzalez/info.txt
├── Masters_Students/
├── Undergraduate_Students/
└── Alumni/
    ├── _past-members.txt         long list: just names + degrees
    └── Jared Schultz/            alumni who get a full card
```

---

## The three-step routine

### 1. Paste what they sent you

Open that person's `info.txt`. Fill in any fields you have, and paste their
blurb under `Bio:` — as many lines and paragraphs as you like. Blank fields are
skipped; `#` lines are comments.

```
Name: Ethan Foley
Role: Doctoral Student, Mechanical Engineering
Email: foley123@umn.edu
LinkedIn: https://linkedin.com/in/...

Bio:
Ethan works on soft robotic actuators for minimally invasive procedures.
He joined the lab in 2025 after finishing his B.S. at ...
```

Recognized fields: **Name, Role, Lab Role, Interests, Email, Website,
Portfolio, LinkedIn, Google Scholar, GitHub, Photo, Photo Focus, File**.
Anything after `Bio:` becomes their card text.

`Interests:` is a shortcut — "Interests: robotics, controls" renders as
"Interested in robotics, controls." If you give both `Interests:` and a `Bio:`,
the interests sentence leads and the bio follows.

### Degrees: lab only

`Role:` lists the degree earned (or being earned) **with this lab** — not prior
degrees from other institutions. Those belong on the person's LinkedIn, which
is linked on the card anyway. This keeps cards uniform and short.

Someone who earned more than one degree here gets a `Role:` line for each,
most recent first:

```
Role: M.S. Robotics (MnRI), 2026
Role: B.S. Computer Engineering, 2024
```

### Downloadable files

Drop a PDF in the person's folder and point at it. Repeat for more than one:

```
File: Engineering Portfolio.pdf | Portfolio
File: resume.pdf | Resume
```

The text after `|` is the link label. The build script copies the file into
`files/people/` under a URL-safe name and marks the link as a download.

### Lab duties

`Lab Role:` is for a job someone holds *alongside* their degree — it shows as a
gold tag under their title:

```
Role: Doctoral Student, Mechanical Engineering
Lab Role: Lab Safety Officer
```

Leave it out for everyone who doesn't hold such a role.

### 2. Drop in a photo

Put an image file in that person's folder. **Any size, any filename** — a
straight-off-the-phone 4000px photo is fine. The build script finds it
automatically and writes a web-sized copy to `images/people/`.

Only set `Photo:` in `info.txt` if the folder has more than one image and you
need to pick which one.

Photos are cropped to a square with the focus slightly above centre, which
suits most portraits. If someone's crop sits wrong, nudge it for that person
only:

```
Photo Focus: 50% 10%     # higher up the image
Photo Focus: 50% 40%     # lower down
```

The first number is horizontal, the second vertical — both measured from the
top-left of the photo.

### 3. Rebuild

```bash
python3 tools/build_people.py
```

Then commit and push. That's it — no HTML or JavaScript to touch.

> `js/people-data.json` is **generated**. Don't edit it by hand; the script
> overwrites it every run.

---

## Ordering people within a group

By default a group lists its people alphabetically. To control the order — by
seniority, say — add an `_order.txt` to that group's folder:

```
# People/PhD_Students/_order.txt
# Most senior first. One folder name per line.

Amit Manicka
Ethan Foley
Rolando Gonzalez
```

Anyone you don't list is appended alphabetically after those you do, and the
build script prints a reminder naming them — so forgetting to add a new
student never drops them from the page.

Any group can have an `_order.txt`; only `PhD_Students/` has one right now.

---

## Adding or removing people

**New person**: make a folder under the right group, add an `info.txt` (copy
one from a teammate), rebuild. The folder name is used as their name if
`info.txt` has no `Name:` line.

**Someone leaves**: move their whole folder into `Alumni/`, or — if they don't
need a full card — delete the folder and add a line to
`Alumni/_past-members.txt`. Rebuild; their old headshot is cleaned out of
`images/people/` automatically.

**New group** (e.g. postdocs): make the folder, then add it to the `GROUPS`
list near the top of `tools/build_people.py` with a title and a default role.

---

## How groups map to the page

| Folder | Section heading | Default Role |
|--------|-----------------|--------------|
| `Professor/` | Lead Faculty | Lead Faculty / Principal Investigator |
| `PhD_Students/` | Doctoral Students | Doctoral Student, Mechanical Engineering |
| `Masters_Students/` | Master's Students | Master's Student, Robotics (MnRI) |
| `Undergraduate_Students/` | Undergraduate Researchers | Undergraduate Researcher, Mechanical Engineering |
| `Alumni/` | Lab Alumni | — |

The default Role is only a starting point — whatever is on the `Role:` line in
`info.txt` wins. Nathan Harbinson is already set to Mechanical Engineering
rather than MnRI.

## Alumni: cards vs. the list

- A folder with an `info.txt` → a **full card** with photo and bio, shown at
  the top of the Lab Alumni section.
- A line in `_past-members.txt` (`Name | Degree`) → an entry in the **compact
  list** below.

Use the list for the long historical roster; use folders for people whose work
you want to keep visible.

## No photo yet?

Nothing breaks. The card shows a maroon tile with the person's initials until
an image appears in their folder. The build script prints a reminder for
everyone still missing one.
