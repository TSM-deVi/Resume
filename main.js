// ── Scroll progress + Back to top + Nav shadow ──
const backBtn      = document.getElementById('back-to-top');
const nav          = document.querySelector('nav');
const progressBar  = document.getElementById('scroll-progress');

const heroSky = document.querySelector('.hero-sky');
const _reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

let _scrollTicking = false;
function _onScroll() {
  const scrollY   = window.scrollY;
  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  progressBar.style.transform = 'scaleX(' + (docHeight > 0 ? scrollY / docHeight : 0) + ')';
  backBtn.classList.toggle('visible', scrollY > 400);
  nav.classList.toggle('scrolled', scrollY > 10);

  // Parallax: the sky trails the page. Capped so the plate never runs out
  // from under its own fade.
  if (heroSky && !_reduceMotion) {
    heroSky.style.setProperty('--par', Math.min(scrollY * 0.18, 90) + 'px');
  }
  _scrollTicking = false;
}
window.addEventListener('scroll', () => {
  if (_scrollTicking) return;
  _scrollTicking = true;
  requestAnimationFrame(_onScroll);
}, { passive: true });

backBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

// ── Scroll reveal ──
const revealObs = new IntersectionObserver(
  entries => entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('v'); }),
  { threshold: 0.1 }
);
document.querySelectorAll('.r').forEach(el => revealObs.observe(el));
// Наблюдатель на месте — аварийное проявление больше не нужно.
clearTimeout(window._revealFallback);

// ── Counter animation ──
function runCounter(el) {
  const text = el.dataset.text;
  if (text) { el.textContent = text; return; }

  const target = parseInt(el.dataset.count, 10);
  const suffix = el.dataset.suffix || '+';
  // Сброс анимаций в CSS не действует на setInterval — при reduced motion
  // ставим конечное значение сразу.
  if (_reduceMotion) { el.textContent = target + suffix; return; }
  const steps  = 55;
  let i = 0;
  el.textContent = '0';   // в разметке лежит итог — для случая без JS

  const timer = setInterval(() => {
    i++;
    el.textContent = Math.round((i / steps) * target) + (i >= steps ? suffix : '');
    if (i >= steps) clearInterval(timer);
  }, 14);
}

const counterObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      runCounter(e.target);
      counterObs.unobserve(e.target);
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('.stat-val[data-count], .stat-val[data-text]')
  .forEach(el => counterObs.observe(el));

// ── Active nav highlight on scroll ──
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-links a');

const navObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      navLinks.forEach(a => {
        a.classList.toggle('active', a.getAttribute('href') === '#' + e.target.id);
      });
    }
  });
}, { rootMargin: '-35% 0px -60% 0px' });

sections.forEach(s => navObs.observe(s));

// ── Hamburger menu ──
const hamburger = document.getElementById('nav-hamburger');
const navMenu   = document.getElementById('nav-links');

hamburger.addEventListener('click', () => {
  const open = hamburger.classList.toggle('open');
  navMenu.classList.toggle('open', open);
  hamburger.setAttribute('aria-expanded', String(open));
});

navMenu.querySelectorAll('a').forEach(a => {
  a.addEventListener('click', () => {
    hamburger.classList.remove('open');
    hamburger.setAttribute('aria-expanded', 'false');
    navMenu.classList.remove('open');
  });
});

// ── Language toggle ──
const langBtn   = document.getElementById('lang-toggle');
const htmlRoot  = document.getElementById('html-root');
// Приоритет: адрес → сохранённый выбор → русский. Адрес выигрывает, чтобы
// ссылка ?lang=en открывала английскую версию у любого получателя.
const _urlLang = new URLSearchParams(location.search).get('lang');
let lang = (_urlLang === 'en' || _urlLang === 'ru')
  ? _urlLang
  : (localStorage.getItem('lang') || 'ru');

