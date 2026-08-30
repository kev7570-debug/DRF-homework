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

###### CI/CD с GitHub Actions
В проекте настроен автоматический CI/CD пайплайн с использованием GitHub Actions.

Что делает workflow:
* Линтинг — проверка кода с помощью Flake8
* Тесты — запуск тестов Django (на SQLite в CI)
* Деплой — автоматическое развертывание на сервер (при пуше в ветку main)

Как это работает:
1. При каждом push или pull request в main или feature/task_08 запускаются тесты.
2. Если тесты и линтер проходят успешно, запускается деплой.
3. Для деплоя используются GitHub Secrets:
* SSH_KEY — приватный ключ для подключения к серверу
* SSH_USER — имя пользователя на сервере
* SERVER_IP — IP-адрес сервера
* DEPLOY_DIR — директория проекта на сервере

Настройка деплоя
1. Добавьте секреты в настройках репозитория: Settings → Secrets and variables → Actions.
2. Убедитесь, что на сервере установлены:
* Git
* Python + виртуальное окружение
* Все зависимости из requirements.txt
3. Workflow автоматически обновит код, применит миграции и перезапустит приложение.

##### Ручной деплой
Если вы хотите развернуть проект вручную:

Склонируйте репозиторий на сервер:
   ```bash
git clone https://github.com/kev7570-debug/DRF-homework.git
   ```

Установите зависимости и настройте окружение:
   ```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
   ```

Примените миграции и соберите статику:
   ```bash
python manage.py migrate
python manage.py collectstatic --noinput
   ```

Настройте Gunicorn и Nginx (по желанию).

###### Деплой

Проект развернут на сервере Yandex Cloud:
- IP-адрес: `51.250.107.126`
- Порт: `8000`
- Админка: `http://51.250.107.126:8000/admin/`
- API: `http://51.250.107.126:8000/api/courses/`

###### Автор 
Elena Kashina