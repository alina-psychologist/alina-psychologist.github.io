#!/usr/bin/env python3
"""Generates the static site (UA at /, EN at /en/) with CSS and JS inlined into every page.

Run from the repository root:  python3 tools/build.py
Settings below (SITE, GA_ID, DEMO) are the only things to change when the real domain,
Google Analytics ID or final content are ready.
"""
import os
import json
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE = "https://alina-psychologist.github.io"  # replace with the custom domain later
GA_ID = "G-NKZ09KV0WY"  # GA4 measurement ID; the tag loads only after the visitor accepts analytics cookies
DEMO = True  # True: noindex + demo ribbon. Set to False for the real launch
TODAY = date.today().isoformat()

SLUGS = {"home": "", "about": "about/", "spec": "specializations/", "services": "services/",
         "faq": "faq/", "contacts": "contacts/", "privacy": "privacy/"}
NAV = ["home", "about", "spec", "services", "faq", "contacts"]


def path(lang, key):
    return ("/" if lang == "uk" else "/en/") + SLUGS[key]


def ph(text):
    return f'<mark class="ph">{text}</mark>'


# ---------------------------------------------------------------- UI strings
UI = {
    "uk": {
        "locale": "uk_UA", "html": "uk", "site": "Аліна · психологиня",
        "nav": {"home": "Головна", "about": "Про мене", "spec": "Спеціалізації", "services": "Послуги",
                "faq": "Питання", "contacts": "Контакти", "privacy": "Конфіденційність"},
        "skip": "До змісту", "menu": "Меню", "theme": "Змінити тему", "other_lang": "EN", "other_lang_name": "English",
        "cta": "Записатися на консультацію", "demo": "Демо-версія: тексти, ціни й контакти є заглушками.",
        "cookie_text": "Ми використовуємо аналітичні cookie Google Analytics, щоб розуміти, які сторінки корисні. Вони вмикаються лише за вашою згодою.",
        "cookie_more": "Докладніше", "accept": "Дозволити", "decline": "Відхилити", "cookie_settings": "Налаштування cookie",
        "crumb_home": "Головна", "rights": "Усі права захищені.",
        "emergency": "Цей сайт не є службою екстреної допомоги. Якщо ви в небезпеці, телефонуйте 112 або на Lifeline Ukraine: 7333.",
        "photo": "Тут буде ваше фото", "letter": "А",
    },
    "en": {
        "locale": "en_US", "html": "en", "site": "Alina · psychologist",
        "nav": {"home": "Home", "about": "About", "spec": "Specializations", "services": "Services",
                "faq": "FAQ", "contacts": "Contacts", "privacy": "Privacy"},
        "skip": "Skip to content", "menu": "Menu", "theme": "Toggle theme", "other_lang": "UA", "other_lang_name": "Українська",
        "cta": "Book a consultation", "demo": "Demo version: texts, prices and contacts are placeholders.",
        "cookie_text": "We use Google Analytics cookies to understand which pages are helpful. They are enabled only with your consent.",
        "cookie_more": "Learn more", "accept": "Allow", "decline": "Decline", "cookie_settings": "Cookie settings",
        "crumb_home": "Home", "rights": "All rights reserved.",
        "emergency": "This website is not an emergency service. If you are in danger, call 112 or Lifeline Ukraine: 7333.",
        "photo": "Your photo goes here", "letter": "A",
    },
}

# ---------------------------------------------------------------- shared components


def photo(lang, label):
    u = UI[lang]
    return (f'<!-- PHOTO: replace this figure with <img> (see PHOTOS.md) -->\n'
            f'<figure class="photo" role="img" aria-label="{label}"><span class="photo-letter">{u["letter"]}</span>'
            f'<figcaption>{u["photo"]}</figcaption></figure>')


def cta_band(lang, title, text):
    u = UI[lang]
    return (f'<section class="band"><div class="wrap band-in"><div><h2>{title}</h2><p>{text}</p></div>'
            f'<a class="btn" href="{path(lang, "contacts")}" data-track="cta_click" data-label="band">{u["cta"]}</a></div></section>')


def hero_simple(h1, lead):
    return f'<section class="page-head"><div class="wrap"><h1>{h1}</h1><p class="lead">{lead}</p></div></section>'


# ---------------------------------------------------------------- page content
C = {"uk": {}, "en": {}}

# ---- UA
C["uk"]["home"] = dict(
    title="Аліна · психологиня онлайн: КПТ і схема-терапія",
    desc="Психологиня Аліна допомагає з тривогою, вигоранням, кризами та складнощами у стосунках. Онлайн-консультації українською та англійською, КПТ і схема-терапія.",
    body=f'''
<section class="hero"><div class="wrap hero-in">
  <div>
    <p class="eyebrow">Психологічна допомога онлайн</p>
    <h1>Жити спокійніше навіть тоді, коли довкола неспокійно</h1>
    <p class="lead">Я Аліна, психологиня. Допомагаю впоратися з тривогою, вигоранням, кризами та складнощами у стосунках. Працюю онлайн в КПТ і схема-терапії, у безпечному й структурованому форматі.</p>
    <div class="actions"><a class="btn" href="{path("uk", "contacts")}" data-track="cta_click" data-label="hero">Записатися на консультацію</a>
    <a class="btn ghost" href="{path("uk", "faq")}#first-session" data-track="cta_click" data-label="hero_first_session">Як проходить перша зустріч</a></div>
    <ul class="chips"><li>КПТ</li><li>Схема-терапія</li><li>Онлайн</li><li>Українська · English</li></ul>
  </div>
  {photo("uk", "Портрет психологині Аліни")}
</div></section>

<section class="sec"><div class="wrap">
  <h2>Можливо, це знайоме</h2>
  <ul class="recognize">
    <li>Думки крутяться по колу, а тіло напружене навіть у спокійні дні.</li>
    <li>Ви багато робите, але радості від результату майже не відчуваєте.</li>
    <li>У близьких стосунках повторюються ті самі конфлікти.</li>
    <li>Після важкої події досі складно повернутися до звичного ритму.</li>
  </ul>
</div></section>

<section class="sec alt"><div class="wrap">
  <h2>З чим я працюю</h2>
  <div class="cards">
    <a class="card" href="{path("uk", "spec")}#anxiety"><h3>Тривога і стрес</h3><p>Панічні атаки, постійне напруження, складнощі зі сном.</p></a>
    <a class="card" href="{path("uk", "spec")}#burnout"><h3>Вигорання і самооцінка</h3><p>Втома, перфекціонізм, вміння відпочивати й казати «ні».</p></a>
    <a class="card" href="{path("uk", "spec")}#relationships"><h3>Стосунки та сім'я</h3><p>Конфлікти, залежність, розставання, батьківство.</p></a>
    <a class="card" href="{path("uk", "spec")}#trauma"><h3>Травма і криза</h3><p>Втрати, війна, адаптація, повільне відновлення.</p></a>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <h2>Як ми працюватимемо</h2>
  <ol class="steps">
    <li><h3>Ви пишете мені</h3><p>Коротко опишіть, що вас турбує, і оберіть зручний час. Відповідаю протягом доби.</p></li>
    <li><h3>Знайомство</h3><p>Коротка розмова на {ph("[20]")} хвилин. Ми окреслимо запит і подивимося, чи комфортно вам зі мною.</p></li>
    <li><h3>Регулярна робота</h3><p>Зустрічі по 50 хвилин, зазвичай раз на тиждень. Ми рухаємося у вашому темпі й звіряємо план.</p></li>
  </ol>
</div></section>

<section class="sec alt"><div class="wrap two">
  <div><h2>Кілька слів про мене</h2>
  <p>Мені важливо, щоб на сесії ви почувалися в безпеці: без оцінок і поспіху. Я поєдную структуру КПТ із глибиною схема-терапії, тож ми працюємо і з тим, що відбувається зараз, і з коренями, звідки це виросло.</p>
  <p><a class="more" href="{path("uk", "about")}">Читати більше про мене</a></p></div>
  <ul class="facts">
    <li><b>КПТ і схема-терапія</b><span>доказові підходи</span></li>
    <li><b>Онлайн</b><span>з будь-якої точки світу</span></li>
    <li><b>UA · EN</b><span>двома мовами</span></li>
  </ul>
</div></section>
''' + cta_band("uk", "Готові зробити перший крок?", "Напишіть мені, і ми знайдемо зручний час для знайомства."),
)

