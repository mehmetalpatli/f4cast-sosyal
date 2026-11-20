import sys, asyncio
from pathlib import Path
from playwright.async_api import async_playwright

OUT = Path(sys.argv[1])
U = lambda n: (OUT / n).as_uri()
NAVY, KOB, SAGE, DSAGE, MINT = "#292744", "#284A98", "#E8EFEA", "#8FA89B", "#2EC4B6"
CSS = f"""@font-face{{font-family:SG;font-weight:600;src:url({U('space-grotesk-latin-600-normal.woff2')})}}
@font-face{{font-family:SG;font-weight:600;src:url({U('space-grotesk-latin-ext-600-normal.woff2')});unicode-range:U+0100-024F}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{position:relative;overflow:hidden;font-family:Inter}}
h1{{font-family:SG;font-weight:600;letter-spacing:-.01em;line-height:1.08}}"""


def page(w, h, bg, body):
    return f"<html><head><style>{CSS} body{{width:{w}px;height:{h}px;background:{bg}}}</style></head><body>{body}</body></html>"


def kisisel_23():
    items = ["Bu girişimin güncel dosyası hangisi?",
             "4.4 tabloları nakit akışıyla tutuyor mu?",
             "İki girişimin rakamları aynı şeyi mi ölçüyor?"]
    li = "".join(
        f"""<div style="display:flex;gap:34px;align-items:center">
<div style="flex:none;width:72px;height:72px;border-radius:18px;background:{MINT};color:{NAVY};font:600 38px SG;display:flex;align-items:center;justify-content:center">{i+1}</div>
<p style="font-size:40px;line-height:1.3;color:{SAGE}">{t}</p></div>""" for i, t in enumerate(items))
    b = f"""<div style="position:absolute;right:-180px;top:-180px;width:560px;height:560px;border-radius:50%;background:{KOB}"></div>
<div style="position:absolute;left:96px;right:96px;top:250px">
<div style="width:96px;height:8px;border-radius:4px;background:{MINT}"></div>
<h1 style="margin-top:56px;font-size:84px;color:#fff">20–40 girişim.<br><span style="color:{MINT}">20–40 ayrı<br>Excel dosyası.</span></h1>
<p style="margin-top:56px;font-size:36px;color:{SAGE};opacity:.85">Panelden önce her dosyada aynı üç soru:</p>
<div style="margin-top:44px;display:flex;flex-direction:column;gap:36px">{li}</div></div>
<p style="position:absolute;left:96px;bottom:80px;font-size:30px;font-weight:500;color:{DSAGE}">Mehmet Alpatlı · finansal planlama notları</p>"""
    return page(1080, 1350, NAVY, b)


def sayfa_24():
    card = lambda n, x, y, w: f'<img src="{U(n)}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;border-radius:14px;box-shadow:0 18px 40px rgba(20,18,40,.35)">'
    # kart genişlikleri: 837px kaynak, 2 sütun
    w = 484
    h1 = int(413 * w / 837); y2 = 630 + h1 + 24
    b = f"""<img src="{U('lockup-ters.png')}" style="position:absolute;left:64px;top:64px;height:52px">
<h1 style="position:absolute;left:64px;top:255px;width:960px;font-size:92px;color:#fff">Dört tablo,<br><span style="color:{MINT}">tek modelden.</span></h1>
<p style="position:absolute;left:64px;top:495px;font-size:34px;font-weight:500;color:{SAGE}">AGY-112 Bölüm 4.4 · Tablo 4.4.1–4.4.4</p>
<div style="position:absolute;left:24px;right:24px;top:598px;height:{y2 + int(319 * w / 837) + 76 - 598}px;border-radius:32px;background:{NAVY}"></div>
{card('c1.png', 48, 630, w)}{card('c2.png', 548, 630, w)}
{card('c3.png', 48, y2, w)}{card('c4.png', 548, y2, w)}
<p style="position:absolute;left:52px;top:{y2 + int(319 * w / 837) + 20}px;font-size:22px;color:{SAGE};opacity:.75">Kurgusal test verisi</p>
<p style="position:absolute;left:64px;bottom:64px;font-size:28px;font-weight:500;color:{SAGE}">Financial forecasting for startups</p>"""
    return page(1080, 1350, KOB, b)


async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch()
        for name, fn in [("23kas-linkedin-kisisel.png", kisisel_23), ("24kas-linkedin-sayfa.png", sayfa_24)]:
            pg = await br.new_page(viewport={"width": 1080, "height": 1350})
            f = OUT / ("_" + name + ".html")
            f.write_text(fn(), encoding="utf-8")
            await pg.goto(f.as_uri())
            await pg.wait_for_timeout(600)
            await pg.screenshot(path=str(OUT / name))
            f.unlink()
            await pg.close()
        await br.close()

asyncio.run(main())
