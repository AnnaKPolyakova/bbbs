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
*тут нужно дополнить*
```

## Установка локально с БД в Docker
1. Сколонируйте репозиторий проекта и перейдите в папку проекта:
    ```shell
    git clone git@github.com:ivartm/bbbs.git
    cd bbbs
    ```
2. Установите рабочее окружение и зависимости (управляются через [poetry](https://python-poetry.org/docs/)). Файлы **requirements** вручную редактировать не нужно
    ```shell
    poetry shell
    poetry install --no-root
    pre-commit install
    ```
3. Убедитесь что установлен и запущен **docker** и **docker-compose**
4. Запустите контейнер с БД:
    ```shell
    docker-compose -f local.yaml up --build -d
    ```
5. Теперь можно запустить проект, он будет использовать БД в контейнере:
    ```python
    python manage.py runserver
    ```
6. Остановить контейнер с БД:
    ```shell
    docker-compose -f local.yaml down
    ```
7. Остановить контейнер с БД удалив данные:
    ```shell
    docker-compose -f local.yaml down --volumes
    ```

## Запуск локально в Docker окружении с заполнением БД случайными данными
1. Убедитесь что установлен и запущен **docker** и **docker-compose**
2. Перейдите в папку проекта
3. Запустить проект и заполнить БД случайными данными:
    ```shell
    docker-compose -f dev.yaml up --build -d
    ```
4. Запущенный проект доступен по ``http://127.0.0.1:8000``
5. Пользователь с правами администратора:
    ```
    Логин: bbbs
    Пароль: Bbbs2021!
    ```
6. Пароль всех созданных тестовых пользователей: ``Bbbs2021!``
7. Остановить проект сохранив данные в БД:
    ```shell
    docker-compose -f local.yaml down
    ```
8. Остановить проект удалив данные в БД:
    ```shell
    docker-compose -f local.yaml down --volumes
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

Примеры и какие переменные нужны в папке '.envs example'.
- Пример файла **.django**:
    ```
    # General
    # --------------------------------------------------------------------
    DJANGO_SETTINGS_MODULE=config.settings.prod
    DJANGO_SECRET_KEY={{ используйте 'make gen-secretkey' для генерации ключа }}
    DJANGO_ALLOWED_HOSTS={{ список IP и FQDN запросы к которым обрабатывает backend }}
    ```
- Пример файла **.postgres**:
    ```
    # PostgreSQL
    # ---------------------------------------------------------------------
    POSTGRES_HOST=postgres
    POSTGRES_PORT=5432
    POSTGRES_DB=bbbs
    POSTGRES_USER={{ задайте имя пользователя или используйте 'make gen-secretkey' для генерации ключа}}
    POSTGRES_PASSWORD={{ используйте 'make gen-secretkey' для генерации ключа }}
    ```


### Примеры работы с docker:

1. Чтоб не указывать файл yaml каждый раз его можно сохранить в env:
    ```bash
    export COMPOSE_FILE=local.yaml # тут экспортировали файл для локальной разработки
    docker-compose up --build -d
    ```
2. Выполнить команду внутри контейнера:
    ```bash
    docker-compose exec {контейнер в котором выполнить} {команда}
    ```
3. Например заполнить базу данных их фикстур:
    ```bash
    docker-compose exec django python manage.py loaddata fixtures_docker.json
    ```
4. Создать суперпользователя:
    ```bash
    docker-compose exec django python manage.py createsuperuser
    ```
5. Как смотреть что происходит в контейнерах:
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

## Заполнение базы данных тестовыми данными

Запуск с предустановленными параметрами:

все города из предустановленного списка + 10 случайных
200 случайных событий
10 случайных тегов для Права ребенка
20 случайных Прав ребенка с 1 до 5 тегов (случайным образом)
30 случайных пользователей, который зарегистрированы на 0-5 мероприятий
15 тегов для Вопросы
30 случайных Вопросов с 1 до 15 тегов (случайным образом)
5 Вопросов без тегов
5 Вопросов без ответов

```python
./manage.py filldb
```
так же есть возможность опционально добавлять тестовые данные, подробности в help:
```python
./manage.py filldb --help
```
для очистки таблиц БД (но не удаление!) можете воспользоваться стандартной командой Django:
```python
./manage.py flush
```

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

Заполнить базу тестовыми данными.

БД:
```shell
make filldb
```
БД + создать суперпользователя (запросит реквизиты):
```shell
make filldb-with-superuser:
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