import sys, asyncio, html
from pathlib import Path
from playwright.async_api import async_playwright
LOGO = Path(sys.argv[1]); OUT = Path(sys.argv[2])
NAVY="#292744"; LAV="#AAA8D3"; OFF="#FAF9F7"; FIN="#4B4A8F"
ico_navy=(LOGO/"ikon/svg/f4cast-ikon-lacivert.svg").as_uri()
ico_rev=(LOGO/"ikon/svg/f4cast-ikon-ters.svg").as_uri()
fin_rev=(LOGO/"moduller/financials/svg/f4cast-financials-yatay-ters.svg").as_uri()
BASE="""<html><head><style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:%dpx;height:%dpx;font-family:Inter;background:%s;color:%s;position:relative;overflow:hidden;font-feature-settings:'tnum'}
.pad{position:absolute;inset:%dpx}
h1{font-weight:600;letter-spacing:.02em;line-height:1.15}
p{font-weight:400;line-height:1.4}
.rule{width:96px;height:8px;background:%s;border-radius:4px}
.lab{font-weight:500;letter-spacing:.04em;text-transform:none}
</style></head><body>%s</body></html>"""
def page(w,h,bg,fg,pad,acc,body): return BASE%(w,h,bg,fg,pad,acc,body)

def li_quote(lines_h, sub, foot):
    b=f"""<div class=pad style="display:flex;flex-direction:column;justify-content:center;gap:56px">
<div class=rule></div><h1 style="font-size:74px">{lines_h}</h1>
<p style="font-size:38px;color:#55536f">{sub}</p></div>
<div style="position:absolute;left:96px;bottom:84px;font-size:30px;color:#55536f" class=lab>{foot}</div>"""
    return page(1080,1350,OFF,NAVY,96,LAV,b)

def li_list(title, items, foot):
    li="".join(f"""<div style="display:flex;gap:36px;align-items:flex-start"><div style="flex:none;width:72px;height:72px;border-radius:18px;background:{NAVY};color:{OFF};font-size:38px;font-weight:600;display:flex;align-items:center;justify-content:center">{i+1}</div><p style="font-size:40px;padding-top:6px">{t}</p></div>""" for i,t in enumerate(items))
    b=f"""<div class=pad style="display:flex;flex-direction:column;justify-content:center;gap:64px">
<div class=rule></div><h1 style="font-size:68px">{title}</h1><div style="display:flex;flex-direction:column;gap:44px">{li}</div></div>
<div style="position:absolute;left:96px;bottom:84px;font-size:30px;color:#55536f" class=lab>{foot}</div>"""
    return page(1080,1350,OFF,NAVY,96,LAV,b)

def ig_card(n,total,head,body,dark=False,last=False):
    bg,fg=(NAVY,OFF) if dark else (OFF,NAVY)
    ico=ico_rev if dark else ico_navy
    sub="#c9c7e6" if dark else "#55536f"
    extra=""
    if last:
        extra=f"""<p style="font-size:34px;color:{LAV if dark else FIN};font-weight:500;margin-top:8px">Financial forecasting for startups</p>"""
    b=f"""<div class=pad style="display:flex;flex-direction:column;justify-content:center;gap:52px">
<div class=rule></div><h1 style="font-size:{86 if n==1 else 70}px">{head}</h1>{f'<p style="font-size:42px;color:{sub}">{body}</p>' if body else ''}{extra}</div>
{"" if last else f'<img src="{ico}" style="position:absolute;left:96px;bottom:80px;width:96px;height:96px">'}
<div style="position:absolute;right:96px;bottom:108px;font-size:30px;color:{sub}" class=lab>{n} / {total}</div>"""
    return page(1080,1350,bg,fg,96,LAV,b)

def story(head, body, cta, icon=True):
    icotag=f'<img src="{ico_rev}" style="position:absolute;left:96px;top:250px;width:160px;height:160px">' if icon else ""
    b=f"""{icotag}
<div class=pad style="display:flex;flex-direction:column;justify-content:center;gap:56px;top:420px;bottom:420px">
<div class=rule></div><h1 style="font-size:92px">{head}</h1><p style="font-size:46px;color:#c9c7e6">{body}</p></div>
<div style="position:absolute;left:96px;right:96px;bottom:300px;font-size:40px;font-weight:500;color:{OFF};border:2px solid {LAV};border-radius:24px;padding:28px 36px" class=lab>{cta}</div>
<p style="position:absolute;left:96px;bottom:220px;font-size:30px;color:{LAV};font-weight:500">Financial forecasting for startups</p>"""
    return page(1080,1920,NAVY,OFF,96,LAV,b)