// Заголовок вкладки и описание жили только по-русски: lang="en" и весь текст
// переключались, а <title> с meta description оставались русскими — в выдаче
// и при отправке ссылки английская версия выглядела русской.
const _metaDesc = document.querySelector('meta[name="description"]');
const _meta = {
  ru: {
    title: document.title,
    desc: _metaDesc ? _metaDesc.content : '',
  },
  en: {
    // Сайт транслитерирует имя как «Ivanov Temir» — заголовок обязан совпадать
    // с <h1> и og:title, иначе вкладка и выдача разойдутся с самой страницей.
    title: 'Ivanov Temir — Middle+ DevOps Engineer',
    desc: 'Middle+ DevOps engineer, Saint Petersburg. Bare-metal Kubernetes, VMware Cloud Director and k3s, ' +
          'GitLab CI/CD, ArgoCD, Terraform, Ansible, observability. 63 VMs across DEV/INF/PROD environments, ' +
          '70+ services in operation.',
  },
};

function applyLang(l) {
  if (l === 'en') {
    document.body.classList.add('lang-en');
    htmlRoot.lang    = 'en';
    langBtn.textContent = 'RU';
    backBtn.setAttribute('aria-label', 'Back to top');
  } else {
    document.body.classList.remove('lang-en');
    htmlRoot.lang    = 'ru';
    langBtn.textContent = 'EN';
    backBtn.setAttribute('aria-label', 'Наверх');
  }

  const m = _meta[l] || _meta.ru;
  document.title = m.title;
  if (_metaDesc) _metaDesc.content = m.desc;

  localStorage.setItem('lang', l);

  // Русский — версия по умолчанию, её параметр в адресе только мусорит и
  // расходится с canonical; в URL держим лишь явный ?lang=en.
  const url = new URL(location.href);
  if (l === 'en') url.searchParams.set('lang', 'en');
  else url.searchParams.delete('lang');
  history.replaceState(null, '', url);
}

applyLang(lang);

langBtn.addEventListener('click', () => {
  lang = lang === 'ru' ? 'en' : 'ru';
  applyLang(lang);
  startTypewriter();
});

// ── Typewriter + Living Terminal ──
const _liveCmds = [
  null,
  'terraform plan       → 0 errors, 0 warnings',
  'argocd app sync      → synced · healthy',
  'ping on-call         → reply: always',
  'systemctl status me  → active (running)',
];
let _liveCmdIdx = 0;

function _typeTW(text, speed, cb) {
  const el = document.getElementById('typewriter-text');
  if (!el) return;
  el.textContent = '';
  let i = 0;
  clearInterval(window._twTimer);
  window._twTimer = setInterval(() => {
    el.textContent += text[i++];
    if (i >= text.length) { clearInterval(window._twTimer); if (cb) cb(); }
  }, speed);
}

function _eraseTW(cb) {
  const el = document.getElementById('typewriter-text');
  if (!el) return;
  clearInterval(window._twTimer);
  window._twTimer = setInterval(() => {
    if (!el.textContent.length) { clearInterval(window._twTimer); if (cb) cb(); return; }
    el.textContent = el.textContent.slice(0, -1);
  }, 22);
}

function _scheduleLive() {
  clearTimeout(window._liveTimer);
  window._liveTimer = setTimeout(() => {
    _liveCmdIdx = (_liveCmdIdx + 1) % _liveCmds.length;
    _eraseTW(() => {
      const heroRole = document.getElementById('hero-role');
      const isEn    = document.body.classList.contains('lang-en');
      const isRole  = _liveCmdIdx === 0;
      const text    = isRole
        ? (isEn ? heroRole.dataset.textEn : heroRole.dataset.textRu)
        : _liveCmds[_liveCmdIdx];
      _typeTW(text, isRole ? 45 : 35, _scheduleLive);
    });
  }, 3200);
}

function startTypewriter() {
  clearTimeout(window._liveTimer);
  clearInterval(window._twTimer);
  _liveCmdIdx = 0;
  const heroRole = document.getElementById('hero-role');
  if (!heroRole) return;
  const isEn = document.body.classList.contains('lang-en');
  const text = isEn ? heroRole.dataset.textEn : heroRole.dataset.textRu;
  // Строка печатается посимвольно и потом бесконечно перебирает команды —
  // это и есть движение, от которого просили избавиться. Показываем сразу.
  if (_reduceMotion) {
    const el = document.getElementById('typewriter-text');
    if (el) el.textContent = text;
    return;
  }
  _typeTW(text, 45, _scheduleLive);
}
startTypewriter();

