# DRF Homework - LMS Project

## Запуск проекта с Docker Compose

### Требования
- Docker Desktop (или Docker + Docker Compose)
- Git

### Переменные окружения
Создайте файл `.env` на основе `.env.sample` и заполните своими данными.

### Команды для запуска

1. Соберите и запустите контейнеры:
   ```bash
   docker-compose up -d --build
   ```
   
2. Примените миграции (если нужно):
   ```bash
   docker-compose exec web python manage.py migrate
   ```
   
3. Создайте суперпользователя:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```
   
4. Остановите контейнеры:
   ```bash
   docker-compose down
   ```
   
#### Полезные команды

* Посмотреть логи:
    ```bash
   docker-compose logs -f
    ```
  
* Зайти в оболочку контейнера web:
    ```bash
   docker-compose exec web bash
    ```
  
##### Доступные сервисы

* Веб-приложение: http://localhost:8000
* Админка: http://localhost:8000/admin
* Swagger-документация: http://localhost:8000/docs/
* ReDoc: http://localhost:8000/redoc/
