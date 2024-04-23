      / \__
     (    @\___
     /         O
    /   (_____/
   /_____/

I'am a pet project using FastAPI🐶
### Woof!

# Запуск:
1) Нужно установить и запустить Docker (https://www.docker.com/products/docker-desktop/);
2) Для начала нужно развернуть БД PostgreSQL;
3) Перед запуском следует создать конфигурационный файл .env содержащий слудующие переменные:
- DSN PostgreSQL
DB_USER
DB_PASS
DB_HOST
DB_PORT
DB_NAME

- DSN PostgreSQL для тестирования
TEST_DB_USER
TEST_DB_PASS
TEST_DB_HOST
TEST_DB_PORT
TEST_DB_NAME

- DSN Redis
REDIS_USER
REDIS_PASS
REDIS_HOST
REDIS_PORT

- Это не обязательно, если мы не хотим протестировать фоновые задачи запускаемые Celery
SMTP_HOST
SMTP_PORT
SMTP_USER
SMTP_PASS

4) Из корня проекта выполнить `uvicorn src.main:app --reload`;
