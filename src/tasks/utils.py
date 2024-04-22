from email.message import EmailMessage



def get_email_template_message_with_image(username: str, from_email: str, to_email: str):  # Вспомогательная функция для формирования email объекта
    
    email = EmailMessage()
    email["Subject"] = f"Привет, это сообщение для тебя, {username}"
    email["From"] = from_email
    email["To"] = to_email
    
    email.set_content(
        'div'
        f'<h1 style="colour: red">Привет, {username}, как тебе картинка?</h1>'
        '<img src="https://www.artsshop.ru/pictures/product/big/5202_big.jpg" width="600">'
        '</div>',
        subtype='html'
    )
    return email