C["uk"]["about"] = dict(
    title="Про мене: Аліна, психологиня (КПТ і схема-терапія)",
    desc="Освіта, підхід і цінності психологині Аліни. КПТ та схема-терапія, онлайн-практика, додаткові навички й принципи роботи.",
    h1="Про мене",
    lead="Психологиня, яка працює з тривогою, вигоранням і кризами в КПТ та схема-терапії.",
    body=f'''
<section class="sec"><div class="wrap two wide-left">
  <div class="prose">
    <h2>Привіт, я Аліна</h2>
    <p>Я психологиня, яка вірить, що змінюватися можна без тиску й самокритики. До професії я прийшла, бо сама знаю, як це відчувається, коли хочеться «просто перестати хвилюватись», але не зрозуміло, з чого почати.</p>
    <p>У роботі мені важливі три речі: безпека, ясність і повага до вашого темпу. Ви завжди знаєте, що ми робимо і навіщо.</p>
    <h2>Мій підхід</h2>
    <p><b>Когнітивно-поведінкова терапія (КПТ).</b> Допомагає помітити думки й звички, що підсилюють тривогу чи виснаження, і поступово замінити їх на корисніші. Це структурна робота з конкретними вправами між сесіями.</p>
    <p><b>Схема-терапія.</b> Працює глибше: з повторюваними сценаріями, які сформувалися в дитинстві й досі керують реакціями та стосунками. Вона допомагає зрозуміти, чому одні ситуації зачіпають так сильно, і дати собі те, чого бракувало.</p>
  </div>
  {photo("uk", "Аліна за робочим столом")}
</div></section>

<section class="sec alt"><div class="wrap">
  <h2>Принципи роботи</h2>
  <div class="cards three">
    <div class="card"><h3>Безпека</h3><p>Повна конфіденційність і відсутність оцінок. Ви самі обираєте, про що говорити.</p></div>
    <div class="card"><h3>Прозорість</h3><p>Ми разом ставимо цілі й періодично дивимося, що вже змінилося.</p></div>
    <div class="card"><h3>Доказовість</h3><p>Використовую методи з підтвердженою ефективністю й регулярно навчаюся.</p></div>
  </div>
</div></section>

<section class="sec"><div class="wrap two">
  <div><h2>Освіта і кваліфікація</h2>
  <ul class="timeline">
    <li><b>{ph("[Рік]")}</b><span>Магістр психології, {ph("[назва ВНЗ]")}</span></li>
    <li><b>{ph("[Рік]")}</b><span>Сертифікат з КПТ, {ph("[навчальна організація]")}</span></li>
    <li><b>{ph("[Рік]")}</b><span>Навчання зі схема-терапії, {ph("[навчальна організація]")}</span></li>
    <li><b>{ph("[Рік]")}</b><span>Курс із роботи з травмою та кризовими станами</span></li>
  </ul>
  <p class="note">Дані в цьому списку демонстраційні й будуть замінені на реальні.</p></div>
  <div><h2>Додаткові вміння</h2>
  <ul class="plain">
    <li>Регулярна супервізія та особиста терапія</li>
    <li>Лекції та воркшопи про емоційну саморегуляцію</li>
    <li>Групові практики з профілактики вигорання</li>
    <li>Робота українською й англійською мовами</li>
  </ul></div>
</div></section>
''' + cta_band("uk", "Хочете познайомитися?", "Короткий дзвінок допоможе зрозуміти, чи підходимо ми одне одному."),
)

C["uk"]["spec"] = dict(
    title="Спеціалізації психологині: тривога, вигорання, стосунки, травма",
    desc="З якими запитами працює психологиня Аліна: тривога і стрес, вигорання та самооцінка, стосунки й сім'я, травма та криза.",
    h1="Спеціалізації",
    lead="Основні запити, з якими до мене приходять, і те, як ми з ними працюємо.",
    body=f'''
<section class="sec"><div class="wrap stack">
  <article id="anxiety" class="topic"><h2>Тривога і стрес</h2>
    <p><b>Як це виглядає.</b> Постійне внутрішнє напруження, панічні атаки, страх помилитися, складнощі зі сном, думки «а раптом».</p>
    <p><b>Як ми працюємо.</b> Вчимося помічати тригери й тілесні сигнали, використовуємо техніки КПТ для роботи з тривожними думками та практики саморегуляції, яких можна навчитися й застосовувати щодня.</p></article>
  <article id="burnout" class="topic"><h2>Вигорання та самооцінка</h2>
    <p><b>Як це виглядає.</b> Виснаження, цинізм, відчуття «я недостатньо добра», перфекціонізм, труднощі з відпочинком і межами.</p>
    <p><b>Як ми працюємо.</b> Шукаємо джерела перевантаження, працюємо з внутрішнім критиком (схема-терапія) і вибудовуємо реалістичні межі та ритм життя.</p></article>
  <article id="relationships" class="topic"><h2>Стосунки та сім'я</h2>
    <p><b>Як це виглядає.</b> Повторювані конфлікти, страх близькості чи самотності, емоційна залежність, розставання, виклики батьківства.</p>
    <p><b>Як ми працюємо.</b> Досліджуємо власні сценарії у стосунках, вчимося чітко говорити про потреби й чути інших. Консультації індивідуальні.</p></article>
  <article id="trauma" class="topic"><h2>Травма і криза</h2>
    <p><b>Як це виглядає.</b> Наслідки втрат, війни, переїзду чи інших важких подій: флешбеки, оніміння, провина, складність довіряти.</p>
    <p><b>Як ми працюємо.</b> У темпі, який вам підходить. Спочатку стабілізація і відчуття безпеки, потім, коли ви готові, обережна робота з пережитим.</p></article>
</div></section>
<section class="sec alt"><div class="wrap two">
  <div><h2>Що виходить за межі моєї роботи</h2>
  <p>Я не працюю з гострими психіатричними станами, залежностями, що потребують медичного лікування, та не призначаю ліки. Якщо вам потрібна допомога лікаря-психіатра, я допоможу зорієнтуватися й порекомендую фахівця.</p></div>
  <div><h2>Чи підходить мені терапія?</h2>
  <p>Якщо ви помічаєте, що проблема триває кілька тижнів і заважає працювати, спати чи спілкуватися, це добрий привід звернутися. Не треба чекати, поки стане «зовсім погано».</p></div>
</div></section>
''' + cta_band("uk", "Не знаєте, з чого почати?", "Напишіть, що вас турбує, і ми разом визначимо, чи можу я бути корисною."),
)

C["uk"]["services"] = dict(
    title="Послуги та вартість: онлайн-консультації психолога",
    desc="Формат, тривалість і вартість онлайн-консультацій психологині Аліни. Індивідуальні сесії, ознайомча розмова, правила скасування.",
    h1="Послуги та формат",
    lead="Індивідуальні онлайн-консультації українською та англійською мовами.",
    body=f'''
<section class="sec"><div class="wrap">
  <div class="cards three">
    <div class="card"><h3>Ознайомча розмова</h3><p class="price">{ph("[безкоштовно]")}</p><p>{ph("[20]")} хвилин. Знайомимося, обговорюємо запит і формат роботи.</p></div>
    <div class="card"><h3>Індивідуальна сесія</h3><p class="price">{ph("[ціна]")} грн</p><p>50 хвилин, відеозв'язок. Зазвичай раз на тиждень.</p></div>
    <div class="card"><h3>Пакет із {ph("[4]")} сесій</h3><p class="price">{ph("[ціна]")} грн</p><p>Зручно, якщо ви хочете спланувати місяць роботи наперед.</p></div>
  </div>
  <p class="note">Ціни демонстраційні. Фінальні значення з'являться перед запуском сайту.</p>
</div></section>
<section class="sec alt"><div class="wrap two">
  <div><h2>Як проходять сесії</h2>
  <ul class="plain">
    <li>Онлайн через {ph("[Zoom / Google Meet]")}, посилання надсилаю заздалегідь</li>
    <li>Мови: українська, англійська</li>
    <li>Для зустрічі потрібні стабільний інтернет і місце, де вас ніхто не відволікає</li>
    <li>Між сесіями можу запропонувати прості вправи для самостійної роботи</li>
  </ul></div>
  <div><h2>Умови</h2>
  <ul class="plain">
    <li>Скасувати або перенести сесію можна не пізніше ніж за 24 години</li>
    <li>Оплата перед сесією переказом на картку</li>
    <li>Усе, що ви розповідаєте, залишається між нами, окрім випадків загрози життю</li>
  </ul></div>
</div></section>
<section class="sec"><div class="wrap">
  <h2>Як записатися</h2>
  <ol class="steps">
    <li><h3>Напишіть мені</h3><p>У Telegram або на пошту, коротко про запит.</p></li>
    <li><h3>Оберіть час</h3><p>Запропоную кілька вільних слотів.</p></li>
    <li><h3>Підтвердіть запис</h3><p>Надішлю посилання на зустріч і нагадування.</p></li>
  </ol>
</div></section>
''' + cta_band("uk", "Записатися на розмову", "Перший крок найпростіший: напишіть мені."),
)

