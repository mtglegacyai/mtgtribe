#!/usr/bin/env python3
"""Check an MTG PDF companion guide before it is shown to MTG.

Lists every link on every page and reports problems:
  - pages with no link at all (every page should have at least one button),
  - empty or placeholder links (example.com, TODO, YOUR_LINK, {{...}}, a bare "#"),
  - em or en dashes anywhere in the text (MTG's brand rule: none, ever),
  - with --online: web addresses that do not answer with a success status.

Usage:
  python3 check_pdf_links.py guide.pdf            # offline checks
  python3 check_pdf_links.py guide.pdf --online   # also open every web address
Exit code 0 when everything is fine, 1 when something needs fixing.
Needs: pypdf (pip install pypdf).
"""
import re
import sys
import urllib.request

try:
    from pypdf import PdfReader
except ImportError:
    sys.exit("pypdf is missing: pip install pypdf")

PLACEHOLDER = re.compile(r"example\.(com|org)|todo|placeholder|your[_-]?link|xxx|\{\{|\}\}|^#?$|^javascript:", re.I)
DASHES = re.compile("[\u2013\u2014]")   # en dash, em dash (written as codes so this file has none)


def page_links(page):
    """Return (kind, target) for every link annotation on a page."""
    out = []
    for ref in page.get("/Annots") or []:
        a = ref.get_object()
        if a.get("/Subtype") != "/Link":
            continue
        act = a.get("/A")
        act = act.get_object() if act is not None else None
        if act is not None and act.get("/S") == "/URI":
            out.append(("web", str(act.get("/URI", "")).strip()))
        elif act is not None and act.get("/S") == "/GoTo" or a.get("/Dest") is not None:
            out.append(("inside", "page link"))
        else:
            out.append(("other", str(act.get("/S") if act is not None else "none")))
    return out


def check_url(url):
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": "pdf-link-check/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:  # network errors, bad addresses
        return type(e).__name__


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path, online = sys.argv[1], "--online" in sys.argv[2:]
    reader = PdfReader(path)
    problems, all_urls = [], {}
    print(f"{path}: {len(reader.pages)} pages")
    for i, page in enumerate(reader.pages, 1):
        links = page_links(page)
        text = page.extract_text() or ""
        print(f"\npage {i}: {len(links)} link(s)")
        for kind, target in links:
            print(f"   {kind:6s} {target}")
            if kind == "web":
                all_urls.setdefault(target, []).append(i)
                if PLACEHOLDER.search(target) or not re.match(r"^(https?://|mailto:|tel:)", target):
                    problems.append(f"page {i}: placeholder or unusable link: {target or '(empty)'}")
        if not links:
            problems.append(f"page {i}: no button or link on this page")
        for m in DASHES.finditer(text):
            around = text[max(0, m.start() - 30):m.end() + 30].replace("\n", " ")
            problems.append(f"page {i}: em or en dash in the text: ...{around}...")
    if online:
        print(f"\nopening {len(all_urls)} web address(es)")
        for url, pages in sorted(all_urls.items()):
            status = check_url(url)
            ok = isinstance(status, int) and 200 <= status < 400
            print(f"   {'ok ' if ok else 'BAD'} {status}  {url}  (pages {', '.join(map(str, pages))})")
            if not ok:
                problems.append(f"pages {', '.join(map(str, pages))}: {url} answered {status}")
    print()
    if problems:
        print(f"{len(problems)} thing(s) to fix:")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print(f"All good: {sum(len(v) for v in all_urls.values())} web link(s) on {len(reader.pages)} page(s), no dashes, no empty pages.")


if __name__ == "__main__":
    main()
