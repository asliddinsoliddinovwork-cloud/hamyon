# Hamyon

Shaxsiy moliya ilovasi: kirim, chiqim, budjet, hisoblar va qarzlar. Bepul, internetsiz ishlaydi.

- **Sayt:** https://hamyonapp.uz/
- **iPhone:** https://hamyonapp.uz/app/ — Safari'da oching → Ulashish → Bosh ekranga qo'shish
- **Android (APK):** https://hamyonapp.uz/Hamyon-2.4.apk — Android 8.0 va undan yuqori, 2.6 MB

## Tuzilma

- `src/template.html` — bosh sahifa qolipi (HTML, CSS, JS). **Sayt shu yerda tahrirlanadi**
- `src/i18n.json` — barcha matnlar (uz, ru, en)
- `src/site.json` — versiya, APK fayl nomi va sanasi, aloqa ma'lumotlari
- `tools/build.py` — qolip va matnlardan tayyor sahifalarni yasaydi (tashqi kutubxona kerak emas)
- `tools/make_assets.py` — `favicon.ico`, `img/og.png` va `fonts/` ni yasaydi (Pillow va fontTools kerak; faqat belgi o'zgarganda)
- `index.html`, `ru/`, `en/`, `privacy.html`, `404.html`, `robots.txt`, `sitemap.xml` — **generatsiya qilinadi, qo'lda tahrirlanmaydi**
- `img/` — skrinshotlar va belgi, `fonts/` — Inter shrifti (OFL litsenziyasi)
- `app/` — iPhone veb-ilovasi (PWA): `index.html`, `manifest.webmanifest`, `sw.js`, `icons/`
- `Hamyon-2.4.apk` — Android ilova
- `CNAME` — GitHub Pages uchun domen (`hamyonapp.uz`)
- `.nojekyll` — GitHub Pages fayllarni o'zgartirmasligi uchun

## Saytni o'zgartirish

1. Matn uchun `src/i18n.json`, tuzilma yoki dizayn uchun `src/template.html` ni tahrirlang.
2. `python3 tools/build.py` ni ishga tushiring. Tarjima yoki kalit yetishmasa, skript xato bilan to'xtaydi.
3. Tekshirish: `python3 -m http.server 8000` va brauzerda `http://localhost:8000/`, `/ru/`, `/en/` ni oching.
4. O'zgargan barcha fayllarni commit qiling.

Aloqa havolalari: `src/site.json` ichidagi `contacts.telegram` (to'liq havola, masalan `https://t.me/...`) va `contacts.email` ni to'ldiring. Bo'sh bo'lsa, saytda ko'rsatilmaydi.

## Yangi versiya chiqarish

iPhone ilovasi: `app/index.html` ni yangilang va `app/sw.js` ichidagi `VERSION` qiymatini oshiring (masalan `hamyon-2.0.2`). Foydalanuvchilarda ilova keyingi ochilishlarda yangilanadi.

Android ilovasi: yangi APK faylni repoga qo'ying, `src/site.json` da `version`, `apk`, `apk_date` ni yangilang, `src/i18n.json` da versiya raqami yozilgan matnlarni (`heroEyebrow`, `s1p`) va `news` ro'yxatini yangilang, so'ng `python3 tools/build.py`. SHA-256 nazorat summasi fayldan avtomatik hisoblanadi.
