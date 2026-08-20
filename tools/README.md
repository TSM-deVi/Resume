# tools

## make_brand.py

Перерисовывает `og-image.png` и весь набор фавиконов в стиле сайта
(AuthKit, «frosted glass cathedral at midnight»: `#05060f`, фиолетовый
`#663af3`, синька `#b6d9fc`, Manrope + Inter + JetBrains Mono).

```bash
pip install pillow
python tools/make_brand.py
```

Шрифты подтягиваются с Google Fonts при первом запуске в `tools/fonts/`
— ставить их в систему не нужно.

Результат появляется в `tools/out/`. Оттуда файлы копируются в корень
репозитория вручную — так проще сравнить старое с новым перед заменой:

| Файл | Размер |
|---|---|
| `og-image.png` | 1200×630 |
| `favicon-512.png` | 512 |
| `apple-touch-icon.png` | 180, непрозрачный (iOS сама скругляет углы) |
| `favicon-32.png` | 32 |
| `favicon-16.png` | 16 |
| `favicon.ico` | 16 / 32 / 48 / 64 |

Палитра и токены заданы константами в начале скрипта — менять цвета там.

### После перерисовки обложки

В `index.html` у `og:image` стоит `?v=N`. Telegram, VK и Facebook кешируют
превью по полному URL и сами его не сбрасывают — подними цифру, иначе в
мессенджерах неделями будет висеть старая картинка. Принудительно сбросить
кеш можно так:

* Telegram — написать `@WebpageBot` ссылку на страницу;
* Facebook / WhatsApp — <https://developers.facebook.com/tools/debug/>;
* LinkedIn — <https://www.linkedin.com/post-inspector/>.

**Известное ограничение:** монограмма `TS‹M` на 16px нечитаема — четыре
глифа не помещаются в шестнадцать пикселей. На 32px и выше всё в порядке.
