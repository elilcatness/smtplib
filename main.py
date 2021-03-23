from dotenv import load_dotenv
from flask import Flask, render_template, request

from mail_sender import send_mail

app = Flask(__name__)
load_dotenv()


@app.route('/', methods=['GET'])
def get_form():
    return render_template('mail_me.html')


@app.route('/', methods=['POST'])
def post_form():
    email = request.values.get('email')
    return ('Письмо отправлено успешно на адрес %s' % email
            if send_mail(email, 'Тестовое письмо', 'Тестовый текст',
                         ['.', 'templates', '.git'])
            else 'Во время отправки письма на адрес %s произошла ошибка' % email)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)