import os
import re
import smtplib
from email.message import EmailMessage

from flask import Flask, render_template, request

app = Flask(__name__)
CONTACT_EMAIL = "jadeaguilar.dev@gmail.com"


def send_feedback_email(sender_email, comment):
    smtp_host = os.environ.get("SMTP_HOST")
    smtp_username = os.environ.get("SMTP_USERNAME")
    smtp_password = os.environ.get("SMTP_PASSWORD")
    missing_settings = [
        name
        for name, value in (
            ("SMTP_HOST", smtp_host),
            ("SMTP_USERNAME", smtp_username),
            ("SMTP_PASSWORD", smtp_password),
        )
        if not value
    ]
    if missing_settings:
        raise ValueError(
            "Faltan variables de configuración de correo: "
            + ", ".join(missing_settings)
        )

    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    if not 1 <= smtp_port <= 65535:
        raise ValueError("SMTP_PORT debe estar entre 1 y 65535.")

    message = EmailMessage()
    message["Subject"] = "Nuevo comentario en tu portafolio"
    message["From"] = smtp_username
    message["To"] = CONTACT_EMAIL
    message["Reply-To"] = sender_email
    message.set_content(f"Correo de quien comentó: {sender_email}\n\n{comment}")

    with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(message)


# Página de contenidos en ejecución
@app.route('/')
def index():
    return render_template('index.html')


# Habilidades dinámicas
@app.route('/', methods=['POST'])
def process_form():
    buttons = {
        'button_python': {
            'title': 'Proyecto Python',
            'image': '../static/img/Datoschistes.png',
            'label': 'Proyecto Python',
            'url': 'https://github.com/DaniDigitalWorld/Datos-curiosos-y-chistes.git'
        },
        'button_discord': {
            'title': 'Proyecto Discord',
            'image': '../static/img/Discordimg.png',
            'label': 'Proyecto Discord',
            'url': 'https://github.com/DaniDigitalWorld/Bot.git'
        },
        'button_html': {
            'title': 'Proyecto HTML',
            'image': '../static/img/python-project.png',
            'label': 'Proyecto HTML',
            'url': 'https://github.com/DaniDigitalWorld/calculator_esp-main.git'
        },
        'button_db': {
            'title': 'Proyecto Base de Datos',
            'image': '../static/img/diary.png',
            'label': 'Proyecto Base de Datos',
            'url': 'https://github.com/DaniDigitalWorld/diary-en-main.git'
        }
    }

    active_project = None
    for key, project in buttons.items():
        if request.form.get(key):
            active_project = project
            break

    if active_project is None and (
        "email" in request.form or "text" in request.form
    ):
        sender_email = request.form.get("email", "").strip()
        comment = request.form.get("text", "").strip()

        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", sender_email):
            return render_template(
                "index.html", feedback_error="Escribe un correo electrónico válido."
            ), 400
        if not comment or len(comment) > 5000:
            return render_template(
                "index.html",
                feedback_error="El comentario debe tener entre 1 y 5000 caracteres.",
            ), 400

        try:
            send_feedback_email(sender_email, comment)
        except (OSError, smtplib.SMTPException, ValueError):
            app.logger.exception("No se pudo enviar el comentario por correo.")
            return render_template(
                "index.html",
                feedback_error=(
                    "No se pudo enviar el comentario. Inténtalo más tarde."
                ),
            ), 500

        return render_template(
            "index.html",
            feedback_success="¡Gracias! Tu comentario fue enviado correctamente.",
        )

    return render_template('index.html', active_project=active_project)


if __name__ == "__main__":
    app.run(debug=True)
