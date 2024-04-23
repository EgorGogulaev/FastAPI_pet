import aiofiles

from fastapi import FastAPI, Request, status
# Импорты для обработки исключений валидации
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException
from fastapi.responses import HTMLResponse, JSONResponse
# ------------------------------------------
# Импорты для кэширования
from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis
# -----------------------

from src.operations.router import router as operations_router
from src.users.router import router as users_router
from src.tasks.router import router as tasks_router 
from src.config import redis_user, redis_pass, redis_host, redis_port, test_db_port, test_db_pass
from service_runners import PostgresRunner, RedisRunner

# Сопрограмма для настройки кэширования перед запуском 
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Перед запуском следует развернуть postgresql! Ниже автоматически разворачивается  только тестовая БД с томами
    PostgresRunner(container_name="test_postgres", port=test_db_port, password=test_db_pass).run()
    RedisRunner(container_name="redis", port=redis_port, password=redis_pass).run()
    redis = aioredis.from_url(f"redis://{redis_user}:{redis_pass}@{redis_host}:{redis_port}/0")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield

app = FastAPI(  # Инициализация приложения
    title="Trading App",
    lifespan=lifespan
)

# Endpoint базовой страницы
@app.get("/", response_class=HTMLResponse)
async def index():
    async with aiofiles.open("./templates/index.html", "r", encoding="utf-8") as file:
        content = await file.read()
    return content
    
# Endpoint долгой операции c примером ускорения ответа при кэшировании данных
@app.get("/long_operation")
@cache(expire=600)  # Использование кэша с заданным временем экспирации
async def get_long_operation():
    import time
    time.sleep(3)
    
    return {"Hello": "World"}
# ----------------------------------------------------

# Подключение роутов приложения "operations"
app.include_router(router=operations_router)
# __________________________________________

# Подключение роутов аутентификации/регистрации/верификации
app.include_router(router=users_router)
# __________________________________________________________

# Подключение роутов фоновых задач
app.include_router(router=tasks_router)
# ________________________________


# Пример обработчика ошибок валидации
@app.exception_handler(ValidationException)
async def validator_exception_handler(request: Request, ex: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": ex.errors()})
    )
# -----------------------------------
