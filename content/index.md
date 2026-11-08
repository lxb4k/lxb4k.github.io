---
title: ФизТех | ПИ
---

<!-- CSS СТИЛИ -->
<style>
  .controls-wrapper {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    margin: 1.2rem 0;
    align-items: center;
  }

  .toggle-group {
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .toggle-label {
    font-size: 0.85rem;
    font-weight: bold;
    color: var(--gray);
    margin-right: 4px;
  }

  .week-btn, .group-btn, .ics-btn {
    background: var(--lightbg);
    color: var(--gray);
    border: 1px solid var(--lightgray);
    padding: 6px 14px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    font-size: 0.85rem;
    transition: all 0.2s ease;
  }

  .week-btn:hover, .group-btn:hover {
    border-color: var(--secondary);
    color: var(--secondary);
  }

  .week-btn.active, .group-btn.active {
    background: var(--secondary);
    color: #ffffff;
    border-color: var(--secondary);
  }

  .ics-btn {
    color: var(--secondary);
    border-color: var(--secondary);
    text-decoration: none;
    display: inline-flex;
    align-items: center;
  }

  .ics-btn:hover {
    background: var(--secondary);
    color: #ffffff;
  }

  .schedule-block {
    display: none;
  }

  /* ПК ВЕРСИЯ: 5 дней на экран + скролл для субботы */
  .schedule-block.active {
    display: flex;
    gap: 8px;
    overflow-x: auto;
    padding-bottom: 10px;
    scroll-behavior: smooth;
    align-items: flex-start;
  }

  .day-column {
    background-color: var(--lightbg);
    border: 1px solid var(--lightgray);
    border-radius: 8px;
    padding: 8px;
    display: flex;
    flex-direction: column;
    min-width: calc((100% - 32px) / 5);
    flex: 0 0 calc((100% - 32px) / 5);
    box-sizing: border-box;
  }

  /* МОБИЛЬНАЯ ВЕРСИЯ: Вертикальный список */
  @media (max-width: 768px) {
    .schedule-block.active {
      flex-direction: column;
      overflow-x: visible;
      align-items: stretch;
    }

    .day-column {
      min-width: 100%;
      flex: 1 1 100%;
    }
  }

  /* Стилизация полосы прокрутки */
  .schedule-block.active::-webkit-scrollbar {
    height: 6px;
  }

  .schedule-block.active::-webkit-scrollbar-track {
    background: var(--lightbg);
    border-radius: 4px;
  }

  .schedule-block.active::-webkit-scrollbar-thumb {
    background: var(--lightgray);
    border-radius: 4px;
  }

  .schedule-block.active::-webkit-scrollbar-thumb:hover {
    background: var(--secondary);
  }

  .day-header {
    font-weight: bold;
    font-size: 0.95rem;
    color: var(--secondary);
    border-bottom: 2px solid var(--tertiary);
    padding-bottom: 4px;
    margin-bottom: 8px;
    text-align: center;
  }

  .lesson-card {
    background-color: var(--highlight);
    border-left: 3px solid var(--secondary);
    border-radius: 4px;
    padding: 6px 8px;
    margin-bottom: 8px;
  }

  .lesson-card:last-child {
    margin-bottom: 0;
  }

  .lesson-time {
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--tertiary);
    margin-bottom: 2px;
  }

  .lesson-type {
    display: inline-block;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    line-height: 1.5;
    padding: 0 6px;
    margin-left: 4px;
    border-radius: 999px;
    border: 1px solid var(--lightgray);
    color: var(--gray);
    vertical-align: middle;
  }

  /* ЛК: синий цвет темы */
  .lesson-type.lk {
    color: var(--secondary);
    background: rgba(123, 151, 170, 0.16);
    background: color-mix(in srgb, var(--secondary) 16%, transparent);
    border-color: rgba(123, 151, 170, 0.5);
    border-color: color-mix(in srgb, var(--secondary) 50%, transparent);
  }

  /* ПЗ: мягкий сиреневый */
  .lesson-type.pz {
    color: #6b5b95;
    background: rgba(155, 138, 196, 0.16);
    border-color: rgba(155, 138, 196, 0.5);
  }

  :root[saved-theme="dark"] .lesson-type.pz { color: #b3a4dc; }

  .type-legend {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: wrap;
    font-size: 0.78rem;
    color: var(--gray);
    margin: -0.4rem 0 1rem;
  }

  .type-legend .lesson-type {
    margin-left: 0;
  }

  .lesson-name {
    font-size: 0.8rem;
    line-height: 1.2;
    color: var(--dark);
    margin-bottom: 4px;
  }

  .lesson-room {
    font-size: 0.7rem;
    display: inline-block;
    background-color: var(--lightgray);
    color: var(--gray);
    padding: 1px 4px;
    border-radius: 3px;
    font-family: monospace;
  }

  .no-lessons {
    font-size: 0.8rem;
    color: var(--gray);
    text-align: center;
    padding: 12px 0;
  }

  /* Блок контактов */
  .contact-box {
    margin-top: 2rem;
    padding: 12px 16px;
    background-color: var(--lightbg);
    border: 1px solid var(--lightgray);
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
  }

  .contact-text {
    font-size: 0.8rem;
    color: var(--gray);
    line-height: 1.3;
  }

  .contact-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 12px;
    border-radius: 5px;
    font-size: 0.8rem;
    font-weight: 600;
    text-decoration: none !important;
    background-color: #2AABEE;
    color: #ffffff !important;
    transition: opacity 0.2s ease;
  }

  .contact-btn:hover {
    opacity: 0.85;
  }

  /* ===== Новое: преподаватель, сегодня, текущая пара, блок «Следующая пара» ===== */
  .lesson-meta {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 3px 8px;
  }

  .lesson-teacher {
    font-size: 0.7rem;
    color: var(--gray);
  }

  .day-column.today,
  .day-column.focus-next {
    border-color: var(--secondary);
    box-shadow: 0 0 0 1px var(--secondary);
  }

  .day-column.today .day-header::after,
  .day-column.focus-next .day-header::after {
    content: "сегодня";
    display: inline-block;
    margin-left: 6px;
    padding: 0 7px;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    line-height: 1.6;
    vertical-align: middle;
    border-radius: 999px;
    background: var(--secondary);
    color: #ffffff;
  }

  .day-column.focus-next .day-header::after {
    content: "Завтра";
    display: inline-block;
    margin-left: 6px;
    padding: 0 7px;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    line-height: 1.6;
    vertical-align: middle;
    border-radius: 999px;
    background: var(--secondary);
    color: #ffffff;
	    
  }

  .lesson-card.now {
    background-color: rgba(123, 151, 170, 0.28);
    background-color: color-mix(in srgb, var(--secondary) 28%, transparent);
    box-shadow: 0 0 0 1px var(--secondary);
  }

  .lesson-card.now .lesson-time::after {
    content: "идёт сейчас";
    display: inline-block;
    margin-left: 6px;
    padding: 0 7px;
    font-size: 0.6rem;
    font-weight: 700;
    line-height: 1.6;
    vertical-align: middle;
    border-radius: 999px;
    background: var(--tertiary);
    color: #ffffff;
  }

  .week-btn.cur::after {
    content: " ●";
    font-size: 0.55em;
    vertical-align: middle;
  }

  .install-hint {
    font-size: 0.8rem;
    color: var(--gray);
    margin: -0.4rem 0 1rem;
  }

  .controls-wrapper .short {
    display: none;
  }

  /* Телефон: расписание должно быть видно сразу, без прокрутки */
  @media (max-width: 768px) {
    .content-meta {
      display: none !important;
    }

    h1.article-title {
      font-size: 1.5rem;
      margin: 0.3rem 0 0.2rem;
    }

    .controls-wrapper {
      gap: 8px;
      margin: 0.6rem 0;
    }

    .controls-wrapper .toggle-label,
    .controls-wrapper .full {
      display: none;
    }

    .controls-wrapper .short {
      display: inline;
    }

    .controls-wrapper .toggle-group {
      gap: 4px;
    }

    .type-legend {
      display: none;
    }
  }

  /* Кнопка «Конспекты»: только на телефоне (на ПК проводник виден сбоку) */
  .notes-btn {
    display: none;
  }

  @media (max-width: 768px) {
    .notes-btn {
      display: inline-flex;
    }

    /* Мигающий ободок на кнопке бокового меню, пока её не нажали */
    .explorer-attn {
      border-radius: 6px;
      animation: explorer-pulse 1.8s ease-out infinite;
    }
  }

  @keyframes explorer-pulse {
    0%   { box-shadow: 0 0 0 0 rgba(123, 151, 170, 0.75); }
    70%  { box-shadow: 0 0 0 10px rgba(123, 151, 170, 0); }
    100% { box-shadow: 0 0 0 0 rgba(123, 151, 170, 0); }
  }

  @media (prefers-reduced-motion: reduce) {
    .explorer-attn { animation: none; box-shadow: 0 0 0 2px var(--secondary); }
  }
