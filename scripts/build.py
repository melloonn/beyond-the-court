#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render a portable multipage basketball publication from structured data."""
import datetime as dt
import argparse
from html import escape
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
DATA = ROOT / 'src/data'
TEAM = json.loads((DATA / 'teams/golden-state-warriors.json').read_text())
PLAYERS = {p['id']: p for p in [json.loads(f.read_text()) for f in (DATA / 'players').glob('*.json')]}
GAMES = {p['id']: p for p in [json.loads(f.read_text()) for f in (DATA / 'games').glob('*.json')]}
STORIES = json.loads((DATA / 'stories.json').read_text())
E = lambda x: escape(str(x if x is not None else ''), quote=True)
ZH = {'3975': '史蒂芬・柯瑞', '5175737': '亞克塞爾・倫德伯格', '6589': '卓雷蒙・格林',
      '6430': '吉米・巴特勒', '4709138': '布蘭丁・波傑姆斯基', '4432171': '摩西・穆迪',
      '3134903': '蓋瑞・裴頓二世', '3213': '艾爾・霍福德', '3102531': '克里斯塔普斯・波爾辛吉斯',
      '4066436': '迪安東尼・梅爾頓', '4997536': '桂・桑托斯', '4897262': '威爾・理查德',
      '2990969': '喬治・尼昂', '4397886': '查爾斯・貝西', '4397040': '布蘭登・威廉斯',
      '4433149': 'LJ・克萊爾', '4897449': '馬勒維・里昂斯', '4703396': '葛拉罕・艾克'}
GLOSSARY = {'GP': '出賽場次', 'GS': '先發場次', 'MIN': '上場時間（平均模式為每場）', 'PTS': '得分', 'REB': '總籃板',
            'AST': '助攻', 'STL': '抄截', 'BLK': '阻攻', 'TO': '失誤', 'PF': '犯規', 'FG': '投籃命中－出手',
            'FG%': '投籃命中率', '3PT': '三分命中－出手', '3P%': '三分命中率', 'FT': '罰球命中－出手',
            'FT%': '罰球命中率', 'OR': '進攻籃板', 'DR': '防守籃板', 'OREB': '進攻籃板', 'DREB': '防守籃板', '+/-': '正負值'}
TZ = dt.timezone(dt.timedelta(hours=8))


def local_time(value, full=False):
    d = dt.datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(TZ)
    return d.strftime('%Y.%m.%d %H:%M' if full else '%m.%d')


def avg_category(p, kind='regular'):
    return next((c for c in p[kind] if c['name'] == 'averages'), {})


def current(p):
    c = avg_category(p)
    rows = [r for r in c.get('rows', []) if r['year'] == TEAM['seasonYear'] and r.get('teamId') == TEAM['id']]
    return dict(zip(c.get('labels', []), rows[-1]['values'])) if rows else {}


def metric(p, key):
    return current(p).get(key, '—')


def player_href(p, base):
    return base + 'players/' + p['slug'] + '.html'


def source_list(sources):
    return '<ul class="source-list">' + ''.join('<li><span>' + E(s['publisher']) + '</span><a href="' + E(s['url']) + '" target="_blank" rel="noopener noreferrer">' + E(s['title']) + ' ↗</a></li>' for s in sources) + '</ul>'


def stat_value(value, label, row=None):
    if value in [None, '', '--', 'N/A', '—']:
        return '—'
    pair = {'FG%': 'FG', '3P%': '3PT', 'FT%': 'FT'}.get(label)
    if pair and row and pair in row:
        shot = str(row[pair]).split('-')
        if len(shot) == 2 and float(shot[1]) == 0:
            return '—'
    return E(value) + ('<span class="pct">%</span>' if label.endswith('%') else '')


def block_title(kicker, title, aside=''):
    return f'<div class="section-heading"><div><span class="eyebrow">{kicker}</span><h2>{title}</h2></div>{aside}</div>'


def page(path, title, body, active='team', description='金州勇士全隊球員、生涯數據與場外故事。每一份數據與人物內容都附上來源。'):
    depth = len(Path(path).parts) - 1
    base = '../' * depth
    nav = ''.join('<a ' + ('aria-current="page"' if active == key else '') + f' href="{base}{link}">{label}</a>' for key, link, label in [
        ('team', 'index.html', '球隊總覽'), ('roster', 'index.html#roster', '球員圖鑑'),
        ('games', 'games.html', '比賽紀錄'), ('stories', 'stories.html', '場外故事')])
    html = f'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#102a43"><title>{E(title)}｜Beyond the Court</title><meta name="description" content="{E(description)}">
