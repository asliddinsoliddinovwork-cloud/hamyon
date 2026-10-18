# Hamyon

Shaxsiy moliya ilovasi: kirim, chiqim, budjet, hisoblar va qarzlar. Bepul, internetsiz ishlaydi.

- **Sayt:** https://hamyonapp.uz/
- **iPhone:** https://hamyonapp.uz/app/ — Safari'da oching → Ulashish → Bosh ekranga qo'shish
- **Android (APK):** https://hamyonapp.uz/Hamyon-2.1.apk — Android 8.0 va undan yuqori, 91 KB

## Tuzilma

- `index.html` — targ'ibot sayti (bosh sahifa)
- `app/` — iPhone veb-ilovasi (PWA): `index.html`, `manifest.webmanifest`, `sw.js`, `icons/`
- `Hamyon-2.1.apk` — Android ilova
- `CNAME` — GitHub Pages uchun domen (`hamyonapp.uz`)
- `.nojekyll` — GitHub Pages fayllarni o'zgartirmasligi uchun

## Yangi versiya chiqarish

iPhone ilovasi: `app/index.html` ni yangilang va `app/sw.js` ichidagi `VERSION` qiymatini oshiring (masalan `hamyon-2.0.2`). Foydalanuvchilarda ilova keyingi ochilishlarda yangilanadi.
