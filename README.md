# BrandsToTry

A small lookbook of homegrown Indian labels for bags, shoes and clothing, curated by MK for friends and family. It is not a shop: every product links to the brand's own website.

**Live site:** https://minervakhajuria-svg.github.io/NewBrandsToTry/

## What the site does

- Tabs for **Bags**, **Shoes** and **Clothing**. Pick a brand to see four of its popular women's pieces, each with a picture, name, price and a link to the product page.
- A short note under each brand on why it is on the list.
- A **Share Your Picks** tab where friends can suggest a brand. Suggestions are emailed to the curator and nothing is added automatically.
- Light and dark theme toggle, mobile-first layout, no login, no cart and no tracking.
- `#bags`, `#shoes`, `#clothing` or `#share` at the end of the link opens that tab directly.

## Project layout

| Path | What it is |
|---|---|
| `docs/index.html` | The whole page (HTML, CSS and JS). GitHub Pages serves the `docs/` folder. |
| `docs/brands.json` | The data the page loads: brands, notes and products. Generated, so don't edit by hand. |
| `docs/img/` | Product pictures, resized to about 600px wide WebP so the site doesn't depend on brands' servers. |
| `brand_list.json` | The brand list you edit: name, category, site, note, and the Shopify collection `handle` to pull products from. |
| `scripts/refresh.py` | Rebuilds `docs/brands.json` and the images from `brand_list.json`. |
| `NewBrandsToTry.md` | The original project brief: goals, selection criteria and design notes. |
| `NewBrandsToTry.html`, `brands.json`, `NewBrandsToTry_shortlist.xlsx` | Earlier first-version files, kept for reference. |

## Brand selection criteria

Homegrown Indian labels that are niche and slightly premium (roughly ₹3,500 and up), with distinctive styles and natural or responsible materials where possible. Not too established, and not mass-market. Products shown are women's pieces, from a bestsellers collection where the brand has one.

## Updating the site

1. Edit `brand_list.json` to add, remove or change a brand. For a new brand, set `handle` to its Shopify collection, such as `bestsellers`. The URL pattern is `<site>/collections/<handle>/products.json`.
2. Run the refresh. It needs Python and Pillow (`pip install pillow`):

   ```bash
   python scripts/refresh.py
   ```

   To refresh only some brands, which also avoids rate limits:

   ```bash
   python scripts/refresh.py --only "Raw Mango,Amama"
   ```

   Other options: `--no-fetch` (keep products, rebuild images only) and `--no-images`.
3. Commit and push. GitHub Pages republishes in a minute or two.

Optional fields in `brand_list.json`: `only_type` keeps only products of one Shopify product type (for example `Bags`).

## Share Your Picks form

The form sends to [Web3Forms](https://web3forms.com), which emails each suggestion. The access key is in `docs/index.html`. Web3Forms keys are meant to be public and can only send mail to the curator. A local `.env` copy is git-ignored and the site does not read it.

## Known limits

- Prices and stock change, so treat them as a snapshot. The footer says so.
- Brand sites sometimes rate-limit the refresh with "too many requests". Wait and retry, or use `--only`. A failed fetch keeps the brand's existing products.
- Tin & Tah is not on Shopify, so its products are maintained by hand in `docs/brands.json`.
- Brands without a `handle` keep their existing hand-picked products.