FAQ_UK = [
    ("first-session", "Як проходить перша сесія?",
     "Ми знайомимося, я розпитую про те, що вас привело, і про ваші очікування. Ви можете ставити будь-які питання про процес. Наприкінці ми домовляємося, чи продовжувати й у якому форматі."),
    ("confidential", "Чи конфіденційні наші розмови?",
     "Так. Я не передаю інформацію про наші зустрічі третім особам. Виняток становлять ситуації, коли є реальна загроза життю й безпеці вам або іншим людям."),
    ("how-many", "Скільки сесій потрібно?",
     "Це залежить від запиту. З тривогою чи вигоранням помітні зміни часто з'являються за 8–12 зустрічей, глибша робота зі сценаріями й травмою триває довше. Ми регулярно звіряємо прогрес."),
    ("online", "Чи ефективна терапія онлайн?",
     "Так. Дослідження показують, що онлайн-формат КПТ працює порівняно з очним. Для зручності потрібні тиха кімната, стабільний зв'язок і навушники."),
    ("difference", "Чим психолог відрізняється від психіатра?",
     "Психолог працює розмовою й практиками, а психіатр лікар, який діагностує та за потреби призначає ліки. Якщо я бачу, що вам потрібен лікар, то кажу про це й допомагаю з направленням."),
    ("cancel", "Що, якщо я не зможу прийти?",
     "Повідомте мене щонайпізніше за 24 години, і ми перенесемо зустріч без оплати."),
    ("cbt-schema", "Що таке КПТ і схема-терапія?",
     "КПТ працює з думками, емоціями й поведінкою «тут і зараз», а схема-терапія додає роботу з глибшими життєвими сценаріями. Докладніше про це на сторінці «Про мене»."),
]
C["uk"]["faq"] = dict(
    title="Часті питання про психотерапію та консультації",
    desc="Відповіді на часті питання: як проходить перша сесія, конфіденційність, кількість зустрічей, відмінність психолога від психіатра, онлайн-формат.",
    h1="Часті питання", lead="Якщо не знайшли відповіді, напишіть мені.", faq=FAQ_UK,
)

C["uk"]["contacts"] = dict(
    title="Контакти: записатися на консультацію до психологині",
    desc="Як зв'язатися з психологинею Аліною: Telegram, пошта, Instagram, графік роботи. Допомога в кризових ситуаціях.",
    h1="Контакти",
    lead="Напишіть мені зручним способом. Відповідаю протягом доби.",
    body=f'''
<section class="sec"><div class="wrap two">
  <div><h2>Як зв'язатися</h2>
  <ul class="contact-list">
    <li><span>Telegram</span><a href="https://t.me/alina_psychologist_demo" data-track="contact_click" data-label="telegram" rel="noopener">{ph("@alina_psychologist_demo")}</a></li>
    <li><span>Пошта</span><a href="mailto:hello@example.com" data-track="contact_click" data-label="email">{ph("hello@example.com")}</a></li>
    <li><span>Instagram</span><a href="https://instagram.com/alina_psychologist_demo" data-track="contact_click" data-label="instagram" rel="noopener">{ph("@alina_psychologist_demo")}</a></li>
  </ul>
  <p class="note">Контакти демонстраційні й будуть замінені.</p></div>
  <div><h2>Години роботи</h2>
  <ul class="plain"><li>Пн-Пт: {ph("[10:00-19:00]")} за київським часом</li><li>Сб: за домовленістю</li><li>Нд: вихідний</li></ul>
  <p>Формат: онлайн. Консультую з будь-якої точки світу.</p></div>
</div></section>
<section class="sec alt"><div class="wrap">
  <div class="alert"><h2>Якщо вам потрібна термінова допомога</h2>
  <p>Я не надаю екстрену допомогу. Якщо ви або хтось поруч у небезпеці, телефонуйте <b>112</b>. Цілодобова безкоштовна лінія підтримки <b>Lifeline Ukraine: 7333</b>.</p></div>
</div></section>
''',
)

C["uk"]["privacy"] = dict(
    title="Політика конфіденційності та cookie",
    desc="Які дані збирає сайт, як працюють аналітичні cookie Google Analytics і як відкликати згоду.",
    h1="Політика конфіденційності та cookie",
    lead=f"Оновлено {TODAY}. Коротко: сайт не збирає ваших особистих даних, а аналітику вмикає тільки з вашої згоди.",
    body=f'''
<section class="sec"><div class="wrap prose narrow">
  <h2>Які дані ми обробляємо</h2>
  <p>На сайті немає форм, реєстрації чи коментарів. Ми не збираємо імен, телефонів чи листування. Якщо ви пишете мені в Telegram чи на пошту, ці повідомлення обробляються відповідною платформою та мною лише для відповіді вам.</p>
  <h2>Аналітичні cookie (Google Analytics 4)</h2>
  <p>Щоб розуміти, які сторінки відвідують і що читають, ми використовуємо Google Analytics 4. Він встановлює cookie <code>_ga</code> і <code>_ga_*</code> та збирає знеособлену статистику: сторінки, тривалість перегляду, глибину прокручування, кліки по контактах, тип пристрою, приблизну країну чи місто.</p>
  <p>Ці cookie вмикаються <b>тільки після вашої згоди</b> у банері. До цього Google Analytics не завантажується, а аналітичне зберігання заборонено (Google Consent Mode v2). Рекламні cookie та персоналізація не використовуються.</p>
  <h2>Ваш вибір</h2>
  <p>Ви можете в будь-який момент змінити рішення: натисніть <button type="button" class="linklike" data-cookie-settings>Налаштування cookie</button> унизу будь-якої сторінки. Якщо відхилити згоду, збережені аналітичні cookie буде видалено.</p>
  <h2>Хто обробляє дані</h2>
  <p>Статистику обробляє Google Ireland Limited / Google LLC відповідно до власної політики конфіденційності. Дані можуть передаватися за межі ЄЕЗ. Власник сайту: {ph("[ПІБ / ФОП]")}, контакт: {ph("hello@example.com")}.</p>
  <h2>Ваші права</h2>
  <p>Ви маєте право на доступ, виправлення, видалення даних і відкликання згоди відповідно до Закону України «Про захист персональних даних» та, для відвідувачів із ЄС, Регламенту GDPR. Напишіть на контактну пошту, і ми відповімо.</p>
  <p class="note">Це шаблонний текст для демо-сайту. Перед публічним запуском його варто перевірити з юристом.</p>
</div></section>
''',
)