<meta property="og:title" content="{E(title)}｜Beyond the Court"><meta property="og:description" content="{E(description)}"><meta property="og:type" content="website">
<link rel="icon" type="image/svg+xml" href="{base}assets/favicon.svg"><link rel="stylesheet" href="{base}assets/style.css">
<script src="{base}assets/utils.js" defer></script><script src="{base}assets/main.js" defer></script><noscript><style>[data-career-view][hidden]{{display:block!important}}.career-controls,#download-csv,.roster-toolbar,.roster-meta,.story-filters{{display:none!important}}</style></noscript></head>
<body><a class="skip" href="#main">跳至主要內容</a>
<div class="topline"><div class="wrap"><span>INDEPENDENT BASKETBALL JOURNAL</span><span>VOL. 01 <b>·</b> GOLDEN STATE</span></div></div>
<header class="site-header"><div class="wrap header-inner"><a class="brand" href="{base}index.html" aria-label="Beyond the Court 首頁"><span class="brand-icon">b<span>c</span></span><span>BEYOND<span class="brand-small">THE COURT <i>場上場下</i></span></span></a>
<button class="menu-toggle" aria-label="展開導覽" aria-expanded="false" aria-controls="navigation">選單 <span>☰</span></button>
<nav id="navigation" aria-label="主要導覽">{nav}</nav><a class="header-season" href="{base}sources.html"><span class="status-dot"></span>2026—27 <span class="small-arrow">↗</span></a></div></header>
<main id="main">{body}</main>
<footer class="site-footer"><div class="wrap"><div class="footer-top"><div><a class="footer-logo" href="{base}index.html">BEYOND THE COURT<span>每個數字背後，都有一個人。</span></a></div><div class="footer-links"><a href="{base}sources.html">資料來源與更新</a><a href="{base}about.html">關於專案</a><a href="{base}AGENTS.md">AGENTS.md ↗</a></div></div><div class="footer-bottom"><p>非官方球迷／課堂專案 · 與 NBA、球隊及球員無隸屬關係。</p><p>統計快照 {local_time(TEAM['retrievedAt'], True)}（台北）· 非即時比分</p></div></div></footer>
</body></html>'''
    target = OUT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html)


def player_card(p, base=''):
    stats = current(p)
    mins = float(stats.get('MIN', 0))
    active = bool(stats)
    return f'''<article class="player-card" data-player data-name="{E(p['name'] + ' ' + ZH.get(p['id'], '') + ' ' + str(p['number']))}" data-position="{E(p['position'])}" data-active="{str(active).lower()}" data-points="{E(stats.get('PTS', -1))}" data-minutes="{mins}" data-number="{E(p['number'])}">
