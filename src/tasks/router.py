from fastapi import APIRouter, Depends

from src.users.config import current_user
from .service import send_email_with_image



router = APIRouter(
    prefix="/task", 
    tags=["Tasks"]
)

@router.get("/send_image")
def get_email_with_message(user=Depends(current_user)):
    try:
        send_email_with_image.delay(user.username)
        return {
            "status": True,
            "msg": "Письмо отправлено"
        }
    except Exception as ex:
        print(ex)
        return {
            "status": False,
            "msg": "Что-то пошло не так"
        }
