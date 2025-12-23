#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

import bibtexparser
import yaml


ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "assets" / "bib" / "publications.bib"
OUT = ROOT / "_data" / "publications.yml"


def clean_tex(s: str) -> str:
    # Minimal TeX → text cleanup (good enough for most BibTeX exports)
    s = s.replace("{", "").replace("}", "")
    s = re.sub(r"\\&", "&", s)
    s = re.sub(r"\\textit\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\emph\{([^}]*)\}", r"\1", s)
    # Common accents (extend as needed)
    s = s.replace("\\'a", "á").replace('\\"o', "ö").replace("\\'e", "é")
    return s.strip()


def authors_to_list(author_field: str) -> list[str]:
    # Scholar BibTeX is usually "Last, First and Last, First ..."
    parts = [a.strip() for a in author_field.split(" and ") if a.strip()]
    cleaned = []
    for a in parts:
        a = clean_tex(a)
        if "," in a:
            last, first = [x.strip() for x in a.split(",", 1)]
            cleaned.append(f"{first} {last}".strip())
        else:
            cleaned.append(a)
    return cleaned


def entry_year(e: dict) -> int:
    y = e.get("year", "") or ""
    m = re.search(r"\d{4}", y)
    return int(m.group(0)) if m else 0


def venue(e: dict) -> str:
    for k in ("journal", "booktitle", "publisher", "institution"):
        if e.get(k):
            return clean_tex(e[k])
    return ""


def main() -> None:
    if not BIB.exists():
        raise SystemExit(f"BibTeX not found: {BIB}")

    parser = bibtexparser.bparser.BibTexParser(common_strings=True)
    bib = bibtexparser.load(BIB.open(encoding="utf-8"), parser=parser)

    pubs = []
    for e in bib.entries:
        title = clean_tex(e.get("title", ""))
        if not title:
            continue

        authors = authors_to_list(e.get("author", "")) if e.get("author") else []
        y = entry_year(e)
        v = venue(e)

        pubs.append(
            {
                "key": e.get("ID", ""),
                "type": e.get("ENTRYTYPE", ""),
                "title": title,
                "authors": authors,
                "year": y,
                "venue": v,
                "volume": clean_tex(e.get("volume", "")) if e.get("volume") else "",
                "number": clean_tex(e.get("number", "")) if e.get("number") else "",
                "pages": clean_tex(e.get("pages", "")) if e.get("pages") else "",
                "doi": clean_tex(e.get("doi", "")) if e.get("doi") else "",
                "url": clean_tex(e.get("url", "")) if e.get("url") else "",
            }
        )

    # Sort newest first, then title
    pubs.sort(key=lambda p: (p["year"], p["title"].lower()), reverse=True)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(yaml.safe_dump(pubs, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"Wrote {len(pubs)} pubs → {OUT}")


if __name__ == "__main__":
    main()
