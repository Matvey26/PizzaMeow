# PizzaMeow

# Содержание
1. О работе над проектом
    - цель
    - задачи
    - как шёл процесс разработки
    - ссылки на таск-трекер и базу знаний
2. О команде
    - Состав команды и роли
3. Структура проекта
4. Установка
    - Подготовка
    - CLI-приложение
    - Сервер

# О работе над проектом
Нашей целью было разработать сервис для заказа пиццы, который позволит, во-первых, легко автоматизировать этот процесс (bash скрипты), и во-вторых, сделать его максимально удобным и простым в рамках CLI-приложения.

**Нашими основными задачами выступили:**
1. Разработка CLI-приложения
2. Создание сервера

Работа шла параллельно над сервером и клиентом. При этом каждый пункт выполнялся примерно в такой последовательности:

1. Одновременно:
    - Пишется документация API и функции, которые обрабатывают запросы
    - Пишутся парсеры и сами команды
3. Если для существенного упрощения кода клиента требуется добавить новый функционал серверу, он дописывается
4. Если изменился API, то вносятся правки в клиенте

Каждая задача разбивалась на множество составных и добавлялась в наш [таск-трекер](https://app.todoist.com/auth/join?invite_code=ks4AAgAc2SA5M2Y0YjhmYjI3YjYzNDdmZTJiYjE0MmRiYWQ5Y2UzNA)  (перейдите во вкладку "Проекты, в которых я не участвую" и нажмите на единственный проект "IT-проекты")

Также некоторые задачи требовали некоторой подготовительной работы, в том числе изучение необходимых технологий. Вы можете посмотреть наш [notion](https://melodic-cormorant-2d7.notion.site/738c803f5ca64cc6b341706a4388f3e1?pvs=25)

# О команде
Наша команда состоит из ~~Python Senior разработчиков~~ 4-х студентов 1-го курса группы М8О-107Б-23

## Состав команды
- **Попов Владимир Дмитриевич** — писал команды для CLI-приложения
- **Усов Сергей Евгеньевич** — писал два интерфейса взаимодействия: приложения с сервером и сервера с БД
- **Ивченко Матвей Сергеевич** — тимлид, полностью бэкенд и особо сложные команды в CLI-приложении
- **Глебова Мария Алексеевна** — фронтенд, презентация, дизайнер


# Структура проекта

```
client/
└── pizza_cli_app/
    ├── api/
    ├── commands/
    ├── utils/
    ├── cli.py
├── requirements.txt
└── setup.py
server/
└── app/
    ├── admin_cli/
    ├── model/
    ├── utils/
    ├── views/
    ├── mock/
    ├── app.py
    ├── database.py
    └── swagger.yml
└── migrations/
    └── versions
├── cli_admin.py
├── requirements.txt
├── runserver.bat
├── runserver.sh
README.md
```

### Описание структуры проекта:

- **client/**: Директория клиента.
  - **pizza_cli_app/**: Основная директория клиента.
    - **api/**: Содержит класс Session, который предоставляет методы для взаимодействия с сервером.
    - **commands/**: Содержит файлы с командами для CLI.
    - **utils/**: Утилиты, вспомогательные функции и модули, такие как постараничный вывод в curses.
    - **cli.py**: Основной файл для запуска CLI приложения.
  - **requirements.txt**: Список зависимостей для установки.
  - **setup.py**: Скрипт для установки пакета.

- **server/**: Директория сервера.
  - **app/**: Основная директория приложения.
    - **admin_cli/**: Содержит файлы CLI-приложения, которое может изменять БД.
    - **model/**: Модели данных.
    - **utils/**: Утилиты, вспомогательные функции и модули, такие как аутентификация и рассылка писем
    - **views/**: Представления (views) для API.
    - **mock/**: Папка с мок данными (ненастоящими данные, которые нужны для наглядности).
    - **app.py**: Основной файл для запуска серверного приложения (однако запускать проект следует с помощью runserver скрипта).
    - **database.py**: Файл для инициализации работы с базой данных.
    - **swagger.yml**: Конфигурация API в формате Swagger.
  - **migrations/**: Директория миграций
    - **versions/**: Директория с разными версиями базы данных
  - **cli_admin.py**: Запуск CLI-приложения для работы с БД.
  - **requirements.txt**: Список зависимостей для установки.
  - **runserver.bat**: Скрипт для запуска сервера в Windows.
  - **runserver.sh**: Скрипт для запуска сервера в Unix-подобных системах.

- **README.md**: Файл с описанием проекта, инструкциями по установке и использованию.

# Установка
1. Склонируйте проект.
2. Зайдите в папку проекта.
3. Для удобства создайте виртуальное окружение (если у вас его нет) `python3 -m venv venv`
4. Активируйте виртуальное окружение 
- `./venv/bin/activate` (или `source venv/bin/activate`) - если вы на **Unix**
- venv/bin/activate - если вы на **Windows**

## CLI-приложение
1. Установите зависимости:
- `pip install -r client/requirements.txt` - для CLI-приложения
2. Пропишите `pip install client/`
3. Теперь вы можете запускать приложение, используя команду pizza (используйте `pizza --help` для получения справки)

**Замечание 1**

Приложение использует встроенную библиотеку curses для работы с терминалом. Эта библиотека плохо реагирует на изменения размеров окна терминала, а также плохо обрабатывает ввод кириллицы.

На Ubuntu эта проблема выглядит так:
- При изменении размеров окна терминала curses может выбросить исключение, программа завершит свою работу и постарается вернуть терминал к прежнему состоянию.
- В полях ввода может потребоваться дважды нажимать Backspace для того, чтобы стереть символ кириллицы. Это связано с тем, что клавиатура генерирует два байт кода. Когда они идут последовательно, терминал правильно их отображает и Python правильно их обрабатывает. Когда вы стираете один байт (одно нажатие Backspace) вы получаете недействительный невидимый символ, который может привести к ошибке исполнения (Python не сможет декодировать этот символ).

## Сервер
1. Установите зависимости:
- `pip install -r server/requirements.txt` - для сервера
2. Находясь в папке PizzaMeow, запустите сервер:
- `server/runserver.sh` - если вы на **Unix**
- `server/runserver.bat` - если вы на **Windows**
3. Откройте в браузере ваш локальный сервер, документация будет находиться в относительном пути `/api/ui`

**Замечание 1**

При регистрации пользователю на почту приходит письмо. Эта функция не будет работать, если не указать `smtp_credentials.json`.
Для этого зайдите в папку `server/app/utils/`, создайте в ней файл `smtp_credentials.json` и напишите в нём следующий словарь:
```json
{
    "username": "email@some.thing",
    "password": "password"
}
```
где вместо `username` следует указать почту, с которой будут приходить письма и вместо `password` нужно указать пароль от этой почты.

**Замечание 2**

На данный момент сервер раздаёт JWT токены доступа. Их проще использовать и обрабатывать. Однако это приводит к некоторым проблемам. 
1. Нельзя напрямую ограничивать доступ к разным ресурсам, как это возможно в OAuth 2.0
2. При смене пароля токен остаётся быть действительным
3. Токены генерируются в огромных количествах, поэтому тяжело поддерживать whitelist и blacklist токенов

Чтобы, например, добавить новую пиццу в БД, не получится написать такой запрос, который будет доступен только администратору сайта. \
Поэтому для работы с закрытыми ресурсами сервера написано небольшое cli-приложение, которое позволяет искать, создавать, изменять и удалять записи в БД. \
Запускается это приложение с помощью команды `python3 server/cli_admin.py`