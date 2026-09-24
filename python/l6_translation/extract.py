"""L6 source-definition extractor (WP-2A step 1).

Reads the frozen L6 PDF bytes (external/papers/, hash-pinned in SHA256SUMS),
extracts text, and locates the definition sites for rank / heavy paths /
heap view / gaps / lazy intervals / pairings / bends / contracted point gaps.
Output: artifacts/v03/translation/l6_source_sites.json (page + verbatim context
per definition slot). Extraction only; mapping judgments belong to WP-2A review.
Console lines prefixed [WP2A-STEP-01] are the audit record.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

PDF = os.path.join(ROOT, "external", "papers", "L6_chmel_et_al_2026_2607.18498.pdf")

SLOTS = {
    "rank": ["rank of", "define the rank", "rank is defined", "ranks are"],
    "heavy": ["heavy path", "heavy edge", "heavy child", "light edge"],
    "heap": ["heap", "heap-ordered", "heap order"],
    "gap": ["point gap", "interval gap", "gap is", "gaps are"],
    "lazy": ["lazy interval", "lazy-interval", "growing", "shrinking", "broken interval"],
    "pairing": ["pairing", "paired ", "good pairing", "bad pairing", "boundary pairing"],
    "bend": ["bend", "bends"],
    "contracted": ["contract", "log log", "loglog", "potential"],
}


# WP2A-STEP-01: extract text and locate definition sites (no interpretation).
def main() -> int:
    from pypdf import PdfReader
    print("[WP2A-STEP-01] extracting frozen L6 bytes", flush=True)
    raw = open(PDF, "rb").read()
    digest = hashlib.sha256(raw).hexdigest().upper()
    print("[WP2A-STEP-01] L6 bytes=%d sha=%s..." % (len(raw), digest[:16]), flush=True)
    reader = PdfReader(PDF)
    pages = [(i + 1, (pg.extract_text() or "")) for i, pg in enumerate(reader.pages)]
    print("[WP2A-STEP-01] pages=%d chars=%d" % (len(pages), sum(len(t) for _, t in pages)), flush=True)
    sites: dict = {}
    for slot, keys in SLOTS.items():
        hits = []
        for pno, text in pages:
            low = text.lower()
            for k in keys:
                j = 0
                while True:
                    j = low.find(k, j)
                    if j < 0 or len(hits) >= 12:
                        break
                    s = max(0, j - 200)
                    hits.append({"page": pno, "keyword": k,
                                 "context": text[s:j + 300].replace("\n", " ")})
                    j += len(k)
        sites[slot] = hits
        print("[WP2A-STEP-01] slot=%s hits=%d" % (slot, len(hits)), flush=True)
    outdir = os.path.join(ROOT, "artifacts", "v03", "translation")
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, "l6_source_sites.json")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"pdf_sha256": digest, "pages": len(pages), "sites": sites},
                  f, sort_keys=True, indent=2)
        f.write("\n")
    print("[WP2A-STEP-01] wrote %s" % out, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
