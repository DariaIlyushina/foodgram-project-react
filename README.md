[![Django-app workflow](https://github.com/DariaIlyushina/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/DariaIlyushina/foodgram-project-react/actions/workflows/main.yml)

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

Локально отредактируйте файлы и укажите везде свой IP

Скопируйте файлы docker-compose.yml и nginx.conf из папки infra на сервер

Создайте .env файл: 

    touch .env

    DB_ENGINE='django.db.backends.postgresql'
    DB_NAME='postgres'
    POSTGRES_USER='postgres'
    POSTGRES_PASSWORD=<Your_password>
    DB_HOST='db'
    DB_PORT=5432
    
Скопируйте папку docs на сервер:

    scp -r docs <username>@<ip host>@<ваш адрес сервера>:/home/<username>/

Запустите создание образа

    sudo docker-compose up -d

Для работы с Workflow вам в Secrets GitHub понадобятся переменные окружения:

    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<имя базы данных postgres>
    DB_USER=<пользователь бд>
    DB_PASSWORD=<пароль>
    DB_HOST=<db>
    DB_PORT=<5432>

    DOCKER_PASSWORD=<пароль от DockerHub>
    DOCKER_USERNAME=<имя пользователя на DockerHub>

    SECRET_KEY=<секретный ключ проекта django>

    USER=<username для подключения к серверу>
    HOST=<IP сервера>
    SSH_KEY=<ваш SSH ключ (для получения выполните команду: cat ~/.ssh/id_rsa)>
    PASSPHRASE=<если при создании ssh-ключа вы использовали фразу-пароль>

    TELEGRAM_TO=<ID чата, в который придет сообщение, узнать свой ID можно у бота @userinfobot>
    TELEGRAM_TOKEN=<токен вашего бота, получить этот токен можно у бота @BotFather>
    

Workflow состоит из четырех шагов:

1.Проверка кода на соответствие PEP8 и выполнение тестов, реализованных в проекте.

2.Сборка и публикация образа приложения на DockerHub.

3.Автоматическое скачивание образа приложения и деплой на удаленном сервере.

4.Отправка уведомления в телеграм-чат./dr