<a class="player-link" href="{player_href(p, base)}"><div class="player-portrait"><span class="jersey-bg">{E(p['number'])}</span><span class="position-label">{E(p['position'])}</span><img src="{base}{E(p['headshot'])}" alt="{E(p['name'])}" loading="lazy" width="600" height="436"><span class="card-arrow" aria-hidden="true">↗</span></div>
<div class="player-card-body"><div class="player-number">#{E(p['number'])} <span>GOLDEN STATE WARRIORS</span></div><h3>{E(p['name'])}</h3><p class="player-zh">{E(ZH.get(p['id'], ''))}</p>
<div class="mini-stats">{''.join(f'<div><b>{E(stats.get(k, "—"))}</b><span>{k}</span></div>' for k in ['PTS', 'REB', 'AST'])}</div>
<div class="card-foot"><span>{E(stats.get('GP', '0'))} 場出賽</span><span>{'查看完整生涯 →' if active else '本季尚無出賽紀錄 →'}</span></div></div></a></article>'''


def story_card(s, base='', large=False):
    p = PLAYERS[s['playerIds'][0]]
    return f'''<article class="story-card {"story-large" if large else ""}" data-story data-category="{E(s['category'])}"><a href="{base}stories/{E(s['id'])}.html"><div class="story-art art-{E(s['category'])}"><span class="story-art-word">{ {'公益':'GIVE BACK.','家庭':'FOR FAMILY.','興趣':'OFF DUTY.','品牌':'NEXT CHAPTER.','影音':'ON THE MIC.','成長':'THE JOURNEY.'}[s['category']] }</span><img src="{base}{p['headshot']}" alt="{E(p['name'])}" loading="lazy" width="600" height="436"><span class="story-category">{E(s['category'])}</span></div><div class="story-body"><div class="story-byline">{E(p['name'])}<span>人物選讀</span></div><h3>{E(s['title'])}</h3><p>{E(s['summary'])}</p><span class="text-link">閱讀故事 <span>↗</span></span></div></a></article>'''


def game_card(g, base=''):
    own = next(t for t in g['teams'] if t['id'] == TEAM['id'])
    opp = next(t for t in g['teams'] if t['id'] != TEAM['id'])
    return f'''<a class="game-card" href="{base}games/{g['id']}.html"><div class="game-card-top"><span>{local_time(g['date'])} <span class="muted">台北</span></span><span class="result {"win" if own['winner'] else "loss"}">{'W 勝' if own['winner'] else 'L 敗'}</span></div><div class="score-line"><span>GSW</span><b>{own['score']}</b></div><div class="score-line opponent"><span>{E(opp['abbr'])}</span><b>{opp['score']}</b></div><div class="game-card-bottom"><span>{'主場' if own['homeAway']=='home' else '客場'} · FINAL</span><span>BOX SCORE ↗</span></div></a>'''


def team_page():
    games = [GAMES[k] for k in TEAM['gameIds']]
    totals = {'PTS': 0, 'REB': 0, 'AST': 0}
    for g in games:
        totals['PTS'] += next(t['score'] for t in g['teams'] if t['id'] == TEAM['id'])
        stats = next(t['statistics'] for t in g['teamStats'] if t['team']['id'] == TEAM['id'])
        vals = {s['name']: float(s['displayValue']) for s in stats if s['name'] in ['totalRebounds', 'assists']}
        totals['REB'] += vals['totalRebounds']
        totals['AST'] += vals['assists']
    curry = PLAYERS['3975']
    active_count = sum(bool(current(p)) for p in PLAYERS.values())
    sorted_players = sorted(PLAYERS.values(), key=lambda p: float(metric(p, 'MIN')) if metric(p, 'MIN') != '—' else -1, reverse=True)
    body = f'''<section class="hero"><div class="hero-court" aria-hidden="true"><div></div><i></i><b></b></div><div class="wrap hero-inner"><div class="hero-copy"><div class="edition"><span></span> THE GOLDEN STATE EDITION <i>01 / 30</i></div><h1>THE GAME.<br><em>THE PEOPLE.</em></h1><p class="hero-zh">看見球場上的數字，也看見場下的人。</p><p class="hero-description">從金州勇士出發，走進每一位球員的生涯與故事。<br>比賽、家庭、熱愛，以及那些數據沒說的事。</p><div class="hero-actions"><a class="button gold" href="#roster">探索勇士全隊 <span>↗</span></a><a class="hero-story-link" href="stories.html">走進場外故事 <span>→</span></a></div><div class="hero-meta"><span>SAN FRANCISCO, CA</span><span>2026—27 REGULAR SEASON</span></div></div><div class="hero-visual"><span class="hero-number" aria-hidden="true">30</span><div class="hero-halo"></div><img class="hero-player" src="{curry['headshot']}" alt="勇士球員 Stephen Curry" width="600" height="436" fetchpriority="high"><div class="hero-player-label"><span>THE BAY'S OWN</span><strong>Stephen Curry</strong><span>#30 / GUARD</span></div><a class="hero-player-note" href="players/stephen-curry.html"><b>{metric(curry,'PTS')}</b><span>本季場均得分<br>探索球員 ↗</span></a></div></div><div class="hero-bottom"><span>MORE THAN A BOX SCORE.</span><span>SCROLL TO EXPLORE ↓</span></div></section>