# ---- EN
C["en"]["home"] = dict(
    title="Alina · online psychologist: CBT and schema therapy",
    desc="Psychologist Alina helps with anxiety, burnout, crises and relationship difficulties. Online sessions in Ukrainian and English, CBT and schema therapy.",
    body=f'''
<section class="hero"><div class="wrap hero-in">
  <div>
    <p class="eyebrow">Online psychological support</p>
    <h1>Live calmer, even when things around you are not</h1>
    <p class="lead">I'm Alina, a psychologist. I help people cope with anxiety, burnout, crises and relationship difficulties. I work online using CBT and schema therapy, in a safe and structured format.</p>
    <div class="actions"><a class="btn" href="{path("en", "contacts")}" data-track="cta_click" data-label="hero">Book a consultation</a>
    <a class="btn ghost" href="{path("en", "faq")}#first-session" data-track="cta_click" data-label="hero_first_session">What the first session is like</a></div>
    <ul class="chips"><li>CBT</li><li>Schema therapy</li><li>Online</li><li>English · Українська</li></ul>
  </div>
  {photo("en", "Portrait of psychologist Alina")}
</div></section>

<section class="sec"><div class="wrap">
  <h2>Does this sound familiar?</h2>
  <ul class="recognize">
    <li>Your thoughts go in circles and your body stays tense even on calm days.</li>
    <li>You do a lot, yet feel almost no joy from the results.</li>
    <li>The same conflicts keep repeating in your close relationships.</li>
    <li>After a hard event, it is still difficult to get back to your usual rhythm.</li>
  </ul>
</div></section>

<section class="sec alt"><div class="wrap">
  <h2>What I work with</h2>
  <div class="cards">
    <a class="card" href="{path("en", "spec")}#anxiety"><h3>Anxiety and stress</h3><p>Panic attacks, constant tension, trouble sleeping.</p></a>
    <a class="card" href="{path("en", "spec")}#burnout"><h3>Burnout and self-esteem</h3><p>Exhaustion, perfectionism, learning to rest and say no.</p></a>
    <a class="card" href="{path("en", "spec")}#relationships"><h3>Relationships and family</h3><p>Conflicts, dependency, break-ups, parenting.</p></a>
    <a class="card" href="{path("en", "spec")}#trauma"><h3>Trauma and crisis</h3><p>Loss, war, adaptation, slow recovery.</p></a>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <h2>How we will work</h2>
  <ol class="steps">
    <li><h3>You write to me</h3><p>Briefly describe what is bothering you and pick a convenient time. I reply within a day.</p></li>
    <li><h3>Getting acquainted</h3><p>A short {ph("[20]")}-minute conversation. We outline your request and see whether you feel comfortable with me.</p></li>
    <li><h3>Regular work</h3><p>50-minute sessions, usually once a week. We move at your pace and review the plan together.</p></li>
  </ol>
</div></section>

<section class="sec alt"><div class="wrap two">
  <div><h2>A few words about me</h2>
  <p>It matters to me that you feel safe in a session: no judgement and no rush. I combine the structure of CBT with the depth of schema therapy, so we work both with what is happening now and with the roots it grew from.</p>
  <p><a class="more" href="{path("en", "about")}">Read more about me</a></p></div>
  <ul class="facts">
    <li><b>CBT and schema therapy</b><span>evidence-based approaches</span></li>
    <li><b>Online</b><span>from anywhere in the world</span></li>
    <li><b>EN · UA</b><span>two languages</span></li>
  </ul>
</div></section>
''' + cta_band("en", "Ready to take the first step?", "Write to me and we will find a convenient time to meet."),
)

C["en"]["about"] = dict(
    title="About Alina: psychologist (CBT and schema therapy)",
    desc="Education, approach and values of psychologist Alina. CBT and schema therapy, online practice, additional skills and working principles.",
    h1="About me",
    lead="A psychologist working with anxiety, burnout and crises using CBT and schema therapy.",
    body=f'''
<section class="sec"><div class="wrap two wide-left">
  <div class="prose">
    <h2>Hi, I'm Alina</h2>
    <p>I'm a psychologist who believes that change is possible without pressure or self-criticism. I came to this profession because I know how it feels to want to "just stop worrying" without knowing where to start.</p>
    <p>Three things matter to me in my work: safety, clarity and respect for your pace. You always know what we are doing and why.</p>
    <h2>My approach</h2>
    <p><b>Cognitive behavioural therapy (CBT).</b> It helps notice thoughts and habits that feed anxiety or exhaustion, and gradually replace them with more helpful ones. It is structured work with specific exercises between sessions.</p>
    <p><b>Schema therapy.</b> It goes deeper: it works with recurring patterns formed in childhood that still drive reactions and relationships. It helps you understand why some situations hit so hard and give yourself what was missing.</p>
  </div>
  {photo("en", "Alina at her desk")}
</div></section>

<section class="sec alt"><div class="wrap">
  <h2>Working principles</h2>
  <div class="cards three">
    <div class="card"><h3>Safety</h3><p>Full confidentiality and no judgement. You choose what to talk about.</p></div>
    <div class="card"><h3>Transparency</h3><p>We set goals together and regularly look at what has already changed.</p></div>
    <div class="card"><h3>Evidence</h3><p>I use methods with proven effectiveness and keep learning.</p></div>
  </div>
</div></section>

<section class="sec"><div class="wrap two">
  <div><h2>Education and qualifications</h2>
  <ul class="timeline">
    <li><b>{ph("[Year]")}</b><span>Master's in Psychology, {ph("[university]")}</span></li>
    <li><b>{ph("[Year]")}</b><span>CBT certificate, {ph("[training organisation]")}</span></li>
    <li><b>{ph("[Year]")}</b><span>Schema therapy training, {ph("[training organisation]")}</span></li>
    <li><b>{ph("[Year]")}</b><span>Course on trauma and crisis work</span></li>
  </ul>
  <p class="note">This list is a demonstration and will be replaced with real data.</p></div>
  <div><h2>Additional skills</h2>
  <ul class="plain">
    <li>Regular supervision and personal therapy</li>
    <li>Lectures and workshops on emotional self-regulation</li>
    <li>Group practices for burnout prevention</li>
    <li>Working in Ukrainian and English</li>
  </ul></div>
</div></section>
''' + cta_band("en", "Want to get acquainted?", "A short call will help you see whether we are a good fit."),
)

C["en"]["spec"] = dict(
    title="Specializations: anxiety, burnout, relationships, trauma",
    desc="What psychologist Alina works with: anxiety and stress, burnout and self-esteem, relationships and family, trauma and crisis.",
    h1="Specializations",
    lead="The main requests people come to me with, and how we work with them.",
    body=f'''
<section class="sec"><div class="wrap stack">
  <article id="anxiety" class="topic"><h2>Anxiety and stress</h2>
    <p><b>What it looks like.</b> Constant inner tension, panic attacks, fear of making mistakes, trouble sleeping, "what if" thoughts.</p>
    <p><b>How we work.</b> We learn to notice triggers and body signals, use CBT techniques for anxious thoughts, and practise self-regulation skills you can apply every day.</p></article>
  <article id="burnout" class="topic"><h2>Burnout and self-esteem</h2>
    <p><b>What it looks like.</b> Exhaustion, cynicism, a feeling of "I'm not good enough", perfectionism, difficulty resting and setting boundaries.</p>
    <p><b>How we work.</b> We look for the sources of overload, work with the inner critic (schema therapy) and build realistic boundaries and a sustainable rhythm.</p></article>
  <article id="relationships" class="topic"><h2>Relationships and family</h2>
    <p><b>What it looks like.</b> Recurring conflicts, fear of closeness or loneliness, emotional dependency, break-ups, parenting challenges.</p>
    <p><b>How we work.</b> We explore your own relationship patterns and learn to speak clearly about needs and hear others. Sessions are individual.</p></article>
  <article id="trauma" class="topic"><h2>Trauma and crisis</h2>
    <p><b>What it looks like.</b> Consequences of loss, war, relocation or other hard events: flashbacks, numbness, guilt, difficulty trusting.</p>
    <p><b>How we work.</b> At a pace that suits you. First stabilisation and a sense of safety, then, when you are ready, careful work with what you have been through.</p></article>
</div></section>
<section class="sec alt"><div class="wrap two">
  <div><h2>What is outside my practice</h2>
  <p>I do not work with acute psychiatric conditions or addictions that need medical treatment, and I do not prescribe medication. If you need a psychiatrist, I will help you find your way and recommend a specialist.</p></div>
  <div><h2>Is therapy right for me?</h2>
  <p>If a problem has lasted several weeks and gets in the way of work, sleep or relationships, that is a good reason to reach out. You do not need to wait until things get "really bad".</p></div>
</div></section>
''' + cta_band("en", "Not sure where to start?", "Tell me what is on your mind and we will work out together whether I can help."),
)

