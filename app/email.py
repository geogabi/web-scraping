from flask_mail import Message
from .initialize import mail

def send_mail(product):
    mail_message = Message(
        'DISCOUNT',
        sender='your_mail@gmail.com',
        recipients=['recipient_mail@gmail.com'])
    mail_message.body = f"The price for {product} has been reduced"
    mail.send(mail_message)
    return "Mail has been sent"
