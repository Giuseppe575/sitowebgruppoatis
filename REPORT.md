# Report

Date: 2025-12-20 21:46

## Summary
- - Added real images and logo replacements, including hero visual and header logo sizing.
- - Created separate pages for Servizi, Metodo, Laboratorio, FAQ, Contatti, and Preventivo; home shows abbreviated sections.
- - Updated contacts/KPI data, added clickable email/phone/map links, and compacted mobile layout.
- - Added simple mailto forms for quick request and preventivo.

## Files
- sito_restyling_ATIS_con_immagini.html
- servizi.html
- metodo.html
- laboratorio.html
- faq.html
- contatti.html
- preventivo.html
- scripts/update_pages.py
- backup_20251220

## Per-file Changes
- sito_restyling_ATIS_con_immagini.html
  - Header logo replaced with assetsimg/logointestaione.jpeg and resized; hero visual switched from SVG to logo image.
  - Immagini a tema uses real photos with 16:9 crop, overlay, and filter; section title removed and padding reduced.
  - KPI updated to real values; contacts updated with legal/operational address, P. IVA, emails, and clickable links.
  - Home abbreviations enabled via CSS; quick request form added; menu links point to new pages; preventivo link updated.
  - Mobile spacing tightened across header, cards, FAQ, CTA, footer, and hero for small screens.
- servizi.html
  - Standalone page for Servizi using data-page filter; full Servizi section visible.
- metodo.html
  - Standalone page for Metodo using data-page filter; full Metodo section visible.
- laboratorio.html
  - Standalone page focused on the Laboratorio card within Servizi.
- faq.html
  - Standalone page for FAQ with full details section.
- contatti.html
  - Standalone page for Contatti with updated contact details and links.
- preventivo.html
  - New preventivo page with simple mailto form in a glass panel.
- scripts/update_pages.py
  - Utility script to apply future text replacements across pages.
- backup_20251220
  - Snapshot of all HTML files and assetsimg directory.

## Section Breakdown
- Header/Hero
  - Logo in topbar replaced with header image; resized to 300x180.
  - Hero visual SVG replaced with the same logo at 720x320.
- Immagini a tema
  - Swapped SVG placeholders for sicurezza/ambiente/laboratorio photos.
  - Removed title/description block and reduced top padding.
- Servizi/Metodo/Laboratorio/FAQ/Contatti
  - Home shows abbreviated content via CSS; full content shown on dedicated pages.
  - Updated contact info with clickable mail/phone and Maps links.
- KPI
  - Updated to +30 years, +1000 companies, +1000 hours.
- CTA/Forms
  - Quick request mailto form added.
  - Preventivo page with mailto form created.
- Footer
  - Added P. IVA, tel (clickable), email, and address (Maps link).
  - Mobile-only separators for legal links; spacing compacted.

## Notes
- Forms use `mailto:` and require a configured mail client.