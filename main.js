// ── Scroll progress + Back to top + Nav shadow ──
const backBtn      = document.getElementById('back-to-top');
const nav          = document.querySelector('nav');
const progressBar  = document.getElementById('scroll-progress');

const _reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

let _scrollTicking = false;
function _onScroll() {
  const scrollY   = window.scrollY;
  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  progressBar.style.transform = 'scaleX(' + (docHeight > 0 ? scrollY / docHeight : 0) + ')';
  backBtn.classList.toggle('visible', scrollY > 400);
  nav.classList.toggle('scrolled', scrollY > 10);

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

// ── Пайплайн в шапке: три прогона, пока блок на экране ──
// CSS описывает один прогон; здесь он повторяется ещё дважды через 12 с,
// затем граф стоит пройденным. Джобы сбрасываются разом, как у нового пайплайна;
// вне экрана повторов нет, при возвращении — снова до трёх прогонов.
const plWrap = document.querySelector('.pipeline-wrap');
if (plWrap && plWrap.getAnimations && !_reduceMotion) {
  const PL_RUNS = 3;
  let plTimer = 0, plSeen = false, plLeft = 0;
  const plRestart = () => plWrap.getAnimations({ subtree: true })
    .forEach(a => { if (a.animationName) a.currentTime = 0; });
  new IntersectionObserver(([e]) => {
    clearInterval(plTimer);
    if (!e.isIntersecting) return;
    if (plSeen) plRestart();
    plSeen = true;
    plLeft = PL_RUNS - 1;
    plTimer = setInterval(() => {
      plRestart();
      if (--plLeft <= 0) clearInterval(plTimer);
    }, 12000);
  }, { threshold: 0.1 }).observe(plWrap);
}

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

// Заголовок вкладки и описание переключаются вместе с языком: иначе ссылка
// ?lang=en показывала бы русский title во вкладке и в превью.
const META = {
  ru: {
    title: 'Иванов Темир — DevOps-инженер',
    desc:  'DevOps-инженер. Kubernetes на bare-metal, ' +
           'VMware Cloud Director и k3s, GitLab CI/CD, ArgoCD, Terraform, Ansible, ' +
           'наблюдаемость. 63 VM в контурах DEV/INF/PROD, 70+ сервисов в эксплуатации.'
  },
  en: {
    title: 'Ivanov Temir — DevOps Engineer',
    desc:  'DevOps engineer. Kubernetes on bare-metal, ' +
           'VMware Cloud Director and k3s, GitLab CI/CD, ArgoCD, Terraform, Ansible, ' +
           'observability. 63 VMs across DEV/INF/PROD, 70+ services in operation.'
  }
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
  const meta = META[l] || META.ru;
  document.title = meta.title;
  const md = document.querySelector('meta[name="description"]');
  if (md) md.setAttribute('content', meta.desc);

  // Печатная версия открывается на том же языке, что и сайт.
  const cv = document.getElementById('cv-link');
  if (cv) cv.href = l === 'en' ? 'cv.html?lang=en' : 'cv.html';

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

// ── Typewriter ──
// Строка роли печатается один раз и остаётся.
function startTypewriter() {
  clearInterval(window._twTimer);
  const heroRole = document.getElementById('hero-role');
  const el = document.getElementById('typewriter-text');
  if (!heroRole || !el) return;
  const isEn = document.body.classList.contains('lang-en');
  const text = isEn ? heroRole.dataset.textEn : heroRole.dataset.textRu;
  if (_reduceMotion) { el.textContent = text; return; }
  el.textContent = '';
  let i = 0;
  window._twTimer = setInterval(() => {
    el.textContent += text[i++];
    if (i >= text.length) clearInterval(window._twTimer);
  }, 45);
}
startTypewriter();

// ── Длинные списки опыта: начало видно, остальное по кнопке ──
(function () {
  const LIMIT = 8;          // столько пунктов видно сразу
  const MIN_HIDDEN = 4;     // ради двух-трёх строк кнопку не заводим

  function plural(n) {
    const d10 = n % 10, d100 = n % 100;
    if (d10 === 1 && d100 !== 11) return 'пункт';
    if (d10 >= 2 && d10 <= 4 && (d100 < 12 || d100 > 14)) return 'пункта';
    return 'пунктов';
  }

  document.querySelectorAll('.jlist').forEach(list => {
    const items = Array.from(list.children);
    const hidden = items.slice(LIMIT);
    if (hidden.length < MIN_HIDDEN) return;

    hidden.forEach(li => li.classList.add('jl-hide'));

    const n = hidden.length;
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'jlist-more';
    btn.setAttribute('aria-expanded', 'false');
    // У должности два списка, ru и en: кнопка наследует язык своего списка,
    // иначе показывалась бы дважды.
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
    'color:#6cc493;font-family:monospace;font-size:12px;line-height:1.6;',
    'color:#eef0ee;font-family:monospace;font-size:11px;',
    'color:#8d948f;font-family:monospace;font-size:11px;',
  ];
  console.log(
    '%c╔══════════════════════════════════════════════╗\n' +
    '║  $ whoami                                    ║\n' +
    '║  > Ivanov Temir · DevOps Engineer            ║\n' +
    '║                                              ║\n' +
    '║  $ kubectl get contact                       ║\n' +
    '║  > TG:    @ktylhus                           ║\n' +
    '║  > email: timir-ivaniv@yandex.ru             ║\n' +
    '╚══════════════════════════════════════════════╝', _cs[0]
  );
  console.log('%c● open to work · remote', _cs[1]);
  console.log('%cLooking for a DevOps engineer? Let\'s talk!', _cs[2]);
} catch(e) {}

// ── Copy helper ──
function setupCopyCard(btnId, labelId, iconId, text) {
  const btn   = document.getElementById(btnId);
  const label = document.getElementById(labelId);
  const icon  = document.getElementById(iconId);
  const checkSvg = '<svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24" aria-hidden="true"><polyline points="20,6 9,17 4,12"/></svg>';
  const copySvg  = '<svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" aria-hidden="true"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>';

  if (!btn) return;

  function flash(msg, ok) {
    label.textContent = msg;
    if (ok) { icon.innerHTML = checkSvg; btn.classList.add('copied'); }
    setTimeout(() => {
      label.textContent = text;
      icon.innerHTML = copySvg;
      btn.classList.remove('copied');
    }, 2000);
  }

  // Запасной путь: navigator.clipboard недоступен в незащищённом контексте
  // и в части старых браузеров.
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

// Контакты — в карточке первого экрана: строка сама служит кнопкой копирования,
// поэтому подсветка .copied ложится прямо на неё.
setupCopyCard('hero-copy-tg',   'hero-tg-label',   'hero-ico-tg',   '@ktylhus');
setupCopyCard('hero-copy-mail', 'hero-mail-label', 'hero-ico-mail', 'timir-ivaniv@yandex.ru');

// ── Pointer sheen: feed the pointer position to the cards ──
(function () {
  if (!window.matchMedia('(pointer: fine) and (hover: hover)').matches) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const SEL = '.ach, .skill-chip, .job-company-block, .edu-row, .hero-cta,' +
              '.cta-terminal, .status-line';
  let latest = null, queued = false;

  // Один делегированный обработчик с rAF — дешевле, чем вешать на каждую карточку.
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
