#!/usr/bin/env python3
"""Generate author contact list for paywalled Tier A papers.

Queries OpenAlex by DOI for each of the 13 paywalled Tier A papers to extract:
- Full title
- All authors with their institutions
- Corresponding author (first author by convention if not marked)
- Email (from OpenAlex authorships where available)
- DOI / OpenAccess URL
- Suggested email request template

Outputs:
  data/processed/tier_a_paywalled_contacts.csv
  data/reports/tier_a_paywalled_contacts.md  (ready-to-send templates)
"""

from __future__ import annotations

import csv
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
SCREENING = ROOT / "data" / "processed" / "fulltext_screening.csv"
QUALITY = ROOT / "data" / "processed" / "quality_assessment.csv"
OUT_CSV = ROOT / "data" / "processed" / "tier_a_paywalled_contacts.csv"
OUT_MD = ROOT / "data" / "reports" / "tier_a_paywalled_contacts.md"

OPENALEX_BASE = "https://api.openalex.org"
MAILTO = "anthony@kumoh.ac.kr"
USER_AGENT = "BCN-SLR-AuthorContact/1.0 (mailto:anthony@kumoh.ac.kr)"
TIMEOUT = 30
DELAY = 1.0


def _headers() -> dict:
    return {"User-Agent": USER_AGENT}


def openalex_by_doi(doi: str) -> dict | None:
    """Query OpenAlex for a work by DOI."""
    doi_encoded = doi.strip().replace(" ", "%20")
    url = f"{OPENALEX_BASE}/works/doi:{doi_encoded}?mailto={MAILTO}"
    try:
        r = requests.get(url, headers=_headers(), timeout=TIMEOUT)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def extract_contact(work: dict) -> dict:
    """Extract contact info from an OpenAlex work record."""
    authorships = work.get("authorships", [])
    title = work.get("title", "")
    doi = work.get("doi", "")
    year = work.get("publication_year", "")
    venue = (work.get("primary_location") or {}).get("source", {})
    venue_name = venue.get("display_name", "") if isinstance(venue, dict) else ""
    oa_url = (work.get("primary_location") or {}).get("landing_page_url", "")

    authors_list = []
    corresponding_name = ""
    corresponding_email = ""
    corresponding_inst = ""

    for auth in authorships:
        a = auth.get("author", {})
        name = a.get("display_name", "")
        is_corresponding = auth.get("is_corresponding", False)
        institutions = auth.get("institutions", [])
        inst_names = "; ".join(i.get("display_name", "") for i in institutions if i.get("display_name"))
        email = a.get("email", "")  # Usually not in OpenAlex; kept for future
        authors_list.append(f"{name} ({inst_names})" if inst_names else name)

        if is_corresponding or not corresponding_name:
            corresponding_name = name
            corresponding_inst = inst_names
            if email:
                corresponding_email = email

    authors_str = "; ".join(authors_list)
    return {
        "title": title,
        "year": year,
        "venue": venue_name,
        "doi": doi,
        "oa_url": oa_url,
        "authors": authors_str,
        "corresponding_author": corresponding_name,
        "corresponding_institution": corresponding_inst,
        "corresponding_email": corresponding_email,
    }


def email_template(row: dict, contact: dict) -> str:
    """Generate a polite preprint request email."""
    name_parts = contact.get("corresponding_author", "Author").split()
    surname = name_parts[-1] if name_parts else "Author"
    title = contact.get("title") or row.get("title", "")
    doi = row.get("doi", "")
    return (
        f"Dear Dr. {surname},\n\n"
        f"I am conducting a PRISMA 2020 systematic literature review on "
        f"blockchain utilization strategies in institutional consortium networks. "
        f"Your paper:\n\n"
        f'  "{title}"\n'
        f"  DOI: {doi}\n\n"
        f"is of direct relevance to my review. Unfortunately, I do not have "
        f"institutional access to this venue. Would you be willing to share a "
        f"preprint or accepted-manuscript version of your paper? I would use it "
        f"solely for academic research purposes.\n\n"
        f"Thank you very much for your time and consideration.\n\n"
        f"Sincerely,\n"
        f"Tony Eneh\n"
        f"anthony@kumoh.ac.kr\n"
        f"Network & Security Lab, Kumoh National Institute of Technology"
    )


