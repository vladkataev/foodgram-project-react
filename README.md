# praktikum_new_diplom

![example workflow](https://github.com/vladkataev/foodgram-project-react/actions/workflows/foodgram_workflows.yml/badge.svg)

### Описание:

Проект Foodgram даёт возможность пользователям публиковать рецепты, подписываться на интересных авторов, добавлять рецепты в избранное и список покупок.

### Данные админки:

http://158.160.5.126/admin/login/?next=/admin/

Логин:
```
admin@admin.ru
```
Пароль:
```
bestofthebest
```

### Как запустить проект:

1. Устоновите Docker (Подробную информацию по установке можно найти на сайте [Docker] (https://www.docker.com/)).
2. Клонируйте репозиторий и перейдите в него в командной строке:
```
git clone https://github.com/vladkataev/foodgram-project-react.git
```
3. Перейдите в директорию infra, добавьте файл .env в котором хранится SECRET_KEY и настройки БД:
```
cd infra
```
- Пример заполниения файла .env:
```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=user # логин для подключения к базе данных
POSTGRES_PASSWORD=password # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
SECRET_KEY=007 # ключ к Django проекту
```
4. Запустите сборку образов:
```
docker-compose up -d --build
```
5. Выполните миграции и создайте суперпользователя:
```
winpty docker-compose exec web python manage.py makemigrations
winpty docker-compose exec web python manage.py migrate
winpty docker-compose exec web python manage.py createsuperuser
```
6. Собирите статические файлы:
```
winpty docker-compose exec web python manage.py collectstatic --no-input
```

### Документация с примерами запросов и ответов на них по адресу:

**[http://localhost/api/docs/](http://localhost/api/docs/)**

### Автор:

**[Владимир Катаев](https://github.com/vladkataev)**

### Запущенный проект - **[здесь](http://158.160.5.126/recipes)**