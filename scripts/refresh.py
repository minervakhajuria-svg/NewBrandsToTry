"""Rebuild docs/brands.json and docs/img/*.webp.

brand_list.json rows: name, cat, site, src, note, handle (Shopify collection handle, may be "").
- handle set  -> fetch https://<site>/collections/<handle>/products.json?limit=4
- handle empty -> keep the curated products already in brands.json (the project root copy)
Then every product image is downloaded, resized to ~600px wide WebP into docs/img/.

Usage: python scripts/refresh.py [--no-fetch] [--no-images]
"""
import json, re, sys, hashlib, io, urllib.request, datetime, pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
UA = {"User-Agent": "Mozilla/5.0 (NewBrandsToTry refresh)"}

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.read()

def womens(p):
    """Drop products tagged for men only (keeps unisex and untagged ones)."""
    t = " ".join(p.get("tags", []) + [p.get("product_type", "")])
    return not (re.search(r"mens?", t, re.I) and not re.search(r"wom[ae]ns?|ladies", t, re.I))

def tidy(t):
    t = re.sub(r"[\u0900-\u097F]+\s*\((.*?)\)", r"\1", t)  # Hindi word followed by its English in brackets: keep the English
    t = re.sub(r"\s+", " ", t).strip()
    return t.title() if t.isupper() else t

def shopify(site, handle, only_type=""):
    d = json.loads(get(f"{site.rstrip('/')}/collections/{handle}/products.json?limit=30"))
    out, seen = [], set()
    for p in [p for p in d["products"] if womens(p) and (not only_type or p.get("product_type", "").lower() == only_type.lower())]:
        if len(out) == 4: break
        if p["title"].strip().lower() in seen: continue
        seen.add(p["title"].strip().lower())
        price = float(p["variants"][0]["price"])
        out.append({"title": tidy(p["title"]), "url": f"{site.rstrip('/')}/products/{p['handle']}",
                    "img": p["images"][0]["src"] if p.get("images") else "",
                    "price": "₹{:,.0f}".format(price)})
    return out

def localise(url):
    name = hashlib.sha1(url.encode()).hexdigest()[:12] + ".webp"
    dest = ROOT / "site" / "img" / name
    if not dest.exists():
        im = Image.open(io.BytesIO(get(url))).convert("RGB")
        if im.width > 600:
            im = im.resize((600, round(im.height * 600 / im.width)), Image.LANCZOS)
        im.save(dest, "WEBP", quality=78)
    return "img/" + name

def main():
    no_fetch, no_img = "--no-fetch" in sys.argv, "--no-images" in sys.argv
    existing = {b["name"]: b for b in json.load(open(ROOT / "brands.json", encoding="utf-8"))}
    brands = []
    for row in json.load(open(ROOT / "brand_list.json", encoding="utf-8")):
        b = {k: row[k] for k in ("name", "cat", "site", "src", "note")}
        prods = existing.get(row["name"], {}).get("products", [])
        if row.get("handle") and not no_fetch:
            try: prods = shopify(row["site"], row["handle"], row.get("only_type", ""))
            except Exception as e: print("fetch failed", row["name"], e)
        b["products"] = [dict(p) for p in prods]
        brands.append(b)
    if not no_img:
        for b in brands:
            for p in b["products"]:
                if p.get("img"):
                    try: p["local"] = localise(p["img"])
                    except Exception as e: print("image failed", b["name"], p["title"], e)
    out = {"updated": datetime.date.today().isoformat(), "brands": brands}
    json.dump(out, open(ROOT / "site" / "brands.json", "w", encoding="utf-8"), ensure_ascii=False)
    print("brands:", len(brands), "products:", sum(len(b["products"]) for b in brands))

main()
