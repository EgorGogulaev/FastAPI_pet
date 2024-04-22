import smtplib

from celery import Celery
from celery.schedules import crontab

from .utils import get_email_template_message_with_image
from src.config import redis_host, redis_port, smtp_user, smtp_pass, smtp_host, smtp_port


celery_app = Celery("tasks", broker=f"redis://{redis_host}:{redis_port}/1")


@celery_app.task
def send_email_with_image(username: str, from_email: str=smtp_user, to_email: str=smtp_user):
    email = get_email_template_message_with_image(username=username, from_email=from_email, to_email=to_email)
    with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
        server.login(smtp_user, smtp_pass)
        server.send_message(email)


# Задачи длязапуска по времени
@celery_app.task
def periodic_task_1():
    print("This is a periodic task №1.")

@celery_app.task
def periodic_task_2():
    print("This is a periodic task №2.")

@celery_app.task
def periodic_task_3():
    print("This is a periodic task №3.")

# Конфигурирование "шедулера" Celery
celery_app.conf.beat_schedule = {
    'task1': {
        'task': 'src.tasks.service.periodic_task_1',
        'schedule': 10.0,  # Здесь можно указать интервал выполнения для periodic_task_1
    },
    'task2': {
        'task': 'src.tasks.service.periodic_task_2',
        'schedule': 20.0,  # Здесь можно указать интервал выполнения для periodic_task_2
    },
    'task3': {
        'task': 'src.tasks.service.periodic_task_3',
        'schedule': crontab(minute="*/1", day_of_week='mon,tue,wed,thu,fri'),  # Здесь можно задать время выполнения для periodic_task_3 (в данном примере исполнение каждую минуту по будням)
    },
}