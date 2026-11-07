#!/usr/bin/env python3
"""Fetch auditable public ESPN snapshots. Standard library only; no browser API dependency."""
import concurrent.futures
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
NOW = dt.datetime.now(dt.timezone.utc).isoformat()
SEASON = 2027
BASE = 'https://site.web.api.espn.com/apis/common/v3/sports/basketball/nba'
SITE = 'https://site.api.espn.com/apis/site/v2/sports/basketball/nba'
RAW = ROOT / 'data/raw'
RECORDS = []


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    os.replace(temp, path)


def fetch(key, url):
    req = urllib.request.Request(url, headers={'User-Agent': 'BeyondTheCourt/1.0 (educational basketball reference)'})
    body = urllib.request.urlopen(req, timeout=45).read()
    value = json.loads(body)
    if not isinstance(value, dict):
        raise ValueError('Unexpected response: ' + url)
    RAW.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(body).hexdigest()
    filename = key + '-' + digest[:12] + '.json'
    (RAW / filename).write_bytes(body)
    RECORDS.append({'key': key, 'url': url, 'retrievedAt': NOW, 'sha256': digest, 'file': filename})
    return value


def source(title, url):
    return {'title': title, 'url': url, 'publisher': 'ESPN', 'retrievedAt': NOW}


def stats_payload(j, expected_type):
    filters = {x['name']: x.get('value') for x in j.get('filters', [])}
    if j.get('categories') and str(filters.get('seasontype')) != str(expected_type):
        available = next((x.get('options', []) for x in j.get('filters', []) if x['name'] == 'seasontype'), [])
        # ESPN falls back to regular-season data when a player has no postseason.
        # An absent postseason option is evidence of no postseason, not permission to copy regular rows.
        if expected_type == 3 and '3' not in [str(x['value']) for x in available]:
            return []
        raise ValueError('Season type mismatch')
    teams = j.get('teams', {})
    categories = []
    for c in j.get('categories', []):
        if c['name'] not in ['averages', 'totals']:
            continue
        rows = []
        for r in c.get('statistics', []):
            if r.get('season', {}).get('year', 9999) > SEASON:
                continue
            team = teams.get(r.get('teamSlug'), {})
            rows.append({'season': r.get('season', {}).get('displayName'),
                         'year': r.get('season', {}).get('year'),
                         'team': team.get('abbreviation') or ('TOT' if not r.get('teamId') or r.get('teamId') == '0' else r.get('teamSlug', str(r.get('teamId')))),
                         'teamId': r.get('teamId'), 'values': r['stats']})
        categories.append({'name': c['name'], 'labels': c['labels'], 'names': c['names'],
                           'rows': rows, 'career': c.get('totals', [])})
    return categories


def player(a):
    aid = a['id']
    prefix = BASE + '/athletes/' + aid
    with concurrent.futures.ThreadPoolExecutor(3) as pool:
        regular, playoffs, log = list(pool.map(lambda p: fetch(*p), [
            ('player-' + aid + '-regular', prefix + '/stats?seasontype=2'),
            ('player-' + aid + '-playoffs', prefix + '/stats?seasontype=3'),
            ('player-' + aid + '-gamelog', prefix + '/gamelog?season=' + str(SEASON))]))
    recent = []
    for season in log.get('seasonTypes', []):
        if season.get('displayName') != '2026-27 Regular Season':
            continue
        for category in season.get('categories', []):
            for row in category.get('events', []):
                e = log.get('events', {}).get(row['eventId'], {})
                if not e.get('gameDate') or e['gameDate'] > NOW:
                    continue
                recent.append({'id': row['eventId'], 'date': e['gameDate'],
                               'opponent': e.get('opponent', {}).get('abbreviation'),
                               'location': e.get('atVs'), 'result': e.get('gameResult'),
                               'score': e.get('score'), 'values': row['stats']})
    links = {r['text']: r['href'] for r in a.get('links', []) if r.get('isExternal') is False and r['href'].startswith('https://')}
    p = {'id': aid, 'slug': a['slug'], 'name': a['fullName'], 'number': a.get('jersey'),
         'position': a.get('position', {}).get('abbreviation'), 'height': a.get('displayHeight'),
         'birthDate': a.get('dateOfBirth', '')[:10], 'birthPlace': a.get('birthPlace', {}),
         'college': a.get('college', {}).get('name'), 'debutYear': a.get('debutYear'),
         'headshot': 'images/players/' + aid + '.png', 'headshotSource': a.get('headshot', {}).get('href'),
         'regular': stats_payload(regular, 2), 'playoffs': stats_payload(playoffs, 3),
         'recent': {'labels': log.get('labels', []), 'names': log.get('names', []), 'rows': sorted(recent, key=lambda r: r['date'], reverse=True)},
         'links': links, 'retrievedAt': NOW,
         'sources': [source('ESPN 球員資料與統計', links.get('Stats', prefix + '/stats')),
                     source('例行賽資料快照', prefix + '/stats?seasontype=2'),
                     source('季後賽資料快照', prefix + '/stats?seasontype=3'),
                     source('近期出賽資料快照', prefix + '/gamelog?season=' + str(SEASON))]}
    print('Fetched player:', p['name'], flush=True)
    return p