</style>

<!-- ПЕРЕКЛЮЧАТЕЛИ, КАЛЕНДАРЬ И УСТАНОВКА -->
<div class="controls-wrapper">
  <div class="toggle-group">
    <span class="toggle-label">Моя группа:</span>
    <button class="group-btn active" data-group="262" onclick="setGroup('262', this)"><span class="full">ПИ-б-о-</span>262</button>
    <button class="group-btn" data-group="261" onclick="setGroup('261', this)"><span class="full">ПИ-б-о-</span>261</button>
  </div>
  <div class="toggle-group">
    <span class="toggle-label">Неделя:</span>
    <button class="week-btn active" data-week="a" onclick="setWeek('a', this)"><span class="full">Неделя </span>А</button>
    <button class="week-btn" data-week="b" onclick="setWeek('b', this)"><span class="full">Неделя </span>Б</button>
  </div>
  <button class="ics-btn" onclick="downloadStaticICS()"><span class="full">В календарь (.ics)</span><span class="short">ICS</span></button>
  <button class="ics-btn notes-btn" onclick="openNotes()">📚 Конспекты</button>
  <button class="ics-btn" id="install-btn" style="display:none" onclick="installApp()"><span class="full">Установить приложение</span><span class="short">Установить</span></button>
</div>

<div class="install-hint" id="ios-hint" style="display:none">Чтобы добавить на экран «Домой»: в Safari нажми «Поделиться» и выбери «На экран „Домой“».</div>

<div class="type-legend">
  <span class="lesson-type lk">ЛК</span> лекция
  <span class="lesson-type pz">ПЗ</span> практика
</div>

