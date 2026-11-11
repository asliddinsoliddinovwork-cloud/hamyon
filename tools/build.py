#!/usr/bin/env python3
"""Hamyon sayti generatori.

Manba fayllar (qo'lda tahrirlanadi):
  src/template.html  - bosh sahifa qolipi (HTML, CSS, JS)
  src/i18n.json      - barcha matnlar: uz, ru, en
  src/site.json      - versiya, APK fayl nomi, aloqa ma'lumotlari

Natija (qo'lda tahrirlanmaydi, har safar qayta yoziladi):
  index.html, ru/index.html, en/index.html
  privacy.html, ru/privacy.html, en/privacy.html
  404.html, robots.txt, sitemap.xml

Ishga tushirish:  python3 tools/build.py
Tashqi kutubxona kerak emas (faqat Python 3.8+).
"""
import hashlib
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANGS = ["uz", "ru", "en"]
LANG_DIR = {"uz": "", "ru": "ru/", "en": "en/"}
LANG_LABEL = {"uz": "UZ", "ru": "RU", "en": "EN"}
OG_LOCALE = {"uz": "uz_UZ", "ru": "ru_RU", "en": "en_US"}


def esc(text):
    return html.escape(str(text), quote=True)


def load():
    template = (ROOT / "src/template.html").read_text(encoding="utf-8")
    i18n = json.loads((ROOT / "src/i18n.json").read_text(encoding="utf-8"))
    site = json.loads((ROOT / "src/site.json").read_text(encoding="utf-8"))
    missing = [(l, k) for l in LANGS for k in i18n["uz"] if k not in i18n[l]]
    if missing:
        sys.exit(f"i18n.json: tarjima yetishmaydi: {missing}")
    apk = ROOT / site["apk"]
    if not apk.is_file():
        sys.exit(f"APK topilmadi: {apk}")
    data = apk.read_bytes()
    site["apk_sha256"] = hashlib.sha256(data).hexdigest()
    site["apk_bytes"] = len(data)
    return template, i18n, site


def rich(value):
    """'Kulrang qism| asosiy qism' -> <span class="dim">..</span>.."""
    if "|" in value:
        a, b = value.split("|", 1)
        return f'<span class="dim">{esc(a)}</span>{esc(b)}'
    return esc(value)


def size_label(n_bytes, lang):
    mb = f"{n_bytes / 1048576:.1f}"
    return (mb.replace(".", ",") + " МБ") if lang == "ru" else mb + " MB"


def lang_switch(t, lang, base, page):
    links = []
    for l in LANGS:
        href = base + LANG_DIR[l] + page or "./"
        cur = ' aria-current="true"' if l == lang else ""
        links.append(f'<a href="{href}" hreflang="{l}" lang="{l}"{cur}>{LANG_LABEL[l]}</a>')
    return f'<div class="lang" role="group" aria-label="{esc(t["aLang"])}">{"".join(links)}</div>'


def foot_links(t, site, base, lang, with_privacy=True):
    out = []
    if with_privacy:
        out.append(f'<a href="{base}{LANG_DIR[lang]}privacy.html">{esc(t["footPrivacy"])}</a>')
    c = site.get("contacts", {})
    if c.get("telegram"):
        out.append(f'<a href="{esc(c["telegram"])}" rel="noopener">{esc(t["footTelegram"])}</a>')
    if c.get("email"):
        out.append(f'<a href="mailto:{esc(c["email"])}">{esc(t["footEmail"])}</a>')
    if site.get("repo"):
        out.append(f'<a href="{esc(site["repo"])}" rel="noopener">{esc(t["footSource"])}</a>')
    return "".join(out)


def head_common(t, site, lang, base, page, title, desc):
    url = site["site"] + LANG_DIR[lang] + page
    alts = "".join(
        f'<link rel="alternate" hreflang="{l}" href="{site["site"]}{LANG_DIR[l]}{page}">\n' for l in LANGS
    ) + f'<link rel="alternate" hreflang="x-default" href="{site["site"]}{page}">\n'
    return (
        f"<title>{esc(title)}</title>\n"
        f'<meta name="description" content="{esc(desc)}">\n'
        f'<link rel="canonical" href="{url}">\n{alts}'
        f'<link rel="icon" href="{base}favicon.ico" sizes="any">\n'
        f'<link rel="icon" type="image/png" href="{base}app/icons/icon-192.png">\n'
        f'<link rel="apple-touch-icon" href="{base}app/icons/apple-touch-icon.png">\n'
        f'<meta property="og:type" content="website">\n'
        f'<meta property="og:site_name" content="Hamyon">\n'
        f'<meta property="og:locale" content="{OG_LOCALE[lang]}">\n'
        f'<meta property="og:url" content="{url}">\n'
        f'<meta property="og:title" content="{esc(t["ogTitle"])}">\n'
        f'<meta property="og:description" content="{esc(t["ogDesc"])}">\n'
        f'<meta property="og:image" content="{site["site"]}img/og.png">\n'
        f'<meta property="og:image:width" content="1200">\n'
        f'<meta property="og:image:height" content="630">\n'
        f'<meta name="twitter:card" content="summary_large_image">'
    )


