[![Django-app workflow](https://github.com/DariaIlyushina/foodgram-projet-react/actions/workflows/main.yml/badge.svg)](https://github.com/DariaIlyushina/foodgram-projet-react/actions/workflows/main.yml)

## Проект Foodgram

Сайт «Продуктовый помощник». На этом сервисе пользователи могут публиковать рецепты, добавлять понравившиеся рецепты в «Избранное», подписываться на других пользователей и составлять продуктовую корзину.

## Ссылки на проект

Проект запущен и доступен по адресу http://158.160.9.160/recipes
Админка доступна по адресу http://158.160.9.160/admin/
Документация для написания api проекта доступна по адресу http://158.160.9.160/api/docs/redoc.html

## Стек 

Python 3.10
Django 4.0
Django REST framework 3.13
Nginx
Docker
Postgres

## Запуск проекта

Для работы с удаленным сервером:

Выполните вход на свой удаленный сервер.

Установите docker на сервер:

    sudo apt install docker.io 

Установите docker-compose на сервер.

Локально отредактируйте файл infra/nginx/default.conf.conf, в строке server_name впишите свой IP

Скопируйте файлы docker-compose.yml и nginx.conf из папки infra на сервер

Создайте .env файл: 

    touch .env

    DB_ENGINE='django.db.backends.postgresql'
    DB_NAME='postgres'
    POSTGRES_USER='postgres'
    POSTGRES_PASSWORD=<Your_password>
    DB_HOST='db'
    DB_PORT=5432
    
Запустите создание образа

    sudo docker-compose up -d