<!-- ================= ПИ-262 / НЕДЕЛЯ А ================= -->
<div id="sched-262-a" class="schedule-block active">
  <div class="day-column" data-d="0">
    <div class="day-header">Пн</div>
    <div class="lesson-card lk" data-start="690" data-end="780">
      <div class="lesson-time">11:30–13:00 <span class="lesson-type lk">ЛК</span></div>
      <div class="lesson-name">История России</div>
      <div class="lesson-meta"><span class="lesson-room">323А</span><span class="lesson-teacher">Манаев А.Ю.</span></div>
    </div>
    <div class="lesson-card lk" data-start="800" data-end="890">
      <div class="lesson-time">13:20–14:50 <span class="lesson-type lk">ЛК</span></div>
      <div class="lesson-name">Русский язык как государственный</div>
      <div class="lesson-meta"><span class="lesson-room">323А</span><span class="lesson-teacher">Прадид О.Ю.</span></div>
    </div>
  </div>
  <div class="day-column" data-d="1">
    <div class="day-header">Вт</div>
    <div class="lesson-card pz" data-start="480" data-end="570">
      <div class="lesson-time">08:00–09:30 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Проектная деятельность</div>
      <div class="lesson-meta"><span class="lesson-room">315А</span><span class="lesson-teacher">Нестеренко Н.А.</span></div>
    </div>
    <div class="lesson-card lk" data-start="590" data-end="680">
      <div class="lesson-time">09:50–11:20 <span class="lesson-type lk">ЛК</span></div>
      <div class="lesson-name">Алгоритмизация и программирование</div>
      <div class="lesson-meta"><span class="lesson-room">302А</span><span class="lesson-teacher">Чабанов В.В.</span></div>
    </div>
    <div class="lesson-card lk" data-start="690" data-end="780">
      <div class="lesson-time">11:30–13:00 <span class="lesson-type lk">ЛК</span></div>
      <div class="lesson-name">Высшая математика</div>
      <div class="lesson-meta"><span class="lesson-room">323А</span><span class="lesson-teacher">Смирнова С.И.</span></div>
    </div>
  </div>
  <div class="day-column" data-d="2">
    <div class="day-header">Ср</div>
    <div class="lesson-card pz" data-start="480" data-end="570">
      <div class="lesson-time">08:00–09:30 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Иностранный язык</div>
      <div class="lesson-meta"><span class="lesson-room">531Б</span><span class="lesson-teacher">Мельниченко Т.В.</span></div>
    </div>
    <div class="lesson-card pz" data-start="590" data-end="680">
      <div class="lesson-time">09:50–11:20 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Высшая математика</div>
      <div class="lesson-meta"><span class="lesson-room">211А</span><span class="lesson-teacher">Смирнова С.И.</span></div>
    </div>
    <div class="lesson-card pz" data-start="690" data-end="780">
      <div class="lesson-time">11:30–13:00 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">История России</div>
      <div class="lesson-meta"><span class="lesson-room">302В</span><span class="lesson-teacher">Манаев А.Ю.</span></div>
    </div>
  </div>
  <div class="day-column" data-d="3">
    <div class="day-header">Чт</div>
    <div class="lesson-card pz" data-start="590" data-end="680">
      <div class="lesson-time">09:50–11:20 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Физическая культура</div>
      <div class="lesson-meta"><span class="lesson-room">спортзал</span><span class="lesson-teacher">Мищенко С.Г.</span></div>
    </div>
    <div class="lesson-card pz" data-start="690" data-end="780">
      <div class="lesson-time">11:30–13:00 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Русский язык как государственный</div>
      <div class="lesson-meta"><span class="lesson-room">412В</span><span class="lesson-teacher">Прадид О.Ю.</span></div>
    </div>
  </div>
  <div class="day-column" data-d="4">
    <div class="day-header">Пт</div>
    <div class="lesson-card pz" data-start="900" data-end="990">
      <div class="lesson-time">15:00–16:30 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Алгоритмизация и программирование</div>
      <div class="lesson-meta"><span class="lesson-room">117А</span><span class="lesson-teacher">Чабанов В.В.</span></div>
    </div>
    <div class="lesson-card pz" data-start="1000" data-end="1090">
      <div class="lesson-time">16:40–18:10 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Информатика и основы программирования</div>
      <div class="lesson-meta"><span class="lesson-room">119А</span><span class="lesson-teacher">ас.Абдурахманова Ф.Э.</span></div>
    </div>
  </div>
  <div class="day-column" data-d="5">
    <div class="day-header">Сб</div>
    <div class="no-lessons">Пар нет</div>
  </div>
</div>

