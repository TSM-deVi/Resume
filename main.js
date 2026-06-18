// ── Back to top + Nav shadow ──
const backBtn = document.getElementById('back-to-top');
const nav = document.querySelector('nav');
window.addEventListener('scroll', () => {
  backBtn.classList.toggle('visible', window.scrollY > 400);
  nav.classList.toggle('scrolled', window.scrollY > 10);
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

// ── Copy email card ──
setupCopyCard('btn-copy-tg',    'btn-tg-label',    'copy-icon-tg', '@ktylhus');
setupCopyCard('btn-copy-email', 'btn-copy-label',  'copy-icon',    'timir-ivaniv@yandex.ru');

// ── Hero contact pills (copy only, no icon swap) ──
function setupPillCopy(btnId, text) {
  const btn = document.getElementById(btnId);
  if (!btn) return;
  btn.addEventListener('click', () => {
    navigator.clipboard.writeText(text).then(() => {
      btn.classList.add('copied');
      setTimeout(() => btn.classList.remove('copied'), 2000);
    });
  });
}

setupCopyCard('hero-btn-tg',    'hero-tg-val',    'hero-tg-icon',    '@ktylhus');
setupCopyCard('hero-btn-email', 'hero-email-val', 'hero-email-icon', 'timir-ivaniv@yandex.ru');
