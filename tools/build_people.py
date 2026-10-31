#!/usr/bin/env python3
"""
Build the People page data from the People/ folder.

    python3 tools/build_people.py

Reads   People/<Group>/<Person Name>/info.txt   (+ any photo in that folder)
Writes  js/people-data.json                     (what the website renders)
        images/people/<slug>.jpg                (web-sized copy of each photo)

Edit the info.txt files, run this, commit. Never edit js/people-data.json by
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
OUT_JSON = os.path.join(ROOT, "js", "people-data.json")
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
    # An extra duty held alongside the degree: "Lab Safety Officer",
    # "Lab Administration", etc. Shown as a gold tag on the card.
    "lab role": "labRole", "duty": "labRole",
    "degree": "degree",
    "email": "email",
    "website": "website", "site": "website", "homepage": "website",
    "portfolio": "portfolio",
    "linkedin": "linkedin",
    "scholar": "scholar", "google scholar": "scholar",
    "github": "github",
    "photo": "photo",
}

# "File: <filename in this folder> | <link label>" — may be repeated.
# Used for resumes, portfolios, posters: anything downloadable.
DOC_EXTS = (".pdf",)
DOC_OUT_REL = "files/people"

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
            # Repeatable: someone can hold more than one degree with the lab
            # (e.g. a B.S. here followed by an M.S. here).
            if key in ("role", "title") and val:
                data.setdefault("roles", []).append(val)
                continue
            # "File: resume.pdf | Resume" — repeatable, so collect into a list.
            if key == "file" and val:
                fname, _, label = val.partition("|")
                data.setdefault("files", []).append(
                    {"file": fname.strip(), "label": label.strip()})
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
    """Write a web-sized JPEG into images/people/. Returns the filename.

    Headshots are always published as JPEG regardless of the source format —
    a PNG photo is several times larger for no visible gain."""
    os.makedirs(PHOTO_OUT, exist_ok=True)
    out_name = slug + ".jpg"
    out_path = os.path.join(PHOTO_OUT, out_name)

    if shutil.which("sips"):
        r = subprocess.run(
            ["sips", "-s", "format", "jpeg", "-s", "formatOptions", "82",
             "-Z", str(MAX_PHOTO_PX), src, "--out", out_path],
            capture_output=True,
        )
        if r.returncode != 0 or not os.path.exists(out_path):
            warn(f"{os.path.basename(src)}: sips failed, copied original instead")
            shutil.copy2(src, out_path)
    else:
        warn("sips not available — photos copied at original size")
        shutil.copy2(src, out_path)

    size = os.path.getsize(out_path)
    if size > 400_000:
        warn(f"{out_name} is {size//1024} KB — consider a smaller source image")
    return out_name


def publish_doc(src, slug, original_name):
    """Copy a downloadable file into files/people/ under a URL-safe name."""
    out_dir = os.path.join(ROOT, *DOC_OUT_REL.split("/"))
    os.makedirs(out_dir, exist_ok=True)

    stem, ext = os.path.splitext(original_name)
    stem_slug = slugify(stem)
    # Avoid "neev-zeroni-neev-zeroni-resume.pdf" when the file is already
    # named after the person.
    if stem_slug.startswith(slug + "-"):
        out_name = f"{stem_slug}{ext.lower()}"
    else:
        out_name = f"{slug}-{stem_slug}{ext.lower()}"
    shutil.copy2(src, os.path.join(out_dir, out_name))

    size = os.path.getsize(src)
    if size > 3_000_000:
        warn(f"{out_name} is {size//1024//1024} MB — large for a web download")
    return out_name


def person_folders(group_dir):
    """Folder names for a group, in display order.

    If the group has an _order.txt, names listed there come first in that
    order (use it for seniority). Anyone not listed follows alphabetically,
    so forgetting to add a new person is never fatal."""
    if not os.path.isdir(group_dir):
        return []

    found = sorted(
        d for d in os.listdir(group_dir)
        if os.path.isdir(os.path.join(group_dir, d)) and not d.startswith(("_", "."))
    )

    order_file = os.path.join(group_dir, "_order.txt")
    if not os.path.exists(order_file):
        return found

    remaining, ordered = list(found), []
    with open(order_file, encoding="utf-8") as fh:
        for line in fh:
            wanted = line.strip()
            if not wanted or wanted.startswith("#"):
                continue
            match = next((d for d in remaining if d.lower() == wanted.lower()), None)
            if match:
                ordered.append(match)
                remaining.remove(match)
            else:
                warn(f"{order_file}: no folder named {wanted!r}")

    if remaining:
        warn(f"{os.path.basename(group_dir)}/_order.txt doesn't list "
             f"{', '.join(remaining)} — appended alphabetically")
    return ordered + remaining


def build_person(folder, display_name, default_role):
    info = parse_info(os.path.join(folder, "info.txt")) \
        if os.path.exists(os.path.join(folder, "info.txt")) else {}

    name = info.get("name") or display_name
    slug = slugify(name)

    # Most recent first, as the person listed them.
    person = {"name": name, "roles": info.get("roles") or [default_role]}

    src = find_photo(folder, info.get("photo"))
    person["photo"] = publish_photo(src, slug) if src else ""
    if not src:
        warn(f"{display_name}: no photo yet — card will show initials")

    if info.get("labRole"):
        person["labRole"] = info["labRole"]
    if info.get("blurb"):
        person["blurb"] = info["blurb"]
    if info.get("email"):
        person["email"] = info["email"]

    links = []
    for key, label in (("website", "Website"), ("portfolio", "Portfolio"),
                       ("scholar", "Google Scholar"),
                       ("linkedin", "LinkedIn"), ("github", "GitHub")):
        if info.get(key):
            url = info[key]
            # People paste bare domains; make them real links.
            if not re.match(r"^(https?:|mailto:)", url):
                url = "https://" + url.lstrip("/")
            links.append({"label": label, "url": url})

    # Downloadable documents (resume, portfolio PDF, poster).
    for doc in info.get("files", []):
        src = os.path.join(folder, doc["file"])
        if not os.path.exists(src):
            warn(f"{display_name}: File: {doc['file']!r} not found in their folder")
            continue
        out_name = publish_doc(src, slug, doc["file"])
        links.append({
            "label": doc["label"] or os.path.splitext(doc["file"])[0],
            "url": DOC_OUT_REL + "/" + out_name,
            "download": True,
        })

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
    everyone = ([lead] if lead else []) + alumni_cards + \
               [m for g in groups for m in g["members"]]

    wanted = {p["photo"] for p in everyone if p.get("photo")}
    if os.path.isdir(PHOTO_OUT):
        for f in sorted(os.listdir(PHOTO_OUT)):
            if f.startswith(".") or f == "README.md":
                continue
            if f not in wanted:
                os.remove(os.path.join(PHOTO_OUT, f))
                print(f"  removed stale photo images/people/{f}")

    # Same for downloadable documents.
    wanted_docs = {l["url"].rsplit("/", 1)[-1]
                   for p in everyone for l in p.get("links", [])
                   if l.get("download")}
    doc_dir = os.path.join(ROOT, *DOC_OUT_REL.split("/"))
    if os.path.isdir(doc_dir):
        for f in sorted(os.listdir(doc_dir)):
            if f.startswith(".") or f == "README.md":
                continue
            if f not in wanted_docs:
                os.remove(os.path.join(doc_dir, f))
                print(f"  removed stale file {DOC_OUT_REL}/{f}")

    data["_generated"] = "GENERATED FILE — do not edit. Source: People/. " \
                         "Rebuild: python3 tools/build_people.py"
    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    n_group = sum(len(g["members"]) for g in groups)
    print(f"Wrote {os.path.relpath(OUT_JSON, ROOT)}")
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
