import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(email: str, subject: str, message: str):
    """
    Параметры
    ---------
    email : str
        Почта, на которую нужно отправить письмо
    subject : str
        Тема письма
    message : str
        Текст письма
    """
    # Настройки SMTP-сервера
    smtp_server = 'smtp.yandex.ru'
    smtp_port = 587

    import json
    with open('server/app/utils/smtp_credentials.json', 'r') as file:
        data = json.load(file)
        username = data['username']
        password = data['password']

    # Создание сообщения
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = email
    msg['Subject'] = subject

    # Тело письма
    msg.attach(MIMEText(message))

    # Отправка письма
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(username, password)
    server.sendmail(username, msg['To'], msg.as_string())
    server.quit()
