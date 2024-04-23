# Файл для чтения конфига .env
from dotenv import load_dotenv
import os


load_dotenv()

db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT")
db_name = os.environ.get("DB_NAME")

test_db_user = os.environ.get("TEST_DB_USER")
test_db_pass = os.environ.get("TEST_DB_PASS")
test_db_host = os.environ.get("TEST_DB_HOST")
test_db_port = os.environ.get("TEST_DB_PORT")
test_db_name = os.environ.get("TEST_DB_NAME")

redis_user = os.environ.get("REDIS_USER")
redis_pass = os.environ.get("REDIS_PASS")
redis_host = os.environ.get("REDIS_HOST")
redis_port = os.environ.get("REDIS_PORT")

smtp_host = os.environ.get("SMTP_HOST")
smtp_port = os.environ.get("SMTP_PORT")
smtp_user = os.environ.get("SMTP_USER")
smtp_pass = os.environ.get("SMTP_PASS")
