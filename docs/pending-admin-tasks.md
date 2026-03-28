# Pending Admin Tasks
> Last verified: 2026-03-28
> All items require action in Shopify Admin — no code changes needed.

---

## 🔴 Critical

- **GL-01 — Fix broken footer links**
  Multiple footer links still point to `#`. Update each in **Admin → Online Store → Navigation → Footer Menu**:
  - Candle Care → (create page or remove)
  - Gifts → `/pages/gifts`
  - Customisation → (create page or remove)
  - Corporate Gifting → (create page or remove)
  - Shipping & Returns → `/policies/refund-policy`
  - Terms & Conditions → `/policies/terms-of-service`
  - FAQs → (create page or remove)

- **CRV-01 — Create "Curvy Body Candles" collection**
  `/collections/shop-by-curvy` returns 404. Create a collection in **Admin → Products → Collections** with handle `shop-by-curvy` (or confirm tag-filtered URL `/collections/body-candles/Curvy` is the intended approach).

- **MM-01/MM-02 — Configure mega menu**
  Clicking "Shop" in the nav goes directly to `/collections/all` — the mega menu never triggers because "Shop" has no child links. In **Admin → Online Store → Navigation → Main Menu**, add child links under "Shop":
  - **POPULAR**: Shop All → `/collections/all`, Bestsellers → `/collections/bestsellers`
  - **BODY CANDLES**: Body Candles → `/collections/body-candles`, plus individual product links
  - **SHOP BY SIZE**: Slim → `/collections/body-candles/Slim`, Curvy → `/collections/body-candles/Curvy`, Plus Size → `/collections/body-candles/Plus+Size`
  - **SHOP BY COLLECTION**: Scar Collection → `/collections/scar-collection`, Sculpted → `/collections/sculpted-collection`

---

## 🟠 High

- **HP-03 — Upload logo image**
  Logo renders as plain text "SCENTS BY SARA". Upload the wordmark in **Admin → Online Store → Themes → Customise → Theme Settings → Logo**.

- **MM-03 — Set mega menu featured image**
  Figma shows a product close-up image on the right side of the mega menu. Set `mega_menu_featured_image` and `mega_menu_featured_link` in **Admin → Online Store → Themes → Customise → Header**.

- **CRV-02/GL-07 — Fix Curvy + Plus Size footer links**
  - "Curvy Body Candles" footer → update to `/collections/body-candles/Curvy` (or dedicated collection once CRV-01 is done)
  - "Plus Size Body Candles" footer → currently `/collections` (wrong) — update to `/collections/body-candles/Plus+Size`
  In **Admin → Online Store → Navigation → Footer Menu**.

- **SCF-01/GL-05 — Enable Body Shape + Body Colour filters**
  Filter panel shows Availability and Price instead of Body Shape and Body Colour. Enable product variant-based filters in **Admin → Apps → Search & Discovery → Filters**. Add "Body Shape" and "Body Colour" (or "Color") as filter options.

- **SC-05/SA-02 — Set default sort to "Featured"**
  Collections currently sort "Best Selling" or "A–Z" by default. Set to **Featured (manual)** for each collection in **Admin → Products → Collections → [Collection] → Sort → Featured**.
  Affects: Scar Collection, Sculpted Collection, Shop All, Bestsellers.

- **PDP-06 — Upload scent card images**
  The Scents section on the PDP shows text-only cards. Upload imagery for VANILLA and LAVENDER in **Admin → Online Store → Themes → Customise → [any product page] → Scents section**.

---

## 🟠 High — Apps

- **PDP-01 — Install Judge.me reviews app**
  Reviews section shows placeholder text. Install and configure **Judge.me** from **Admin → Apps → App Store → search "Judge.me"**.

---

## 🟡 Medium

- **GL-06 / HP-07 — Update announcement bar text**
  Live: "LAUNCHING APRIL 2026 — JOIN THE WAITING LIST FOR EARLY ACCESS"
  Confirm the correct launch date and update in **Admin → Online Store → Themes → Customise → Announcement Bar**.