<!-- ================= ПИ-262 / НЕДЕЛЯ Б ================= -->
<div id="sched-262-b" class="schedule-block">
  <div class="day-column" data-d="0">
    <div class="day-header">Пн</div>
    <div class="lesson-card lk" data-start="690" data-end="780">
      <div class="lesson-time">11:30–13:00 <span class="lesson-type lk">ЛК</span></div>
      <div class="lesson-name">История России</div>
      <div class="lesson-meta"><span class="lesson-room">323А</span><span class="lesson-teacher">Манаев А.Ю.</span></div>
    </div>
    <div class="lesson-card lk" data-start="800" data-end="890">
      <div class="lesson-time">13:20–14:50 <span class="lesson-type lk">ЛК</span></div>
      <div class="lesson-name">Информатика и основы программирования</div>
      <div class="lesson-meta"><span class="lesson-room">323А</span><span class="lesson-teacher">Брецько М.В.</span></div>
    </div>
    <div class="lesson-card lk" data-start="900" data-end="990">
      <div class="lesson-time">15:00–16:30 <span class="lesson-type lk">ЛК</span></div>
      <div class="lesson-name">Структуры и алгоритмы обработки данных</div>
      <div class="lesson-meta"><span class="lesson-room">323А</span><span class="lesson-teacher">Горская И.Ю.</span></div>
    </div>
  </div>
  <div class="day-column" data-d="1">
    <div class="day-header">Вт</div>
    <div class="lesson-card lk" data-start="590" data-end="680">
      <div class="lesson-time">09:50–11:20 <span class="lesson-type lk">ЛК</span></div>
      <div class="lesson-name">Алгоритмизация и программирование</div>
      <div class="lesson-meta"><span class="lesson-room">302А</span><span class="lesson-teacher">Чабанов В.В.</span></div>
    </div>
    <div class="lesson-card lk" data-start="690" data-end="780">
      <div class="lesson-time">11:30–13:00 <span class="lesson-type lk">ЛК</span></div>
      <div class="lesson-name">Высшая математика</div>
      <div class="lesson-meta"><span class="lesson-room">323А</span><span class="lesson-teacher">Смирнова С.И.</span></div>
    </div>
  </div>
  <div class="day-column" data-d="2">
    <div class="day-header">Ср</div>
    <div class="lesson-card pz" data-start="480" data-end="570">
      <div class="lesson-time">08:00–09:30 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Иностранный язык</div>
      <div class="lesson-meta"><span class="lesson-room">525Б</span><span class="lesson-teacher">Мельниченко Т.В.</span></div>
    </div>
    <div class="lesson-card pz" data-start="590" data-end="680">
      <div class="lesson-time">09:50–11:20 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Высшая математика</div>
      <div class="lesson-meta"><span class="lesson-room">211А</span><span class="lesson-teacher">Смирнова С.И.</span></div>
    </div>
    <div class="lesson-card pz" data-start="690" data-end="780">
      <div class="lesson-time">11:30–13:00 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">История России</div>
      <div class="lesson-meta"><span class="lesson-room">302В</span><span class="lesson-teacher">Манаев А.Ю.</span></div>
    </div>
  </div>
  <div class="day-column" data-d="3">
    <div class="day-header">Чт</div>
    <div class="lesson-card pz" data-start="590" data-end="680">
      <div class="lesson-time">09:50–11:20 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Физическая культура</div>
      <div class="lesson-meta"><span class="lesson-room">спортзал</span><span class="lesson-teacher">Мищенко С.Г.</span></div>
    </div>
  </div>
  <div class="day-column" data-d="4">
    <div class="day-header">Пт</div>
    <div class="lesson-card pz" data-start="900" data-end="990">
      <div class="lesson-time">15:00–16:30 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Алгоритмизация и программирование</div>
      <div class="lesson-meta"><span class="lesson-room">117А</span><span class="lesson-teacher">Чабанов В.В.</span></div>
    </div>
    <div class="lesson-card pz" data-start="1000" data-end="1090">
      <div class="lesson-time">16:40–18:10 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Информатика и основы программирования</div>
      <div class="lesson-meta"><span class="lesson-room">119А</span><span class="lesson-teacher">ас.Абдурахманова Ф.Э.</span></div>
    </div>
  </div>
  <div class="day-column" data-d="5">
    <div class="day-header">Сб</div>
    <div class="lesson-card pz" data-start="800" data-end="890">
      <div class="lesson-time">13:20–14:50 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Структуры и алгоритмы обработки данных</div>
      <div class="lesson-meta"><span class="lesson-room">308А</span><span class="lesson-teacher">Горская И.Ю.</span></div>
    </div>
  </div>
</div>

