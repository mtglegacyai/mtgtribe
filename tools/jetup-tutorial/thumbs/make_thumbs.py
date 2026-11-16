# Series thumbnails for MTG's JetUP step-by-step videos (1080 x 1920, also used as the website poster).
# The official JetUP logo sits in the gold ring, not MTG's photo (MTG, 8 Nov 2026).
# Safe areas for the website phone card: camera island top centre, play button in the centre, duration tag bottom left.
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PARTS = {
    1: dict(title='Create your<br><span class="hl">JetUP</span> account', scr='scr1.jpg', badge='Account Type: Partner',
            steps=['Sign up as Individual', 'Verify your email', 'Log in']),
    2: dict(title='Link JetUP to<br><span class="hl">TAG Markets</span>', scr='scr2.jpg', badge='User Active',
            steps=['Register CopyX', 'Sync your account', 'Confirm your email']),
    3: dict(title='Verify your<br><span class="hl">identity (KYC)</span>', scr='scr3.jpg', badge='Sumsub ID created',
            steps=['Upload documents', 'Scan your ID', 'Take a selfie']),
}
CSS = r"""
@font-face{font-family:'Anton';src:url(Anton-Regular.ttf)}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:#07050f}
body{font-family:'Manrope',system-ui,sans-serif;color:#fff;position:relative}
.bg{position:absolute;inset:0;background:
  radial-gradient(900px 700px at 85% 58%,rgba(124,58,237,.42),transparent 70%),
  radial-gradient(700px 600px at 8% 18%,rgba(196,255,61,.16),transparent 70%),
  radial-gradient(800px 700px at 20% 92%,rgba(232,194,90,.20),transparent 70%),
  linear-gradient(170deg,#120a26 0%,#0a0716 55%,#07050f 100%)}
.grid{position:absolute;inset:0;opacity:.10;background-image:linear-gradient(rgba(255,255,255,.5) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.5) 1px,transparent 1px);background-size:72px 72px;
  -webkit-mask-image:radial-gradient(900px 900px at 50% 45%,#000 30%,transparent 80%)}
.top{position:absolute;left:70px;right:70px;top:178px}
.pill{display:inline-flex;align-items:center;gap:14px;height:62px;padding:0 30px;border-radius:999px;background:#c4ff3d;color:#14110b;font:800 27px/1 'Manrope';letter-spacing:.14em}
.pill img{width:34px;height:34px;border-radius:8px}
.part{margin-top:22px;font:400 250px/0.9 'Anton';letter-spacing:.01em;background:linear-gradient(180deg,#fff3c4 0%,#f3d27a 38%,#c99a2e 100%);-webkit-background-clip:text;background-clip:text;color:transparent;
  filter:drop-shadow(0 10px 30px rgba(232,194,90,.35))}
.title{margin-top:14px;font:800 92px/1.04 'Manrope';letter-spacing:-.015em;text-shadow:0 6px 30px rgba(0,0,0,.5)}
.title .hl{color:#c4ff3d}
.phone{position:absolute;left:545px;top:735px;width:470px;height:880px;border-radius:64px;padding:10px;transform:rotate(7deg);
  background:linear-gradient(135deg,#f6e3a1,#b8862b 35%,#fbe7a8 55%,#9c6f1f 80%,#e9c76d);box-shadow:0 40px 90px rgba(0,0,0,.65),0 0 60px rgba(232,194,90,.25)}
.phone .in{position:relative;width:100%;height:100%;border-radius:55px;background:#000;padding:12px;overflow:hidden}
.phone img{width:100%;height:100%;object-fit:cover;object-position:top;border-radius:44px;display:block}
.phone .isl{position:absolute;left:50%;top:22px;width:120px;height:32px;margin-left:-60px;border-radius:999px;background:#000}
.badge{position:absolute;left:70px;top:1540px;display:flex;align-items:center;gap:14px;padding:20px 30px;border-radius:22px;background:rgba(14,10,26,.92);
  box-shadow:0 0 0 3px #c4ff3d,0 18px 50px rgba(0,0,0,.6);font:800 40px/1 'Manrope';transform:rotate(-3deg)}
.badge i{display:grid;place-items:center;width:52px;height:52px;border-radius:50%;background:#c4ff3d;color:#14110b;font:900 34px/1 'Manrope';font-style:normal}
.logo{position:absolute;left:46px;top:1015px;width:476px;height:476px;border-radius:50%;padding:12px;
  background:conic-gradient(from 210deg,#fff1b8,#c99a2e,#f7dd8d,#9c6f1f,#fff1b8);box-shadow:0 0 70px rgba(232,194,90,.45),0 30px 70px rgba(0,0,0,.55)}
.logo .disc{width:100%;height:100%;border-radius:50%;display:grid;place-items:center;border:6px solid #0b0716;
  background:radial-gradient(circle at 50% 38%,#3a1d6e 0%,#1a0f36 52%,#0b0716 100%)}
.logo img{width:68%;margin-top:-6px;filter:drop-shadow(0 0 34px rgba(214,120,255,.55)) drop-shadow(0 10px 20px rgba(0,0,0,.5))}
.steps{position:absolute;left:70px;top:1420px;width:420px;display:flex;flex-direction:column;gap:16px}
.steps div{display:flex;align-items:center;gap:16px;font:800 34px/1.1 'Manrope';color:#efeaff}
.steps b{display:grid;place-items:center;flex:0 0 auto;width:54px;height:54px;border-radius:16px;background:linear-gradient(135deg,#7c3aed,#c026d3);font:800 30px/1 'Manrope'}
.brand{position:absolute;left:0;right:0;bottom:205px;text-align:center;font:800 30px/1 'Manrope';letter-spacing:.16em;color:#e8c25a}
.brand span{color:#fff}.brand em{font-style:normal;font-family:'Noto Color Emoji'}
"""
def html(n, p):
    steps = ''.join(f'<div><b>{i + 1}</b>{s}</div>' for i, s in enumerate(p['steps']))
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@600;700;800&display=block" rel="stylesheet">
<style>{CSS}</style></head><body><div class="bg"></div><div class="grid"></div>
<div class="top"><span class="pill"><img src="jetup-mark.png" alt="">JETUP STEP BY STEP</span>
<div class="part">PART {n}</div><div class="title">{p['title']}</div></div>
<div class="phone"><div class="in"><img src="{p['scr']}" alt=""><span class="isl"></span></div></div>
<div class="logo"><div class="disc"><img src="jetup-logo.webp" alt="JetUP"></div></div>
<div class="badge"><i>&#10003;</i>{p['badge']}</div>
<div class="brand">MTG <em>&#128081;</em> <span>|</span> YOUR DIGITAL ARCHITECT</div>
</body></html>"""
for n, p in PARTS.items():
    open(os.path.join(HERE, f'thumb_p{n}.html'), 'w').write(html(n, p))
print('html written')
