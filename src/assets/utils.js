/* Shared deterministic interaction rules, also exercised by the Node test suite. */
(function (root) {
  'use strict';
  const utils = {
    matchesPlayer(player, query = '', position = 'all', activeOnly = false) {
      return player.name.toLocaleLowerCase().includes(query.trim().toLocaleLowerCase())
        && (position === 'all' || player.position.includes(position))
        && (!activeOnly || player.active === 'true');
    },
    comparePlayers(a, b, key) {
      return key === 'number' ? Number(a.number) - Number(b.number) : Number(b[key]) - Number(a[key]);
    },
    csvCell(text) {
      const value = String(text).replace(/\s+/g, ' ').trim();
      return '"' + (/^[=+@\-]/.test(value) ? "'" : '') + value.replaceAll('"', '""') + '"';
    }
  };
  root.CourtUtils = utils;
  if (typeof module !== 'undefined' && module.exports) module.exports = utils;
})(globalThis);
