# Hamyon — iPhone (veb-ilova)

Bu papka iPhone uchun Hamyon veb-ilovasi (PWA). Android versiyasi bilan bir xil imkoniyatlar, internetsiz ishlaydi.

## GitHub Pages'ga joylash (bepul)

1. github.com → **New repository** → nomi: `hamyon` → **Public** → **Create repository**.
2. **uploading an existing file** havolasini bosing va shu papkadagi barcha fayllarni (shu jumladan `icons` papkasini) sudrab tashlang → **Commit changes**.
3. **Settings → Pages** → *Source*: **Deploy from a branch** → Branch: **main**, papka: **/(root)** → **Save**.
4. 1–2 daqiqadan keyin ilova manzili chiqadi: `https://<github-login>.github.io/hamyon/`

## iPhone'ga o'rnatish

1. Manzilni iPhone'da **Safari**'da oching.
2. **Ulashish** (□↑) → **Bosh ekranga qo'shish** (iOS 26'da avval **•••**).
3. **Veb-ilova sifatida ochish** yoqilgan holda **Qo'shish**.

## Yangi versiya chiqarish

`index.html` ni yangilang va `sw.js` ichidagi `VERSION` qiymatini o'zgartiring (masalan `hamyon-2.0.1`), keyin GitHub'ga yuklang. Foydalanuvchilarda ilova keyingi ochilishlarda yangilanadi.

## Fayllar

- `index.html` — ilovaning o'zi
- `manifest.webmanifest` — nom, ikonka, to'liq ekran rejimi
- `sw.js` — internetsiz ishlash (kesh)
- `icons/` — bosh ekran ikonkalari (180, 192, 512 px)
- `.nojekyll` — GitHub Pages fayllarni o'zgartirmasligi uchun