// ── Длинные списки опыта: начало видно, остальное по кнопке ──
(function () {
  const LIMIT = 6;          // столько содержательных пунктов видно сразу
  const MIN_HIDDEN = 4;     // ради двух-трёх строк кнопку не заводим

  function plural(n) {
    const d10 = n % 10, d100 = n % 100;
    if (d10 === 1 && d100 !== 11) return 'пункт';
    if (d10 >= 2 && d10 <= 4 && (d100 < 12 || d100 > 14)) return 'пункта';
    return 'пунктов';
  }

  // Подзаголовки и названия проектов лимит не тратят: в списке ДЮК их шесть
  // на 27 пунктов, и при общем счёте читатель до сворачивания видел бы почти
  // одни заголовки. Считаем только содержательные пункты, а заголовок прячем
  // тогда, когда скрыта вся его группа.
  const isHead = li => li.classList.contains('jlist-head') ||
                       li.classList.contains('jlist-proj');

  document.querySelectorAll('.jlist').forEach(list => {
    const items = Array.from(list.children);
    let shown = 0;
    const hidden = items.filter(li => {
      if (isHead(li)) return false;
      return ++shown > LIMIT;
    });
    if (hidden.length < MIN_HIDDEN) return;

    // Заголовок без единого видимого пункта под ним — тоже в скрытую часть.
    for (let i = 0; i < items.length; i++) {
      if (!isHead(items[i])) continue;
      let j = i + 1, empty = true;
      for (; j < items.length && !isHead(items[j]); j++) {
        if (!hidden.includes(items[j])) { empty = false; break; }
      }
      if (empty && j > i + 1) hidden.push(items[i]);
    }

    hidden.forEach(li => li.classList.add('jl-hide'));

    // В счётчике на кнопке — только содержательные пункты, заголовки не в счёт.
    const n = hidden.filter(li => !isHead(li)).length;
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'jlist-more';
    btn.setAttribute('aria-expanded', 'false');
    // У каждой должности два списка, ru и en; кнопка без языка показывалась
    // дважды подряд. Наследуем язык своего списка.
    const listLang = list.getAttribute('data-lang');
    if (listLang) btn.setAttribute('data-lang', listLang);
    btn.innerHTML =
      '<span class="jm-ico" aria-hidden="true"></span>' +
      '<span class="jm-more" data-lang="ru">показать ещё ' + n + ' ' + plural(n) + '</span>' +
      '<span class="jm-more" data-lang="en">show ' + n + ' more</span>' +
      '<span class="jm-less" data-lang="ru">свернуть</span>' +
      '<span class="jm-less" data-lang="en">collapse</span>';

    btn.addEventListener('click', () => {
      const open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!open));
      hidden.forEach(li => li.classList.toggle('jl-hide', open));
      if (open) list.scrollIntoView({ block: 'nearest' });
    });

    list.after(btn);
  });
})();

// ── Console Easter Egg ──
try {
  const _cs = [
    'color:#8a68f7;font-family:monospace;font-size:12px;line-height:1.6;',
    'color:#b6d9fc;font-family:monospace;font-size:11px;',
    'color:#9da7ba;font-family:monospace;font-size:11px;',
  ];
  console.log(
    '%c╔══════════════════════════════════════════════╗\n' +
    '║  $ whoami                                    ║\n' +
    '║  > Ivanov Temir · Middle+ DevOps Engineer    ║\n' +
    '║                                              ║\n' +
    '║  $ kubectl get contact                       ║\n' +
    '║  > TG:    @ktylhus                           ║\n' +
    '║  > email: timir-ivaniv@yandex.ru             ║\n' +
    '╚══════════════════════════════════════════════╝', _cs[0]
  );
  console.log('%c● open to work · remote', _cs[1]);
  console.log('%cLooking for a DevOps engineer? Let\'s talk!', _cs[2]);
} catch(e) {}

