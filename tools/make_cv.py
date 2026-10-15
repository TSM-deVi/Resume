# -*- coding: utf-8 -*-
"""Собирает cv.html — печатную версию резюме на одном источнике с сайтом.

Страница светлая: резюме печатают и пересылают файлом. Акцент — тёмный зелёный
той же семьи, что на сайте (#2e7a4c: сайтовый #4fae7c на белом дал бы 2.7:1),
шрифты те же — Geist и Geist Mono.

Запуск из любой папки:  python tools/make_cv.py  → пишет cv.html в корень.
"""
import io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from hl_data import DUC, SLETAT_DEVOPS, SLETAT_SYS, REAL_DEVOPS, REAL_SYS, FORUM

SITE = 'https://tsm-devi.github.io/Resume/'

JOBS = [
    ('ООО ДЮК Технологии', 'DUC Technologies', 'апр 2026 — июл 2026', 'Apr 2026 — Jul 2026',
     [('DevOps-инженер', 'DevOps Engineer', DUC)]),
    ('Слетать.ру', 'Sletat.ru', 'фев 2024 — апр 2026', 'Feb 2024 — Apr 2026',
     [('DevOps-инженер', 'DevOps Engineer', SLETAT_DEVOPS),
      ('Системный администратор', 'System Administrator', SLETAT_SYS)]),
    ('РеалЪ ТД, ООО', 'Real TD', 'авг 2022 — фев 2024', 'Aug 2022 — Feb 2024',
     [('Системный администратор / DevOps-инженер', 'System Administrator / DevOps Engineer', REAL_DEVOPS),
      ('Системный администратор / Специалист технической поддержки',
       'System Administrator / Technical Support Specialist', REAL_SYS)]),
    ('ООО «Форум»', 'Forum', 'май 2022 — июл 2022', 'May 2022 — Jul 2022',
     [('Системный администратор', 'System Administrator', FORUM)]),
]

FACTS = [
    ('63', '63', 'VM в трёх контурах', 'VMs across three environments'),
    ('70+', '70+', 'сервисов в эксплуатации', 'services in operation'),
    ('40 → 8 мин', '40 → 8 min', 'время деплоя', 'deploy time'),
    ('часы → 5 мин', 'hours → 5 min', 'обнаружение инцидентов', 'incident detection'),
]