<section class="team-strip"><div class="wrap team-strip-inner"><div class="team-identity"><span class="team-symbol">W</span><div><h2>金州勇士</h2><span>GOLDEN STATE WARRIORS</span></div></div><div class="team-stats"><div><strong>{TEAM['wins']}<span>—</span>{TEAM['losses']}</strong><small>本季戰績</small></div>{''.join(f'<div><strong>{v/len(games):.1f}</strong><small>場均{label}</small></div>' for (k,v),label in zip(totals.items(),['得分','籃板','助攻']))}</div></div></section>
<div class="wrap data-stamp"><span><span class="status-dot"></span>資料截至 {local_time(TEAM['latestGameAt'],True)} 的完賽紀錄（台北）</span><a href="sources.html">來源與統計定義 ↗</a></div>
<section class="wrap section" id="recent-games">{block_title('01 / THE LATEST', '比賽，把故事繼續寫下去。', '<a class="text-link" href="games.html">全部比賽 ↗</a>')}<div class="games-grid">{''.join(game_card(g) for g in games[:5])}</div></section>
<section class="roster-section" id="roster"><div class="wrap section">{block_title('02 / MEET THE SQUAD', '同一件球衣，不同的人生。', f'<span class="count-note">{len(PLAYERS)} 位球員 <span>／</span> {active_count} 位本季有出賽</span>')}<p class="section-intro">從熟悉的名字，到正在發光的新面孔。每一位，都值得你認識。</p><div class="roster-toolbar"><label class="search-box"><span aria-hidden="true">⌕</span><input id="player-search" type="search" placeholder="搜尋球員、中文名或背號" aria-label="搜尋球員、中文名或背號"></label><div class="filter-chips" aria-label="球員位置篩選">{''.join(f'<button class="filter-chip {"active" if v=="all" else ""}" data-position-filter="{v}" aria-pressed="{str(v=="all").lower()}">{label}</button>' for v,label in [('all','全部'),('G','後衛'),('F','前鋒'),('C','中鋒')])}</div><label class="sort-control"><span class="sr-only">球員排序</span><select id="player-sort"><option value="minutes">上場時間 ↓</option><option value="points">場均得分 ↓</option><option value="number">球衣背號 ↑</option></select></label></div><div class="roster-meta"><label><input id="active-only" type="checkbox"> 僅顯示本季有出賽球員</label><span id="player-count" aria-live="polite">顯示 {len(PLAYERS)} 位球員</span></div><div class="players-grid" id="players-grid">{''.join(player_card(p) for p in sorted_players)}</div><div class="empty-state" id="roster-empty" hidden><strong>沒有符合的球員</strong><p>試試其他姓名、背號，或切換位置篩選。</p><button class="button navy" id="reset-filters">清除篩選</button></div><p class="table-note">數據為 2026–27 例行賽場均。名單包含雙向合約球員；「—」表示本季尚無出賽資料。</p></div></section>
<section class="wrap section" id="off-court">{block_title('03 / LIFE BEYOND THE LINES', '脫下球衣，故事才剛開始。', '<a class="text-link" href="stories.html">全部故事 ↗</a>')}<div class="stories-grid">{''.join(story_card(s) for s in [STORIES[0],STORIES[2],STORIES[4]])}</div></section>
<section class="manifesto wrap"><span class="eyebrow">NUMBERS HAVE SOURCES. PEOPLE HAVE STORIES.</span><h2>喜歡一支球隊，<br>從認識每一個人開始。</h2><a class="text-link" href="about.html">關於場上場下 ↗</a><span class="manifesto-ball" aria-hidden="true">◎</span></section>'''
    page('index.html', '金州勇士・場上場下', body)


def career_table(p, category, kind):
    labels = category['labels']
    names = category['names']
    preferred = ['GP', 'GS', 'MIN', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'FG', 'FG%', '3PT', '3P%', 'FT', 'FT%', 'OR', 'DR', 'PF', 'TO']
    order = sorted(range(len(labels)), key=lambda i: preferred.index(labels[i]) if labels[i] in preferred else 99)
    def cells(values):
        vals = dict(zip(labels, values))
        return ''.join(f'<td>{stat_value(values[i], labels[i], vals)}</td>' for i in order)
    rows = ''.join(f'<tr class="{"current-season" if r["year"]==TEAM["seasonYear"] else ""}"><th scope="row">{E(r["season"])}</th><td>{E(r["team"])}</td>{cells(r["values"])}</tr>' for r in reversed(category['rows']))
    foot = f'<tfoot><tr><th scope="row">生涯合計</th><td>Career</td>{cells(category["career"])}</tr></tfoot>' if category.get('career') else ''
    headings = ''.join('<th scope="col" title="' + E(GLOSSARY.get(labels[i], names[i])) + '">' + E(labels[i]) + '</th>' for i in order)
    return f'<div data-career-view="{kind}-{category["name"]}" {"hidden" if kind+"-"+category["name"]!="regular-averages" else ""}><div class="table-scroll" tabindex="0" role="region" aria-label="{E(p["name"])} {kind} {category["name"]} 統計表"><table class="stats-table career-table"><caption class="sr-only">{E(p["name"])} NBA 逐季統計</caption><thead><tr><th scope="col">賽季</th><th scope="col">球隊</th>{headings}</tr></thead><tbody>{rows}</tbody>{foot}</table></div></div>'


def recent_table(p):
    log = p['recent']
    preferred = ['MIN','PTS','REB','AST','STL','BLK','FG','FG%','3PT','3P%','FT','FT%','TO','PF']
    order = sorted(range(len(log['labels'])),key=lambda i: preferred.index(log['labels'][i]) if log['labels'][i] in preferred else 99)
    rows = ''
    for r in log['rows'][:10]:
        day = local_time(r['date'])
        link = f'../games/{r["id"]}.html' if r['id'] in GAMES else p['links'].get('Game Log', '#recent')
        vals = dict(zip(log['labels'],r['values']))
        rows += f'<tr><th scope="row"><a href="{E(link)}">{day} ↗</a></th><td>{E(r["location"])} {E(r["opponent"])}</td><td><span class="result {"win" if r["result"]=="W" else "loss"}">{E(r["result"])}</span></td>' + ''.join(f'<td>{stat_value(r["values"][i],log["labels"][i], vals)}</td>' for i in order) + '</tr>'
    if not rows:
        return '<div class="empty-state"><strong>本季尚無出賽紀錄</strong><p>球員仍在名單中；可切換至生涯數據，查看過去的 NBA 賽季。</p></div>'
    return '<div class="table-scroll" tabindex="0" role="region" aria-label="近期比賽數據"><table class="stats-table"><caption class="sr-only">最近十次以內 NBA 例行賽出賽，台北時間</caption><thead><tr><th scope="col">日期 ↗</th><th scope="col">對手</th><th scope="col">勝負</th>' + ''.join(f'<th scope="col" title="{E(GLOSSARY.get(log["labels"][i],""))}">{E(log["labels"][i])}</th>' for i in order) + '</tr></thead><tbody>'+rows+'</tbody></table></div>'


def profile(p):
    base = '../'
    stats = current(p)
    stories = [s for s in STORIES if p['id'] in s['playerIds']]
    tables = ''.join(career_table(p,c,kind) for kind in ['regular','playoffs'] for c in p[kind])
    playoff_empty = '<div data-career-view="playoffs-averages" hidden><div class="empty-state"><strong>尚無 NBA 季後賽出賽紀錄</strong><p>季後賽與例行賽分開統計，不包含附加賽。</p></div></div><div data-career-view="playoffs-totals" hidden><div class="empty-state"><strong>尚無 NBA 季後賽出賽紀錄</strong></div></div>' if not p['playoffs'] else ''
    bio = [('位置',p['position']),('身高',p['height']),('生日',p['birthDate']),('最後就讀',p['college'] or '—')]
    career = avg_category(p)
    career_dict = dict(zip(career.get('labels',[]),career.get('career',[])))
    body = f'''<div class="profile-hero"><div class="wrap"><div class="breadcrumbs"><a href="../index.html">勇士隊</a><span>/</span><a href="../index.html#roster">球員圖鑑</a><span>/</span>{E(p['name'])}</div><div class="profile-hero-inner"><div class="profile-copy"><span class="eyebrow">GOLDEN STATE WARRIORS / #{E(p['number'])}</span><h1>{E(p['name'])}</h1><p class="profile-zh">{E(ZH.get(p['id'],''))}</p><p class="profile-deck">{E(stories[0]['summary'])}</p><dl class="player-bio">{''.join(f'<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>' for k,v in bio)}</dl></div><div class="profile-portrait"><span aria-hidden="true">{E(p['number'])}</span><img src="../{p['headshot']}" alt="{E(p['name'])}" width="600" height="436" fetchpriority="high"></div></div></div></div>
