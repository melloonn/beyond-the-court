/* Small progressive enhancements. All content and navigation work without JS. */
(() => {
  'use strict';
  const $ = (s, root = document) => root.querySelector(s);
  const $$ = (s, root = document) => [...root.querySelectorAll(s)];
  const menu = $('.menu-toggle');
  menu?.addEventListener('click', () => {
    const expanded = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(expanded));
    $('#navigation')?.classList.toggle('is-open', expanded);
  });
  $$('#navigation a').forEach(a => a.addEventListener('click', () => {
    menu?.setAttribute('aria-expanded', 'false');
    $('#navigation')?.classList.remove('is-open');
  }));

  const search = $('#player-search');
  const cards = $$('[data-player]');
  let position = 'all';
  function filterPlayers() {
    const query = search?.value.trim().toLocaleLowerCase() || '';
    let count = 0;
    cards.forEach(card => {
      const show = CourtUtils.matchesPlayer(card.dataset, query, position, $('#active-only')?.checked);
      card.hidden = !show;
      if (show) count++;
    });
    if ($('#player-count')) $('#player-count').textContent = `顯示 ${count} 位球員`;
    if ($('#roster-empty')) $('#roster-empty').hidden = count > 0;
  }
  search?.addEventListener('input', filterPlayers);
  $('#active-only')?.addEventListener('change', filterPlayers);
  $$('[data-position-filter]').forEach(button => button.addEventListener('click', () => {
    position = button.dataset.positionFilter;
    $$('[data-position-filter]').forEach(b => {
      b.classList.toggle('active', b === button);
      b.setAttribute('aria-pressed', String(b === button));
    });
    filterPlayers();
  }));
  $('#player-sort')?.addEventListener('change', event => {
    const key = event.target.value;
    cards.sort((a, b) => CourtUtils.comparePlayers(a.dataset, b.dataset, key));
    cards.forEach(card => $('#players-grid').append(card));
  });
  $('#reset-filters')?.addEventListener('click', () => {
    search.value = '';
    $('#active-only').checked = false;
    $('[data-position-filter="all"]').click();
    search.focus();
  });

  $$('[data-story-filter]').forEach(button => button.addEventListener('click', () => {
    const category = button.dataset.storyFilter;
    let count = 0;
    $$('[data-story]').forEach(story => {
      const show = category === '全部' || story.dataset.category === category;
      story.hidden = !show;
      if (show) count++;
    });
    $$('[data-story-filter]').forEach(b => {
      b.classList.toggle('active', b === button);
      b.setAttribute('aria-pressed', String(b === button));
    });
    if ($('#story-count')) $('#story-count').textContent = `顯示 ${count} 篇故事`;
  }));

  let kind = 'regular';
  let mode = 'averages';
  function updateCareer() {
    $$('[data-career-view]').forEach(table => {
      table.hidden = table.dataset.careerView !== `${kind}-${mode}`;
    });
    $$('[data-career-kind]').forEach(b => {
      const on = b.dataset.careerKind === kind;
      b.classList.toggle('active', on);
      b.setAttribute('aria-pressed', String(on));
    });
    $$('[data-career-mode]').forEach(b => {
      const on = b.dataset.careerMode === mode;
      b.classList.toggle('active', on);
      b.setAttribute('aria-pressed', String(on));
    });
    const table = $(`[data-career-view="${kind}-${mode}"] table`);
    if ($('#download-csv')) $('#download-csv').disabled = !table;
  }
  $$('[data-career-kind]').forEach(b => b.addEventListener('click', () => {
    kind = b.dataset.careerKind;
    updateCareer();
  }));
  $$('[data-career-mode]').forEach(b => b.addEventListener('click', () => {
    mode = b.dataset.careerMode;
    updateCareer();
  }));
  $('#download-csv')?.addEventListener('click', () => {
    const table = $(`[data-career-view="${kind}-${mode}"] table`);
    if (!table) return;
    const safeCell = CourtUtils.csvCell;
    const csv = $$('tr', table).map(row => $$('th,td', row).map(cell => safeCell(cell.textContent)).join(',')).join('\r\n');
    const blob = new Blob(['\uFEFF', csv], { type: 'text/csv;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${document.title.split('｜')[0]}-${kind}-${mode}.csv`;
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
})();