<!-- ================= ПИ-261 / НЕДЕЛЯ А ================= -->
<div id="sched-261-a" class="schedule-block">
  <div class="day-column" data-d="0">
    <div class="day-header">Пн</div>
    <div class="lesson-card lk" data-start="690" data-end="780">
      <div class="lesson-time">11:30–13:00 <span class="lesson-type lk">ЛК</span></div>
      <div class="lesson-name">История России</div>
      <div class="lesson-meta"><span class="lesson-room">323А</span><span class="lesson-teacher">Манаев А.Ю.</span></div>
    </div>
    <div class="lesson-card lk" data-start="800" data-end="890">
      <div class="lesson-time">13:20–14:50 <span class="lesson-type lk">ЛК</span></div>
      <div class="lesson-name">Русский язык как государственный</div>
      <div class="lesson-meta"><span class="lesson-room">323А</span><span class="lesson-teacher">Прадид О.Ю.</span></div>
    </div>
    <div class="lesson-card pz" data-start="900" data-end="990">
      <div class="lesson-time">15:00–16:30 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Русский язык как государственный</div>
      <div class="lesson-meta"><span class="lesson-room">411В</span><span class="lesson-teacher">Прадид О.Ю.</span></div>
    </div>
    <div class="lesson-card pz" data-start="1000" data-end="1090">
      <div class="lesson-time">16:40–18:10 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Иностранный язык (п/гр 2)</div>
      <div class="lesson-meta"><span class="lesson-room">531Б</span><span class="lesson-teacher">Мельниченко Т.В.</span></div>
    </div>
  </div>
  <div class="day-column" data-d="1">
    <div class="day-header">Вт</div>
    <div class="lesson-card lk" data-start="590" data-end="680">
      <div class="lesson-time">09:50–11:20 <span class="lesson-type lk">ЛК</span></div>
      <div class="lesson-name">Алгоритмизация и программирование</div>
      <div class="lesson-meta"><span class="lesson-room">302А</span><span class="lesson-teacher">Чабанов В.В.</span></div>
    </div>
    <div class="lesson-card lk" data-start="690" data-end="780">
      <div class="lesson-time">11:30–13:00 <span class="lesson-type lk">ЛК</span></div>
      <div class="lesson-name">Высшая математика</div>
      <div class="lesson-meta"><span class="lesson-room">323А</span><span class="lesson-teacher">Смирнова С.И.</span></div>
    </div>
  </div>
  <div class="day-column" data-d="2">
    <div class="day-header">Ср</div>
    <div class="lesson-card pz" data-start="590" data-end="680">
      <div class="lesson-time">09:50–11:20 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">История России</div>
      <div class="lesson-meta"><span class="lesson-room">302В</span><span class="lesson-teacher">Манаев А.Ю.</span></div>
    </div>
    <div class="lesson-card pz" data-start="690" data-end="780">
      <div class="lesson-time">11:30–13:00 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Иностранный язык (п/гр 1)</div>
      <div class="lesson-meta"><span class="lesson-room">500Б</span><span class="lesson-teacher">Шестакова Е.С.</span></div>
    </div>
    <div class="lesson-card pz" data-start="800" data-end="890">
      <div class="lesson-time">13:20–14:50 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Высшая математика</div>
      <div class="lesson-meta"><span class="lesson-room">211А</span><span class="lesson-teacher">Смирнова С.И.</span></div>
    </div>
  </div>
  <div class="day-column" data-d="3">
    <div class="day-header">Чт</div>
    <div class="lesson-card pz" data-start="590" data-end="680">
      <div class="lesson-time">09:50–11:20 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Физическая культура</div>
      <div class="lesson-meta"><span class="lesson-room">спортзал</span><span class="lesson-teacher">Ковальчук Е.С.</span></div>
    </div>
    <div class="lesson-card pz" data-start="690" data-end="780">
      <div class="lesson-time">11:30–13:00 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Информатика и основы программирования (п/гр 1)</div>
      <div class="lesson-meta"><span class="lesson-room">119А</span><span class="lesson-teacher">ас.Абдурахманова Ф.Э.</span></div>
    </div>
    <div class="lesson-card pz" data-start="800" data-end="890">
      <div class="lesson-time">13:20–14:50 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Информатика и основы программирования (п/гр 2)</div>
      <div class="lesson-meta"><span class="lesson-room">119А</span><span class="lesson-teacher">ас.Абдурахманова Ф.Э.</span></div>
    </div>
  </div>
  <div class="day-column" data-d="4">
    <div class="day-header">Пт</div>
    <div class="lesson-card pz" data-start="690" data-end="780">
      <div class="lesson-time">11:30–13:00 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Алгоритмизация и программирование (п/гр 1)</div>
      <div class="lesson-meta"><span class="lesson-room">8А</span><span class="lesson-teacher">Чабанов В.В.</span></div>
    </div>
    <div class="lesson-card pz" data-start="800" data-end="890">
      <div class="lesson-time">13:20–14:50 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Алгоритмизация и программирование (п/гр 2)</div>
      <div class="lesson-meta"><span class="lesson-room">8А</span><span class="lesson-teacher">Чабанов В.В.</span></div>
    </div>
  </div>
  <div class="day-column" data-d="5">
    <div class="day-header">Сб</div>
    <div class="no-lessons">Пар нет</div>
  </div>
</div>