def game(event):
    gid = event['id']
    url = SITE + '/summary?event=' + gid
    j = fetch('game-' + gid, url)
    c = j['header']['competitions'][0]
    teams = []
    for t in c['competitors']:
        teams.append({'id': t['id'], 'name': t['team']['displayName'], 'abbr': t['team']['abbreviation'],
                      'homeAway': t['homeAway'], 'score': int(t['score']), 'winner': t.get('winner', False),
                      'quarters': [x.get('displayValue', str(x.get('value', ''))) for x in t.get('linescores', [])]})
    box = []
    for group in j.get('boxscore', {}).get('players', []):
        for table in group.get('statistics', []):
            athletes = []
            for r in table.get('athletes', []):
                athletes.append({'id': r['athlete']['id'], 'name': r['athlete']['displayName'],
                                 'starter': r.get('starter', False), 'didNotPlay': r.get('didNotPlay', False),
                                 'reason': r.get('reason', ''), 'values': r.get('stats', [])})
            box.append({'teamId': group['team']['id'], 'teamName': group['team']['displayName'],
                        'labels': table['labels'], 'names': table.get('names', []),
                        'athletes': athletes, 'totals': table.get('totals', [])})
    return {'id': gid, 'date': event['date'], 'season': '2026-27', 'seasonType': 'Regular Season',
            'status': c['status']['type']['name'], 'venue': j.get('gameInfo', {}).get('venue', {}).get('fullName'),
            'teams': teams, 'boxscore': box, 'teamStats': j.get('boxscore', {}).get('teams', []),
            'source': source('ESPN 比賽紀錄', 'https://www.espn.com/nba/boxscore/_/gameId/' + gid),
            'retrievedAt': NOW}


def download_image(pair):
    path, url = pair
    if not url:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return
    body = urllib.request.urlopen(url, timeout=30).read()
    if not body.startswith(b'\x89PNG'):
        raise ValueError('Expected PNG from ' + url)
    path.write_bytes(body)


