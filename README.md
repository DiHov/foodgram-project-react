# Foodgram

[Проект расположен по адресу](http://62.84.114.225/) http://62.84.114.225/

[![foodgram workflow](https://github.com/DiHov/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/DiHov/foodgram-project-react/actions/workflows/main.yml)

Foodgram - «Продуктовый помощник». На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Технологии
- [Python 3.7](https://www.python.org/)
- [Django 3.0.5](https://www.djangoproject.com/) - свободный фреймворк для веб-приложений на языке Python
- [Django REST framework](https://www.django-rest-framework.org/) (DRF) - мощный и гибкий инструмент для построения Web API.
- [Docker](https://www.docker.com/) - это программное обеспечение для автоматизации развёртывания и управления приложениями в средах с поддержкой контейнеризации, контейнеризатор приложений.
- [Gunicorn](https://gunicorn.org/) - это HTTP-сервер Python WSGI для UNIX.
- [nginx](https://www.nginx.com/) — это HTTP-сервер и обратный прокси-сервер, почтовый прокси-сервер, а также TCP/UDP прокси-сервер общего назначения/

### Запуск проекта в dev-режиме
- Для запуска приложения выполните команды: 
```
docker-compose up
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py load_data
``` 
- Для создания суперпользователя выполните команду:
```
docker-compose exec web python manage.py createsuperuser
```

### Автор
Дмитрий Хижянков