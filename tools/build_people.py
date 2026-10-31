#!/usr/bin/env python3
"""
Build the People page data from the People/ folder.

    python3 tools/build_people.py

Reads   People/<Group>/<Person Name>/info.txt   (+ any photo in that folder)
Writes  js/people-data.js                       (what the website renders)
        images/people/<slug>.jpg                (web-sized copy of each photo)

Edit the info.txt files, run this, commit. Never edit js/people-data.js by
hand — this script overwrites it.
"""

import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PEOPLE_DIR = os.path.join(ROOT, "People")
OUT_JS = os.path.join(ROOT, "js", "people-data.js")
PHOTO_OUT = os.path.join(ROOT, "images", "people")

MAX_PHOTO_PX = 800          # longest edge of the copy we publish
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".webp", ".heic")

# Group folder -> how it appears on the site, and the default Role for
# someone in that group. Order here is the order of sections on the page.
GROUPS = [
    ("Professor",             {"kind": "lead"}),
    ("PhD_Students",          {"kind": "group", "title": "Doctoral Students",
                               "role": "Doctoral Student, Mechanical Engineering"}),
    ("Masters_Students",      {"kind": "group", "title": "Master's Students",
                               "role": "Master's Student, Robotics (MnRI)"}),
    ("Undergraduate_Students", {"kind": "group", "title": "Undergraduate Researchers",
                                "role": "Undergraduate Researcher, Mechanical Engineering"}),
    ("Alumni",                {"kind": "alumni"}),
]

# Keys understood in info.txt. Everything after a "Bio:" line is the bio.
FIELD_KEYS = {
    "name": "name", "role": "role", "title": "role",
    "degree": "degree",
    "email": "email",
    "website": "website", "site": "website", "homepage": "website",
    "linkedin": "linkedin",
    "scholar": "scholar", "google scholar": "scholar",
    "github": "github",
    "photo": "photo",
}

warnings = []


def warn(msg):
    warnings.append(msg)


# Degree and generational suffixes aren't part of a filename.
SUFFIXES = {"phd", "md", "ms", "msme", "bs", "bsme", "dsc", "scd",
            "jr", "sr", "ii", "iii", "iv"}


def slugify(name):
    parts = []
    for chunk in re.split(r"[\s,]+", name.lower()):
        word = re.sub(r"[^a-z0-9]", "", chunk)
        if word and word not in SUFFIXES:
            parts.append(word)
    return "-".join(parts) or "person"


def parse_info(path):
    """Parse an info.txt into a dict. Forgiving: unknown lines before Bio are
    ignored, '#' lines are comments, and everything after 'Bio:' is prose."""
    data, bio_lines, in_bio = {}, [], False

    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            stripped = line.strip()

            if in_bio:
                bio_lines.append(line)
                continue
            if not stripped or stripped.startswith("#"):
                continue

            m = re.match(r"^([A-Za-z][A-Za-z ]{0,20}):\s*(.*)$", stripped)
            if not m:
                continue
            key, val = m.group(1).strip().lower(), m.group(2).strip()

            if key == "bio":
                in_bio = True
                if val:
                    bio_lines.append(val)
                continue
            if key in FIELD_KEYS and val:
                data[FIELD_KEYS[key]] = val

    bio = "\n".join(bio_lines).strip()
    bio = re.sub(r"\n\s*\n+", "\n\n", bio)
    # Collapse to a single paragraph-ish string; the card shows one block.
    bio = " ".join(part.strip() for part in bio.split("\n") if part.strip())
    if bio:
        data["blurb"] = bio
    return data


def find_photo(folder, declared):
    """Return the source photo path, or None."""
    if declared:
        p = os.path.join(folder, declared)
        if os.path.exists(p):
            return p
        warn(f"{folder}: Photo: {declared!r} not found, falling back to folder scan")

    cands = sorted(
        f for f in os.listdir(folder)
        if f.lower().endswith(IMAGE_EXTS) and not f.startswith(".")
    )
    return os.path.join(folder, cands[0]) if cands else None


def publish_photo(src, slug):
    """Copy a web-sized version into images/people/. Returns the filename."""
    os.makedirs(PHOTO_OUT, exist_ok=True)
    ext = ".jpg" if not src.lower().endswith(".png") else ".png"
    out_name = slug + ext
    out_path = os.path.join(PHOTO_OUT, out_name)

    if shutil.which("sips"):
        r = subprocess.run(
            ["sips", "-Z", str(MAX_PHOTO_PX), src, "--out", out_path],
            capture_output=True,
        )
        if r.returncode != 0 or not os.path.exists(out_path):
            warn(f"{src}: sips failed, copied original instead")
            shutil.copy2(src, out_path)
    else:
        warn("sips not available — photos copied at original size")
        shutil.copy2(src, out_path)

    size = os.path.getsize(out_path)
    if size > 600_000:
        warn(f"{out_name} is {size//1024} KB — consider a smaller source image")
    return out_name


