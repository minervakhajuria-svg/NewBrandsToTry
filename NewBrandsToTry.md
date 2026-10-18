# NewBrandsToTry

A small website that lists niche, slightly premium Indian fashion labels (shoes, bags, clothing) for friends and family. It is not a shop: every product links out to the brand's own website.

## Goal

- One page, three tabs: **Shoes**, **Bags**, **Clothing**.
- Each tab lists its brands as buttons. Clicking a brand shows **4 products** (its bestsellers where the site has a bestsellers collection), each with a picture, name, price and a link to the product page.
- A shareable link that anyone can open on a phone, with no login.

## Audience and tone

Friends and family in India. Keep it simple, mobile-first and visual, like a lookbook. No cart, no accounts, no tracking.

## Brand selection criteria

- Homegrown Indian labels, niche and slightly premium (roughly ₹3,500 and up).
- Distinctive styles, not mass-market.
- Natural or responsible materials where possible (handloom cotton, linen, leather, plant-based leather).
- Not too established. Zouk, Hidesign, Mulmul, Nicobar and Sue Mue were dropped for this reason or for being outside the price range.

## Current files

| File | What it is |
|---|---|
| `brands.json` | The data: 24 brands, 91 products. Fields: `name`, `cat`, `site`, `src` (where the products were picked from), `note`, and `products[]` with `title`, `url`, `img`, `price`. |
| `NewBrandsToTry.html` | First version of the page. A single file with the data inlined. Product images are hotlinked from the brands' CDNs. |
| `NewBrandsToTry_shortlist.xlsx` | The shortlist spreadsheet: Brand, Category, Website, then Product 1–4 as linked names, then "Picked from". |

## Brands (as of 18 Oct 2026)

| Tab | Brand | Website | Products picked from | # |
|---|---|---|---|---|
| Shoes | Banjaaran Studio | https://banjaaran.in/ | New arrivals | 4 |
| Shoes | Disobedience | https://thedisobedience.com/ | Bestsellers | 4 |
| Shoes | Kilchu | https://kilchu.com/ | From women's footwear | 4 |
| Shoes | The Ferrier | https://theferrier.com/ | From the women's collection | 4 |
| Shoes | Daang | — | — | 0 |
| Shoes | Slomotion | https://www.slomotion.in/ | Latest products | 4 |
| Shoes | Chal Shoes | https://chalshoes.in/ | Bestsellers | 4 |
| Shoes | Ceecee | https://shopceecee.com/ | Best picks | 4 |
| Bags | Tin & Tah (Tintah) | https://tintah.com/ | Featured on homepage | 4 |
| Bags | Tanned | https://tanned.in/ | Featured: Season's Hottest | 4 |
| Bags | Behno | https://behno.com/ | Latest products (prices in US$) | 4 |
| Bags | Amama | https://www.amama.in/ | Bestsellers | 4 |
| Bags | Tiger Marron | https://www.tigermarron.com/ | Bestsellers | 4 |
| Bags | AMPM | https://ampm.in/ | From the bags collection | 4 |
| Bags | Mai Soli | https://maisoli.in/ | Latest products | 3 |
| Bags | Mistry | https://www.shopmistry.com/ | From the handbags collection | 4 |
| Bags | Nappa Dori | https://www.nappadori.com/ | Bestsellers | 4 |
| Clothing | Khara Kapas | https://kharakapas.com/ | Bestsellers | 4 |
| Clothing | Verb by Pallavi Singhee | https://shopverb.com/ | Bestsellers | 4 |
| Clothing | The Jodi Life | https://thejodilife.com/ | Best-selling styles | 4 |
| Clothing | Niharika Vivek | https://www.niharikavivek.com/ | Latest products | 4 |
| Clothing | July Issue | https://julyissue.com/ | Bestsellers | 4 |
| Clothing | Drawn | https://shopdrawn.com/ | Latest products | 4 |
| Clothing | The Summer House | https://thesummerhouse.in/ | Bestsellers | 4 |

## How the product data was collected

Most of these brands run on **Shopify**, which exposes public JSON:

- `https://<site>/collections/<handle>/products.json?limit=4` gives products in a collection, including `title`, `handle`, `images[0].src` and `variants[0].price`.
- Common bestseller handles: `best-sellers`, `bestsellers`, `bestsellers-1`, `best-selling-styles`, `best-picks`. Check the homepage nav for the real one.
- Product URL = `https://<site>/products/<handle>`.
- `?sort_by=best-selling` is usually blocked by robots.txt, so use a bestsellers collection instead.
- Where there is no bestsellers collection, the newest or featured products were used, and `src` says so.

**Tin & Tah (Tintah)** is not on Shopify (it uses Instadukan). Its image URLs came from each product page's `og:image`.

## Known gaps

- **Daang**: no website found. It has no products, so either find the site or Instagram handle, or drop it.
- **Mai Soli**: only 3 bag products were readable. Its Founder's Picks (Dune Hobo, Meridian Baguette, Crescendo Handbag) need their product URLs.
- **Behno** prices are in US$.
- **Nappa Dori** sits under Bags only, because its bestsellers are bags.
- The images are hotlinked. If a brand changes a photo, that card breaks. The page shows a "Picture unavailable – view on site" fallback.
- Prices and stock change. Treat them as a snapshot.

## Next steps

1. Set up the project folder with these three files.
2. Write a script, for example `scripts/refresh.py`, that reads a simple brand list (name, category, site, bestseller collection handle) and rebuilds `brands.json` from Shopify `products.json`.
3. Download product images locally (resized to about 600px wide, WebP) so the site doesn't depend on hotlinks.
4. Turn `NewBrandsToTry.html` into a small static site that loads `brands.json` instead of inlining it.
5. Deploy to a free host, such as Firebase Hosting (`newbrandstotry.web.app`), Netlify or GitHub Pages, and share the link.
6. Nice to have: a "Last updated" date, a note per brand on why it's on the list, and search or filter by price.

## Design notes

- Lookbook feel: a light sage-grey background with deep indigo accents, Gloock for headings and Figtree for body text, and light and dark themes.
- Category tabs, then brand chips, then a 4-up product grid (2-up on phones). Images use a 3:4 crop.
- The page remembers the last tab, and `#shoes`, `#bags` or `#clothing` in the URL opens that tab directly.
