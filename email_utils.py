import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_EMAIL_APP_PASSWORD = os.getenv("SENDER_EMAIL_APP_PASSWORD")

def enviar_email(destinatario, status, comentario=None):
    if status == "APROVADO":
        assunto = "Status do seu cadastro"
        corpo = (
            "Olá!\n\n"
            "Seu cadastro foi aprovado ✅.\n"
            "Em breve nossa equipe seguirá com o próximo passo.\n\n"
            "Obrigada!"
        )
    elif status == "REPROVADO":
        assunto = "Status do seu cadastro"
        corpo = (
            "Olá!\n\n"
            "Seu cadastro não foi aprovado neste momento ❌.\n"
            "Você pode responder este e-mail para tirar dúvidas ou reenviar documentação.\n"
        )
        if comentario:
            corpo += f"\nObservação: {comentario}\n"
        corpo += "\nObrigada!"
    else:
        # fallback seguro
        assunto = "Status do seu cadastro"
        corpo = "Seu cadastro foi atualizado."

    msg = MIMEText(corpo)
    msg["Subject"] = assunto
    msg["From"] = SENDER_EMAIL
    msg["To"] = destinatario

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_EMAIL_APP_PASSWORD)
        server.send_message(msg)