# Стек по типам, с раскрытием: дистрибутивы, компоненты, состав кластеров.
# Версии продуктов не указаны: в резюме их нет.
STACK = [
    ('ОС и платформы', 'OS & platforms',
     'Linux — Debian, Ubuntu (администрирование, systemd, networking) · '
     'Windows Server — IIS, Active Directory, групповые политики, DNS, DHCP, RDS и RDP, PowerShell',
     'Linux — Debian, Ubuntu (administration, systemd, networking) · '
     'Windows Server — IIS, Active Directory, group policies, DNS, DHCP, RDS and RDP, PowerShell'),
    ('Контейнеры и оркестрация', 'Containers & orchestration',
     'Docker · Docker Compose · Kubernetes с нуля в трёх средах — bare-metal на физических серверах, ВМ в приватном '
     'облаке VMware Cloud Director, single-node k3s на ВМ в публичном облаке '
     '(etcd, CNI, storage, обновления, Ingress, HPA, RBAC, namespace-изоляция) · '
     'ресурсные лимиты · Helm · Longhorn',
     'Docker · Docker Compose · Kubernetes from scratch in three environments — bare metal on physical servers, '
     'VMs in a private VMware Cloud Director cloud, single-node k3s on a VM in a public cloud '
     '(etcd, CNI, storage, upgrades, Ingress, HPA, RBAC, namespace isolation) · '
     'resource limits · Helm · Longhorn'),
    ('CI/CD и GitOps', 'CI/CD & GitOps',
     'GitLab CI/CD — GitLab CE, GitLab Runner · Jenkins · ArgoCD · '
     'полный цикл: линтинг (hadolint, yamllint) → сборка (Docker, multi-stage) → '
     'тесты (pytest, coverage) → сканирование (Trivy, Gitleaks) → '
     'публикация образа в Harbor → деплой на ВМ и в Kubernetes',
     'GitLab CI/CD — GitLab CE, GitLab Runner · Jenkins · ArgoCD · '
     'full cycle: linting (hadolint, yamllint) → build (Docker, multi-stage) → '
     'tests (pytest, coverage) → scanning (Trivy, Gitleaks) → '
     'image publishing to Harbor → deploy to VMs and Kubernetes'),
    ('IaC и автоматизация', 'IaC & automation',
     'Terraform · Ansible — роли, плейбуки, идемпотентность · Python · Bash · PowerShell',
     'Terraform · Ansible — roles, playbooks, idempotency · Python · Bash · PowerShell'),
    ('Service mesh, доступ, безопасность', 'Service mesh, access, security',
     'Istio + Kiali — Gateway, VirtualService, DestinationRule, ServiceEntry, AuthorizationPolicy, '
     'WorkloadGroup · Envoy + OPA/OPAL через ext_authz · Keycloak/OIDC SSO · '
     'HashiCorp Vault (секреты, токены, схема External Secrets) · Secret Server · Passbolt · '
     'Trivy и Gitleaks — сканирование образов и поиск утечек секретов · '
     'bastion и jump host, firewall и NAT, сегментация сетей, UFW, TLS/PKI',
     'Istio + Kiali — Gateway, VirtualService, DestinationRule, ServiceEntry, AuthorizationPolicy, '
     'WorkloadGroup · Envoy + OPA/OPAL through ext_authz · Keycloak/OIDC SSO · '
     'HashiCorp Vault (secrets, tokens, External Secrets design) · Secret Server · Passbolt · '
     'Trivy and Gitleaks — image scanning and secret-leak detection · '
     'bastion and jump host, firewall and NAT, network segmentation, UFW, TLS/PKI'),
    ('Реестры и артефакты', 'Registries & artifacts',
     'Harbor — проекты, retention-политики, робот-аккаунты · GitLab Container Registry с pull secrets · '
     'Verdaccio — приватный npm-registry с проксированием npmjs · MinIO · S3 в Yandex Cloud',
     'Harbor — projects, retention policies, robot accounts · GitLab Container Registry with pull secrets · '
     'Verdaccio — a private npm registry proxying npmjs · MinIO · S3 in Yandex Cloud'),
    ('Наблюдаемость', 'Observability',
     'Prometheus + Grafana · Alertmanager · Loki + Promtail · '
     'ELK — Elasticsearch, Logstash, Kibana · Graylog · Sentry · Zabbix в HA-кластере на двух нодах · '
     'Uptime Kuma · LibreNMS + Oxidized · NetBox',
     'Prometheus + Grafana · Alertmanager · Loki + Promtail · '
     'ELK — Elasticsearch, Logstash, Kibana · Graylog · Sentry · Zabbix in a two-node HA cluster · '
     'Uptime Kuma · LibreNMS + Oxidized · NetBox'),
    ('Базы данных и хранилища', 'Databases & storage',
     'PostgreSQL + Patroni + etcd — отказоустойчивый кластер на трёх нодах, uptime 99.9% · '
     'MS SQL Server с репликацией master-slave · MySQL · MongoDB · '
     'ClickHouse — аналитическое хранилище ~4 ТБ · Qdrant · Vespa',
     'PostgreSQL + Patroni + etcd — a fault-tolerant three-node cluster, 99.9% uptime · '
     'MS SQL Server with master-slave replication · MySQL · MongoDB · '
     'ClickHouse — a ~4 TB analytics store · Qdrant · Vespa'),
    ('Очереди и служебные сервисы', 'Messaging & platform services',
     'Kafka — топики, партиции, политики хранения, мониторинг лага консьюмеров · '
     'RabbitMQ — очереди, exchange, DLQ, разграничение по vhost · '
     'Redis — кэш и сессии · Consul — service discovery, health-checks, KV · '
     'Unleash — feature-флаги',
     'Kafka — topics, partitions, retention policies, consumer lag monitoring · '
     'RabbitMQ — queues, exchanges, DLQ, access separation by vhost · '
     'Redis — cache and sessions · Consul — service discovery, health checks, KV · '
     'Unleash — feature flags'),
    ('Web и балансировка', 'Web & load balancing',
     'Nginx — reverse proxy, TLS-терминация, балансировка, заголовки CSP · HAProxy + Keepalived',
     'Nginx — reverse proxy, TLS termination, load balancing, CSP headers · HAProxy + Keepalived'),
    ('Виртуализация и облака', 'Virtualization & clouds',
     'VMware vSphere и Cloud Director — виртуальные ЦОД (vDC), vApp, firewall и NAT · Hyper-V · '
     'Veeam Backup &amp; Replication — резервное копирование и восстановление · антивирусная защита · '
     'Cloud.ru · Timeweb Cloud · Yandex Cloud',
     'VMware vSphere and Cloud Director — virtual data centres (vDC), vApp, firewall and NAT · Hyper-V · '
     'Veeam Backup &amp; Replication — backup and restore · antivirus protection · '
     'Cloud.ru · Timeweb Cloud · Yandex Cloud'),
    ('LLM-платформа', 'LLM platform',
     'LiteLLM · Ollama · GigaChat · Langflow · Langfuse · SmartSearch · '
     'векторный поиск на Qdrant и Vespa',
     'LiteLLM · Ollama · GigaChat · Langflow · Langfuse · SmartSearch · '
     'vector search on Qdrant and Vespa'),
    ('Внешний периметр и DNS', 'External perimeter & DNS',
     'Cloudflare, Qrator — проксирование внешнего домена, защита от DDoS и фильтрация трафика '
     'на периметре · внешние DNS-записи: A, CNAME, MX, TXT (SPF, DKIM, DMARC) · внутренний DNS · '
     'Let’s Encrypt и внутренний центр сертификации',
     'Cloudflare, Qrator — external domain proxying, DDoS protection and edge traffic filtering · '
     'external DNS records: A, CNAME, MX, TXT (SPF, DKIM, DMARC) · internal DNS · '
     'Let’s Encrypt and an internal certificate authority'),
    ('Сетевое оборудование и VPN', 'Network equipment & VPN',
     'MikroTik · Cisco · Kerio VPN · маршрутизация и коммутация · VPN между объектами',
     'MikroTik · Cisco · Kerio VPN · routing and switching · site-to-site VPN'),
    ('Управление и инструменты', 'Management & tools',
     'Git · Jira и Jira Service Desk · Confluence — администрирование и развёртывание · '
     'Zimbra · Exchange · Outlook · IMAP/SMTP · OCS Inventory',
     'Git · Jira and Jira Service Desk · Confluence — administration and deployment · '
     'Zimbra · Exchange · Outlook · IMAP/SMTP · OCS Inventory'),
]

