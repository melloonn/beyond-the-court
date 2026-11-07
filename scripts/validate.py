#!/usr/bin/env python3
"""Data integrity and static-site link checks; no third-party dependencies."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text())


def validate_data(team, players, games, check_assets=True):
    assert len({p['id'] for p in players}) == len(players), 'Duplicate player ID'
    assert len({p['slug'] for p in players}) == len(players), 'Duplicate player slug'
    assert set(team['playerIds']) == {p['id'] for p in players}, 'Roster coverage'
    assert set(team['gameIds']) == {g['id'] for g in games}, 'Schedule coverage'
    for p in players:
        assert p['sources'] and all(urlsplit(s['url']).scheme == 'https' for s in p['sources'])
        if check_assets:
            assert (ROOT / 'public' / p['headshot']).exists(), 'Missing image: ' + p['name']
        for kind in ['regular', 'playoffs']:
            for c in p[kind]:
                assert len(c['labels']) == len(c['names']), p['name']
                if c['career']:
                    assert len(c['career']) == len(c['names']), p['name'] + ' career width'
                for r in c['rows']:
                    assert r['year'] <= team['seasonYear']
                    assert len(r['values']) == len(c['names']), p['name'] + ' row width'
                    for name, v in zip(c['names'], r['values']):
                        if ('Made-' in name) and '-' in str(v):
                            made, attempts = map(float, v.split('-'))
                            assert made <= attempts, p['name'] + ' shot count'
                        if 'Pct' in name and v not in ['', '--', '—', None]:
                            assert 0 <= float(v) <= 100, p['name'] + ' percentage'
        assert len({r['id'] for r in p['recent']['rows']}) == len(p['recent']['rows']), 'Duplicate game log'
        # Every actual current-team box-score appearance must be represented, even
        # when the provider rounds its duration down to 0 minutes.
        played_ids = {g['id'] for g in games for b in g['boxscore'] if b['teamId'] == team['id']
                      for a in b['athletes'] if a['id'] == p['id'] and not a['didNotPlay']}
        logged_ids = {r['id'] for r in p['recent']['rows']}
        assert played_ids.issubset(logged_ids), 'Missing played game: ' + p['name']
    wins = 0
    for g in games:
        assert g['status'] == 'STATUS_FINAL', g['id'] + ' not final'
        assert len(g['teams']) == 2
        a, b = g['teams']
        assert a['score'] != b['score']
        assert a['winner'] == (a['score'] > b['score'])
        assert b['winner'] == (b['score'] > a['score'])
        wins += next(t for t in g['teams'] if t['id'] == team['id'])['winner']
        for box in g['boxscore']:
            assert len(box['athletes']) > 0
            pts = box['labels'].index('PTS')
            total = 0
            for a in box['athletes']:
                if a['didNotPlay']:
                    continue
                assert len(a['values']) == len(box['labels']), g['id'] + ' box width'
                total += int(a['values'][pts])
                labels = dict(zip(box['labels'], a['values']))
                if all(k in labels for k in ['FG', '3PT', 'FT']):
                    fg, three, ft = [int(labels[k].split('-')[0]) for k in ['FG', '3PT', 'FT']]
                    assert 2 * fg + three + ft == int(a['values'][pts]), g['id'] + ' points formula'
            assert total == next(t['score'] for t in g['teams'] if t['id'] == box['teamId']), g['id'] + ' box total'
    assert wins == team['wins'] and len(games) - wins == team['losses']


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, 'Duplicate HTML id: ' + attrs['id']
            self.ids.add(attrs['id'])
        for key in ['href', 'src']:
            if attrs.get(key):
                self.links.append(attrs[key])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data-only', action='store_true')
    args = ap.parse_args()
    team = read(ROOT / 'src/data/teams/golden-state-warriors.json')
    players = [read(p) for p in (ROOT / 'src/data/players').glob('*.json')]
    games = [read(p) for p in (ROOT / 'src/data/games').glob('*.json')]
    validate_data(team, players, games)
    stories = read(ROOT / 'src/data/stories.json')
    assert len({s['id'] for s in stories}) == len(stories)
    for p in players:
        assert any(p['id'] in s['playerIds'] for s in stories), 'Missing story for ' + p['name']
    for s in stories:
        assert set(s['playerIds']).issubset(set(team['playerIds']))
        assert s['sources'] and s['paragraphs']
        assert all(urlsplit(x['url']).scheme == 'https' for x in s['sources'])
    manifest = read(ROOT / 'data/raw/manifest.json')
    for r in manifest['records']:
        assert hashlib.sha256((ROOT / 'data/raw' / r['file']).read_bytes()).hexdigest() == r['sha256']
    print('PASS: roster, career tables, percentages, completed scores, box scores, stories, raw SHA-256')
    if args.data_only:
        return
    dist = ROOT / 'dist'
    parsed = {}
    for file in dist.rglob('*.html'):
        parser = Links()
        parser.feed(file.read_text())
        parsed[file.resolve()] = parser
    assert len(parsed) >= 1 + len(players) + len(games) + len(stories)
    for file, parser in parsed.items():
        for link in parser.links:
            u = urlsplit(link)
            if u.scheme or u.netloc:
                assert u.scheme in ['http', 'https', 'mailto'], 'Unexpected URL scheme'
                continue
            assert not u.path.endswith('.md'), 'Developer Markdown exposed in visitor navigation: ' + link
            assert not u.path.startswith('/'), 'Root-absolute path breaks project Pages: ' + link
            target = (file.parent / unquote(u.path)).resolve() if u.path else file
            if target.is_dir():
                target /= 'index.html'
            assert target.is_relative_to(dist.resolve()), 'Link escapes site: ' + link
            assert target.exists(), str(file) + ': broken link ' + link
            if u.fragment and target in parsed:
                assert unquote(u.fragment) in parsed[target].ids, 'Missing anchor: ' + link
    print('PASS:', len(parsed), 'HTML pages; all internal links, fragments and local assets')
    entry = ROOT / 'index.html'
    home = entry.read_text()
    assert 'hero-copy' in home and 'explore-grid' in home, 'Root must serve the complete visual homepage'
    assert 'http-equiv="refresh"' not in home and 'location.replace' not in home, 'Root must not redirect'
    parser = Links()
    parser.feed(home)
    for link in parser.links:
        u = urlsplit(link)
        if u.scheme or u.netloc:
            continue
        target = (ROOT / unquote(u.path)).resolve() if u.path else entry.resolve()
        assert target.is_relative_to(ROOT), 'Root entry link escapes project'
        assert target.exists(), 'Broken root homepage link: ' + link
        assert not u.path.endswith('.md'), 'Root homepage exposes Markdown navigation'
        if not u.path and u.fragment:
            assert u.fragment in parser.ids, 'Root homepage missing anchor'
    print('PASS: root serves a complete frontend; visitor navigation contains no Markdown links')


if __name__ == '__main__':
    main()
