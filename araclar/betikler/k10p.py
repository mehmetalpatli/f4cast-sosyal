import sys, asyncio
from pathlib import Path
from playwright.async_api import async_playwright
LOGO=Path(sys.argv[1]); OUT=Path(sys.argv[2]); PHOTO=Path(sys.argv[3]).as_uri()
ico=(LOGO/"ikon/svg/f4cast-ikon-ters.svg").as_uri()
def doc(logo):
    lg=f'<img src="{ico}" style="position:absolute;right:72px;bottom:64px;width:64px;height:64px">' if logo else ""
    return f"""<html><head><style>*{{margin:0;padding:0;box-sizing:border-box}}body{{width:1080px;height:1350px;background:#000;color:#FAF9F7;font-family:Inter;position:relative;text-align:center}}</style></head><body>
<img src="{PHOTO}" style="position:absolute;left:50%;top:60px;width:600px;transform:translateX(-50%)">
<div style="position:absolute;left:0;right:0;top:0;height:900px;background:linear-gradient(to bottom,rgba(0,0,0,0) 70%,#000 100%)"></div>
<div style="position:absolute;left:100px;right:100px;top:930px">
<p style="font-size:36px;font-weight:500;color:#AAA8D3;letter-spacing:.06em">10 KASIM 1938</p>
<h1 style="font-size:46px;font-weight:600;line-height:1.3;margin-top:28px">Gazi Mustafa Kemal Atatürk'ü<br>saygı, minnet ve özlemle anıyoruz.</h1>
<p style="font-size:30px;color:#c9c7e6;margin-top:36px;font-style:italic">"Hayatta en hakiki mürşit ilimdir."</p></div>{lg}</body></html>"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={"width":1080,"height":1350})
        for n,l in [("10kasim-kisisel-foto.png",False),("10kasim-f4cast-foto.png",True)]:
            f=OUT/("_"+n+".html"); f.write_text(doc(l),encoding="utf-8"); await pg.goto(f.as_uri()); await pg.wait_for_timeout(300); await pg.screenshot(path=str(OUT/n)); f.unlink()
        await b.close()
asyncio.run(main())