EDU = [
    ('2020', 'КГУ им. Б.Б. Городовикова', 'Kalmyk State University',
     'Информационная безопасность', 'Information Security',
     'Неоконченное высшее', 'Incomplete higher education'),
    ('2019', 'КГУ им. Б.Б. Городовикова', 'Kalmyk State University',
     'Программирование в компьютерных системах — техник-программист',
     'Computer Systems Programming — programmer technician',
     'Среднее специальное', 'Vocational education'),
]

ABOUT = (
    'Самостоятельно реализую проекты от проектирования до продакшена: разворачиваю контуры '
    'с нуля, строю CI/CD и наблюдаемость, отвечаю за эксплуатацию.',
    'I deliver projects end to end — building environments from scratch, setting up CI/CD and '
    'observability, and owning them in production.')

GOAL = (
    'Ищу позицию DevOps / Platform Engineer. Интересны Kubernetes, CI/CD, IaC, внутренние '
    'платформы и отказоустойчивая инфраструктура; развиваюсь в сторону Platform Engineering и SRE, '
    'отдельно интересна эксплуатация инфраструктуры LLM-платформ.',
    'Looking for a DevOps / Platform Engineer role. Interested in Kubernetes, CI/CD, IaC, '
    'internal platforms and fault-tolerant infrastructure; growing towards Platform Engineering and SRE, '
    'with a particular interest in running LLM-platform infrastructure.')

# Курсов три: BASE, PRO и EXP.
CERTS = [('BASE', 'Базовый курс', 'Foundational course'),
         ('PRO', 'Профессиональный курс', 'Professional course'),
         ('EXP', 'Экспертный курс', 'Expert course')]
CERT_ISSUER = ('Облако VMware · 2026', 'VMware Cloud · 2026')

LANGS = [('Русский', 'Russian', 'родной', 'native'),
         ('Английский', 'English', 'B1 — средний', 'B1 — intermediate')]


