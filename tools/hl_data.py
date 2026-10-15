# -*- coding: utf-8 -*-
"""Пункты опыта — единый источник для сайта и печатного резюме.

Отсюда пункты попадают в два места:
  tools/make_cv.py          → cv.html
  tools/sync_experience.py  → списки опыта в index.html
Править пункты руками в cv.html или index.html нельзя — следующая сборка
их перезапишет. Правится этот файл, затем запускаются оба скрипта.

Пункт — кортеж (ru, en) или (ru, en, 'site'). С меткой 'site' пункт идёт только
на сайт: в печатном CV эти технологии уже есть в разделе стека.
"""

# (ru, en) — по одному пункту на строку
DUC = [
 ('Проектная работа: production-контур мультиагентной low-code платформы для заказчика '
  'банковского сектора — спроектирован, развёрнут, сдан и закрыт в июле 2026',
  'Project work: the production environment of a multi-agent low-code platform for a banking-sector '
  'client — designed, deployed, handed over and closed in July 2026'),

 ('Развернул с нуля три изолированных контура <strong>DEV / INF / PROD</strong> в VMware Cloud Director: '
  'отдельные виртуальные ЦОД, группировка по vApp, сетевая сегментация — суммарно '
  '<strong>63 виртуальные машины</strong>',
  'Built three isolated <strong>DEV / INF / PROD</strong> environments from scratch in VMware Cloud Director: '
  'separate virtual data centres, vApp grouping, network segmentation — <strong>63 virtual machines</strong> '
  'in total'),

 ('DEV и PROD зеркальны 1:1, каждый — 28 VM / 90 vCPU / 191 GB RAM / 2.7 TB дисков; провёл '
  'right-sizing по компонентам и подготовил ресурсный план',
  'DEV and PROD mirror each other 1:1, each 28 VMs / 90 vCPU / 191 GB RAM / 2.7 TB of disk; I right-sized '
  'the components and prepared the resource plan'),

 ('INF — контур сквозных сервисов на <strong>7 VM</strong> (21 vCPU / 39 GB RAM / 0.9 TB): GitLab, центральный Harbor, Nginx, Prometheus, Grafana и Loki вынесены из прикладных контуров; реестр образов двухуровневый — центральный на INF, локальные на DEV и PROD: меньше внешнего трафика при сохранении изоляции',
  'INF is the shared-services environment on <strong>7 VMs</strong> (21 vCPU / 39 GB RAM / 0.9 TB): GitLab, the central Harbor, Nginx, Prometheus, Grafana and Loki moved out of the application environments; the image registry is two-tier — central on INF, local ones on DEV and PROD: less external traffic while isolation holds'),

 ('<strong>Kubernetes</strong> на виртуальных машинах (master + 3 worker), Helm-чарты, RBAC и namespace-изоляция; '
  '<strong>GitLab CI/CD</strong> с разделением dev/prod и ручными production-джобами; Terraform и Ansible '
  'для воспроизводимости окружений',
  '<strong>Kubernetes</strong> on virtual machines (master + 3 workers), Helm charts, RBAC and namespace isolation; '
  '<strong>GitLab CI/CD</strong> with dev/prod separation and manual production jobs; Terraform and Ansible '
  'for reproducible environments'),

 ('Изменения — только через merge request и CI-джобы, по схеме <strong>pre-check → change → verification → rollback</strong> со smoke-тестами на каждом шаге; вёл runbooks, change log и матрицу соответствия, сверял контуры с требованиями ПМИ/КБ/SOC',
  'Changes went only through merge requests and CI jobs, following <strong>pre-check → change → verification → rollback</strong> with smoke tests at every step; kept runbooks, a change log and a compliance matrix, checking the environments against the client’s acceptance, security and SOC requirements'),

 ('L3-связности между контурами нет — доступ открывался точечно через firewall и NAT. Вход администратора: '
  '<strong>PAM заказчика → jump host контура → целевая ВМ</strong>; для CI/CD отдельный путь — bastion на '
  'jump host DEV и PROD, через который раннер с INF ходит в прикладные контуры',
  'There is no L3 connectivity between environments — access was opened per service through firewall and NAT. '
  'Admin path: <strong>the client’s PAM → the environment’s jump host → the target VM</strong>; CI/CD has its '
  'own route through a bastion on the DEV and PROD jump hosts, which the INF runner uses to reach them'),

 ('Слой доступа и авторизации: <strong>Istio + Kiali</strong> для Kubernetes-нагрузок и сервисов на ВМ, авторизация <strong>Envoy + OPA/OPAL</strong> через ext_authz с политиками из GitLab, SSO через Keycloak/OIDC для SmartSearch, Langflow, Langfuse и Grafana',
  'Access and authorization layer: <strong>Istio + Kiali</strong> for Kubernetes workloads and VM-backed services, <strong>Envoy + OPA/OPAL</strong> authorization through ext_authz with policies pulled from GitLab, Keycloak/OIDC SSO for SmartSearch, Langflow, Langfuse and Grafana', 'site'),

 ('Сквозная наблюдаемость на Prometheus, Grafana, Loki и Promtail; разбирал production-инциденты — '
  'TLS SAN mismatch, Redis NOPERM, исчерпание PostgreSQL connections, MinIO mesh timeout, '
  'Vault sealed, переполнение диска Docker-логами',
  'End-to-end observability on Prometheus, Grafana, Loki and Promtail; handled production incidents — '
  'TLS SAN mismatch, Redis NOPERM, PostgreSQL connection exhaustion, MinIO mesh timeout, Vault sealed, '
  'disks filled by Docker logs'),

 ('Сопровождал LLM-слой платформы: LiteLLM, GigaChat, Ollama, векторный поиск на '
  '<strong>Qdrant и Vespa</strong>, Langflow, Langfuse и SmartSearch — отделял инфраструктурные '
  'отказы от ошибок внешних API и конфигурации',
  'Operated the platform’s LLM layer: LiteLLM, GigaChat, Ollama, vector search on '
  '<strong>Qdrant and Vespa</strong>, Langflow, Langfuse and SmartSearch — separating infrastructure '
  'failures from external API and configuration errors'),

 ('Отдельно воспроизвёл ту же архитектуру в одном контуре вместо трёх на Timeweb Cloud: уложил платформу '
  'с <strong>28 VM в 10 VM</strong> (34 vCPU, 96 GB, 1.8 TB NVMe) — single-node k3s на ВМ вместо кластера, standalone '
  'PostgreSQL и ClickHouse, сервисы на общих узлах',
  'Separately reproduced the same architecture in a single environment instead of three on Timeweb Cloud: '
  'fitted a platform of <strong>28 VMs into 10</strong> (34 vCPU, 96 GB, 1.8 TB NVMe) — single-node k3s on a VM instead of a cluster, '
  'standalone PostgreSQL and ClickHouse, services sharing nodes'),
]

