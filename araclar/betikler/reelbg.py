import sys, asyncio
from pathlib import Path
from playwright.async_api import async_playwright
LOGO=Path(sys.argv[1]); OUT=Path(sys.argv[2])
ico=(LOGO/"ikon/svg/f4cast-ikon-ters.svg").as_uri()
def doc(tag,title):
    return f"""<html><head><style>*{{margin:0;padding:0;box-sizing:border-box}}body{{width:1080px;height:1920px;background:#292744;color:#FAF9F7;font-family:Inter;position:relative}}</style></head><body>
<div style="position:absolute;left:96px;right:96px;top:300px">
<div style="width:96px;height:8px;background:#AAA8D3;border-radius:4px;margin-bottom:40px"></div>
<p style="font-size:34px;font-weight:500;color:#AAA8D3;letter-spacing:.04em;margin-bottom:24px">{tag}</p>
<h1 style="font-size:64px;font-weight:600;letter-spacing:.02em;line-height:1.15">{title}</h1></div>
<img src="{ico}" style="position:absolute;left:96px;bottom:300px;width:120px;height:120px">
<p style="position:absolute;left:250px;bottom:338px;font-size:34px;color:#AAA8D3;font-weight:500">Financial forecasting for startups</p></body></html>"""
jobs={"bg1.png":doc("Başa baş serisi · 1 / 3","AGY-112 Bölüm 4.4:<br>formun kısıtları"),
"bg2.png":doc("Başa baş serisi · 2 / 3","Çok ürünlü bir işi<br>forma sığdırmak"),
"bg3.png":doc("Başa baş serisi · 3 / 3","Uygulayıcı kuruluşlar<br>için tek model")}
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={"width":1080,"height":1920})
        for n,d in jobs.items():
            f=OUT/("_"+n+".html"); f.write_text(d,encoding="utf-8"); await pg.goto(f.as_uri()); await pg.wait_for_timeout(200)
            await pg.screenshot(path=str(OUT/n)); f.unlink()
        await b.close()
asyncio.run(main())