def json_ld(t, site, lang):
    app = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "Hamyon",
        "description": t["desc"],
        "url": site["site"] + LANG_DIR[lang],
        "applicationCategory": "FinanceApplication",
        "operatingSystem": "Android 8.0+, iOS (Safari)",
        "softwareVersion": site["version"],
        "downloadUrl": site["site"] + site["apk"],
        "fileSize": size_label(site["apk_bytes"], "en"),
        "inLanguage": LANGS,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "UZS"},
    }
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]
        ],
    }
    dump = lambda o: json.dumps(o, ensure_ascii=False).replace("</", "<\\/")
    return f'\n<script type="application/ld+json">{dump(app)}</script>\n<script type="application/ld+json">{dump(faq)}</script>'


def build_home(template, t, site, lang):
    base = "../" if LANG_DIR[lang] else ""
    s = template
    head = head_common(t, site, lang, base, "", t["title"], t["desc"]) + json_ld(t, site, lang)

    faq = "".join(
        f'<details{" open" if i == 0 else ""}><summary>{esc(q)}<i></i></summary><p class="t-body">{esc(a)}</p></details>'
        for i, (q, a) in enumerate(t["faq"])
    )
    fileinfo = (
        f'{esc(t["fileVersion"])} {esc(site["version"])} · {esc(t["fileDate"])} {esc(site["apk_date"])} · '
        f'{size_label(site["apk_bytes"], lang)}<br>{esc(t["fileSha"])}: <code>{site["apk_sha256"]}</code>'
    )
    changelog = f'<summary>{esc(t["newsTitle"])}</summary><ul>' + "".join(
        f"<li><b>{esc(v)}</b> — {esc(text)}</li>" for v, text in t["news"]
    ) + "</ul>"

    for key, val in {
        "@@LANG@@": lang,
        "@@HEAD@@": head,
        "@@LANGSWITCH@@": lang_switch(t, lang, base, ""),
        "@@FAQ@@": faq,
        "@@FILEINFO@@": fileinfo,
        "@@CHANGELOG@@": changelog,
        "@@FOOTLINKS@@": foot_links(t, site, base, lang),
        "@@APK@@": base + site["apk"],
        "@@BASE@@": base,
    }.items():
        s = s.replace(key, val)

    # Matnlar: <tag data-i="kalit"></tag>
    def fill(m):
        key = m.group(3)
        if key not in t:
            sys.exit(f"template.html: i18n.json da '{key}' kaliti yo'q")
        return f"<{m.group(1)}{m.group(2)}{m.group(4)}>{rich(t[key])}</{m.group(1)}>"

    s = re.sub(r'<(\w+)([^<>]*?) data-i="(\w+)"([^<>]*)></\1>', fill, s)
    # Chiplar: <div data-chips="kalit"></div>
    s = re.sub(
        r'(<div class="chips") data-chips="(\w+)">',
        lambda m: m.group(1) + ">" + "".join(f"<span>{esc(c)}</span>" for c in t[m.group(2)]),
        s,
    )
    # Atributlar: {{kalit}}
    s = re.sub(r"\{\{(\w+)\}\}", lambda m: esc(t[m.group(1)]), s)

    left = re.findall(r'@@\w+@@|\{\{\w+\}\}|data-i="\w+"|data-chips', s)
    if left:
        sys.exit(f"To'ldirilmagan joylar qoldi ({lang}): {sorted(set(left))}")
    return s


PAGE_CSS = """
:root{--bg:#FFFFFF;--bg-alt:#F5F5F7;--ink:#1D1D1F;--ink-2:#6E6E73;--line:#D2D2D7;--link:#0066CC;--chip:#F0F0F2;--card:#FFFFFF}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0E0E10;--bg-alt:#161618;--ink:#F2F2F4;--ink-2:#A1A1A6;--line:#3A3A3D;--link:#3A9BFF;--chip:#1E1E21;--card:#1E1E21;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0E0E10;--bg-alt:#161618;--ink:#F2F2F4;--ink-2:#A1A1A6;--line:#3A3A3D;--link:#3A9BFF;--chip:#1E1E21;--card:#1E1E21;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.7 -apple-system,BlinkMacSystemFont,"SF Pro Text","Inter","Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--link);text-decoration:none}a:hover{text-decoration:underline}
:focus-visible{outline:2px solid var(--link);outline-offset:3px;border-radius:6px}
.wrap{max-width:760px;margin:0 auto;padding:0 22px}
header{border-bottom:1px solid var(--line)}
.bar{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:52px}
.brand{display:flex;align-items:center;gap:10px;font-size:20px;font-weight:600;color:var(--ink)}
.brand img{width:28px;height:28px;border-radius:6.5px}
.lang{display:flex;background:var(--chip);border-radius:980px;padding:2px}
.lang a{font-size:12px;font-weight:600;padding:4px 9px;border-radius:980px;color:var(--ink-2);min-width:34px;text-align:center}
.lang a[aria-current="true"]{background:var(--card);color:var(--ink);box-shadow:0 1px 3px rgba(0,0,0,.12)}
main{padding:56px 0 72px}
h1{font-size:clamp(30px,5vw,44px);line-height:1.1;letter-spacing:-.022em;font-weight:600;margin:0 0 8px}
h2{font-size:20px;line-height:1.3;font-weight:600;margin:36px 0 6px}
p{margin:0 0 12px;color:var(--ink-2)}
.meta{font-size:14px}
ul{margin:0;padding-left:20px;color:var(--ink-2)}
footer{background:var(--bg-alt);color:var(--ink-2);font-size:13px;padding:22px 0}
"""