def person_folders(group_dir):
    if not os.path.isdir(group_dir):
        return []
    return sorted(
        d for d in os.listdir(group_dir)
        if os.path.isdir(os.path.join(group_dir, d)) and not d.startswith(("_", "."))
    )


def build_person(folder, display_name, default_role):
    info = parse_info(os.path.join(folder, "info.txt")) \
        if os.path.exists(os.path.join(folder, "info.txt")) else {}

    name = info.get("name") or display_name
    slug = slugify(name)

    person = {"name": name, "role": info.get("role") or default_role}

    src = find_photo(folder, info.get("photo"))
    person["photo"] = publish_photo(src, slug) if src else ""
    if not src:
        warn(f"{display_name}: no photo yet — card will show initials")

    if info.get("blurb"):
        person["blurb"] = info["blurb"]
    if info.get("email"):
        person["email"] = info["email"]

    links = []
    for key, label in (("website", "Website"), ("scholar", "Google Scholar"),
                       ("linkedin", "LinkedIn"), ("github", "GitHub")):
        if info.get(key):
            links.append({"label": label, "url": info[key]})
    if links:
        person["links"] = links

    if info.get("degree"):
        person["degree"] = info["degree"]
    return person


def read_past_members(path):
    """People/Alumni/_past-members.txt — one 'Name | Degree' per line."""
    out = []
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "|" in line:
                name, degree = line.split("|", 1)
            else:
                name, degree = line, ""
            out.append({"name": name.strip(), "degree": degree.strip()})
    return out


def main():
    if not os.path.isdir(PEOPLE_DIR):
        sys.exit(f"No People/ folder at {PEOPLE_DIR}")

    lead, groups, alumni_cards = None, [], []

    for folder_name, cfg in GROUPS:
        group_dir = os.path.join(PEOPLE_DIR, folder_name)
        people = person_folders(group_dir)

        if cfg["kind"] == "lead":
            if not people:
                warn("People/Professor/ has no person folder — keeping no lead entry")
                continue
            lead = build_person(os.path.join(group_dir, people[0]), people[0],
                                "Lead Faculty / Principal Investigator")

        elif cfg["kind"] == "group":
            members = [build_person(os.path.join(group_dir, p), p, cfg["role"])
                       for p in people]
            if members:
                groups.append({"title": cfg["title"], "members": members})

        elif cfg["kind"] == "alumni":
            alumni_cards = [build_person(os.path.join(group_dir, p), p, "Former Lab Member")
                            for p in people]

    past = read_past_members(os.path.join(PEOPLE_DIR, "Alumni", "_past-members.txt"))

    data = {
        "lead": lead,
        "groups": groups,
        "alumniCards": alumni_cards,
        "alumni": [{"name": a["name"], "degree": a.get("degree", "")} for a in alumni_cards] + past,
    }
    # alumniCards people already appear as cards; don't repeat them in the list.
    data["alumni"] = past

    # Remove published photos for people no longer in People/ — otherwise
    # images/people/ accumulates headshots of folks who have left.
    wanted = {p["photo"] for p in
              ([lead] if lead else []) + alumni_cards +
              [m for g in groups for m in g["members"]] if p.get("photo")}
    if os.path.isdir(PHOTO_OUT):
        for f in sorted(os.listdir(PHOTO_OUT)):
            if f.startswith(".") or f == "README.md":
                continue
            if f not in wanted:
                os.remove(os.path.join(PHOTO_OUT, f))
                print(f"  removed stale photo images/people/{f}")

    body = json.dumps(data, indent=2, ensure_ascii=False)
    with open(OUT_JS, "w", encoding="utf-8") as fh:
        fh.write(
            "/* GENERATED FILE — DO NOT EDIT BY HAND.\n"
            "   Source: the People/ folder (one info.txt per person).\n"
            "   Rebuild: python3 tools/build_people.py\n"
            "*/\n\n"
            "window.MRD = window.MRD || {};\n"
            "window.MRD.people = " + body + ";\n"
        )

    n_group = sum(len(g["members"]) for g in groups)
    print(f"Wrote {os.path.relpath(OUT_JS, ROOT)}")
    print(f"  lead:         {lead['name'] if lead else '(none)'}")
    for g in groups:
        print(f"  {g['title']:26} {len(g['members'])}")
    print(f"  alumni cards: {len(alumni_cards)}")
    print(f"  past members: {len(past)}")
    print(f"  total current members: {n_group + (1 if lead else 0)}")

    if warnings:
        print("\nNotes:")
        for w in warnings:
            print("  - " + w)


if __name__ == "__main__":
    main()