C["en"]["services"] = dict(
    title="Services and pricing: online psychologist sessions",
    desc="Format, duration and prices of online sessions with psychologist Alina. Individual sessions, an introductory call and the cancellation policy.",
    h1="Services and format",
    lead="Individual online sessions in Ukrainian and English.",
    body=f'''
<section class="sec"><div class="wrap">
  <div class="cards three">
    <div class="card"><h3>Introductory call</h3><p class="price">{ph("[free]")}</p><p>{ph("[20]")} minutes. We get acquainted and discuss your request and the format of work.</p></div>
    <div class="card"><h3>Individual session</h3><p class="price">{ph("[price]")} UAH</p><p>50 minutes, video call. Usually once a week.</p></div>
    <div class="card"><h3>Package of {ph("[4]")} sessions</h3><p class="price">{ph("[price]")} UAH</p><p>Convenient if you want to plan a month of work ahead.</p></div>
  </div>
  <p class="note">Prices are a demonstration. Final values will appear before the site launches.</p>
</div></section>
<section class="sec alt"><div class="wrap two">
  <div><h2>How sessions work</h2>
  <ul class="plain">
    <li>Online via {ph("[Zoom / Google Meet]")}; I send the link in advance</li>
    <li>Languages: English, Ukrainian</li>
    <li>You need a stable internet connection and a place where nobody disturbs you</li>
    <li>Between sessions I may suggest simple exercises for independent practice</li>
  </ul></div>
  <div><h2>Terms</h2>
  <ul class="plain">
    <li>Cancel or reschedule at least 24 hours in advance</li>
    <li>Payment before the session by card transfer</li>
    <li>Everything you share stays between us, except where there is a threat to life</li>
  </ul></div>
</div></section>
<section class="sec"><div class="wrap">
  <h2>How to book</h2>
  <ol class="steps">
    <li><h3>Write to me</h3><p>On Telegram or by email, briefly about your request.</p></li>
    <li><h3>Pick a time</h3><p>I will suggest a few available slots.</p></li>
    <li><h3>Confirm the booking</h3><p>I will send the meeting link and a reminder.</p></li>
  </ol>
</div></section>
''' + cta_band("en", "Book a conversation", "The first step is the easiest: write to me."),
)

FAQ_EN = [
    ("first-session", "What is the first session like?",
     "We get acquainted, and I ask about what brought you here and what you expect. You can ask any questions about the process. At the end we agree whether to continue and in what format."),
    ("confidential", "Are our conversations confidential?",
     "Yes. I do not share information about our meetings with third parties. The exception is a real threat to the life or safety of you or others."),
    ("how-many", "How many sessions will I need?",
     "It depends on the request. With anxiety or burnout, noticeable changes often appear within 8-12 meetings; deeper work with patterns and trauma takes longer. We review progress regularly."),
    ("online", "Is online therapy effective?",
     "Yes. Research shows that online CBT works comparably to in-person. For comfort you need a quiet room, a stable connection and headphones."),
    ("difference", "How is a psychologist different from a psychiatrist?",
     "A psychologist works through conversation and practices, while a psychiatrist is a medical doctor who diagnoses and, if needed, prescribes medication. If I see that you need a doctor, I will say so and help with a referral."),
    ("cancel", "What if I cannot attend?",
     "Let me know at least 24 hours ahead and we will reschedule at no charge."),
    ("cbt-schema", "What are CBT and schema therapy?",
     "CBT works with thoughts, emotions and behaviour in the here and now, while schema therapy adds work with deeper life patterns. More on the About page."),
]
C["en"]["faq"] = dict(
    title="FAQ about psychotherapy and consultations",
    desc="Answers to common questions: what the first session is like, confidentiality, number of sessions, psychologist versus psychiatrist, online format.",
    h1="Frequently asked questions", lead="If you did not find your answer, write to me.", faq=FAQ_EN,
)

C["en"]["contacts"] = dict(
    title="Contacts: book a session with a psychologist",
    desc="How to reach psychologist Alina: Telegram, email, Instagram and working hours. Help in crisis situations.",
    h1="Contacts",
    lead="Write to me in whichever way is convenient. I reply within a day.",
    body=f'''
<section class="sec"><div class="wrap two">
  <div><h2>How to reach me</h2>
  <ul class="contact-list">
    <li><span>Telegram</span><a href="https://t.me/alina_psychologist_demo" data-track="contact_click" data-label="telegram" rel="noopener">{ph("@alina_psychologist_demo")}</a></li>
    <li><span>Email</span><a href="mailto:hello@example.com" data-track="contact_click" data-label="email">{ph("hello@example.com")}</a></li>
    <li><span>Instagram</span><a href="https://instagram.com/alina_psychologist_demo" data-track="contact_click" data-label="instagram" rel="noopener">{ph("@alina_psychologist_demo")}</a></li>
  </ul>
  <p class="note">Contacts are a demonstration and will be replaced.</p></div>
  <div><h2>Working hours</h2>
  <ul class="plain"><li>Mon-Fri: {ph("[10:00-19:00]")} Kyiv time</li><li>Sat: by arrangement</li><li>Sun: day off</li></ul>
  <p>Format: online. I see clients from anywhere in the world.</p></div>
</div></section>
<section class="sec alt"><div class="wrap">
  <div class="alert"><h2>If you need urgent help</h2>
  <p>I do not provide emergency care. If you or someone near you is in danger, call <b>112</b>. The free 24/7 support line is <b>Lifeline Ukraine: 7333</b>.</p></div>
</div></section>
''',
)

C["en"]["privacy"] = dict(
    title="Privacy and cookie policy",
    desc="What data this website collects, how Google Analytics cookies work and how to withdraw consent.",
    h1="Privacy and cookie policy",
    lead=f"Updated {TODAY}. In short: the site does not collect your personal data, and analytics is enabled only with your consent.",
    body=f'''
<section class="sec"><div class="wrap prose narrow">
  <h2>What data we process</h2>
  <p>The site has no forms, registration or comments. We do not collect names, phone numbers or correspondence. If you write to me on Telegram or by email, those messages are handled by the respective platform and by me only to reply to you.</p>
  <h2>Analytics cookies (Google Analytics 4)</h2>
  <p>To understand which pages are visited and read, we use Google Analytics 4. It sets the <code>_ga</code> and <code>_ga_*</code> cookies and collects anonymised statistics: pages, time on page, scroll depth, clicks on contacts, device type and approximate country or city.</p>
  <p>These cookies are enabled <b>only after you consent</b> in the banner. Until then Google Analytics is not loaded and analytics storage is denied (Google Consent Mode v2). Advertising cookies and personalisation are not used.</p>
  <h2>Your choice</h2>
  <p>You can change your decision at any time: click <button type="button" class="linklike" data-cookie-settings>Cookie settings</button> at the bottom of any page. If you decline, stored analytics cookies are removed.</p>
  <h2>Who processes the data</h2>
  <p>Statistics are processed by Google Ireland Limited / Google LLC under Google's own privacy policy. Data may be transferred outside the EEA. Site owner: {ph("[full name / sole proprietor]")}, contact: {ph("hello@example.com")}.</p>
  <h2>Your rights</h2>
  <p>You have the right to access, correct and delete data and to withdraw consent under the Law of Ukraine "On Personal Data Protection" and, for visitors from the EU, the GDPR. Write to the contact email and we will reply.</p>
  <p class="note">This is template text for a demo site. Have it reviewed by a lawyer before the public launch.</p>
</div></section>
''',
)

# ---------------------------------------------------------------- CSS / JS
FONTS_CSS = open(os.path.join(ROOT, "tools", "fonts.css"), encoding="utf-8").read()