<!-- ================= ПИ-261 / НЕДЕЛЯ Б ================= -->
<div id="sched-261-b" class="schedule-block">
  <div class="day-column" data-d="0">
    <div class="day-header">Пн</div>
    <div class="lesson-card lk" data-start="690" data-end="780">
      <div class="lesson-time">11:30–13:00 <span class="lesson-type lk">ЛК</span></div>
      <div class="lesson-name">История России</div>
      <div class="lesson-meta"><span class="lesson-room">323А</span><span class="lesson-teacher">Манаев А.Ю.</span></div>
    </div>
    <div class="lesson-card lk" data-start="800" data-end="890">
      <div class="lesson-time">13:20–14:50 <span class="lesson-type lk">ЛК</span></div>
      <div class="lesson-name">Информатика и основы программирования</div>
      <div class="lesson-meta"><span class="lesson-room">323А</span><span class="lesson-teacher">Брецько М.В.</span></div>
    </div>
    <div class="lesson-card lk" data-start="900" data-end="990">
      <div class="lesson-time">15:00–16:30 <span class="lesson-type lk">ЛК</span></div>
      <div class="lesson-name">Структуры и алгоритмы обработки данных</div>
      <div class="lesson-meta"><span class="lesson-room">323А</span><span class="lesson-teacher">Горская И.Ю.</span></div>
    </div>
    <div class="lesson-card pz" data-start="1000" data-end="1090">
      <div class="lesson-time">16:40–18:10 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Иностранный язык (п/гр 2)</div>
      <div class="lesson-meta"><span class="lesson-room">531Б</span><span class="lesson-teacher">Мельниченко Т.В.</span></div>
    </div>
  </div>
  <div class="day-column" data-d="1">
    <div class="day-header">Вт</div>
    <div class="lesson-card pz" data-start="480" data-end="570">
      <div class="lesson-time">08:00–09:30 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Проектная деятельность</div>
      <div class="lesson-meta"><span class="lesson-room">315А</span><span class="lesson-teacher">Нестеренко Н.А.</span></div>
    </div>
    <div class="lesson-card lk" data-start="590" data-end="680">
      <div class="lesson-time">09:50–11:20 <span class="lesson-type lk">ЛК</span></div>
      <div class="lesson-name">Алгоритмизация и программирование</div>
      <div class="lesson-meta"><span class="lesson-room">302А</span><span class="lesson-teacher">Чабанов В.В.</span></div>
    </div>
    <div class="lesson-card lk" data-start="690" data-end="780">
      <div class="lesson-time">11:30–13:00 <span class="lesson-type lk">ЛК</span></div>
      <div class="lesson-name">Высшая математика</div>
      <div class="lesson-meta"><span class="lesson-room">323А</span><span class="lesson-teacher">Смирнова С.И.</span></div>
    </div>
  </div>
  <div class="day-column" data-d="2">
    <div class="day-header">Ср</div>
    <div class="lesson-card pz" data-start="480" data-end="570">
      <div class="lesson-time">08:00–09:30 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Высшая математика</div>
      <div class="lesson-meta"><span class="lesson-room">211А</span><span class="lesson-teacher">Смирнова С.И.</span></div>
    </div>
    <div class="lesson-card pz" data-start="590" data-end="680">
      <div class="lesson-time">09:50–11:20 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">История России</div>
      <div class="lesson-meta"><span class="lesson-room">302В</span><span class="lesson-teacher">Манаев А.Ю.</span></div>
    </div>
    <div class="lesson-card pz" data-start="690" data-end="780">
      <div class="lesson-time">11:30–13:00 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Иностранный язык (п/гр 1)</div>
      <div class="lesson-meta"><span class="lesson-room">500Б</span><span class="lesson-teacher">Шестакова Е.С.</span></div>
    </div>
  </div>
  <div class="day-column" data-d="3">
    <div class="day-header">Чт</div>
    <div class="lesson-card pz" data-start="590" data-end="680">
      <div class="lesson-time">09:50–11:20 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Физическая культура</div>
      <div class="lesson-meta"><span class="lesson-room">спортзал</span><span class="lesson-teacher">Ковальчук Е.С.</span></div>
    </div>
    <div class="lesson-card pz" data-start="690" data-end="780">
      <div class="lesson-time">11:30–13:00 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Информатика и основы программирования (п/гр 1)</div>
      <div class="lesson-meta"><span class="lesson-room">120А</span><span class="lesson-teacher">ас.Абдурахманова Ф.Э.</span></div>
    </div>
    <div class="lesson-card pz" data-start="800" data-end="890">
      <div class="lesson-time">13:20–14:50 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Информатика и основы программирования (п/гр 2)</div>
      <div class="lesson-meta"><span class="lesson-room">120А</span><span class="lesson-teacher">ас.Абдурахманова Ф.Э.</span></div>
    </div>
  </div>
  <div class="day-column" data-d="4">
    <div class="day-header">Пт</div>
    <div class="lesson-card pz" data-start="690" data-end="780">
      <div class="lesson-time">11:30–13:00 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Алгоритмизация и программирование (п/гр 1)</div>
      <div class="lesson-meta"><span class="lesson-room">8А</span><span class="lesson-teacher">Чабанов В.В.</span></div>
    </div>
    <div class="lesson-card pz" data-start="800" data-end="890">
      <div class="lesson-time">13:20–14:50 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Алгоритмизация и программирование (п/гр 2)</div>
      <div class="lesson-meta"><span class="lesson-room">8А</span><span class="lesson-teacher">Чабанов В.В.</span></div>
    </div>
  </div>
  <div class="day-column" data-d="5">
    <div class="day-header">Сб</div>
    <div class="lesson-card pz" data-start="590" data-end="680">
      <div class="lesson-time">09:50–11:20 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Структуры и алгоритмы обработки данных (п/гр 1)</div>
      <div class="lesson-meta"><span class="lesson-room">308А</span><span class="lesson-teacher">Горская И.Ю.</span></div>
    </div>
    <div class="lesson-card pz" data-start="690" data-end="780">
      <div class="lesson-time">11:30–13:00 <span class="lesson-type pz">ПЗ</span></div>
      <div class="lesson-name">Структуры и алгоритмы обработки данных (п/гр 2)</div>
      <div class="lesson-meta"><span class="lesson-room">308А</span><span class="lesson-teacher">Горская И.Ю.</span></div>
    </div>
  </div>
</div>

