![pep8 codestyle](https://github.com/ivartm/bbbs/actions/workflows/codestyle.yml/badge.svg)

[![afisha app tests](https://github.com/ivartm/bbbs/actions/workflows/tests.yml/badge.svg)](https://github.com/ivartm/bbbs/actions/workflows/tests.yml)

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

## Docker (альфа версия 🤷, добавим вариант сборки с DEBUG=True в ближайшее время)
Приложение готово к запуску в окруженни docker.\
Есть два варианта запуска: используя **local.yaml** и **production.yaml**. Пока разница не оч большая: в версии production не устанавливаются пакеты для отладки, режим DEBUG отключен.
Параметры запуска описаны в 'production.yaml' (для локального окружения есть 'local.yaml', но не настроен)

Создаются три контейнера:

 - контейнер базы данных **postgres**
 - контейнер приложения **django**
 - контейнер web-сервера **nginx**

Как запустить:

1. Создайте и сохраните переменные окружения в **.envs/.prod** файлы.\
Используйте для примера папку **.envs_example** в корне проекта (итоговая папка должна называться **.envs**, структура точно такая же как в примере).
2. Запустите docker-compose

```bash
docker-compose -f local.yaml up --build -d
```
3. Выполните миграции и подключите статику

```bash
docker-compose -f local.yaml exec django python manage.py makemigrations
docker-compose -f local.yaml exec django python manage.py migrate
docker-compose -f local.yaml exec django python manage.py collectstatic --noinput
```
4. Для тестовых целей базу данных можно наполнить данными

```bash
docker-compose -f local.yaml exec django python manage.py loaddata fixtures_docker.json
```
5. Создайте пользователя

```bash
docker-compose -f local.yaml exec django python manage.py createsuperuser
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
- 30 случайных вопросов с случайными тегам (от 0 до 14 (точно ли так?) )
- 5 вопросов без тегов
- 5 вопросов без ответов


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
.../api/schema/
.../api/schema/swagger-ui/,
.../api/schema/redoc/,
```