def L(ru, en, tag='span', cls=''):
    c = ' class="%s"' % cls if cls else ''
    return ('<%s%s data-lang="ru">%s</%s><%s%s data-lang="en">%s</%s>'
            % (tag, c, ru, tag, tag, c, en, tag))


def for_cv(items):
    """Пункты для печатного CV: без меток 'site' (см. hl_data.py)."""
    return [it for it in items if len(it) < 3 or it[2] != 'site']


def bullets(items):
    return '\n'.join('        <li>%s</li>' % L(it[0], it[1], 'span') for it in for_cv(items))


jobs_html = []
for ru_name, en_name, ru_per, en_per, roles in JOBS:
    rr = []
    for ru_role, en_role, items in roles:
        rr.append('''      <div class="role">
        <div class="role-t">%s</div>
        <ul>
%s
        </ul>
      </div>''' % (L(ru_role, en_role), bullets(items)))
    jobs_html.append('''    <article class="job">
      <header class="job-h">
        <h3>%s</h3>
        <span class="per">%s</span>
      </header>
%s
    </article>''' % (L(ru_name, en_name), L(ru_per, en_per), '\n'.join(rr)))

facts_html = '\n'.join(
    '      <div class="fact"><b>%s</b>%s</div>' % (L(rv, ev), L(ru, en, 'i'))
    for rv, ev, ru, en in FACTS)

stack_html = '\n'.join(
    '      <div class="srow"><span class="sk">%s</span><span class="sv">%s</span></div>'
    % (L(ru, en), L(rt, et)) for ru, en, rt, et in STACK)

edu_html = '\n'.join(
    '''      <div class="erow">
        <span class="eyr">%s</span>
        <span class="ebody"><b>%s</b><br>%s<br><i>%s</i></span>
      </div>''' % (yr, L(ru_n, en_n), L(ru_d, en_d), L(ru_b, en_b))
    for yr, ru_n, en_n, ru_d, en_d, ru_b, en_b in EDU)

certs_html = '\n'.join(
    '''      <div class="crow">
        <span class="cbadge">%s</span>
        <span class="cbody">%s <span class="cissuer">%s</span></span>
      </div>''' % (t, L(ru, en), L(*CERT_ISSUER))
    for t, ru, en in CERTS)

langs_html = ' &middot; '.join('%s — %s' % (L(ru, en), L(lru, len_)) for ru, en, lru, len_ in LANGS)