THEME_BOOT = (
    "<script>(function(){var r=document.documentElement,t=null;try{t=localStorage.getItem('hamyon_site_theme')}catch(e){}"
    "if(t==='dark'||t==='light')r.dataset.theme=t;})();</script>"
)


def simple_page(t, site, lang, base, page, title, desc, body, robots=None):
    head = head_common(t, site, lang, base, page, title, desc)
    if robots:
        head = re.sub(r'<link rel="(canonical|alternate)"[^>]*>\n', "", head) + f'\n<meta name="robots" content="{robots}">'
    home = base + LANG_DIR[lang] or "./"
    switch = lang_switch(t, lang, base, page) if page else ""
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{THEME_BOOT}
{head}
<style>{PAGE_CSS}</style>
</head>
<body>
<header><div class="wrap bar"><a class="brand" href="{home}"><img src="{base}img/icon.webp" width="192" height="192" alt=""><span>Hamyon</span></a>{switch}</div></header>
<main><div class="wrap">
{body}
</div></main>
<footer><div class="wrap">© 2026 Hamyon</div></footer>
</body>
</html>
"""


def build_privacy(t, site, lang):
    base = "../" if LANG_DIR[lang] else ""
    home = base + LANG_DIR[lang] or "./"
    body = [f'<p class="meta"><a href="{home}">← {esc(t["backHome"])}</a></p>', f'<h1>{esc(t["ppTitle"])}</h1>']
    body.append(f'<p class="meta">{esc(t["ppUpdated"])}: {esc(site["privacy_updated"])}</p>')
    for h, p in t["pp"]:
        body.append(f"<h2>{esc(h)}</h2>\n<p>{esc(p)}</p>")
    contacts = foot_links(t, site, base, lang, with_privacy=False)
    if contacts:
        items = "".join(f"<li>{a}</li>" for a in re.findall(r"<a .*?</a>", contacts))
        body.append(f'<h2>{esc(t["ppContactH"])}</h2>\n<p>{esc(t["ppContactP"])}</p>\n<ul>{items}</ul>')
    desc = t["pp"][0][1]
    return simple_page(t, site, lang, base, "privacy.html", f'{t["ppTitle"]} — Hamyon', desc, "\n".join(body))


def build_404(i18n, site):
    # GitHub Pages bitta 404.html ni har qanday chuqurlikdagi manzil uchun beradi: havolalar mutlaq bo'lishi shart
    t = i18n["uz"]
    body = "\n".join(
        f'<h1 lang="{l}">{esc(i18n[l]["nfTitle"])}</h1>\n<p lang="{l}">{esc(i18n[l]["nfLead"])} '
        f'<a href="/{LANG_DIR[l]}">{esc(i18n[l]["backHome"])}</a></p>'
        for l in LANGS
    )
    page = simple_page(t, site, "uz", "/", "", f'{t["nfTitle"]} — Hamyon', t["nfLead"], body, robots="noindex")
    return page.replace('href="./"', 'href="/"')


def write(rel, text):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"  {rel:22} {len(text.encode('utf-8')) / 1024:6.1f} KB")


def main():
    template, i18n, site = load()
    print("Yozildi:")
    urls = []
    for lang in LANGS:
        t = i18n[lang]
        write(LANG_DIR[lang] + "index.html", build_home(template, t, site, lang))
        write(LANG_DIR[lang] + "privacy.html", build_privacy(t, site, lang))
        urls += [site["site"] + LANG_DIR[lang], site["site"] + LANG_DIR[lang] + "privacy.html"]
    write("404.html", build_404(i18n, site))
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /src/\nDisallow: /tools/\n\nSitemap: {site['site']}sitemap.xml\n")
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n"
    write("sitemap.xml", sitemap)
    print(f"APK: {site['apk']}  SHA-256: {site['apk_sha256']}")


if __name__ == "__main__":
    main()
