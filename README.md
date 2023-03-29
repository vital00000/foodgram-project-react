# Foodgram project 1
***
[![workflow foodgram-project-react](https://github.com/vital00000/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/vital00000/foodgram-project-react/actions/workflows/main.yml)
***
## Продуктовый помощник
***
### Описание
***
##### «**Продуктовый помощник**» - это сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «**Список покупок**» позволяет пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.
***
### Функционал
***
- Рецепты на всех страницах сортируются по дате публикации (новые — выше)
- Работает фильтрация по тегам, в том числе на странице избранного и на странице рецептов одного автора
- Работает пагинатор (в том числе при фильтрации по тегам)
- Для авторизованных пользователей:.
   - Доступна страница «**Мои подписки**»:
   - Доступна главная страница
   - Доступна страница другого пользователя
   - Доступна страница отдельного рецепта
   - Доступна страница «**Избранное**»:
   - Доступна страница «**Список покупок**»:
   - Доступна страница «**Создать рецепт**»:
   - Доступна и работает форма **изменения пароля**
   - Доступна возможность **выйти из системы** (разлогиниться)
- Для **неавторизованных** пользователей:.
   - Доступна **главная страница**
   - Доступна **страница отдельного рецепта**
   - Доступна и работает **форма авторизации**
   - Доступна и работает **система восстановления пароля**
   - Доступна и работает **форма регистрации**
- **Администратор** и **админ-зона**:
   - Все модели выведены в админ-зону
   - Для модели пользователей включена **фильтрация** по имени и email
   - Для модели рецептов включена **фильтрация** по названию, автору и тегам
   - На админ-странице рецепта отображается общее число добавлений этого рецепта в избранное
   - Для модели ингредиентов включена **фильтрация** по названию
***
### Технологии
- Python 3.8.8
- Django 2.2.16
- Django Rest Framework 3.13.1
- PostgreSQL 13.0
- gunicorn 20.0.4
- nginx 1.21.3
***
### Контейнер
- Docker 20.10.14
- Docker Compose 2.4.1
***
### URL's
- http://51.250.105.164/
- http://51.250.105.164/admin/
- http://51.250.105.164/api/
***
### Админ-панель
> Данные для доступа в админ-панель:
- email: 123@ma2.com
- password: test_test
***
### Документация
> Для просмотра документации к API перейдите по адресу:
- http://51.250.105.164/api/docs/
***
### Локальная установка
***
- Клонируйте репозиторий и перейдите в него в командной строке:
```
        git@github.com:vital00000/foodgram-project-react.git 
```
- Перейдите в директорию с файлом Dockerfile и запустите сборку образа:
```
        cd backend 
        docker build -t <ваш_логин_докерхаб>/<название_образа_придумать>:v1 .
        - пушим образ
        docker login -u <ваш_логин_докерхаб>
        docker push <ваш_логин_докерхаб>/<название_образа_придумать>:v1 
        cd .. 
        cd frontend 
        docker build -t <ваш_логин_докерхаб>/<название_образа_придумать>:v1 .
        docker login -u <ваш_логин_докерхаб>
        docker push <ваш_логин_докерхаб>/<название_образа_придумать>:v1 
```
- Перейдите в директорию с файлом docker-compose.yaml:
```
        cd ../infra
```
- Создайте .env файл:
```
        #.env
        DB_ENGINE=<django.db.backends.postgresql>
        DB_NAME=<имя базы данных postgres>
        DB_USER=<пользователь бд>
        DB_PASSWORD=<пароль>
        DB_HOST=<db>
        DB_PORT=<5432>
        SECRET_KEY=<секретный ключ проекта django>
```
- Запустите контейнеры:
```
        docker-compose up -d --build
```
- После успешного запуска контейнеров выполните миграции в проекте:
```
        docker-compose exec backend python manage.py makemigrations
        docker-compose exec backend python manage.py
```
- Создайте суперпользователя:
```
        docker-compose exec backend python manage.py createsuperuser
```
- Соберите статику:
```
        docker-compose exec backend python manage.py collectstatic --no-input
```
- Для остановки контейнеров и удаления всех зависимостей воспользуйтесь командой:
```
        docker-compose down -v
```
***
### Примеры запросов
- GET: http://127.0.0.1:8000/api/users/
- Пример ответа:
```
{
  "count": 123,
  "next": "http://foodgram.example.org/api/users/?page=4",
  "previous": "http://foodgram.example.org/api/users/?page=2",
  "results": [
    {
      "email": "user@example.com",
      "id": 0,
      "username": "string",
      "first_name": "Вася",
      "last_name": "Пупкин",
      "is_subscribed": false
    }
  ]
}
```
- GET: http://127.0.0.1:8000/api/recipes/
- Пример ответа:
```
    {
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```
***
**Автор**
 Виталий Станкевич - https://github.com/vital00000