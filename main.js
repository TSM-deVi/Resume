// ── Scroll progress + Back to top + Nav shadow ──
const backBtn      = document.getElementById('back-to-top');
const nav          = document.querySelector('nav');
const progressBar  = document.getElementById('scroll-progress');

window.addEventListener('scroll', () => {
  const scrollY   = window.scrollY;
  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  progressBar.style.width = (scrollY / docHeight * 100) + '%';
  backBtn.classList.toggle('visible', scrollY > 400);
  nav.classList.toggle('scrolled', scrollY > 10);
});

backBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

// ── Scroll reveal ──
const revealObs = new IntersectionObserver(
  entries => entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('v'); }),
  { threshold: 0.1 }
);
document.querySelectorAll('.r').forEach(el => revealObs.observe(el));

// ── Counter animation ──
function runCounter(el) {
  const text = el.dataset.text;
  if (text) { el.textContent = text; return; }

  const target = parseInt(el.dataset.count, 10);
  const suffix = el.dataset.suffix || '+';
  const steps  = 55;
  let i = 0;

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
  hamburger.classList.toggle('open');
  navMenu.classList.toggle('open');
});

navMenu.querySelectorAll('a').forEach(a => {
  a.addEventListener('click', () => {
    hamburger.classList.remove('open');
    navMenu.classList.remove('open');
  });
});

// ── Language toggle ──
const langBtn   = document.getElementById('lang-toggle');
const htmlRoot  = document.getElementById('html-root');
let lang = localStorage.getItem('lang') || 'ru';

function applyLang(l) {
  if (l === 'en') {
    document.body.classList.add('lang-en');
    htmlRoot.lang    = 'en';
    langBtn.textContent = 'RU';
  } else {
    document.body.classList.remove('lang-en');
    htmlRoot.lang    = 'ru';
    langBtn.textContent = 'EN';
  }
  localStorage.setItem('lang', l);
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
  _typeTW(isEn ? heroRole.dataset.textEn : heroRole.dataset.textRu, 45, _scheduleLive);
}
startTypewriter();

// ── Console Easter Egg ──
try {
  const _cs = [
    'color:#818cf8;font-family:monospace;font-size:12px;line-height:1.6;',
    'color:#22c55e;font-family:monospace;font-size:11px;',
    'color:#94a3b8;font-family:monospace;font-size:11px;',
  ];
  console.log(
    '%c╔══════════════════════════════════════════════╗\n' +
    '║  $ whoami                                    ║\n' +
    '║  > Ivanov Temir · Middle DevOps Engineer     ║\n' +
    '║                                              ║\n' +
    '║  $ kubectl get contact                       ║\n' +
    '║  > TG:    @ktylhus                           ║\n' +
    '║  > email: timir-ivaniv@yandex.ru             ║\n' +
    '╚══════════════════════════════════════════════╝', _cs[0]
  );
  console.log('%c● open to work · remote / hybrid', _cs[1]);
  console.log('%cLooking for a DevOps engineer? Let\'s talk!', _cs[2]);
} catch(e) {}

// ── Custom cursor ──
if (window.matchMedia('(pointer: fine)').matches) {
  const dot  = document.getElementById('cursor-dot');
  const ring = document.getElementById('cursor-ring');

  let mx = -200, my = -200, rx = -200, ry = -200;

  document.addEventListener('mousemove', e => {
    mx = e.clientX; my = e.clientY;
    dot.style.left = mx + 'px';
    dot.style.top  = my + 'px';
  });

  (function rafLoop() {
    rx += (mx - rx) * 0.16;
    ry += (my - ry) * 0.16;
    ring.style.left = rx + 'px';
    ring.style.top  = ry + 'px';
    requestAnimationFrame(rafLoop);
  })();

  document.addEventListener('mouseenter', () => document.body.classList.add('cur-active'));
  document.addEventListener('mouseleave', () => document.body.classList.remove('cur-active'));

  document.querySelectorAll('a, button, .sg-label, .chip-cat, .stack-tag, .stat, .ach, .cert-card, .edu-card, .job-company-block').forEach(el => {
    el.addEventListener('mouseenter', () => document.body.classList.add('cur-hover'));
    el.addEventListener('mouseleave', () => document.body.classList.remove('cur-hover'));
  });
}

// ── Interactive terminal ──
const _termInput = document.getElementById('term-input');
const _termOut   = document.getElementById('term-output');

const _termCmds = {
  help:       'contact · skills · location · ls\nclear · git log · sudo su',
  contact:    'TG:    @ktylhus\nemail: timir-ivaniv@yandex.ru',
  skills:     'K8s · Helm · ArgoCD · Vault\nTerraform · Ansible · GitLab CI\nPrometheus · Grafana · Loki',
  location:   'Saint Petersburg · UTC+3\nremote / hybrid ✓',
  ls:         'experience/  skills/  certs/\nachievements/ education/',
  'git log':  '* feat: HA clusters · 99.9% uptime\n* feat: MTTD hours → 5 min\n* feat: server setup 2h → 15 min',
  'sudo su':  'Permission denied (insufficient coffee ☕)',
  sudo:       'Permission denied (insufficient coffee ☕)',
  exit:       'Nice try. The terminal stays open.',
  'rm -rf /': '🔥 ...just kidding. Not today.',
  pwd:        '/home/temiriv/devops',
  uname:      'Linux devops-node 5.15.0-k8s #1 SMP x86_64',
};

if (_termInput) {
  _termInput.addEventListener('keydown', e => {
    if (e.key !== 'Enter') return;
    const cmd = _termInput.value.trim().toLowerCase();
    _termInput.value = '';
    if (!cmd) return;

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
  document.querySelectorAll('.skill-row').forEach(r => r.classList.remove('sf-dim', 'sf-on'));
}

document.querySelectorAll('.sg-label').forEach(lbl => {
  lbl.addEventListener('click', () => {
    const row = lbl.closest('.skill-row');
    const cat = row.dataset.cat;
    const rows = document.querySelectorAll('.skill-row');

    if (_activeFilter === cat) {
      _clearFilter();
    } else {
      _activeFilter = cat;
      rows.forEach(r => {
        const active = r.dataset.cat === cat;
        r.classList.toggle('sf-dim', !active);
        r.classList.toggle('sf-on', active);
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
  const checkSvg = '<svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20,6 9,17 4,12"/></svg>';
  const copySvg  = '<svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>';

  if (!btn) return;
  btn.addEventListener('click', () => {
    navigator.clipboard.writeText(text).then(() => {
      label.textContent = document.body.classList.contains('lang-en') ? '✓ Copied!' : '✓ Скопировано!';
      icon.innerHTML = checkSvg;
      btn.classList.add('copied');
      setTimeout(() => {
        label.textContent = text;
        icon.innerHTML = copySvg;
        btn.classList.remove('copied');
      }, 2000);
    });
  });
}

setupCopyCard('btn-copy-tg',    'btn-tg-label',   'copy-icon-tg', '@ktylhus');
setupCopyCard('btn-copy-email', 'btn-copy-label', 'copy-icon',    'timir-ivaniv@yandex.ru');
