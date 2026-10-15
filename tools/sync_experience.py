# -*- coding: utf-8 -*-
"""Переносит пункты опыта из hl_data.py в списки опыта index.html.

В index.html двенадцать списков <ul class="jlist" data-lang="ru|en"> — по паре
на каждую из шести ролей, в порядке hl_data.ROLES. Скрипт заменяет только их
содержимое; остальная разметка страницы не трогается.

Запуск из любой папки:  python tools/sync_experience.py
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from hl_data import ROLES

PATH = os.path.join(ROOT, 'index.html')
html = io.open(PATH, encoding='utf-8').read()

m = re.search(r'<section id="experience">.*?\n  </section>', html, re.S)
assert m, 'раздел опыта не найден'
section = m.group(0)
lists = list(re.finditer(r'( *)<ul class="jlist" data-lang="(ru|en)">(.*?)</ul>', section, re.S))
assert len(lists) == 2 * len(ROLES), \
    'списков опыта %d, а ролей %d — разметка разошлась с hl_data' % (len(lists), len(ROLES))

out, pos = [], 0
for i, l in enumerate(lists):
    items = ROLES[i // 2]
    lang = l.group(2)
    body = '\n'.join('              <li>%s</li>' % (ru if lang == 'ru' else en) for ru, en, *_ in items)
    out.append(section[pos:l.start()])
    out.append('%s<ul class="jlist" data-lang="%s">\n%s\n%s</ul>' % (l.group(1), lang, body, l.group(1)))
    pos = l.end()
out.append(section[pos:])

new = html[:m.start()] + ''.join(out) + html[m.end():]
changed = new != html
io.open(PATH, 'w', encoding='utf-8').write(new)
print('index.html: %s, пунктов %d' % ('обновлён' if changed else 'без изменений',
                                     sum(len(r) for r in ROLES)))
