# Дипломный проект foodgram-project-react по django-rest на основе docker
![example workflow](https://github.com/astrahov90-yandex-practicum/foodgram-project-react/actions/workflows/main.yml/badge.svg)
### Описание
Проект API предназначен для хранения базы рецептов с категоризациям по тегам.
Рецепты можно добавлять в любимые и в корзину.
Авторов рецептов можно добавлять в подписки
### Технологии
Python 3.7
Django 2.2.19
Postgres
Nginx
### Подготовка данных
Необходимо заполнить .env файл со следующими переменными:
SECRET_KEY=ваш ключ
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=Имя пользователя БД
POSTGRES_PASSWORD=Пароль пользователя БД
DB_HOST=db
DB_PORT=5432
### Старт контейнера
docker run --name <имя контейнера> -it -p 8000:8000 backend
### Адрес проекта
Готовый проект можно посмотреть по <a href='http://sai-testlab.ddns.net/'>ссылке</a>.
Данные администратора admin - qpwoeiruty
### Автор
astrahov90