def reconcile_recent(players, games):
    """A 0-minute rounded appearance can be omitted from ESPN's athlete log.

    Add only an actual played box-score row. Never interpret DNP as an appearance.
    """
    by_id = {p['id']: p for p in players}
    mapping = {'MIN': 'MIN', 'FG': 'FG', '3PT': '3PT', 'FT': 'FT',
               'REB': 'REB', 'AST': 'AST', 'BLK': 'BLK', 'STL': 'STL', 'PF': 'PF', 'TO': 'TO', 'PTS': 'PTS'}
    for g in games:
        own = next(t for t in g['teams'] if t['id'] == '9')
        opp = next(t for t in g['teams'] if t['id'] != '9')
        for box in g['boxscore']:
            if box['teamId'] != '9':
                continue
            for a in box['athletes']:
                p = by_id.get(a['id'])
                if not p or a['didNotPlay'] or any(r['id'] == g['id'] for r in p['recent']['rows']):
                    continue
                values = dict(zip(box['labels'], a['values']))
                result = []
                for label in p['recent']['labels']:
                    if label in mapping:
                        result.append(values[mapping[label]])
                    elif label in ['FG%', '3P%', 'FT%']:
                        pair = {'FG%': 'FG', '3P%': '3PT', 'FT%': 'FT'}[label]
                        made, attempts = map(float, values[pair].split('-'))
                        result.append(format(made / attempts * 100, '.1f') if attempts else '--')
                    else:
                        raise ValueError('Unknown game log label: ' + label)
                p['recent']['rows'].append({'id': g['id'], 'date': g['date'], 'opponent': opp['abbr'],
                                           'location': 'vs' if own['homeAway'] == 'home' else '@',
                                           'result': 'W' if own['winner'] else 'L',
                                           'score': str(own['score']) + '-' + str(opp['score']),
                                           'values': result, 'reconciledFromBoxscore': True})
                p['recent']['rows'].sort(key=lambda r: r['date'], reverse=True)
                p['sources'].append(source('補充出賽紀錄：比賽 box score', g['source']['url']))


def main():
    roster_url = SITE + '/teams/gs/roster'
    schedule_url = SITE + '/teams/gs/schedule?season=' + str(SEASON) + '&seasontype=2'
    roster = fetch('roster', roster_url)
    schedule = fetch('schedule', schedule_url)
    if roster.get('season', {}).get('year') != SEASON or len(roster.get('athletes', [])) < 12:
        raise ValueError('Roster season/size mismatch; preserve previous data')
    with concurrent.futures.ThreadPoolExecutor(4) as pool:
        players = list(pool.map(player, roster['athletes']))
    completed = [e for e in schedule['events'] if e.get('seasonType', {}).get('type') == 2 and e['date'] <= NOW
                 and e['competitions'][0].get('status', {}).get('type', {}).get('completed')]
    completed.sort(key=lambda e: e['date'], reverse=True)
    with concurrent.futures.ThreadPoolExecutor(4) as pool:
        games = list(pool.map(game, completed))
    reconcile_recent(players, games)
    wins = sum(next(t for t in g['teams'] if t['id'] == '9')['winner'] for g in games)
    team = {'id': '9', 'slug': 'golden-state-warriors', 'name': 'Golden State Warriors', 'nameZh': '金州勇士',
            'season': '2026-27', 'seasonYear': SEASON, 'seasonType': 'Regular Season',
            'venue': 'Chase Center', 'location': 'San Francisco, California',
            'wins': wins, 'losses': len(games) - wins, 'playerIds': [p['id'] for p in players],
            'gameIds': [g['id'] for g in games], 'latestGameAt': games[0]['date'] if games else None,
            'retrievedAt': NOW, 'sources': [source('ESPN 勇士名單', roster_url), source('ESPN 當季賽程', schedule_url)]}
    # Validate complete candidate data before touching published datasets.
    from validate import validate_data
    validate_data(team, players, games, check_assets=False)
    images = [(ROOT / 'public' / p['headshot'], p['headshotSource']) for p in players]
    with concurrent.futures.ThreadPoolExecutor(5) as pool:
        list(pool.map(download_image, images))
    candidate = ROOT / 'data/candidate.json'
    write_json(candidate, {'team': team, 'players': players, 'games': games, 'sources': RECORDS})
    for p in players:
        write_json(ROOT / 'src/data/players' / (p['slug'] + '.json'), p)
    for g in games:
        write_json(ROOT / 'src/data/games' / (g['id'] + '.json'), g)
    write_json(ROOT / 'src/data/teams/golden-state-warriors.json', team)
    write_json(RAW / 'manifest.json', {'retrievedAt': NOW, 'records': RECORDS})
    print('Published snapshot:', len(players), 'players;', len(games), 'completed games;', wins, 'wins')


if __name__ == '__main__':
    main()