<div class="profile-subnav"><nav class="wrap" aria-label="球員頁內導覽"><a href="#season">本季表現</a><a href="#recent">近期比賽</a><a href="#career">生涯數據</a><a href="#stories">場外故事 <span>{len(stories):02d}</span></a></nav></div>
<div class="wrap"><section class="section" id="season">{block_title('01 / THIS SEASON', '本季，寫下的數字。', '<span class="count-note">2026–27 / 例行賽 / 場均</span>')}<div class="profile-stats">{''.join(f'<div><span>{label}</span><strong>{stat_value(stats.get(k),k,stats)}</strong><small>{k}</small></div>' for k,label in [('PTS','得分'),('REB','籃板'),('AST','助攻'),('STL','抄截'),('BLK','阻攻'),('FG%','投籃命中率')])}</div><p class="table-note">{'本季 '+E(stats.get('GP',''))+' 場出賽，'+E(stats.get('GS',''))+' 場先發；每場 '+E(stats.get('MIN',''))+' 分鐘。' if stats else '資料截止時，本季尚無出賽統計。此處不以去年數據替代。'} · 快照取得 {local_time(p['retrievedAt'],True)}（台北）</p></section>
<section class="section" id="recent">{block_title('02 / GAME BY GAME', '最近的每一次上場。', '<span class="count-note">例行賽 / 台北時間</span>')}{recent_table(p)}<p class="table-note">最多顯示近 10 次來源提供的出賽紀錄，不是球隊近 10 場；未出賽不視為零得分。</p></section>
<section class="section" id="career">{block_title('03 / THE WHOLE JOURNEY', '從第一季，到現在。', '<button class="text-button" id="download-csv">下載目前表格 CSV ↓</button>')}<div class="career-summary"><p><strong>{E(career_dict.get('GP','—'))}</strong> NBA 生涯例行賽出賽</p><p><strong>{E(career_dict.get('PTS','—'))}</strong> 生涯場均得分</p><p><strong>{len(set(r['year'] for r in career.get('rows',[])))}</strong> 有出賽紀錄的賽季</p></div><div class="career-controls"><div class="segmented" aria-label="生涯賽事類型"><button class="active" data-career-kind="regular" aria-pressed="true">例行賽</button><button data-career-kind="playoffs" aria-pressed="false">季後賽</button></div><div class="segmented" aria-label="生涯統計模式"><button class="active" data-career-mode="averages" aria-pressed="true">每場平均</button><button data-career-mode="totals" aria-pressed="false">總計</button></div></div>{tables}{playoff_empty}<p class="table-note">左右滑動查看完整欄位。由新至舊列出所有有紀錄的 NBA 賽季；同季轉隊的球隊列與 TOT 合計依來源保留，請勿重複加總。季後賽不含附加賽；「—」表示缺值或無出手，Career 列沿用來源。</p><details class="glossary"><summary>看懂數據縮寫</summary><dl>{''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k,v in GLOSSARY.items())}</dl></details></section>
<section class="section" id="stories">{block_title('04 / BEYOND THE COURT', '數字之外，認識這個人。')}<div class="stories-grid">{''.join(story_card(s,base) for s in stories)}</div></section><section class="section sources-section">{block_title('THE RECEIPTS', '資料都有來處。')}{source_list(p['sources'])}<p class="table-note">基本資料採 ESPN 名單快照；不同來源的量測值可能不同，本站不混用。中文姓名為閱讀輔助，英文姓名為識別依據。</p></section><a class="back-link" href="../index.html#roster">← 回到勇士全隊</a></div>'''
    page('players/'+p['slug']+'.html',p['name'],body,'roster')


def game_page(g):
    teams = sorted(g['teams'],key=lambda t: t['homeAway']=='home')
    a,b=teams
    period_count = max(len(t['quarters']) for t in teams)
    quarters = '<div class="table-scroll"><table class="stats-table"><caption class="sr-only">各節得分</caption><thead><tr><th>球隊</th>'+''.join(f'<th>{"Q"+str(i+1) if i<4 else "OT"+str(i-3)}</th>' for i in range(period_count))+'<th>總分</th></tr></thead><tbody>'+''.join('<tr><th scope="row">'+E(t['abbr'])+'</th>'+''.join('<td>'+E(q)+'</td>' for q in t['quarters'])+f'<td><b>{t["score"]}</b></td></tr>' for t in teams)+'</tbody></table></div>'
    boxes=''
    for box in g['boxscore']:
        rows=''
        for p in box['athletes']:
            name = '<a href="'+player_href(PLAYERS[p['id']],'../')+'">'+E(p['name'])+' ↗</a>' if p['id'] in PLAYERS else E(p['name'])
            if p['didNotPlay']:
                row=f'<td colspan="{len(box["labels"])}" class="dnp">DNP · {E(p["reason"])}</td>'
            else:
                row=''.join('<td>'+E(v)+'</td>' for v in p['values'])
            starter = '<span class="starter">先發</span>' if p['starter'] else ''
            rows+=f'<tr><th scope="row">{name}{starter}</th>{row}</tr>'
        foot = '<tfoot><tr><th scope="row">全隊合計</th>'+''.join('<td>'+E(v)+'</td>' for v in box['totals'])+'</tr></tfoot>' if box['totals'] else ''
        boxes+=f'<h3 class="box-team">{E(box["teamName"])}</h3><div class="table-scroll" tabindex="0" role="region" aria-label="{E(box["teamName"])} box score"><table class="stats-table"><thead><tr><th scope="col">球員</th>'+''.join(f'<th scope="col" title="{E(GLOSSARY.get(k,k))}">{E(k)}</th>' for k in box['labels'])+'</tr></thead><tbody>'+rows+'</tbody>'+foot+'</table></div>'
    comparison=''
    for key, label in [('totalRebounds','籃板'),('assists','助攻'),('steals','抄截'),('blocks','阻攻'),('turnovers','失誤'),('pointsInPaint','禁區得分')]:
        values=[]
        for t in teams:
            ts=next(x for x in g['teamStats'] if x['team']['id']==t['id'])
            values.append(next(x['displayValue'] for x in ts['statistics'] if x['name']==key))
        av,bv=map(float,values);ratio=av/(av+bv)*100 if av+bv else 50
        comparison+=f'<div class="comparison-row"><div><b>{E(values[0])}</b><span>{label}</span><b>{E(values[1])}</b></div><div class="comparison-bar"><span style="width:{ratio:.1f}%"></span></div></div>'
    body=f'''<div class="wrap"><div class="breadcrumbs"><a href="../games.html">比賽紀錄</a><span>/</span>{local_time(g['date'],True)}</div><section class="game-hero"><span class="eyebrow">2026–27 REGULAR SEASON / FINAL</span><p class="muted">{local_time(g['date'],True)} 台北時間 · {E(g['venue'])}</p><h1 class="sr-only">{E(a['name'])} 對 {E(b['name'])}</h1><div class="big-score"><div><span>{E(a['abbr'])}</span><small>{E(a['name'])} · 客場</small></div><strong>{a['score']}<i>:</i>{b['score']}</strong><div><span>{E(b['abbr'])}</span><small>{E(b['name'])} · 主場</small></div></div>{quarters}</section><section class="section">{block_title('01 / TEAM COMPARISON','一場比賽，兩種節奏。')}<div class="comparison"><div class="comparison-label"><span>{E(a['abbr'])}</span><span>{E(b['abbr'])}</span></div>{comparison}</div></section><section class="section">{block_title('02 / THE BOX SCORE','每一位上場的人。')}{boxes}<p class="table-note">DNP 表示未出賽，不等同於出賽零得分。正負值與上場時間依來源顯示。</p></section><section class="section sources-section">{source_list([g['source']])}</section><a class="back-link" href="../games.html">← 回到比賽紀錄</a></div>'''
    page('games/'+g['id']+'.html',a['abbr']+' '+str(a['score'])+' : '+str(b['score'])+' '+b['abbr'],body,'games')


def story_page(s):
    p=PLAYERS[s['playerIds'][0]]
    body=f'''<div class="wrap"><div class="breadcrumbs"><a href="../stories.html">場外故事</a><span>/</span>{E(s['category'])}</div><article class="story-article"><header><span class="eyebrow">BEYOND THE LINES / {E(s['category'])}</span><h1>{E(s['title'])}</h1><p class="article-deck">{E(s['summary'])}</p><div class="article-meta"><a href="{player_href(p,'../')}">{E(p['name'])} ↗</a><span>編輯／查核 {E(s['verifiedAt'])}</span></div></header><div class="article-visual art-{E(s['category'])}"><span aria-hidden="true">{E(p['number'])}</span><img src="../{p['headshot']}" alt="{E(p['name'])}" width="600" height="436"></div><div class="article-prose">{''.join('<p>'+E(t)+'</p>' for t in s['paragraphs'])}<div class="editor-note"><span>EDITOR'S NOTE</span><p>本文為原創摘要與整理。事件日期：{E(s['eventDate'] or '來源未明確提供／涉及一段期間')}。原始來源發布日期與本站編輯日期分開記錄，歷史活動不代表目前仍在進行。</p></div><h2>回到故事的來源</h2>{source_list(s['sources'])}<a class="button navy" href="{player_href(p,'../')}">認識 {E(p['name'])} 的場上表現 ↗</a></div></article><section class="section">{block_title('KEEP READING','還有更多，值得認識。')}<div class="stories-grid">{''.join(story_card(x,'../') for x in [x for x in STORIES if x['id']!=s['id']][:3])}</div></section></div>'''
    page('stories/'+s['id']+'.html',s['title'],body,'stories',s['summary'])


