from flask import current_app, render_template, request
from flask_mail import Message


def send_dynamic_email(recipient):
    subject = "Dynamic Email Example"
    greeting = "Hello!"
    message = "This is a dynamic email generated using Flask."

    template_content = '''
        <html>
            <head>
                <title>{{ subject }}</title>
            </head>
            <body>
                <h1>{{ greeting }}</h1>
                <p>{{ message }}</p>
            </body>
        </html>
    '''

    placeholders = {
        "subject": subject,
        "greeting": greeting,
        "message": message
    }

    for key, value in placeholders.items():
        template_content = template_content.replace(
            f"{{{{ {key} }}}}", str(value))

    msg = Message(subject=subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[recipient])
    msg.html = template_content

    current_app.extensions['mail'].send(msg)


def modify_template_placeholders(template_content, placeholders):
    for key, value in placeholders.items():
        template_content = template_content.replace(
            f"{{{{ {key} }}}}", str(value))
    return template_content