SLETAT_DEVOPS = [
 ('Инфраструктурная команда из <strong>2 человек</strong> на <strong>50+ разработчиков</strong>: окружения, '
  'доступы, сертификаты, CI/CD и мониторинг для <strong>более 70 сервисов</strong> — 12+ микросервисов '
  'в Kubernetes, 40+ Node.js под pm2, 20–30 бэкендов на C#/.NET',
  'An infrastructure team of <strong>2</strong> serving <strong>50+ developers</strong>: environments, access, '
  'certificates, CI/CD and monitoring for <strong>70+ services</strong> — 12+ microservices in Kubernetes, '
  '40+ Node.js under pm2, 20–30 C#/.NET backends'),

 ('Гетерогенная инфраструктура: legacy .NET Framework под <strong>IIS на Windows Server</strong> '
  'и новые .NET-сервисы на Linux под systemd — выстроил CI/CD и сопровождение для обоих, '
  'сохранив исторический контур сборки на Jenkins рядом с новым конвейером на GitLab CI',
  'Heterogeneous infrastructure: legacy .NET Framework under <strong>IIS on Windows Server</strong> '
  'and new .NET services on Linux under systemd — built CI/CD and support for both, keeping the '
  'historical Jenkins build path alongside the new GitLab CI pipeline'),

 ('Развернул <strong>Kubernetes на bare-metal</strong> (мастер и два воркера на физических серверах) и '
  'мигрировал <strong>12+ микросервисов</strong> из Docker Compose: время деплоя сократилось '
  '<strong>с ~40 до ~8 минут</strong>',
  'Deployed <strong>bare-metal Kubernetes</strong> (a master and two workers on physical servers) and migrated '
  '<strong>12+ microservices</strong> off Docker Compose: deploy time dropped <strong>from ~40 to ~8 minutes</strong>'),

 ('Покрыл <strong>100% продакшен-репозиториев</strong> автоматической сборкой и деплоем в GitLab CI и Jenkins, '
  'внедрил GitOps-доставку через ArgoCD и встроил сканирование <strong>Trivy и Gitleaks</strong> в пайплайн',
  'Covered <strong>100% of production repositories</strong> with automated build and deploy in GitLab CI and Jenkins, '
  'introduced GitOps delivery through ArgoCD and built <strong>Trivy and Gitleaks</strong> scanning into the pipeline'),

 ('Секреты и артефакты: <strong>HashiCorp Vault</strong> для секретов приложений и CI с политиками доступа, Passbolt — менеджер паролей для команды, <strong>Harbor</strong> с retention-политиками, робот-аккаунтами и сканированием образов, Verdaccio — приватный npm-registry',
  'Secrets and artifacts: <strong>HashiCorp Vault</strong> for application and CI secrets with access policies, Passbolt as the team’s password manager, <strong>Harbor</strong> with retention policies, robot accounts and image scanning, Verdaccio as a private npm registry', 'site'),

 ('Разработал Ansible-роли и плейбуки — настройка нового сервера занимает <strong>15 минут вместо 2–3 часов</strong>; '
  'Terraform под воспроизводимые среды и version control конфигураций',
  'Wrote Ansible roles and playbooks — a new server is set up in <strong>15 minutes instead of 2–3 hours</strong>; '
  'Terraform for reproducible environments and configuration version control'),

 ('Внешний периметр и DNS: домен продукта проксировался через <strong>Cloudflare и Qrator</strong> — '
  'защита от DDoS и фильтрация трафика на периметре; вёл внешние записи A, CNAME, MX и TXT '
  '(SPF, DKIM, DMARC) и маршрутизацию внешнего трафика на origin по цепочке внешний прокси → Nginx',
  'External perimeter and DNS: the product domain was proxied through <strong>Cloudflare and Qrator</strong> — '
  'DDoS protection and edge traffic filtering; I maintained the external A, CNAME, MX and TXT records '
  '(SPF, DKIM, DMARC) and the routing of external traffic to origin along the chain external proxy → Nginx'),

 ('Отказоустойчивый кластер <strong>PostgreSQL + Patroni + etcd</strong> на трёх нодах с uptime СУБД '
  '<strong>99.9%</strong>; аналитическое хранилище <strong>ClickHouse ~4 ТБ</strong> на выделенных серверах',
  'A fault-tolerant <strong>PostgreSQL + Patroni + etcd</strong> cluster on three nodes with <strong>99.9%</strong> '
  'database uptime; a <strong>ClickHouse</strong> analytics store of <strong>~4 TB</strong> on dedicated servers'),

 ('Убрал <strong>единые точки отказа</strong> во внутренних сервисах: Zabbix в HA-кластере на двух нодах с базой на отказоустойчивом PostgreSQL, Jira и Confluence — на HA-кластере PostgreSQL',
  'Removed <strong>single points of failure</strong> in internal services: Zabbix as a two-node HA cluster on fault-tolerant PostgreSQL, Jira and Confluence on the HA PostgreSQL cluster'),

 ('Внедрил Prometheus с Grafana и алертингом через Alertmanager, ELK и Graylog для логов, Zabbix для '
  'инфраструктуры — среднее время обнаружения инцидентов упало <strong>с нескольких часов до ~5 минут</strong>',
  'Introduced Prometheus with Grafana and Alertmanager alerting, ELK and Graylog for logs, Zabbix for '
  'infrastructure — mean time to detect incidents fell <strong>from several hours to ~5 minutes</strong>'),
]