def reel_end():
    b=f"""<img src="{ico_rev}" style="position:absolute;left:50%;top:560px;width:240px;height:240px;transform:translateX(-50%)">
<div style="position:absolute;left:96px;right:96px;top:900px;text-align:center">
<h1 style="font-size:72px">Hesabını oluştur,<br>onaydan sonra<br>kullanmaya başla.</h1>
<p style="font-size:42px;color:{LAV};margin-top:48px;font-weight:500">Bağlantı profilde</p></div>
<p style="position:absolute;left:0;right:0;bottom:300px;text-align:center;font-size:34px;color:#c9c7e6;font-weight:500">Financial forecasting for startups</p>"""
    return page(1080,1920,NAVY,OFF,96,LAV,b)

def reel_frame():
    # background + header for letterboxed video (video area 1080x608 at y=656)
    b=f"""<div style="position:absolute;left:96px;right:96px;top:330px">
<h1 style="font-size:64px">Geliştirme döneminden<br>5. yıl sonuna kadar<br>tek finansal model</h1></div>
<img src="{ico_rev}" style="position:absolute;left:96px;bottom:300px;width:120px;height:120px">
<p style="position:absolute;left:250px;bottom:338px;font-size:34px;color:{LAV};font-weight:500">Financial forecasting for startups</p>"""
    return page(1080,1920,NAVY,OFF,96,LAV,b)

FINLOCK=f'<img src="{fin_rev}" style="width:100%;height:auto;display:block">'
jobs={
 "01-linkedin-kisisel-09kas.png":li_quote("Geliştirme dönemi ayrı planlanmazsa, nakit ihtiyacı olduğundan küçük görünür.","Satışa başlamadan önce ne kadar nakit gerekiyor? Bu soru, ilk yılın içinde kaybolmamalı.","Mehmet Alpatlı · finansal planlama notları"),
 "03-linkedin-kisisel-13kas.png":li_list("AGY-112 Bölüm 4.4 tablolarında en sık gördüğüm 3 tutarsızlık",["Satış adedi × birim fiyat, satış gelirini tutmuyor.","Personel planındaki kişiler gider tablosunda maaş olarak yok.","Yatırım harcaması nakit akışında aynı yılda çıkış olarak görünmüyor."],"Mehmet Alpatlı · finansal planlama notları"),
 "04-instagram-story-11kas.png":story(FINLOCK+"<span style='display:block;margin-top:40px'>yayında</span>","Geliştirme döneminden 5. yıl sonuna kadar finansal projeksiyon, tek modelde.","Hesabını oluştur, onaydan sonra kullanmaya başla · Bağlantı profilde", icon=False),
 "06-instagram-story-12kas.png":story("Yıl 0 nedir?","Finansal planın en çok atlanan dönemini yeni gönderide anlattık.","Profildeki son gönderiye bak"),
 "07-reel-bitis-karti.png":reel_end(),
 "07-reel-zemin.png":reel_frame(),
}
cards=[("Yıl 0 nedir?","Finansal planın en çok atlanan dönemi.",True),
("Çoğu girişim, ilk satıştan önce aylarca ürün geliştirir.","",False),
("Bu aylarda gelir yoktur.","Ama personel, yazılım, prototip ve kira giderleri vardır.",False),
("Bu döneme geliştirme dönemi ya da Yıl 0 denir.","Süresi 1 ay da olabilir, 18 ay da.",False),
("Yıl 0'ı ayrı planlarsan,","satışa başlamadan önce ne kadar nakde ihtiyacın olduğunu görürsün.",False),
(FINLOCK,"Yıl 0 ve 5 faaliyet yılı tek modelde. Hesabını oluştur, onaydan sonra kullanmaya başla: bağlantı profilde.",True)]
for i,(h,bd,dk) in enumerate(cards,1):
    jobs[f"05-instagram-karusel-12kas-{i}.png"]=ig_card(i,6,h,bd,dark=dk,last=(i==6))
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch()
        for name,doc in jobs.items():
            w,h=(1080,1920) if ("story" in name or "reel" in name) else (1080,1350)
            pg=await br.new_page(viewport={"width":w,"height":h})
            f=OUT/("_"+name+".html"); f.write_text(doc,encoding="utf-8")
            await pg.goto(f.as_uri()); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(OUT/name)); await pg.close(); f.unlink()
        await br.close()
asyncio.run(main())
