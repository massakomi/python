from flask import Flask, render_template, request, jsonify
from forms import ContactForm
from werkzeug.datastructures import MultiDict

app = Flask(__name__, template_folder="templates", static_folder="static")
app.debug = True
app.config['SECRET_KEY'] = 'a really really really really long secret key'


@app.route('/')
def index():
    form1 = ContactForm(MultiDict([('name', 'jerry'),('email', 'jerry@mail.com'),('message', 'xxx')]), meta={'csrf': False})
    res = form1.validate()
    return jsonify(message="user saved!"), 200
    #return render_template('index.html', name=form1.errors)

@app.route('/login/', methods=['post', 'get'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')  # запрос к данным формы
        password = request.form.get('password')
        if username == 'root' and password == 'pass':
            message = "Correct username and password"
        else:
            message = "Wrong username or password"

    return render_template('login.html', message=message)


if __name__ == "__main__":
    app.run(debug=True)