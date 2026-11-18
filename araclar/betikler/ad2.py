import sys, asyncio
from pathlib import Path
from playwright.async_api import async_playwright
LOGO=Path(sys.argv[1]); OUT=Path(sys.argv[2])
lockN=(LOGO/"moduller/financials/svg/f4cast-financials-yatay-lacivert.svg").as_uri()
lockW=(LOGO/"moduller/financials/svg/f4cast-financials-yatay-ters.svg").as_uri()
shot=(OUT/"shot-nakit.png").as_uri()
f1=(OUT/"space-grotesk-latin-600-normal.woff2").as_uri(); f2=(OUT/"space-grotesk-latin-ext-600-normal.woff2").as_uri()
CSS=f"""@font-face{{font-family:SG;font-weight:600;src:url({f1})}}@font-face{{font-family:SG;font-weight:600;src:url({f2});unicode-range:U+0100-024F}}
*{{margin:0;padding:0;box-sizing:border-box}}body{{position:relative;overflow:hidden;font-family:Inter}}
h1{{font-family:SG;font-weight:600;letter-spacing:-.01em;line-height:1.05}}
.card{{position:absolute;border-radius:18px;overflow:hidden;background:#fff;box-shadow:0 30px 70px rgba(41,39,68,.28),0 4px 12px rgba(41,39,68,.12)}}
.card img{{display:block;width:100%}}"""
def page(w,h,bg,body): return f"<html><head><style>{CSS} body{{width:{w}px;height:{h}px;background:{bg}}}</style></head><body>{body}</body></html>"
def A(w,h):
    if w>h:
        b=f"""<div style="position:absolute;right:-120px;top:-160px;width:620px;height:620px;border-radius:50%;background:#8FA89B;opacity:.55"></div>
<img src="{lockN}" style="position:absolute;left:56px;top:54px;height:30px">
<h1 style="position:absolute;left:56px;top:170px;width:470px;font-size:58px;color:#292744">Programınız için tek finansal model.</h1>
<div style="position:absolute;left:56px;top:420px;width:72px;height:8px;border-radius:4px;background:#2EC4B6"></div>
<p style="position:absolute;left:56px;bottom:52px;font-size:18px;font-weight:500;color:#284A98">Financial forecasting for startups</p>
<div class=card style="left:560px;top:122px;width:800px"><img src="{shot}"></div>"""
    else:
        b=f"""<div style="position:absolute;right:-160px;top:-200px;width:700px;height:700px;border-radius:50%;background:#8FA89B;opacity:.55"></div>
<img src="{lockN}" style="position:absolute;left:64px;top:64px;height:40px">
<h1 style="position:absolute;left:64px;top:190px;width:820px;font-size:76px;color:#292744">Programınız için<br>tek finansal model.</h1>
<div style="position:absolute;left:64px;top:390px;width:96px;height:10px;border-radius:5px;background:#2EC4B6"></div>
<div class=card style="left:64px;top:500px;width:1120px"><img src="{shot}"></div>"""
    return page(w,h,"#E8EFEA",b)
def B(w,h):
    if w>h:
        b=f"""<img src="{lockW}" style="position:absolute;left:56px;top:54px;height:30px">
<h1 style="position:absolute;left:56px;top:170px;width:470px;font-size:58px;color:#fff">Programınız için <span style="color:#2EC4B6">tek finansal model.</span></h1>
<p style="position:absolute;left:56px;bottom:52px;font-size:18px;font-weight:500;color:#E8EFEA">Financial forecasting for startups</p>
<div style="position:absolute;left:530px;top:82px;width:820px;height:600px;border-radius:28px;background:#292744"></div>
<div class=card style="left:570px;top:122px;width:800px"><img src="{shot}"></div>"""
    else:
        b=f"""<img src="{lockW}" style="position:absolute;left:64px;top:64px;height:40px">
<h1 style="position:absolute;left:64px;top:190px;width:860px;font-size:76px;color:#fff">Programınız için<br><span style="color:#2EC4B6">tek finansal model.</span></h1>
<div style="position:absolute;left:24px;top:460px;width:1100px;height:700px;border-radius:32px;background:#292744"></div>
<div class=card style="left:64px;top:500px;width:1120px"><img src="{shot}"></div>"""
    return page(w,h,"#284A98",b)
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch()
        for n,fn,w,h in [("A-adacayi-1200x627.png",A,1200,627),("A-adacayi-1080x1080.png",A,1080,1080),("B-kobalt-1200x627.png",B,1200,627),("B-kobalt-1080x1080.png",B,1080,1080)]:
            pg=await br.new_page(viewport={"width":w,"height":h})
            f=OUT/("_"+n+".html"); f.write_text(fn(w,h),encoding="utf-8"); await pg.goto(f.as_uri()); await pg.wait_for_timeout(500)
            await pg.screenshot(path=str(OUT/("linkedin-reklam-"+n))); f.unlink(); await pg.close()
        await br.close()
asyncio.run(main())
