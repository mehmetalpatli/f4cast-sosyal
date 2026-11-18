import sys, asyncio
from pathlib import Path
from playwright.async_api import async_playwright
LOGO=Path(sys.argv[1]); OUT=Path(sys.argv[2]); SHOT=Path(sys.argv[3]).as_uri()
lock=(LOGO/"moduller/financials/svg/f4cast-financials-yatay-lacivert.svg").as_uri()
BASE="""<html><head><style>*{margin:0;padding:0;box-sizing:border-box}body{width:%dpx;height:%dpx;background:#FAF9F7;color:#292744;font-family:Inter;position:relative;overflow:hidden}
.card{position:absolute;border-radius:14px;overflow:hidden;box-shadow:0 18px 48px rgba(41,39,68,.16),0 2px 6px rgba(41,39,68,.08);border:1px solid #E6E4F0;background:#fff}
.card img{display:block;width:100%%}</style></head><body>%s</body></html>"""
def wide():
    b=f"""<img src="{lock}" style="position:absolute;left:56px;top:52px;height:34px">
<h1 style="position:absolute;left:56px;top:126px;font-size:48px;font-weight:600;letter-spacing:.01em">Programınız için tek finansal model.</h1>
<div class=card style="left:56px;top:236px;width:1088px"><img src="{SHOT}"></div>
<p style="position:absolute;left:56px;bottom:46px;font-size:18px;font-weight:500;color:#4B4A8F">Financial forecasting for startups</p>"""
    return BASE%(1200,627,b)
def square():
    b=f"""<img src="{lock}" style="position:absolute;left:64px;top:64px;height:48px">
<h1 style="position:absolute;left:64px;top:250px;width:900px;font-size:64px;font-weight:600;line-height:1.15;letter-spacing:.01em">Programınız için<br>tek finansal model.</h1>
<div class=card style="left:64px;top:500px;width:952px"><img src="{SHOT}"></div>
<p style="position:absolute;left:64px;bottom:64px;font-size:24px;font-weight:500;color:#4B4A8F">Financial forecasting for startups</p>"""
    return BASE%(1080,1080,b)
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch()
        for n,(w,h,d) in {"linkedin-reklam-1200x627.png":(1200,627,wide()),"linkedin-reklam-1080x1080.png":(1080,1080,square())}.items():
            pg=await br.new_page(viewport={"width":w,"height":h},device_scale_factor=1)
            f=OUT/("_"+n+".html"); f.write_text(d,encoding="utf-8"); await pg.goto(f.as_uri()); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(OUT/n)); f.unlink(); await pg.close()
        await br.close()
asyncio.run(main())