def main() -> None:
    # Load tier map
    cid_to_tier: dict[str, str] = {}
    with open(QUALITY, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cid_to_tier[row["candidate_id"]] = row["tier"]

    # Load screening rows; find Tier A paywalled (no local_path)
    screening_rows: list[dict] = []
    with open(SCREENING, encoding="utf-8") as f:
        screening_rows = list(csv.DictReader(f))

    tier_a_paywalled = [
        r for r in screening_rows
        if cid_to_tier.get(r["candidate_id"]) == "A"
        and not r.get("local_path", "").strip()
        and r.get("doi", "").strip()
    ]

    print(f"Tier A paywalled papers: {len(tier_a_paywalled)}")

    contacts: list[dict] = []
    md_sections: list[str] = []

    for i, row in enumerate(tier_a_paywalled, 1):
        cid = row["candidate_id"]
        doi = row["doi"].strip()
        title = row.get("title", "")[:80]
        print(f"[{i:2}/{len(tier_a_paywalled)}] {cid}: {title}")

        work = openalex_by_doi(doi)
        time.sleep(DELAY)

        if work is None:
            print(f"          -> OpenAlex: not found")
            contact = {
                "title": row.get("title", ""),
                "year": row.get("year", ""),
                "venue": row.get("venue", ""),
                "doi": doi,
                "oa_url": "",
                "authors": row.get("authors", ""),
                "corresponding_author": (row.get("authors", "").split(";")[0]).strip(),
                "corresponding_institution": "",
                "corresponding_email": "",
            }
        else:
            contact = extract_contact(work)
            print(f"          -> Found: {contact['corresponding_author']} @ {contact['corresponding_institution'][:50]}")

        template = email_template(row, contact)
        contacts.append({
            "candidate_id": cid,
            **contact,
            "email_template": template.replace("\n", " | "),
        })

        # Markdown section
        md_sections.append(
            f"### {i}. {cid} — {contact['title'] or row.get('title','')}\n\n"
            f"**DOI:** {doi}  \n"
            f"**Year:** {contact['year']}  \n"
            f"**Venue:** {contact['venue']}  \n"
            f"**Authors:** {contact['authors']}  \n"
            f"**Corresponding:** {contact['corresponding_author']} "
            f"({contact['corresponding_institution']})  \n"
            f"**Email on file:** {contact['corresponding_email'] or '*(not in OpenAlex)*'}  \n\n"
            f"**Suggested email:**\n\n```\n{template}\n```\n"
        )

    # Write CSV
    fieldnames = [
        "candidate_id", "title", "year", "venue", "doi", "oa_url",
        "authors", "corresponding_author", "corresponding_institution",
        "corresponding_email", "email_template",
    ]
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(contacts)
    print(f"\nContact CSV -> {OUT_CSV}")

    # Write Markdown
    import datetime
    md = (
        "# Tier A Paywalled Papers — Author Contact List\n\n"
        f"**Date:** {datetime.date.today().isoformat()}  \n"
        f"**Papers:** {len(tier_a_paywalled)}  \n"
        "**Purpose:** Request preprints/accepted manuscripts for SLR full-text extraction\n\n"
        "---\n\n"
        + "\n---\n\n".join(md_sections)
        + "\n---\n\n"
        "## Sending checklist\n\n"
        "- [ ] Find corresponding author email via Google Scholar / ResearchGate if not in OpenAlex\n"
        "- [ ] Send from `anthony@kumoh.ac.kr`\n"
        "- [ ] Subject line: *Preprint request — [Title]*\n"
        "- [ ] After receiving, save PDF as `FT-XXXX.pdf` in `data/fulltext/tier-ab/`\n"
        "- [ ] Update `fulltext_screening.csv` `local_path` column\n"
        "- [ ] Re-run `scripts/extract_tierab_data.py` to extract fields\n"
    )
    OUT_MD.write_text(md, encoding="utf-8")
    print(f"Contact MD  -> {OUT_MD}")


if __name__ == "__main__":
    main()