CSS = FONTS_CSS + r"""
:root{--bg:#F3EFE8;--surface:#FBF9F5;--alt:#EAE5DA;--fg:#2B3A33;--muted:#58675F;--accent:#4F7360;--accent-fg:#FFFFFF;--line:#DDD7CB;--mark:#F4E3B5;--mark-fg:#4A3B0E;--radius:18px;
--display:"Lora",Georgia,"Times New Roman",serif;--body:"Onest",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#1B211E;--surface:#232B27;--alt:#202824;--fg:#E8EDE7;--muted:#A3B0A8;--accent:#9DBFA9;--accent-fg:#12201A;--line:#33403A;--mark:#4A3F1C;--mark-fg:#F1E2B1;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#1B211E;--surface:#232B27;--alt:#202824;--fg:#E8EDE7;--muted:#A3B0A8;--accent:#9DBFA9;--accent-fg:#12201A;--line:#33403A;--mark:#4A3F1C;--mark-fg:#F1E2B1;color-scheme:dark}
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important;animation:none!important}}
body{margin:0;background:var(--bg);color:var(--fg);font:400 17px/1.65 var(--body);display:flex;flex-direction:column;min-height:100vh}
main{flex:1}
img{max-width:100%;height:auto}
a{color:var(--accent);text-underline-offset:3px}
a:hover{text-decoration-thickness:2px}
:focus-visible{outline:3px solid var(--accent);outline-offset:3px;border-radius:4px}
h1,h2,h3{font-family:var(--display);font-weight:500;line-height:1.2;margin:0 0 .6em;text-wrap:balance}
h1{font-size:clamp(32px,5.2vw,52px)}
h2{font-size:clamp(24px,3.2vw,32px)}
h3{font-size:19px}
p{margin:0 0 1em}
.wrap{max-width:1080px;margin:0 auto;padding-left:max(20px,env(safe-area-inset-left,0px));padding-right:max(20px,env(safe-area-inset-right,0px))}
.skip{position:absolute;left:-999px;top:8px;background:var(--accent);color:var(--accent-fg);padding:8px 14px;border-radius:8px;z-index:100}
.skip:focus{left:12px}
.demo{background:var(--mark);color:var(--mark-fg);text-align:center;font-size:13px;padding:6px 16px}
.ph{background:var(--mark);color:var(--mark-fg);border-radius:4px;padding:0 4px}
/* header */
.site-head{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.head-in{display:flex;align-items:center;gap:12px 24px;padding-block:14px;flex-wrap:wrap}
.logo{font-family:var(--display);font-weight:600;font-size:21px;color:var(--fg);text-decoration:none;margin-right:auto}
.logo span{color:var(--muted);font-weight:500}
.menu{display:flex;gap:4px 20px;flex-wrap:wrap;font-size:15px}
.menu a{color:var(--muted);text-decoration:none;padding:6px 0;border-bottom:2px solid transparent}
.menu a:hover{color:var(--fg)}
.menu a[aria-current="page"]{color:var(--fg);border-bottom-color:var(--accent)}
.tools{display:flex;gap:8px;align-items:center}
.pill,.icon-btn,.burger{font:inherit;font-size:13px;color:var(--fg);background:transparent;border:1px solid var(--line);border-radius:999px;padding:5px 12px;cursor:pointer;text-decoration:none;line-height:1.4}
.pill:hover,.icon-btn:hover,.burger:hover{background:var(--surface)}
.icon-btn{width:34px;height:34px;padding:0;display:grid;place-items:center}
.icon-btn svg{width:18px;height:18px}
.burger{display:none}
@media (max-width:760px){
 .js .burger{display:inline-block}
 .js .menu{display:none;width:100%;order:5;flex-direction:column;gap:0}
 .js .menu.open{display:flex}
 .js .menu a{padding:10px 0;border-bottom:1px solid var(--line)}
}
/* hero */
.hero{padding-block:clamp(36px,7vw,84px)}
.hero-in{display:grid;grid-template-columns:1.3fr 1fr;gap:clamp(24px,5vw,64px);align-items:center}
.hero-in>*,.two>*{min-width:0}
.eyebrow{font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);font-weight:600;margin-bottom:14px}
.lead{font-size:clamp(17px,2vw,20px);color:var(--muted);max-width:56ch}
.actions{display:flex;flex-wrap:wrap;gap:12px;margin-top:28px}
.btn{display:inline-block;background:var(--accent);color:var(--accent-fg);font-weight:600;text-decoration:none;padding:13px 24px;border-radius:12px;font-size:16px;border:1px solid var(--accent)}
.btn:hover{filter:brightness(1.06)}
.btn.ghost{background:transparent;color:var(--fg);border-color:var(--line)}
.btn.ghost:hover{background:var(--surface)}
.chips{list-style:none;display:flex;flex-wrap:wrap;gap:8px;padding:0;margin:28px 0 0}
.chips li{font-size:13px;padding:4px 12px;border-radius:999px;background:var(--surface);border:1px solid var(--line);color:var(--muted)}
.photo{margin:0;aspect-ratio:4/5;max-width:100%;width:100%;background:var(--surface);border:1px solid var(--line);border-radius:999px 999px var(--radius) var(--radius);display:grid;place-items:center;position:relative;overflow:hidden}
.photo-letter{font-family:var(--display);font-size:clamp(80px,12vw,140px);color:var(--accent)}
.photo figcaption{position:absolute;bottom:14px;left:0;right:0;text-align:center;font-size:13px;color:var(--muted)}
.photo img{width:100%;height:100%;object-fit:cover}
@media (max-width:760px){.hero-in{grid-template-columns:1fr}.photo{max-width:300px}}
/* sections */
.page-head{padding-block:clamp(32px,6vw,64px) clamp(8px,2vw,16px)}
.page-head h1{margin-bottom:.4em}
.sec{padding-block:clamp(36px,6vw,72px)}
.sec.alt{background:var(--alt)}
.recognize{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}
.recognize li{padding:18px 20px;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius)}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px}
.cards.three{grid-template-columns:repeat(auto-fit,minmax(250px,1fr))}
.card{display:block;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:22px;color:var(--fg);text-decoration:none;min-width:0}
a.card:hover{border-color:var(--accent)}
.card p{color:var(--muted);margin:0;font-size:16px}
.price{font-family:var(--display);font-size:24px;color:var(--fg)!important;margin-bottom:.4em!important}
.steps{list-style:none;counter-reset:s;display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px;padding:0;margin:0}
.steps li{counter-increment:s;position:relative;padding-top:48px}
.steps li::before{content:counter(s);position:absolute;top:0;left:0;width:36px;height:36px;border-radius:50%;background:var(--accent);color:var(--accent-fg);display:grid;place-items:center;font-weight:600}
.steps p{color:var(--muted)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:clamp(24px,5vw,64px);align-items:start}
.two.wide-left{grid-template-columns:1.4fr 1fr}
@media (max-width:760px){.two,.two.wide-left{grid-template-columns:1fr}}
.facts{list-style:none;padding:0;margin:0;display:grid;gap:12px}
.facts li{display:flex;flex-direction:column;padding:16px 20px;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius)}
.facts span{color:var(--muted);font-size:15px}
.more{font-weight:600}
.plain{padding-left:1.1em;margin:0 0 1em}
.plain li{margin-bottom:.4em}
.timeline{list-style:none;padding:0;margin:0 0 1em;display:grid;gap:12px}
.timeline li{display:grid;grid-template-columns:90px 1fr;gap:12px;padding-bottom:12px;border-bottom:1px solid var(--line)}
.timeline b{font-weight:600;color:var(--accent)}
.note{font-size:14px;color:var(--muted)}
.stack{display:grid;gap:20px;max-width:820px}
.topic{padding:26px;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);scroll-margin-top:90px}
.topic p:last-child{margin-bottom:0}
.prose h2{margin-top:1.4em}
.prose h2:first-child{margin-top:0}
.narrow{max-width:760px}
.contact-list{list-style:none;padding:0;margin:0 0 1em;display:grid;gap:10px}
.contact-list li{display:flex;flex-direction:column;padding:14px 18px;background:var(--surface);border:1px solid var(--line);border-radius:14px}
.contact-list span{font-size:13px;color:var(--muted);letter-spacing:.06em;text-transform:uppercase}
.alert{max-width:760px;padding:24px 26px;border:1px solid var(--accent);border-radius:var(--radius);background:var(--surface)}
.alert p{margin:0}
code{font-size:.9em;background:var(--alt);padding:1px 6px;border-radius:5px}
.linklike{font:inherit;color:var(--accent);background:none;border:0;padding:0;cursor:pointer;text-decoration:underline;text-underline-offset:3px}
/* faq */
.faq{display:grid;gap:10px;max-width:820px}
.faq details{background:var(--surface);border:1px solid var(--line);border-radius:14px;scroll-margin-top:90px}
.faq summary{cursor:pointer;list-style:none;padding:16px 20px;font-weight:500;display:flex;justify-content:space-between;gap:16px;align-items:center}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";color:var(--accent);font-size:24px;line-height:1}
.faq details[open] summary::after{content:"\2212"}
.faq details p{padding:0 20px 18px;margin:0;color:var(--muted)}
/* band + footer */
.band{background:var(--accent);color:var(--accent-fg)}
.band-in{display:flex;flex-wrap:wrap;gap:20px 32px;align-items:center;justify-content:space-between;padding-block:clamp(32px,5vw,52px)}
.band h2{margin-bottom:.3em}
.band p{margin:0;opacity:.9}
.band .btn{background:var(--accent-fg);color:var(--accent);border-color:var(--accent-fg)}
.site-foot{border-top:1px solid var(--line);font-size:14px;color:var(--muted)}
.foot-in{display:flex;flex-wrap:wrap;gap:10px 28px;justify-content:space-between;padding-block:26px}
.foot-in p{margin:0}
.foot-links{display:flex;flex-wrap:wrap;gap:6px 20px}
.foot-links a,.foot-links button{color:var(--muted)}
.emerg{flex-basis:100%;font-size:13px}
/* cookie */
.cookie{position:fixed;left:max(12px,env(safe-area-inset-left,0px));right:max(12px,env(safe-area-inset-right,0px));bottom:max(12px,env(safe-area-inset-bottom,0px));z-index:50;max-width:720px;margin:0 auto;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:16px 18px;box-shadow:0 8px 30px rgba(0,0,0,.18);display:flex;flex-wrap:wrap;gap:12px 18px;align-items:center;font-size:14px}
.cookie[hidden]{display:none}
.cookie p{margin:0;flex:1 1 300px;color:var(--muted)}
.cookie .acts{display:flex;gap:8px}
.cookie .btn{padding:9px 18px;font-size:14px}
"""