SLETAT_SYS = [
 ('Администрировал доменную инфраструктуру <strong>Active Directory</strong>: групповые политики, права '
  'доступа, профили пользователей',
  'Administered the <strong>Active Directory</strong> domain: group policies, access rights, user profiles'),

 ('Организовал удалённый доступ через терминальные фермы RDS, настроил и перенёс '
  '<strong>30+ рабочих станций</strong> при расширении офиса',
  'Set up remote access through RDS terminal farms, configured and relocated <strong>30+ workstations</strong> '
  'during an office expansion'),
]

REAL_DEVOPS = [
 ('Автоматизировал развёртывание ОС Linux, сократив подготовку рабочего места '
  '<strong>с 3 часов до 40 минут</strong>',
  'Automated Linux OS provisioning, cutting workstation setup <strong>from 3 hours to 40 minutes</strong>'),

 ('Настроил мониторинг распределённой сети на <strong>Zabbix</strong>: сетевое оборудование торговых точек, '
  'доступность модемов и каналов связи',
  'Set up monitoring of a distributed network on <strong>Zabbix</strong>: retail-site network equipment, '
  'modem and link availability'),

 ('Автоматизировал рутину скриптами на Bash и PowerShell, хранил и версионировал конфигурации '
  'в self-hosted GitLab',
  'Automated routine work with Bash and PowerShell scripts, keeping configurations versioned in a '
  'self-hosted GitLab'),
]

REAL_SYS = [
 ('Администрировал серверы Windows Server и Linux и сетевое оборудование <strong>MikroTik, Cisco</strong> '
  'в розничной сети из <strong>40+ объектов</strong>',
  'Administered Windows Server and Linux servers and <strong>MikroTik, Cisco</strong> network equipment '
  'across a retail network of <strong>40+ sites</strong>'),

 ('Настроил VPN-инфраструктуру между объектами (Kerio), маршрутизацию и коммутацию; HelpDesk-поддержка '
  'парка <strong>100+ компьютеров</strong> и кассовой техники',
  'Built the site-to-site VPN infrastructure (Kerio), routing and switching; HelpDesk support for a fleet of '
  '<strong>100+ computers</strong> and POS equipment'),
]

FORUM = [
 ('Настройка сетевого и телекоммуникационного оборудования, монтажные работы, подключение абонентов к сети',
  'Configuration of network and telecom equipment, installation work, connecting subscribers to the network'),
]

ROLES = [DUC, SLETAT_DEVOPS, SLETAT_SYS, REAL_DEVOPS, REAL_SYS, FORUM]
NAMES = ['ДЮК', 'Слетать DevOps', 'Слетать сисадмин', 'РеалЪ DevOps', 'РеалЪ сисадмин', 'Форум']
