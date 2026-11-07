const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const utils = require('../src/assets/utils.js');
const dir = path.join(__dirname, '../src/data/players');
const players = fs.readdirSync(dir).filter(f => f.endsWith('.json')).map(f => {
  const p = JSON.parse(fs.readFileSync(path.join(dir, f)));
  const c = p.regular.find(c => c.name === 'averages');
  const r = c?.rows.findLast(r => r.year === 2027 && r.teamId === '9');
  const s = r ? Object.fromEntries(c.labels.map((k, i) => [k, r.values[i]])) : {};
  return { id: p.id, name: `${p.name} ${p.id === '3975' ? '史蒂芬・柯瑞' : ''} ${p.number}`,
    number: p.number, position: p.position, active: String(Boolean(r)),
    points: s.PTS ?? -1, minutes: s.MIN ?? -1 };
});

test('English, Chinese, jersey and whitespace queries find Curry in the real roster', () => {
  for (const query of ['  CURRY  ', '柯瑞', '30']) {
    assert.deepEqual(players.filter(p => utils.matchesPlayer(p, query)).map(p => p.id), ['3975']);
  }
});
test('No-result query and reset preserve all 18 roster members', () => {
  assert.equal(players.filter(p => utils.matchesPlayer(p, '不存在的球員')).length, 0);
  assert.equal(players.filter(p => utils.matchesPlayer(p)).length, 18);
});
test('Active-only excludes the three players without current-season appearances', () => {
  const active = players.filter(p => utils.matchesPlayer(p, '', 'all', true));
  assert.equal(active.length, 15);
  for (const id of ['6430', '4432171', '3102531']) assert.ok(!active.some(p => p.id === id));
});
test('Position filter respects actual source positions', () => {
  const centers = players.filter(p => utils.matchesPlayer(p, '', 'C'));
  assert.ok(centers.some(p => p.id === '3213'));
  assert.ok(!centers.some(p => p.id === '3975'));
});
test('Numeric sorts give Curry first by PPG, Podziemski by minutes, Payton by jersey', () => {
  assert.equal([...players].sort((a,b) => utils.comparePlayers(a,b,'points'))[0].id, '3975');
  assert.equal([...players].sort((a,b) => utils.comparePlayers(a,b,'minutes'))[0].id, '4709138');
  assert.equal([...players].sort((a,b) => utils.comparePlayers(a,b,'number'))[0].id, '3134903');
});
test('CSV preserves commas/quotes and prevents spreadsheet formula execution', () => {
  assert.equal(utils.csvCell('30.1'), '"30.1"');
  assert.equal(utils.csvCell('Team, "A"'), '"Team, ""A"""');
  assert.equal(utils.csvCell('=1+1'), '"\'=1+1"');
  assert.equal(utils.csvCell('—'), '"—"');
});