SUN_MOON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 3v18" /><path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor"/></svg>')

JS = r"""
(function(){
var d=document,GA='__GA__',KEY='cookie-consent';
window.dataLayer=window.dataLayer||[];
function gtag(){dataLayer.push(arguments)}
gtag('consent','default',{analytics_storage:'denied',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',wait_for_update:500});
function get(k){try{return localStorage.getItem(k)}catch(e){return null}}
function set(k,v){try{localStorage.setItem(k,v)}catch(e){}}
var loaded=false,granted=false;
function track(name,p){if(granted&&loaded)gtag('event',name,p||{})}
function loadGA(){
  if(loaded||!/^G-[A-Z0-9]+$/.test(GA)||false)return;
  loaded=true;
  var s=d.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+GA;d.head.appendChild(s);
  gtag('js',new Date());gtag('config',GA);
}
function dropCookies(){
  var h=location.hostname.split('.');
  d.cookie.split(';').forEach(function(c){
    var n=c.split('=')[0].trim();
    if(n==='_ga'||n.indexOf('_ga_')===0){
      for(var i=0;i<h.length;i++){var dom=h.slice(i).join('.');
        d.cookie=n+'=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;domain='+dom;
        d.cookie=n+'=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;domain=.'+dom}
      d.cookie=n+'=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/'}});
}
function apply(v){
  granted=v==='granted';
  gtag('consent','update',{analytics_storage:granted?'granted':'denied'});
  if(granted)loadGA();else dropCookies();
}
var bar=d.getElementById('cookie');
function show(){if(bar)bar.hidden=false}
function choose(v){set(KEY,v);if(bar)bar.hidden=true;apply(v)}
var saved=get(KEY);
if(saved==='granted'||saved==='denied')apply(saved);else show();
d.querySelectorAll('[data-consent]').forEach(function(b){b.addEventListener('click',function(){choose(b.dataset.consent)})});
d.querySelectorAll('[data-cookie-settings]').forEach(function(b){b.addEventListener('click',show)});

/* theme */
var root=d.documentElement;
var tb=d.getElementById('theme');
if(tb)tb.addEventListener('click',function(){
  var cur=root.dataset.theme||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');
  var next=cur==='dark'?'light':'dark';
  root.dataset.theme=next;set('theme',next);track('theme_change',{theme:next});
});

/* mobile menu */
var bg=d.getElementById('burger'),menu=d.getElementById('menu');
if(bg&&menu)bg.addEventListener('click',function(){
  var o=menu.classList.toggle('open');bg.setAttribute('aria-expanded',String(o));
});

/* events */
d.addEventListener('click',function(e){
  var el=e.target.closest('[data-track]');if(!el)return;
  track(el.dataset.track,{label:el.dataset.label||'',link_url:el.getAttribute('href')||'',page_path:location.pathname});
});
d.querySelectorAll('.faq details').forEach(function(x){
  x.addEventListener('toggle',function(){if(x.open)track('faq_open',{question:x.querySelector('summary').textContent.trim(),id:x.id})});
});
if(location.hash){var t=d.querySelector(location.hash.replace(/[^#\w-]/g,''));if(t&&t.tagName==='DETAILS')t.open=true}
var sent={};
function onScroll(){
  var h=d.documentElement.scrollHeight-innerHeight;if(h<=0)return;
  var p=scrollY/h*100;
  [50,90].forEach(function(m){if(p>=m&&!sent[m]){sent[m]=1;track('scroll_depth',{percent:m,page_path:location.pathname})}});
}
addEventListener('scroll',onScroll,{passive:true});
})();
""".replace("__GA__", GA_ID)

HEAD_BOOT = ("<script>(function(){var r=document.documentElement;r.classList.add('js');"
             "try{var t=localStorage.getItem('theme');if(t==='dark'||t==='light')r.dataset.theme=t}catch(e){}})()</script>")


# ---------------------------------------------------------------- page rendering
def abs_url(p):
    return SITE + p


def alt_links(key):
    return (f'<link rel="alternate" hreflang="uk" href="{abs_url(path("uk", key))}">\n'
            f'<link rel="alternate" hreflang="en" href="{abs_url(path("en", key))}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{abs_url(path("uk", key))}">')


def jsonld(lang, key, page):
    u = UI[lang]
    url = abs_url(path(lang, key))
    person = {"@type": "Person", "@id": SITE + "/#alina", "name": "Аліна" if lang == "uk" else "Alina",
              "jobTitle": "Психологиня" if lang == "uk" else "Psychologist",
              "knowsAbout": ["Cognitive behavioural therapy", "Schema therapy", "Anxiety", "Burnout", "Trauma"],
              "knowsLanguage": ["uk", "en"]}
    graph = [{"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": u["site"], "inLanguage": ["uk", "en"]}]
    if key == "home":
        graph.append(person)
        graph.append({"@type": "ProfessionalService", "@id": SITE + "/#service", "name": u["site"], "url": url,
                      "image": SITE + "/og-image.png", "description": page["desc"], "provider": {"@id": SITE + "/#alina"},
                      "areaServed": "Worldwide", "availableLanguage": ["Ukrainian", "English"],
                      "serviceType": "Psychological counselling"})
    else:
        label = page.get("h1") or page["title"]
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": u["crumb_home"], "item": abs_url(path(lang, "home"))},
            {"@type": "ListItem", "position": 2, "name": label, "item": url}]})
    if key == "about":
        graph.append(person)
    if key == "faq":
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for _, q, a in page["faq"]]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))


