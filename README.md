![example workflow](https://github.com/patridon87/foodgram-project-react/actions/workflows/yamdb_workflow.yml/badge.svg)

### Проект "FOODGRAM"

### Описание:
Проект Foodgram продуктовый помощник - платформа для публикации рецептов. 

### О проекте:
Пользователи Foodgram могут публиковать рецепты, подписываться на авторов рецептов, 
добавлять рецепты в избранное и в список покупок. Из списка покупок можно
скачать файл с ингредиентами и их количеством для приготовления добавленных рецептов.

### Технологии:
- python 3.7
- django 2.2.19
- djangorestframework 3.13.1
- nginx
- gunicorn
- PostgreSQL


### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone ...прописываем путь...
```

```
cd infra
```

Разверните проект:

```
docker-compose up -d --build
```

```
docker-compose exec web python manage.py migrate
```

```
docker-compose exec backend python manage.py collectstatic --no-input 
```

Заполните базу данных фикстурами рецептов:

```
docker-compose exec backend python manage.py import ---path "/data/ingredients.json"
```

### Об Авторе

Автор проекта студент backend-факультета Яндекс.Практикум:

Карагодин Сергей

##### IP-адрес сервера

51.250.4.83

