from flask import render_template, request, Blueprint, current_app, jsonify
from flask_mail import Message
from Mail.utils import send_dynamic_email, modify_template_placeholders

eemail = Blueprint("mail", __name__, url_prefix="/mail")


@eemail.post('/send_email')
def send_email():
    if request.method == 'POST':
        data = request.get_json()
        recipient = data.get('recipient_email', '')

        send_dynamic_email(recipient)
        return "Email sent successfully!"
    return render_template('email_form.html')


@eemail.post('/modify_template')
def modify_template():
    data = request.get_json()  # Use get_json() to extract JSON data from the request

    template_content = data.get('template_content', '')
    placeholders = data.get('placeholders', {})

    modified_template = modify_template_placeholders(
        template_content, placeholders)
    return jsonify({"modified_template": modified_template})


@eemail.get('/view_modified_template')
def view_modified_template():
    data = request.get_json()
    template_content = '<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>'
    placeholders = {
        "Title": "Modified Title",
        "Content": "Hello, world!"
    }

    # Make a POST request to /modify_template to get the modified template
    with current_app.test_client() as client:
        response = client.post('/modify_template', json={
            "template_content": template_content,
            "placeholders": placeholders
        })

    if response.status_code == 200:
        try:
            modified_template = data.get('modified_template', '')
            return modified_template
        except Exception as e:
            return str(e)
    else:
        return f"Failed to retrieve modified template. Status code: {response.status_code}"
