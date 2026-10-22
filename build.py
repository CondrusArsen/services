"""Builds index.html from ../portfolio-bot/catalog.json so the site, the bot and the
gig texts always show the same services, scope and prices.  Run: python build.py"""
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CAT = json.loads((HERE.parent / "portfolio-bot" / "catalog.json").read_text(encoding="utf-8"))
COVERS = {"lumen": "img/game.jpg", "cowork": "img/cowork.jpg", "coffee": "img/promo.jpg", "playable": "img/playable.jpg"}
BOT = "https://t.me/arseni_games_bot"
e = html.escape


def rub(n):
    return f"{n:,}".replace(",", " ") + " ₽"


cases = "\n".join(f"""
    <a class="case" href="{e(c['url'])}">
      {f'<img src="{COVERS[c["id"]]}" alt="" loading="lazy">' if c['id'] in COVERS else '<div class="case-bot"><span>@arseni_games_bot</span></div>'}
      <div class="case-body"><h3>{e(c['title'])}</h3><p>{e(c['summary'])}</p><small>{e(c['status'])}</small></div>
    </a>""" for c in CAT["cases"])

case_url = {c["id"]: c["url"] for c in CAT["cases"]}
services = "\n".join(f"""
    <article class="svc">
      <div class="svc-head"><h3>{e(s['title'])}</h3><div class="price">от {rub(s['price'])}<span>{e(s['days'])}</span></div></div>
      <p class="result">{e(s['result'])}</p>
      <ul>{''.join(f'<li>{e(i)}</li>' for i in s['includes'])}</ul>
      <p class="ex"><b>Не входит:</b> {e(s['excludes'])}</p>
      <div class="svc-foot"><a class="btn" href="{BOT}">Обсудить задачу</a>{f'<a class="link" href="{e(case_url[s["case_id"]])}">Пример →</a>' if s.get('case_id') in case_url else ''}</div>
    </article>""" for s in CAT["services"])

page = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Арсений Атрохов — игровые интерфейсы, промо-игры и playable</title>
<meta name="description" content="Интерфейсы игр и приложений, промо-игры для брендов, HTML5 playable-реклама, сайты с интерактивным сценарием и Telegram-боты. Понятный объём и цена до старта.">
<meta property="og:title" content="Арсений Атрохов — игровые интерфейсы, промо-игры и playable">
<meta property="og:image" content="https://condrusarsen.github.io/services/img/game.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{{--bg:#0b1020;--surface:#121a33;--surface2:#18223f;--line:#24305a;--ink:#eef2ff;--mute:#9aa6cf;--acc:#2ee6c9;--gold:#ffd166}}
*{{box-sizing:border-box}}
body{{margin:0;background:radial-gradient(80% 50% at 80% 0%,#1b2c63 0%,var(--bg) 60%);background-color:var(--bg);color:var(--ink);font:16px/1.6 Inter,system-ui,sans-serif}}
a{{color:inherit}}
.wrap{{max-width:1160px;margin:0 auto;padding:0 20px}}
nav{{display:flex;justify-content:space-between;align-items:center;height:72px}}
nav b{{font-weight:800;letter-spacing:-.01em}}
nav .links{{display:flex;gap:24px;color:var(--mute);font-weight:600;font-size:15px}}
nav .links a{{text-decoration:none}}
@media (max-width:720px){{nav .links{{display:none}}}}
.btn{{display:inline-flex;align-items:center;justify-content:center;height:48px;padding:0 20px;border-radius:14px;background:var(--acc);color:#03332c;font-weight:800;text-decoration:none;white-space:nowrap}}
.btn.ghost{{background:transparent;color:var(--ink);border:1.5px solid var(--line)}}
header.hero{{padding:56px 0 24px;max-width:820px}}
.eyebrow{{display:inline-block;font-weight:700;font-size:14px;color:var(--gold);background:rgba(255,209,102,.1);border-radius:999px;padding:5px 12px}}
h1{{font-size:clamp(36px,5.6vw,62px);line-height:1.04;letter-spacing:-.03em;margin:18px 0 16px;font-weight:800}}
.lead{{color:var(--mute);font-size:clamp(17px,2vw,20px);margin:0 0 26px}}
.cta-row{{display:flex;gap:10px;flex-wrap:wrap}}
h2{{font-size:clamp(26px,3.6vw,36px);letter-spacing:-.02em;margin:72px 0 8px;font-weight:800}}
.sub{{color:var(--mute);margin:0 0 24px;max-width:720px}}
.cases{{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:18px}}
.case{{display:flex;flex-direction:column;background:var(--surface);border:1px solid var(--line);border-radius:22px;overflow:hidden;text-decoration:none;transition:transform .25s,border-color .25s}}
.case:hover{{transform:translateY(-4px);border-color:#3a4a85}}
.case img{{width:100%;aspect-ratio:16/10;object-fit:cover;display:block}}
.case-bot{{aspect-ratio:16/10;display:grid;place-items:center;background:linear-gradient(135deg,#229ed9,#1b4880)}}
.case-bot span{{font-weight:800;font-size:24px;background:rgba(0,0,0,.25);padding:10px 18px;border-radius:14px}}
.case-body{{padding:18px 20px 20px}}
.case-body h3{{margin:0 0 6px;font-size:19px}}
.case-body p{{margin:0 0 10px;color:var(--mute);font-size:15px}}
.case-body small{{display:block;color:#7180b3;font-size:12.5px;line-height:1.45}}
.svcs{{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:16px}}
.svc{{background:var(--surface);border:1px solid var(--line);border-radius:22px;padding:22px;display:flex;flex-direction:column}}
.svc-head{{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}}
.svc h3{{margin:0;font-size:19px;line-height:1.25}}
.price{{text-align:right;font-weight:800;font-size:20px;color:var(--acc);white-space:nowrap}}
.price span{{display:block;font-weight:600;font-size:12.5px;color:var(--mute)}}
.result{{margin:12px 0 10px}}
.svc ul{{margin:0 0 12px;padding-left:18px;color:var(--mute);font-size:15px}}
.ex{{font-size:13px;color:#7f8dbd;background:var(--surface2);border-radius:12px;padding:10px 12px;margin:0 0 16px}}
.ex b{{color:var(--mute)}}
.svc-foot{{margin-top:auto;display:flex;gap:14px;align-items:center}}
.link{{font-weight:700;color:var(--mute);text-decoration:none}}
.link:hover{{color:var(--ink)}}
.note{{color:var(--mute);font-size:14px;margin-top:14px}}
.steps{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;counter-reset:s}}
.step{{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:18px}}
.step::before{{counter-increment:s;content:counter(s);display:inline-grid;place-items:center;width:30px;height:30px;border-radius:50%;background:var(--gold);color:#3a2600;font-weight:800;margin-bottom:8px}}
.step b{{display:block}}
.step p{{margin:4px 0 0;color:var(--mute);font-size:15px}}
.about{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
@media (max-width:820px){{.about{{grid-template-columns:1fr}}}}
.box{{background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:22px}}
.box p{{margin:6px 0;color:var(--mute)}}
.final{{margin:72px 0 24px;background:linear-gradient(135deg,#123461,#0d4a5a);border:1px solid var(--line);border-radius:26px;padding:32px}}
.final h2{{margin:0 0 8px}}
footer{{padding:28px 0 48px;color:#7180b3;font-size:14px}}
</style>
</head>
<body>
<div class="wrap">
  <nav><b>Арсений Атрохов</b><div class="links"><a href="#cases">Кейсы</a><a href="#services">Услуги</a><a href="#process">Как работаю</a></div><a class="btn" href="{BOT}">Написать</a></nav>

  <header class="hero">
    <span class="eyebrow">Геймдизайн · UI/UX · HTML5 · с ИИ-агентами</span>
    <h1>Игровые интерфейсы, промо-игры и playable — с понятным объёмом и ценой до старта</h1>
    <p class="lead">Проектирую и собираю интерактивные прототипы: заказчик сразу пробует решение на своём телефоне, а не смотрит на статичные картинки. Код пишут ИИ-агенты, сценарии, решения и проверку каждой сборки делаю я.</p>
    <div class="cta-row"><a class="btn" href="{BOT}">Обсудить задачу в Telegram</a><a class="btn ghost" href="#cases">Смотреть кейсы</a></div>
  </header>

  <h2 id="cases">Кейсы</h2>
  <p class="sub">Самостоятельные концепты, сделанные с ИИ. Это не клиентские релизы: коммерческие показатели не заявляю. Каждый можно открыть и пройти.</p>
  <div class="cases">{cases}
  </div>

  <h2 id="services">Услуги и стартовые цены</h2>
  <p class="sub">Цена указана за описанный объём. Всё, что не входит, видно заранее и оценивается отдельно.</p>
  <div class="svcs">{services}
  </div>
  <p class="note">{e(CAT['price_note'])}</p>

  <h2 id="process">Как работаю</h2>
  <div class="steps">
    <div class="step"><b>ТЗ и оценка</b><p>Задаю вопросы, фиксирую объём, срок, цену и что не входит.</p></div>
    <div class="step"><b>Первая версия</b><p>Присылаю ссылку на рабочую версию, её можно открыть на телефоне.</p></div>
    <div class="step"><b>Правки</b><p>Один согласованный раунд правок входит в цену.</p></div>
    <div class="step"><b>Передача</b><p>Исходники, инструкция и размещение демо.</p></div>
  </div>

  <h2>Обо мне</h2>
  <div class="about">
    <div class="box"><b>Опыт</b><p>4 месяца в игровой студии (2026): разборы игр, экономика live-игры, плейтесты, релизный QA.</p><p>600+ разборов игр, 6+ лет в Roblox Studio (Luau), математик по образованию.</p></div>
    <div class="box"><b>Условия</b><p>Удалённо из Беларуси (UTC+3), общение на русском, английский — переписка.</p><p>Способ оплаты и документы согласуем до начала работы.</p></div>
  </div>

  <section class="final">
    <h2>Есть задача?</h2>
    <p class="lead" style="margin-bottom:18px">Опишите её в боте: он соберёт заявку за 4 шага, а я отвечу лично.</p>
    <div class="cta-row"><a class="btn" href="{BOT}">Открыть @arseni_games_bot</a><a class="btn ghost" href="https://github.com/CondrusArsen">GitHub</a><a class="btn ghost" href="https://www.linkedin.com/in/arseni-atrokhov/">LinkedIn</a></div>
  </section>
  <footer>© 2026 Арсений Атрохов · Сайт собирается из того же каталога, что и бот: цены и объёмы везде одинаковые.</footer>
</div>
</body>
</html>
"""
(HERE / "index.html").write_text(page, encoding="utf-8")
print("built index.html:", len(CAT["services"]), "services,", len(CAT["cases"]), "cases")