Официальное расписание на [cfuv.ru](https://cfuv.ru/raspisanie/): [ПИ-б-о-262](https://cfuv.ru/raspisanie/#g=%D0%9F%D0%98-%D0%B1-%D0%BE-262) · [ПИ-б-о-261](https://cfuv.ru/raspisanie/#g=%D0%9F%D0%98-%D0%B1-%D0%BE-261)

Ещё: [[Учёба/index|Учёба]] (в разработке)

<!-- БЛОК ОБ АВТОРЕ -->
<div class="contact-box">
  <span class="contact-text">Заметили ошибку в расписании или есть предложения?</span>
  <a href="https://t.me/lxb4k" target="_blank" class="contact-btn">
    Telegram
  </a>
</div>

<!-- СКРИПТ: переключатели, сегодня, текущая пара, календарь, веб-приложение -->
<script>
var currentGroup = '262';
var currentWeek = 'a';
var realWeek = 'a';
var schedTimer = null;
var installPrompt = null;
var BASE = Date.UTC(2026, 8, 7);
var DAY_NAMES = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'];
var DAY_ON = ['в понедельник', 'во вторник', 'в среду', 'в четверг', 'в пятницу', 'в субботу'];

var icsFiles = {
  '261': '/static/files/pi-261.ics',
  '262': '/static/files/pi-262.ics'
};

function esc(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function hm(m) {
  var h = Math.floor(m / 60), x = m % 60;
  return (h < 10 ? '0' : '') + h + ':' + (x < 10 ? '0' : '') + x;
}

function weekOf(utcMs) {
  var w = Math.floor((utcMs - BASE) / 86400000 / 7);
  return (((w % 2) + 2) % 2) ? 'b' : 'a';
}

function nowInfo() {
  var n = new Date();
  return {
    utc: Date.UTC(n.getFullYear(), n.getMonth(), n.getDate()),
    dow: (n.getDay() + 6) % 7,
    mins: n.getHours() * 60 + n.getMinutes()
  };
}

function lessonsOf(g, w, d) {
  var col = document.querySelector('#sched-' + g + '-' + w + ' .day-column[data-d="' + d + '"]');
  if (!col) return [];
  return Array.prototype.map.call(col.querySelectorAll('.lesson-card'), function (c) {
    var room = c.querySelector('.lesson-room');
    var teacher = c.querySelector('.lesson-teacher');
    return {
      start: Number(c.getAttribute('data-start')),
      end: Number(c.getAttribute('data-end')),
      name: c.querySelector('.lesson-name').textContent,
      room: room ? room.textContent : '',
      teacher: teacher ? teacher.textContent : ''
    };
  });
}

/* День, который показываем «в фокусе»: сегодня, пока есть пары, иначе ближайший день с парами */
function focusFor(g) {
  var n = nowInfo();
  for (var i = 0; i < 14; i++) {
    var d = (n.dow + i) % 7;
    if (d > 5) continue;
    var w = weekOf(n.utc + i * 86400000);
    var list = lessonsOf(g, w, d);
    if (!list.length) continue;
    if (i === 0) {
      var last = 0;
      list.forEach(function (l) { if (l.end > last) last = l.end; });
      if (n.mins >= last) continue;
    }
    return { i: i, d: d, week: w };
  }
  return null;
}

function markToday() {
  var n = nowInfo();
  Array.prototype.forEach.call(document.querySelectorAll('.day-column.today, .day-column.focus, .day-column.focus-next, .lesson-card.now'), function (el) {
    el.classList.remove('today');
    el.classList.remove('focus');
    el.classList.remove('focus-next');
    el.removeAttribute('data-badge');
    el.classList.remove('now');
  });
  ['262', '261'].forEach(function (g) {
    if (n.dow <= 5) {
      var col = document.querySelector('#sched-' + g + '-' + realWeek + ' .day-column[data-d="' + n.dow + '"]');
      if (col) {
        col.classList.add('today');
        Array.prototype.forEach.call(col.querySelectorAll('.lesson-card'), function (c) {
          var s0 = Number(c.getAttribute('data-start'));
          var e0 = Number(c.getAttribute('data-end'));
          if (n.mins >= s0 && n.mins < e0) c.classList.add('now');
        });
      }
    }
    var f = focusFor(g);
    if (!f) return;
    var fc = document.querySelector('#sched-' + g + '-' + f.week + ' .day-column[data-d="' + f.d + '"]');
    if (!fc) return;
    fc.classList.add('focus');
    if (f.i > 0) {
      fc.classList.add('focus-next');
      fc.setAttribute('data-badge', f.i === 1 ? 'завтра' : 'далее');
    }
  });
}

function scrollToToday() {
  var blk = document.getElementById('sched-' + currentGroup + '-' + currentWeek);
  if (!blk) return;
  var col = blk.querySelector('.day-column.focus');
  if (!col || blk.scrollWidth <= blk.clientWidth) return;
  var r = col.getBoundingClientRect();
  var b = blk.getBoundingClientRect();
  if (r.right > b.right || r.left < b.left) blk.scrollLeft += r.left - b.left;
}

/* Телефон: при открытии прокручиваем так, чтобы нужный день оказался по центру экрана */
function scrollToTodayMobile() {
  if (!window.matchMedia || !window.matchMedia('(max-width: 768px)').matches) return;
  if (window.scrollY > 100) return;
  var blk = document.getElementById('sched-' + currentGroup + '-' + currentWeek);
  var col = blk && blk.querySelector('.day-column.focus');
  if (!col) return;
  var r = col.getBoundingClientRect();
  var vh = window.innerHeight;
  var target = r.height > vh * 0.85
    ? r.top + window.scrollY - 16
    : r.top + window.scrollY - (vh - r.height) / 2;
  if (target < 0) target = 0;
  if (Math.abs(target - window.scrollY) < 30) return;
  window.scrollTo(0, target);
}

/* Боковое меню с конспектами (Quartz Explorer) */
function explorerToggles() {
  return Array.prototype.slice.call(document.querySelectorAll(
    '.explorer-toggle.mobile-explorer, .mobile-explorer, .explorer > button, .explorer-toggle'
  ));
}

function markNotesToggle() {
  var seen = false;
  try { seen = localStorage.getItem('explorer-seen') === '1'; } catch (e) {}
  if (seen) return;
  explorerToggles().forEach(function (b) {
    if (b.__attn) return;
    b.__attn = true;
    b.classList.add('explorer-attn');
    b.addEventListener('click', function () {
      explorerToggles().forEach(function (x) { x.classList.remove('explorer-attn'); });
      try { localStorage.setItem('explorer-seen', '1'); } catch (e) {}
    });
  });
}

function openNotes() {
  var list = explorerToggles();
  for (var i = 0; i < list.length; i++) {
    if (list[i].offsetParent !== null) { list[i].click(); return; }
  }
  window.scrollTo(0, 0);
  markNotesToggle();
}

function syncButtons() {
  Array.prototype.forEach.call(document.querySelectorAll('.group-btn'), function (b) {
    b.classList.toggle('active', b.getAttribute('data-group') === currentGroup);
  });
  Array.prototype.forEach.call(document.querySelectorAll('.week-btn'), function (b) {
    b.classList.toggle('active', b.getAttribute('data-week') === currentWeek);
    b.classList.toggle('cur', b.getAttribute('data-week') === realWeek);
  });
}

var userWeek = false;

function showBlock() {
  Array.prototype.forEach.call(document.querySelectorAll('.schedule-block'), function (el) {
    el.classList.remove('active');
  });
  var target = document.getElementById('sched-' + currentGroup + '-' + currentWeek);
  if (target) target.classList.add('active');
}

function tick() {
  realWeek = weekOf(nowInfo().utc);
  if (!userWeek) {
    var f = focusFor(currentGroup);
    if (f && f.week !== currentWeek) { currentWeek = f.week; showBlock(); }
  }
  markToday();
  syncButtons();
}

function updateDisplay() {
  showBlock();
  tick();
  scrollToToday();
}

function setGroup(group) {
  currentGroup = group;
  try { localStorage.setItem('sched-group', group); } catch (e) {}
  updateDisplay();
}

function setWeek(week) {
  userWeek = true;
  currentWeek = week;
  updateDisplay();
}

function downloadStaticICS() {
  var filePath = icsFiles[currentGroup];
  if (filePath) {
    var link = document.createElement('a');
    link.href = filePath;
    link.download = 'ПИ-б-о-' + currentGroup + '.ics';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
}

function installApp() {
  if (!installPrompt) return;
  installPrompt.prompt();
  installPrompt.userChoice.then(function () {
    installPrompt = null;
    var b = document.getElementById('install-btn');
    if (b) b.style.display = 'none';
  });
}

function setupPWA() {
  var head = document.head;
  function add(tag, attrs) {
    var el = document.createElement(tag);
    Object.keys(attrs).forEach(function (k) { el.setAttribute(k, attrs[k]); });
    head.appendChild(el);
  }
  if (!document.querySelector('link[rel="manifest"]')) add('link', { rel: 'manifest', href: '/static/manifest.json' });
  if (!document.querySelector('link[rel="apple-touch-icon"]')) add('link', { rel: 'apple-touch-icon', href: '/static/icons/apple-touch-icon.png' });
  if (!document.querySelector('meta[name="apple-mobile-web-app-capable"]')) {
    add('meta', { name: 'apple-mobile-web-app-capable', content: 'yes' });
    add('meta', { name: 'apple-mobile-web-app-title', content: 'Расписание' });
    add('meta', { name: 'mobile-web-app-capable', content: 'yes' });
  }
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(function () {});
  }
  var standalone = (window.matchMedia && window.matchMedia('(display-mode: standalone)').matches) || window.navigator.standalone;
  var hint = document.getElementById('ios-hint');
  if (hint && !standalone && /iphone|ipad|ipod/i.test(navigator.userAgent)) hint.style.display = 'block';
}

/* Первый заход: тёмная тема. Дальше работает обычный переключатель, выбор запоминается. */
function defaultDarkTheme() {
  try {
    if (localStorage.getItem('theme')) return;
    var root = document.documentElement;
    root.setAttribute('saved-theme', 'dark');
    localStorage.setItem('theme', 'dark');
    var tgl = document.querySelector('#darkmode-toggle');
    if (tgl) tgl.checked = true;
  } catch (e) {}
}

function initSchedule() {
  if (!document.getElementById('sched-262-a')) return;
  defaultDarkTheme();
  var n = nowInfo();
  realWeek = weekOf(n.utc);
  try {
    var sg = localStorage.getItem('sched-group');
    if (sg === '261' || sg === '262') currentGroup = sg;
  } catch (e) {}
  var f0 = focusFor(currentGroup);
  currentWeek = f0 ? f0.week : (n.dow > 5 ? (realWeek === 'a' ? 'b' : 'a') : realWeek);
  userWeek = false;
  updateDisplay();
  if (schedTimer) clearInterval(schedTimer);
  schedTimer = setInterval(tick, 30000);
  setupPWA();
  if (document.readyState === 'complete') setTimeout(scrollToTodayMobile, 80);
  else window.addEventListener('load', function () { setTimeout(scrollToTodayMobile, 80); }, { once: true });
  setTimeout(markNotesToggle, 300);
}

if (!window.__schedBound) {
  window.__schedBound = true;
  document.addEventListener('nav', initSchedule);
  window.addEventListener('beforeinstallprompt', function (e) {
    e.preventDefault();
    installPrompt = e;
    var b = document.getElementById('install-btn');
    if (b) b.style.display = 'inline-flex';
  });
  window.addEventListener('appinstalled', function () {
    var b = document.getElementById('install-btn');
    if (b) b.style.display = 'none';
  });
  document.addEventListener('visibilitychange', function () {
    if (!document.hidden) tick();
  });
}

initSchedule();

</script>