// ── Курсор-спутник: точка и кольцо рядом с системным указателем ──
if (window.matchMedia('(pointer: fine)').matches
    && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const dot  = document.getElementById('cursor-dot');
  const ring = document.getElementById('cursor-ring');

  let mx = -200, my = -200, rx = -200, ry = -200;

  document.addEventListener('mousemove', e => {
    mx = e.clientX; my = e.clientY;
    dot.style.left = mx + 'px';
    dot.style.top  = my + 'px';
  });

  (function rafLoop() {
    rx += (mx - rx) * 0.18;
    ry += (my - ry) * 0.18;
    ring.style.left = rx + 'px';
    ring.style.top  = ry + 'px';
    requestAnimationFrame(rafLoop);
  })();

  document.addEventListener('mouseenter', () => document.body.classList.add('cur-active'));
  document.addEventListener('mouseleave', () => document.body.classList.remove('cur-active'));

  const hoverSelector = 'a, button, .skill-filter, .skill-tile, .stack-tag, .status-item, .ach, ' +
    '.cert-pill, .edu-row, .job-company-block, .pl-stage';
  document.querySelectorAll(hoverSelector).forEach(el => {
    el.addEventListener('mouseenter', () => document.body.classList.add('cur-hover'));
    el.addEventListener('mouseleave', () => document.body.classList.remove('cur-hover'));
  });
}

// ── Interactive terminal ──
const _termInput = document.getElementById('term-input');
const _termOut   = document.getElementById('term-output');

const _termCmds = {
  help:       'contact · skills · location · ls\ngit log · sudo su\n\n── hotkeys ──\n[Tab]  autocomplete\n[↑]    previous command\n[↓]    next command',
  contact:    'TG:    @ktylhus\nemail: timir-ivaniv@yandex.ru',
  skills:     'K8s · Helm · ArgoCD · Vault\nTerraform · Ansible · GitLab CI\nPrometheus · Grafana · Loki',
  location:   'Saint Petersburg · UTC+3\nremote ✓ · occasional trips',
  ls:         'K8s         ✓ prod\nTerraform   ✓ no drift\nArgoCD      ✓ synced\nVault       ✓ unsealed\nGitLab CI   ✓ 100%',
  'git log':  '* feat: HA clusters · 99.9% uptime\n* feat: MTTD hours → 5 min\n* feat: server setup 2h → 15 min',
  'sudo su':  'Permission denied (insufficient coffee ☕)',
  sudo:       'Permission denied (insufficient coffee ☕)',
  exit:       'Nice try. The terminal stays open.',
  'rm -rf /': '🔥 …just kidding. Not today.',
  pwd:        '/home/temiriv/devops',
  uname:      'Linux devops-node 5.15.0-k8s #1 SMP x86_64',
};

if (_termInput) {
  const _history = [];
  let _histIdx = -1;

  _termInput.addEventListener('keydown', e => {
    // ── History navigation ──
    if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (_history.length === 0) return;
      _histIdx = Math.min(_histIdx + 1, _history.length - 1);
      _termInput.value = _history[_histIdx];
      return;
    }
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      _histIdx = Math.max(_histIdx - 1, -1);
      _termInput.value = _histIdx === -1 ? '' : _history[_histIdx];
      return;
    }

    // ── Tab autocomplete ──
    if (e.key === 'Tab') {
      e.preventDefault();
      const partial = _termInput.value.toLowerCase();
      if (!partial) return;
      const keys = Object.keys(_termCmds).filter(k => !k.includes(' '));
      const matches = keys.filter(k => k.startsWith(partial));
      if (matches.length === 1) {
        _termInput.value = matches[0];
      } else if (matches.length > 1) {
        _termOut.textContent = matches.join('   ');
        _termOut.className = 'term-output';
      }
      return;
    }

    if (e.key !== 'Enter') return;
    const cmd = _termInput.value.trim().toLowerCase();
    _termInput.value = '';
    if (!cmd) return;
    _history.unshift(cmd);
    _histIdx = -1;

    if (cmd === 'clear') { _termOut.textContent = ''; _termOut.className = 'term-output'; return; }

    const resp = _termCmds[cmd] ?? _termCmds[cmd.replace(/\/$/, '')];
    if (resp !== undefined) {
      _termOut.textContent = resp;
      _termOut.className = 'term-output';
    } else {
      _termOut.textContent = `command not found: ${cmd}\ntry 'help'`;
      _termOut.className = 'term-output err';
    }
  });
}

// ── Skill category filter ──
let _activeFilter = null;

