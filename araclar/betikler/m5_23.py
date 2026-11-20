import sys, asyncio
from pathlib import Path
from playwright.async_api import async_playwright
OUT = Path(sys.argv[1]); U = lambda n: (OUT / n).as_uri()
NAVY, KOB, SAGE, DSAGE, MINT = "#292744", "#284A98", "#E8EFEA", "#8FA89B", "#2EC4B6"
CSS = f"""@font-face{{font-family:SG;font-weight:600;src:url({U('space-grotesk-latin-600-normal.woff2')})}}
@font-face{{font-family:SG;font-weight:600;src:url({U('space-grotesk-latin-ext-600-normal.woff2')});unicode-range:U+0100-024F}}
*{{margin:0;padding:0;box-sizing:border-box}}body{{width:1080px;height:1350px;background:{NAVY};position:relative;overflow:hidden;font-family:Inter}}
h1{{font-family:SG;font-weight:600;letter-spacing:-.01em;line-height:1.08}}"""
rows = [("Modül 5", "3 yıllık gelir–gider projeksiyonu ve nakit akışı"),
        ("Çıktı", "Finansal projeksiyon dosyası"),
        ("Kuruluşun desteği", "Bütçeleme şablonu, örnek finansal planlar")]
items = "".join(f"""<div style="display:flex;gap:28px;align-items:flex-start;padding:26px 0;{'border-top:2px solid rgba(41,39,68,.18);' if i else ''}">
<div style="flex:none;width:250px;font:600 30px SG;color:{NAVY};padding-top:4px">{k}</div>
<p style="font-size:36px;line-height:1.3;color:{NAVY}">{v}</p></div>""" for i, (k, v) in enumerate(rows))
body = f"""<div style="position:absolute;right:-220px;top:-240px;width:600px;height:600px;border-radius:50%;background:{KOB}"></div>
<div style="position:absolute;left:96px;top:130px">
<div style="width:96px;height:8px;border-radius:4px;background:{MINT}"></div>
<h1 style="margin-top:52px;font-size:82px;color:#fff">Kılavuz şablon<br>bekliyor.</h1>
<h1 style="margin-top:16px;font-size:82px;color:{MINT}">Şablonu kim<br>hazırlıyor?</h1></div>
<div style="position:absolute;left:56px;right:56px;top:690px;border-radius:32px;background:{DSAGE};padding:28px 48px 20px">
<p style="font:600 26px SG;color:{NAVY};letter-spacing:.02em;margin-bottom:6px">BİGG Aşama 1 · Uygulayıcı Kuruluş Kılavuzu</p>{items}</div>
<p style="position:absolute;left:96px;bottom:118px;font-size:22px;color:{SAGE};opacity:.75">Kaynak: 1812 Aşama 1 Uygulayıcı Kuruluş Kılavuzu, Sürüm 1.0, Ağustos 2025</p>
<p style="position:absolute;left:96px;bottom:66px;font-size:30px;font-weight:500;color:{DSAGE}">Mehmet Alpatlı · finansal planlama notları</p>"""
async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch(); pg = await br.new_page(viewport={"width": 1080, "height": 1350})
        f = OUT / "_m5.html"; f.write_text(f"<html><head><style>{CSS}</style></head><body>{body}</body></html>", encoding="utf-8")
        await pg.goto(f.as_uri()); await pg.wait_for_timeout(600)
        await pg.screenshot(path=str(OUT / "23kas-linkedin-kisisel-v3.png")); f.unlink(); await br.close()
asyncio.run(main())
