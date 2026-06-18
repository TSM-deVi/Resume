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

// ── Typewriter ──
function startTypewriter() {
  const el       = document.getElementById('typewriter-text');
  const heroRole = document.getElementById('hero-role');
  if (!el || !heroRole) return;
  const isEn = document.body.classList.contains('lang-en');
  const text = isEn ? heroRole.dataset.textEn : heroRole.dataset.textRu;
  el.textContent = '';
  clearInterval(window._twTimer);
  let i = 0;
  window._twTimer = setInterval(() => {
    el.textContent += text[i++];
    if (i >= text.length) clearInterval(window._twTimer);
  }, 40);
}
startTypewriter();

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
      label.textContent = '✓ Скопировано!';
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