def render(lang, key):
    u = UI[lang]
    page = C[lang][key]
    url = abs_url(path(lang, key))
    other = path("en" if lang == "uk" else "uk", key)
    if "faq" in page:
        items = "\n".join(
            f'<details id="{i}"><summary>{q}</summary><p>{a}</p></details>' for i, q, a in page["faq"])
        body = (hero_simple(page["h1"], page["lead"]) +
                f'<section class="sec"><div class="wrap"><div class="faq">{items}</div></div></section>' +
                cta_band(lang, "Залишилися питання?" if lang == "uk" else "Still have questions?",
                         "Напишіть мені, і я відповім." if lang == "uk" else "Write to me and I will answer."))
    elif key == "home":
        body = page["body"]
    else:
        body = hero_simple(page["h1"], page["lead"]) + page["body"]

    nav = "".join(
        f'<a href="{path(lang, k)}"{" aria-current=\"page\"" if k == key else ""}>{u["nav"][k]}</a>' for k in NAV)
    robots = '<meta name="robots" content="noindex,nofollow">\n' if DEMO else '<meta name="robots" content="index,follow,max-image-preview:large">\n'
    demo = f'<div class="demo">{u["demo"]}</div>' if DEMO else ""
    title = page["title"]
    desc = page["desc"]
    og_alt = "Аліна, психологиня онлайн" if lang == "uk" else "Alina, online psychologist"
    return f'''<!doctype html>
<html lang="{u["html"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}<link rel="canonical" href="{url}">
{alt_links(key)}
<meta name="theme-color" content="#F3EFE8" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#1B211E" media="(prefers-color-scheme: dark)">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{u["site"]}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{u["locale"]}">
<meta property="og:locale:alternate" content="{UI["en" if lang == "uk" else "uk"]["locale"]}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{og_alt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/og-image.png">
<link rel="preload" href="/fonts/onest-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/lora-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
{HEAD_BOOT}
<style>{CSS}</style>
<script type="application/ld+json">{jsonld(lang, key, page)}</script>
</head>
<body>
<a class="skip" href="#main">{u["skip"]}</a>
{demo}
<header class="site-head"><div class="wrap head-in">
  <a class="logo" href="{path(lang, "home")}">{"Аліна" if lang == "uk" else "Alina"} <span>{"психологиня" if lang == "uk" else "psychologist"}</span></a>
  <nav class="menu" id="menu" aria-label="{u["menu"]}">{nav}</nav>
  <div class="tools">
    <a class="pill" href="{other}" hreflang="{"en" if lang == "uk" else "uk"}" lang="{"en" if lang == "uk" else "uk"}" title="{u["other_lang_name"]}" data-track="lang_switch" data-label="{u["other_lang"]}">{u["other_lang"]}</a>
    <button class="icon-btn" id="theme" type="button" aria-label="{u["theme"]}" title="{u["theme"]}">{SUN_MOON}</button>
    <button class="burger" id="burger" type="button" aria-controls="menu" aria-expanded="false">{u["menu"]}</button>
  </div>
</div></header>
<main id="main">
{body}
</main>
<footer class="site-foot"><div class="wrap foot-in">
  <p>&copy; {date.today().year} {"Аліна" if lang == "uk" else "Alina"}. {u["rights"]}</p>
  <div class="foot-links"><a href="{path(lang, "privacy")}">{u["nav"]["privacy"]}</a><button type="button" class="linklike" data-cookie-settings>{u["cookie_settings"]}</button></div>
  <p class="emerg">{u["emergency"]}</p>
</div></footer>
<div class="cookie" id="cookie" role="dialog" aria-live="polite" aria-label="Cookie" hidden>
  <p>{u["cookie_text"]} <a href="{path(lang, "privacy")}">{u["cookie_more"]}</a></p>
  <div class="acts"><button type="button" class="btn ghost" data-consent="denied">{u["decline"]}</button><button type="button" class="btn" data-consent="granted">{u["accept"]}</button></div>
</div>
<script>{JS}</script>
</body>
</html>
'''


def write(rel, text):
    full = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)


def build_pages():
    for lang in ("uk", "en"):
        for key in SLUGS:
            write(path(lang, key).lstrip("/") + "index.html", render(lang, key))
    # 404 (bilingual, never indexed)
    write("404.html", f'''<!doctype html>
<html lang="uk"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>404</title>
<style>body{{font:18px/1.6 system-ui,sans-serif;display:grid;place-items:center;min-height:100vh;margin:0;padding:20px;background:#F3EFE8;color:#2B3A33;text-align:center}}
@media (prefers-color-scheme:dark){{body{{background:#1B211E;color:#E8EDE7}}a{{color:#9DBFA9}}}}a{{color:#4F7360}}</style></head>
<body><div><h1>404</h1><p>Сторінку не знайдено. <a href="/">На головну</a></p><p>Page not found. <a href="/en/">Go home</a></p></div></body></html>
''')


def build_seo():
    urls = []
    for key in SLUGS:
        for lang in ("uk", "en"):
            urls.append(
                f'  <url>\n    <loc>{abs_url(path(lang, key))}</loc>\n    <lastmod>{TODAY}</lastmod>\n'
                f'    <xhtml:link rel="alternate" hreflang="uk" href="{abs_url(path("uk", key))}"/>\n'
                f'    <xhtml:link rel="alternate" hreflang="en" href="{abs_url(path("en", key))}"/>\n'
                f'    <xhtml:link rel="alternate" hreflang="x-default" href="{abs_url(path("uk", key))}"/>\n  </url>')
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
          + "\n".join(urls) + "\n</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    write("site.webmanifest", json.dumps({
        "name": "Аліна · психологиня", "short_name": "Аліна", "lang": "uk", "start_url": "/",
        "display": "browser", "background_color": "#F3EFE8", "theme_color": "#4F7360",
        "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False, indent=2) + "\n")
    write("favicon.svg", '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<style>.b{fill:#4F7360}.t{fill:#fff}@media (prefers-color-scheme:dark){.b{fill:#9DBFA9}.t{fill:#12201A}}</style>
<rect class="b" width="64" height="64" rx="16"/>
<text class="t" x="32" y="45" text-anchor="middle" font-family="Georgia,serif" font-size="40" font-weight="700">А</text>
</svg>
''')


def build_images():
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Pillow not installed, skipping PNG icons")
        return
    serif = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
    sans = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    if not (os.path.exists(serif) and os.path.exists(sans)):
        print("DejaVu fonts not found, skipping PNG icons")
        return

    def icon(size, name):
        im = Image.new("RGB", (size, size), "#4F7360")
        m = Image.new("L", (size, size), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, size - 1, size - 1), size // 4, fill=255)
        bg = Image.new("RGB", (size, size), "#F3EFE8")
        bg.paste(im, mask=m)
        dr = ImageDraw.Draw(bg)
        f = ImageFont.truetype(serif, int(size * .62))
        dr.text((size / 2, size / 2 + size * .02), "А", font=f, fill="#FFFFFF", anchor="mm")
        bg.save(os.path.join(ROOT, name), optimize=True)

    icon(32, "favicon-32.png")
    icon(180, "apple-touch-icon.png")
    icon(192, "icon-192.png")
    icon(512, "icon-512.png")

    W, H = 1200, 630
    im = Image.new("RGB", (W, H), "#F3EFE8")
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle((820, 80, 1100, 560), 140, fill="#FBF9F5", outline="#DDD7CB", width=3)
    dr.text((960, 330), "А", font=ImageFont.truetype(serif, 200), fill="#4F7360", anchor="mm")
    dr.text((80, 200), "Аліна", font=ImageFont.truetype(serif, 96), fill="#2B3A33")
    dr.text((80, 330), "Психологиня онлайн", font=ImageFont.truetype(sans, 44), fill="#58675F")
    dr.text((80, 400), "Psychologist · Online", font=ImageFont.truetype(sans, 36), fill="#58675F")
    dr.rounded_rectangle((80, 490, 560, 550), 14, fill="#4F7360")
    dr.text((320, 520), "КПТ · Схема-терапія", font=ImageFont.truetype(sans, 30), fill="#FFFFFF", anchor="mm")
    im.save(os.path.join(ROOT, "og-image.png"), optimize=True)


if __name__ == "__main__":
    build_pages()
    build_seo()
    build_images()
    print("done")