function _clearFilter() {
  _activeFilter = null;
  document.querySelectorAll('.skill-tile').forEach(t => t.classList.remove('sf-dim', 'sf-on'));
  document.querySelectorAll('.skill-filter').forEach(b => {
    b.classList.remove('sf-active');
    b.setAttribute('aria-pressed', 'false');
  });
}

document.querySelectorAll('.skill-filter').forEach(btn => {
  btn.addEventListener('click', () => {
    const cat = btn.dataset.cat;
    const tiles = document.querySelectorAll('.skill-tile');
    const buttons = document.querySelectorAll('.skill-filter');

    if (_activeFilter === cat) {
      _clearFilter();
    } else {
      _activeFilter = cat;
      tiles.forEach(t => {
        const active = t.dataset.cat === cat;
        t.classList.toggle('sf-dim', !active);
        t.classList.toggle('sf-on', active);
      });
      buttons.forEach(b => {
        const on = b.dataset.cat === cat;
        b.classList.toggle('sf-active', on);
        b.setAttribute('aria-pressed', String(on));
      });
    }
  });
});

document.addEventListener('keydown', e => { if (e.key === 'Escape') _clearFilter(); });
document.addEventListener('click', e => { if (_activeFilter && !e.target.closest('#skills')) _clearFilter(); });

// ── Copy helper ──
function setupCopyCard(btnId, labelId, iconId, text) {
  const btn   = document.getElementById(btnId);
  const label = document.getElementById(labelId);
  const icon  = document.getElementById(iconId);
  const checkSvg = '<svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24" aria-hidden="true"><polyline points="20,6 9,17 4,12"/></svg>';
  const copySvg  = '<svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" aria-hidden="true"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>';

  if (!btn) return;

  function flash(msg, ok) {
    // Подпись живёт в соседней ссылке, а не внутри кнопки: подсветку вешаем
    // на строку целиком, чтобы значок и значение мигали вместе.
    const row = btn.closest('.tl-contact-row') || btn;
    label.textContent = msg;
    if (ok) { icon.innerHTML = checkSvg; row.classList.add('copied'); }
    setTimeout(() => {
      label.textContent = text;
      icon.innerHTML = copySvg;
      row.classList.remove('copied');
    }, 2000);
  }

  // Запасной путь: navigator.clipboard недоступен в незащищённом контексте и
  // в части старых браузеров. Без него кнопка молча ничего не делала.
  function legacyCopy() {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.cssText = 'position:fixed;top:-1000px;opacity:0';
    document.body.appendChild(ta);
    ta.select();
    let ok = false;
    try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
    document.body.removeChild(ta);
    return ok;
  }

  btn.addEventListener('click', () => {
    const isEn = document.body.classList.contains('lang-en');
    const done = () => flash(isEn ? '✓ Copied!' : '✓ Скопировано!', true);
    const failed = () => {
      if (legacyCopy()) { done(); return; }
      flash(isEn ? 'Copy failed — select manually' : 'Не скопировалось — выделите вручную', false);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done).catch(failed);
    } else {
      failed();
    }
  });
}

setupCopyCard('btn-copy-tg',    'btn-tg-label',   'copy-icon-tg', '@ktylhus');
setupCopyCard('btn-copy-email', 'btn-copy-label', 'copy-icon',    'timir-ivaniv@yandex.ru');

// ── Pipeline animation ──
(function () {
  const stages  = Array.from(document.querySelectorAll('.pl-stage'));
  const lines   = Array.from(document.querySelectorAll('.pl-line'));
  if (!stages.length) return;

  let running = false;

  function runPipeline() {
    if (running) return;
    running = true;
    stages.forEach(s => s.classList.remove('pl-run', 'pl-done'));
    lines.forEach(l => l.classList.remove('pl-done'));

    let i = 0;
    function step() {
      if (i >= stages.length) { running = false; return; }
      stages[i].classList.add('pl-run');
      setTimeout(() => {
        stages[i].classList.remove('pl-run');
        stages[i].classList.add('pl-done');
        if (lines[i]) {
          setTimeout(() => {
            lines[i].classList.add('pl-done');
            i++;
            setTimeout(step, 120);
          }, 280);
        } else {
          i++;
          running = false;
        }
      }, 520);
    }
    step();
  }

  // Автозапуск — украшение; кнопка «re-run» остаётся и в этом режиме.
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    setTimeout(runPipeline, 1600);
  } else {
    stages.forEach(st => st.classList.add('pl-done'));
    lines.forEach(l => l.classList.add('pl-done'));
  }

  document.querySelector('.pl-rerun')?.addEventListener('click', () => {
    if (!running) runPipeline();
  });
})();