def index_pages():
    header=lambda k,t,d:f'<header class="listing-header"><span class="eyebrow">{k}</span><h1>{t}</h1><p>{d}</p></header>'
    page('games.html','比賽紀錄','<div class="wrap">'+header('GAME JOURNAL / 2026–27','一場一場，記住這個賽季。',f'勇士本季 {len(GAMES)} 場完賽紀錄 · 台北時間 · 點擊查看完整 box score。')+'<div class="games-grid all-games">'+''.join(game_card(GAMES[k]) for k in TEAM['gameIds'])+'</div><p class="table-note">只收錄本快照已完成的例行賽，不包含熱身賽與尚未開打賽事。</p></div>','games')
    filters='<div class="filter-chips story-filters" aria-label="故事分類">'+''.join(f'<button class="filter-chip {"active" if c=="全部" else ""}" data-story-filter="{c}" aria-pressed="{str(c=="全部").lower()}">{c}</button>' for c in ['全部','公益','家庭','興趣','品牌','影音','成長'])+'</div>'
    page('stories.html','場外故事','<div class="wrap">'+header('LIFE BEYOND THE LINES','球場之外，還有整個人生。',f'家庭、公益、熱愛與成長。{len(PLAYERS)} 位球員，{len(STORIES)} 個讓你更認識他們的切面。')+filters+'<p class="filter-status" id="story-count" aria-live="polite">顯示 '+str(len(STORIES))+' 篇故事</p><div class="stories-grid story-list">'+''.join(story_card(s) for s in STORIES)+'</div></div>','stories')
    sources = TEAM['sources']+[{'publisher':'NBA','title':'勇士官方名單（交叉查核）','url':'https://www.nba.com/team/1610612744/warriors/roster'},{'publisher':'Basketball Reference','title':'Stephen Curry 逐季統計（歷史抽查）','url':'https://www.basketball-reference.com/players/c/curryst01.html'}]
    page('sources.html','資料來源與更新','<div class="wrap prose-page">'+header('DATA, WITH CONTEXT','每個數字，都有來處。','公開、可追溯，也清楚說明資料的邊界。')+f'<div class="info-grid"><div><span>統計賽季</span><strong>2026–27 例行賽</strong></div><div><span>最近完賽</span><strong>{local_time(TEAM["latestGameAt"],True)} 台北</strong></div><div><span>快照取得時間</span><strong>{local_time(TEAM["retrievedAt"],True)} 台北</strong></div><div><span>目前涵蓋</span><strong>{len(PLAYERS)} 人 / {len(GAMES)} 場完賽</strong></div></div><h2>怎麼取得與呈現資料？</h2><p>名單、基本資料、逐季平均、逐季總計、生涯合計、近期出賽與比賽 box score，採同一次匯入的 ESPN 公開資料。這是一份固定快照，不是即時轉播。網站建置後不會在瀏覽器呼叫統計 API，因此資料來源暫時中斷時，已發布頁面仍能閱讀。</p><p>例行賽和季後賽分開保留；生涯表涵蓋來源提供的全部 NBA 有出賽賽季。附加賽、熱身賽、大學、國家隊與 G League 不混入統計。球員名單包含雙向合約球員，沒有本季紀錄的人仍有完整個人頁。</p><h2>怎麼避免數字看起來正確，定義卻不同？</h2><p>球隊場均來自本季已完賽 box score 的總量除以完賽場數；球員平均與生涯 Career 列保留來源數值及四捨五入方式。轉隊的單隊列與 TOT 列並列時，不再相加。「—」表示缺值或沒有出手，未出賽不當成零得分。</p><p>不同資料表可能因來源更新時間有短暫差異。例如某位球員的賽季出賽數與近期出賽列表若不一致，不能靠編造比賽補齊；原始回應與取得時間保留供查核。</p><h2>人物故事如何查核？</h2><p>每篇故事有原始連結，優先引用本人、基金會、大學、品牌與球隊公告。媒體報導會標示媒體名稱；本網站使用自己的文字整理。事件日期不確定時明確標示，歷史活動不當成新消息，未查證的「第一支影片」與現役代言不自行下結論。</p><h2>資料與圖片來源</h2>'+source_list(sources)+'<p>每位球員頁與比賽頁另附各自的資料來源，每篇故事也保留自己的引用。球員肖像來自 ESPN 提供的公開頭像網址，僅作非商業課堂與人物識別用途，著作權歸原權利人；本專案不宣稱擁有或可再授權這些圖片。</p><h2>如何更新與更正？</h2><p>執行匯入工具 → 驗證候選資料 → 建置 → 檢查頁面 → 發布。每次匯入保留原始 JSON、UTC 時間與 SHA-256。來源讀取失敗時停止更新，保留上一份可用資料；尚未確認的事實不發布。詳細規則請見 <a href="AGENTS.md">AGENTS.md</a>。</p></div>','sources')
    page('about.html','關於專案','<div class="wrap prose-page">'+header('ABOUT THE JOURNAL','每個數字背後，都有一個人。','Beyond the Court｜場上場下，是一個從勇士隊開始的籃球人物與數據專題。')+'<h2>為什麼做這個網站？</h2><p>球迷記得一場比賽的得分，也會記得球員送給媽媽的驚喜、回到家鄉的公益，或在另一項運動裡的熱情。我們把這些入口放在一起，讓認識一支球隊變得更完整。</p><h2>讓下一次擴充，有章可循。</h2><p>本專案的核心是 <a href="AGENTS.md">AGENTS.md</a>：它定義頁面結構、視覺、資料格式、來源政策與完成檢查。新增球員不需重做頁面；新增故事不需到各個頁面貼卡片。共用模板依照人物 ID 與資料關聯，自動產生連結。</p><h2>已實際示範的延伸</h2><p>第一版包含名單中的 18 位球員、全體逐季生涯表與 20 篇故事；Curry 的公益、高爾夫與品牌合作，使用同一套故事格式分別建立，再自動匯入個人頁。這套結構可延伸到其他球員與球隊。</p><h2>專案方式</h2><p>使用 Python 標準函式庫產生靜態網頁，搭配原生 HTML、CSS 與 JavaScript。無第三方套件、無資料庫、無登入需求，產出的 dist 資料夾可部署至 GitHub Pages 等靜態服務。</p><p>這是非官方球迷與課堂作品，與 NBA、球隊、球員及品牌無隸屬或背書關係。數據來源、快照範圍及圖片說明請見 <a href="sources.html">資料來源與更新</a>。</p></div>','about')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pages', action='store_true', help='Also prepare docs/ for GitHub Pages branch publishing')
    args = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    shutil.copytree(ROOT/'src/assets',OUT/'assets',dirs_exist_ok=True)
    shutil.copytree(ROOT/'public',OUT,dirs_exist_ok=True)
    shutil.copy2(ROOT/'AGENTS.md',OUT/'AGENTS.md')
    team_page()
    for p in PLAYERS.values():
        profile(p)
    for g in GAMES.values():
        game_page(g)
    for s in STORIES:
        story_page(s)
    index_pages()
    (OUT/'.nojekyll').write_text('')
    if args.pages:
        shutil.copytree(OUT, ROOT / 'docs', dirs_exist_ok=True)
    print('Built',len(list(OUT.rglob('*.html'))),'pages in',OUT)


if __name__=='__main__':
    main()
