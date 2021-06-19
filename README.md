[![CI/CD](https://github.com/ivartm/bbbs/actions/workflows/build_and_deploy.yml/badge.svg)](https://github.com/ivartm/bbbs/actions/workflows/build_and_deploy.yml)
[![tests](https://github.com/ivartm/bbbs/actions/workflows/tests.yml/badge.svg)](https://github.com/ivartm/bbbs/actions/workflows/tests.yml)
![pep8 codestyle](https://github.com/ivartm/bbbs/actions/workflows/codestyle.yml/badge.svg)


# bbbs
Бэкенд для проекта Старшие Братья Старшие Сестры https://www.nastavniki.org/


## Технологии и требования
```
Python 3.9+
Django
Django REST Framework
Poetry
Docker
```
*тут нужно дополнить*

## Установка локально
Установкой локального окружения и зависимости занимается [poetry](https://python-poetry.org/docs/).

```shell
git clone git@github.com:ivartm/bbbs.git
cd bbbs
poetry shell
poetry install --no-root
pre-commit install
```

## CI/CD и Docker (бэта версия 🤷)

### CI/CD и продакшн
Используется github Actions, workflow **build_deploy**

#### Переменные окружения
Контейнерам нужны переменные окружения для хранения секретов.
Структура переменных окружения (разделение для локального запуска и в продакшн):
```
.envs/
├── .local
│   ├── .django
│   └── .postgres
└── .prod
    ├── .django
    └── .postgres
```

Примеры и какие переменные нужны в папке '.envs example'
Что заполнять в .prod/.django:
```
# General
# --------------------------------------------------------------------
DJANGO_SETTINGS_MODULE=config.settings.prod
DJANGO_SECRET_KEY={{ используйте 'make gen-secretkey' для генерации ключа }}
DJANGO_ALLOWED_HOSTS={{ список IP и FQDN запросы к которым обрабатывает backend }}
```
Что заполнять в .postfres:
```
# PostgreSQL
# ---------------------------------------------------------------------
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=bbbs
POSTGRES_USER={{ задайте имя пользователя или используйте 'make gen-secretkey' для генерации ключа}}
POSTGRES_PASSWORD={{ используйте 'make gen-secretkey' для генерации ключа }}
```



Приложение готово к запуску в окруженни docker.\
Есть два варианта запуска: используя **local.yaml** и **production.yaml**:

- **production.yaml**: разворачивает 3 контейнера с базой данных, django, nginx. Режим DEBUG отключен. Может быть использован для деплоймента.
- **local.yaml**: используется для локальной разработки.
    - Разворачивает 2 контейнера с postgres и django
    - Локальная папка проекта отображается в папку **code** в контейнер django. Все изменения в папке проекта видны в запущенном контейнере и наоборот
    - Создает миграции и применят их
    - Запускает встроенный веб-сервер django
    - Режим DEBUG включен


### Как запустить:

1. Создайте и сохраните переменные окружения в **.envs/.prod** файлы.\
Используйте для примера папку **.envs_example** в корне проекта (итоговая папка должна называться **.envs**, структура точно такая же как в примере).
2. **docker-compose** должен понимать какой **yaml** файл ему использовать. Файл можно указывать вручную (например ``docker-compose -f local.yaml up``). Удобнее экспортировать нужный для запуска файл в переменную окружения:
    ```bash
    export COMPOSE_FILE=local.yaml # тут экспортировали файл для локальной разработки
    ```

3. Собрать контейнеры и запустить в фоновом режим
    ```bash
    docker-compose up --build -d
    ```

### Как выполнить команду внутри контейнера:
Команды выполняются по шаблону
```bash
docker-compose exec {контейнер в котором выполнить} {команда}
```

Например заполнить базу данных их фикстур:
```bash
docker-compose exec django python manage.py loaddata fixtures_docker.json
```

или создать суперпользователя:
```bash
docker-compose exec django python manage.py createsuperuser
```

### Как смотреть что происходит в контейнерах:
Есть два варианты:
1. Запустить контейнеры интерактивно (**не использовать** флаг -d (--detach , -d)):
    ```bash
    docker-compose up
    ```
2. Если контейнеры уже запущены в фоновом режим, то можно выводить журнал. Например контейнера django:
    ```bash
    docker-compose logs --follow django
    ```

### Работа с зависимостями и пакетами
Управляется **poetry**. Детальное описание в [документации poetry](https://python-poetry.org/docs/cli/)

Если кратко, то:
- добавить пакет в список зависимостей для **Production**
```shell
poetry add {название пакета}
```

- установить пакет в **окружение разработки** (dev):
```shell
poetry add --dev {название пакета}
```

- обновить список зависимостей:
```shell
poetry update
```

- узнать путь до интепретатора:
```shell
poetry env info --path
```

## Pre-commit хуки
Настроена интеграций с pre-commit для проверки кода и более простой интеграции с CI/CD.

Выполняются:

- проверка PEP8 flake8
- проверка PEP8 black
- если есть изменения в **poetry.lock** или **pyproject.toml**, то обновляются файлы с зависимостями в **requirements/**. Добавляйте изменения в коммит.

Выполнить pre-commit хуки локально:
```shell
pre-commit run ----all-files
```

Обновить версии репозиториев с pre-commit хуками:
```shell
pre-commit autoupdate
```


## Настройки проекта settings
Разделены на 3 ветки **prod.py, dev.py, local.py**, находятся в **config/settings** Корневые настройки в **base.py**

Хорошая практика при разработке использовать local.py.
После окончания тестирования переносить в dev, prod, base в зависимости от значимости.

## Запуск проекта
По умолчанию проект запускается с локальными настройками в confg.settings.local

Запуск с определенной конфигурацией:
```python
./manage.py runserver --settings=config.settings.dev
```

## Создание фикстур

Создаёт:

- все города из предустановленного списка + 10 случайных
- 200 случайных событий
- 10 случайных тегов для **Права ребенка**
    - 20 случайных **Прав ребенка** с 1 до 5 тегов (случайным образом)
- 30 случайных пользователей, который зарегистрированы на 0-5 мероприятий
- 15 тегов для **Вопросы**
- 30 случайных **Вопросов** с 1 до 15 тегов (случайным образом)
- 5 **Вопросов** без тегов
- 5 **Вопросов** без ответов


```shell
make shell
```

```python
from common.fixtures import make_fixtures
make_fixtures()
````

## В проект добавлен Makefile для облегчения запуска management команд в DEV окружении

Подготовка локального окружения
```shell
configurelocaly
```

Запуск django сервера c локальными настройками

```shell
make runserver
```

Собрать статику

```shell
make build-static
```

Заполнить базу тестовыми данными. Разные фикстуры для разных баз данных + создать суперпользователя (запросит реквизиты).

Postgres:
```shell
make fill-pg
```
SQLite
```shell
make fill-sqlite:
```

Создать и применить миграции, без заполнения данными
```shell
make migrate
```

Создать суперпользователя:
```shell
make createsuperuser
```

Запуск shell plus (должен быть установлен)
```shell
make shell
```

Сгенерирвоать новый SECRET_KEY и показать его на экране:
```shell
make gen-secretkey
```

# Запуск тестов

```shell
pytest
```
# Просмотр автодокументации по API

```shell
.../schema/
.../redoc/,
```
