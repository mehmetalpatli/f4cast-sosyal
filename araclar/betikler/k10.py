import sys, asyncio
from pathlib import Path
from playwright.async_api import async_playwright
LOGO=Path(sys.argv[1]); OUT=Path(sys.argv[2]); ico=(LOGO/"ikon/svg/f4cast-ikon-ters.svg").as_uri()
def doc(logo):
    lg=f'<img src="{ico}" style="position:absolute;left:50%;bottom:90px;width:72px;height:72px;transform:translateX(-50%)">' if logo else ""
    return f"""<html><head><style>*{{margin:0;padding:0;box-sizing:border-box}}body{{width:1080px;height:1350px;background:#1E1C33;color:#FAF9F7;font-family:Inter;position:relative;text-align:center}}</style></head><body>
<div style="position:absolute;left:110px;right:110px;top:300px">
<p style="font-size:44px;font-weight:500;color:#AAA8D3;letter-spacing:.06em">10 KASIM 1938</p>
<div style="width:96px;height:6px;background:#AAA8D3;border-radius:3px;margin:56px auto"></div>
<h1 style="font-size:60px;font-weight:600;line-height:1.3;letter-spacing:.01em">Gazi Mustafa Kemal<br>Atatürk'ü saygı, minnet<br>ve özlemle anıyoruz.</h1>
<p style="font-size:38px;font-weight:400;color:#c9c7e6;margin-top:96px;font-style:italic">"Hayatta en hakiki mürşit ilimdir."</p>
<p style="font-size:30px;font-weight:400;color:#AAA8D3;margin-top:20px">Mustafa Kemal Atatürk</p></div>{lg}</body></html>"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={"width":1080,"height":1350})
        for n,l in [("10kasim-kisisel.png",False),("10kasim-f4cast.png",True)]:
            f=OUT/("_"+n+".html"); f.write_text(doc(l),encoding="utf-8"); await pg.goto(f.as_uri()); await pg.wait_for_timeout(200); await pg.screenshot(path=str(OUT/n)); f.unlink()
        await b.close()
asyncio.run(main())