HTML = '''<!DOCTYPE html>
<html lang="ru" id="root">
<head>
<meta charset="utf-8">
<title>Иванов Темир — DevOps-инженер</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<link rel="icon" href="favicon-32.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Geist+Mono:wght@400;500&display=swap">
<style>
  :root {
    --ink:#151716; --mute:#5c625e; --line:#dde1de; --accent:#2e7a4c; --wash:#eef4f0;
    --ui:'Geist',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
    --mono:'Geist Mono',ui-monospace,'SFMono-Regular',Consolas,monospace;
  }
  *{box-sizing:border-box}
  body{margin:0;background:#eef0ee;color:var(--ink);font-family:var(--ui);
       font-size:10.2pt;line-height:1.5;-webkit-font-smoothing:antialiased}
  .sheet{max-width:210mm;margin:0 auto;background:#fff;padding:16mm 15mm 14mm}
  h1{font-size:24pt;line-height:1.08;margin:0;letter-spacing:-.02em;font-weight:700}
  .role-line{font-family:var(--mono);font-size:10pt;color:var(--accent);
             margin:.35rem 0 0;letter-spacing:.01em}
  .meta{margin-top:.7rem;font-size:9.4pt;color:var(--mute)}
  .meta a{color:var(--ink);text-decoration:none;border-bottom:1px solid var(--line)}
  h2{font-family:var(--mono);font-size:8.6pt;letter-spacing:.14em;text-transform:uppercase;
     color:var(--mute);margin:9mm 0 3mm;padding-bottom:1.6mm;border-bottom:1px solid var(--line);
     font-weight:500}
  .facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(38mm,1fr));gap:3mm 4mm}
  .fact{background:var(--wash);border-radius:5px;padding:3mm 3.5mm}
  .fact b{display:block;font-size:13pt;font-weight:600;letter-spacing:-.01em}
  .fact i{display:block;font-style:normal;font-size:8.4pt;color:var(--mute);margin-top:.6mm}
  .job{margin-bottom:6mm;break-inside:avoid}
  .job-h{display:flex;justify-content:space-between;align-items:baseline;gap:6mm;
         border-left:2px solid var(--accent);padding-left:3mm}
  .job-h h3{margin:0;font-size:11.4pt;font-weight:600}
  .per{font-family:var(--mono);font-size:8.6pt;color:var(--mute);white-space:nowrap}
  .role{padding-left:3mm;margin-top:2.4mm}
  .role-t{font-size:9.6pt;font-weight:500;color:var(--accent);margin-bottom:1.4mm}
  .role ul{margin:0;padding-left:4.4mm}
  .role li{margin-bottom:1.5mm}
  .role li::marker{color:var(--accent)}
  strong{font-weight:600}
  .srow{display:flex;gap:4mm;margin-bottom:2mm;break-inside:avoid}
  .sk{flex:0 0 40mm;font-size:8.8pt;color:var(--mute)}
  .sv{flex:1;font-family:var(--mono);font-size:8.8pt;line-height:1.55}
  .erow{display:flex;gap:4mm;margin-bottom:2.6mm;break-inside:avoid}
  .eyr{flex:0 0 14mm;font-family:var(--mono);font-size:9pt;color:var(--accent)}
  .ebody{font-size:9.4pt}
  .ebody i{font-style:normal;color:var(--mute);font-size:8.6pt}
  .crow{display:flex;gap:4mm;align-items:baseline;margin-bottom:1.8mm;break-inside:avoid}
  .cbadge{flex:0 0 14mm;font-family:var(--mono);font-size:8.6pt;font-weight:500;
          color:var(--accent);letter-spacing:.06em}
  .cbody{font-size:9.4pt}
  .cissuer{color:var(--mute);font-size:8.6pt}
  .langs{margin-top:3mm;font-size:9.2pt;color:var(--mute)}
  .about{margin:4mm 0 0;font-size:9.6pt;max-width:62ch}
  .goal{margin:5mm 0 0;padding:3mm 3.5mm;background:var(--wash);border-radius:5px;
        font-size:9.2pt}
  .foot{margin-top:8mm;padding-top:3mm;border-top:1px solid var(--line);
        font-size:8.6pt;color:var(--mute)}
  /* Панель управления на экране; на печати её нет. */
  .bar{position:sticky;top:0;z-index:5;display:flex;gap:8px;justify-content:center;
       padding:10px;background:rgba(238,240,244,.92);backdrop-filter:blur(8px)}
  .bar button,.bar a{font-family:var(--ui);font-size:13px;font-weight:500;
       padding:9px 16px;min-height:44px;display:inline-flex;align-items:center;
       border-radius:999px;border:1px solid var(--line);background:#fff;color:var(--ink);
       cursor:pointer;text-decoration:none}
  .bar button.primary{background:var(--accent);border-color:var(--accent);color:#fff}
  html:not(.lang-en) [data-lang="en"]{display:none}
  html.lang-en [data-lang="ru"]{display:none}
  /* Цель — два листа A4: интервалы подобраны под это. */
  @media print{
    @page{size:A4;margin:11mm}
    body{background:#fff;font-size:8.5pt;line-height:1.31}
    .sheet{max-width:none;padding:0;margin:0}
    .bar{display:none}
    h1{font-size:17pt}
    .role-line{font-size:8.6pt}
    .meta{margin-top:.3rem;font-size:8pt}
    h2{margin:2.9mm 0 1.2mm;font-size:7.4pt;padding-bottom:.9mm}
    .facts{grid-template-columns:repeat(4,1fr);gap:1.4mm}
    .fact{padding:1.6mm 2mm}
    .fact b{font-size:9.6pt}
    .fact i{font-size:6.9pt}
    .job{margin-bottom:2.6mm}
    .job-h h3{font-size:10pt}
    .per{font-size:7.8pt}
    .role{margin-top:1.2mm}
    .role-t{font-size:8.6pt;margin-bottom:.9mm}
    .role li{margin-bottom:.4mm}
    .srow{margin-bottom:.42mm}
    .sk{flex-basis:29mm;font-size:7.1pt}
    .sv{font-size:6.9pt;line-height:1.32}
    .erow{margin-bottom:1.2mm}
    .crow{margin-bottom:1mm}
    .cbody{font-size:8.4pt}
    .cbadge{flex-basis:12mm;font-size:8pt}
    .cissuer{font-size:7.8pt}
    .langs{margin-top:1.6mm;font-size:8pt}
    .ebody{font-size:8.4pt}
    .about{margin-top:1.7mm;font-size:8.1pt;max-width:none}
    .goal{margin-top:2mm;padding:1.5mm 2mm;font-size:7.6pt}
    .foot{margin-top:2.2mm;padding-top:1.5mm;font-size:7.2pt}
    a{color:inherit}
  }
</style>
</head>
<body>

<div class="bar">
  <button class="primary" id="print" type="button">%(btn_print)s</button>
  <button id="lang" type="button">EN</button>
  <a href="./">%(btn_site)s</a>
</div>

<main class="sheet">
  <h1>%(name)s</h1>
  <div class="role-line">DevOps / Platform Engineer</div>
  <div class="meta">
    %(city)s &middot; timir-ivaniv@yandex.ru &middot; telegram @ktylhus
    &middot; <a href="%(site)s">%(site_label)s</a>
  </div>

  <p class="about">%(about)s</p>

  <h2>%(h_facts)s</h2>
  <div class="facts">
%(facts)s
  </div>

  <h2>%(h_exp)s</h2>
%(jobs)s

  <h2>%(h_stack)s</h2>
%(stack)s

  <h2>%(h_edu)s</h2>
%(edu)s

  <h2>%(h_certs)s</h2>
%(certs)s
  <div class="langs">%(h_langs)s: %(langs)s</div>

  <p class="goal">%(goal)s</p>

  <div class="foot">%(foot)s</div>
</main>

<script>
  // Язык берём из адреса, чтобы ссылка с сайта открывала нужную версию.
  var root = document.getElementById('root');
  function setLang(l) {
    root.classList.toggle('lang-en', l === 'en');
    root.lang = l;
    document.getElementById('lang').textContent = l === 'en' ? 'RU' : 'EN';
    document.title = l === 'en'
      ? 'Ivanov Temir \\u2014 DevOps Engineer'
      : '\\u0418\\u0432\\u0430\\u043d\\u043e\\u0432 \\u0422\\u0435\\u043c\\u0438\\u0440 \\u2014 DevOps-\\u0438\\u043d\\u0436\\u0435\\u043d\\u0435\\u0440';
  }
  var q = new URLSearchParams(location.search).get('lang');
  var cur = q === 'en' ? 'en' : 'ru';
  setLang(cur);
  document.getElementById('lang').addEventListener('click', function () {
    cur = cur === 'ru' ? 'en' : 'ru';
    setLang(cur);
    var u = new URL(location.href);
    if (cur === 'en') u.searchParams.set('lang', 'en'); else u.searchParams.delete('lang');
    history.replaceState(null, '', u);
  });
  document.getElementById('print').addEventListener('click', function () { window.print(); });
</script>
</body>
</html>
''' % {
    'btn_print': L('Сохранить в PDF', 'Save as PDF'),
    'btn_site': L('На сайт', 'Back to site'),
    'name': L('Иванов Темир', 'Ivanov Temir'),
    'city': L('удалённо', 'remote'),
    'site': SITE,
    'site_label': 'tsm-devi.github.io/Resume',
    'about': L(*ABOUT),
    'goal': L(*GOAL),
    'h_facts': L('Ключевое', 'Key figures'),
    'h_exp': L('Опыт', 'Experience'),
    'h_stack': L('Стек', 'Stack'),
    'h_edu': L('Образование', 'Education'),
    'h_certs': L('Сертификаты', 'Certifications'),
    'h_langs': L('Языки', 'Languages'),
    'langs': langs_html,
    'facts': facts_html,
    'jobs': '\n'.join(jobs_html),
    'stack': stack_html,
    'edu': edu_html,
    'certs': certs_html,
    'foot': L('Это выжимка. Развёрнутое резюме со всеми обязанностями — на hh.ru.',
              'This is a summary. The full resume with every responsibility is on hh.ru.'),
}

io.open(os.path.join(ROOT, 'cv.html'), 'w', encoding='utf-8').write(HTML)
n = sum(len(for_cv(items)) for _, _, _, _, roles in JOBS for _, _, items in roles)
print('cv.html собран: %d байт, пунктов опыта %d, компаний %d'
      % (len(HTML.encode('utf-8')), n, len(JOBS)))