// ── Frost sheen: feed the pointer position to the glass surfaces ──
(function () {
  if (!window.matchMedia('(pointer: fine) and (hover: hover)').matches) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const SEL = '.ach, .skill-tile, .job-company-block, .edu-row, .ticket,' +
              '.hero-terminal, .cta-terminal, .status-line';
  let latest = null, queued = false;

  // One delegated listener, rAF-throttled — cheaper than binding ~70 cards.
  document.addEventListener('mousemove', e => {
    latest = e;
    if (queued) return;
    queued = true;
    requestAnimationFrame(() => {
      queued = false;
      const card = latest.target.closest && latest.target.closest(SEL);
      if (!card) return;
      const r = card.getBoundingClientRect();
      card.style.setProperty('--mx', (latest.clientX - r.left) + 'px');
      card.style.setProperty('--my', (latest.clientY - r.top) + 'px');
    });
  }, { passive: true });
})();

// ── Tilt + shine: removed.
// The Slash system defines elevation through surface steps and 1px hairlines,
// never through shadows or 3D transforms. Cards stay flat on purpose.

// ── Full-page network background ──
(function () {
  const canvas = document.getElementById('bg-net');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // На тач-устройствах бесконечный цикл с попарным перебором узлов греет
  // батарею ради фона, который там почти не читается. Как и курсор, выключаем.
  const coarse = window.matchMedia('(pointer: coarse)').matches;
  if (coarse) { canvas.style.display = 'none'; return; }

  let w, h, nodes, dpr = Math.min(window.devicePixelRatio || 1, 2);
  const COUNT = 70;
  const LINK_DIST = 150;

  function resize() {
    w = window.innerWidth;
    h = window.innerHeight;
    canvas.width  = w * dpr;
    canvas.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function init() {
    resize();
    nodes = Array.from({ length: COUNT }, () => ({
      x: Math.random() * w,
      y: Math.random() * h,
      vx: (Math.random() - 0.5) * 0.16,
      vy: (Math.random() - 0.5) * 0.16,
    }));
  }

  function frame() {
    ctx.clearRect(0, 0, w, h);
    nodes.forEach(n => {
      n.x += n.vx; n.y += n.vy;
      if (n.x < 0 || n.x > w) n.vx *= -1;
      if (n.y < 0 || n.y > h) n.vy *= -1;
    });
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const dx = nodes[i].x - nodes[j].x, dy = nodes[i].y - nodes[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < LINK_DIST) {
          ctx.strokeStyle = `rgba(186,215,247,${0.14 * (1 - dist / LINK_DIST)})`;
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(nodes[i].x, nodes[i].y);
          ctx.lineTo(nodes[j].x, nodes[j].y);
          ctx.stroke();
        }
      }
    }
    nodes.forEach(n => {
      ctx.fillStyle = 'rgba(209,228,250,.45)';
      ctx.beginPath();
      ctx.arc(n.x, n.y, 1.6, 0, Math.PI * 2);
      ctx.fill();
    });
    if (!reduce) requestAnimationFrame(frame);
  }

  init();
  window.addEventListener('resize', resize);
  if (reduce) { frame(); } else { requestAnimationFrame(frame); }
})();

// ── Saint Petersburg live clock ──
(function () {
  const el = document.getElementById('spb-clock');
  if (!el) return;
  // Форматтер тяжёлый и неизменный — один на модуль, а не новый каждую секунду.
  const fmt = new Intl.DateTimeFormat('en-GB', {
    timeZone: 'Europe/Moscow',
    hour: '2-digit', minute: '2-digit', second: '2-digit',
    hour12: false,
  });
  function tick() {
    el.textContent = `${fmt.format(new Date())} MSK`;
  }
  tick();
  setInterval(tick, 1000);
})();
