"""
Put your Flask app code here.
"""
from flask import render_template, Flask, request
import webbrowser
import threading

app = Flask(__name__)
image = None;
@app.route('/')
def index():
    global image
    # if request.form['pic']:
    #     image = request.form['pic']
    return render_template('index.html')


@app.route('/hello')
def hello_world():
    return request.form['pic']


# @app.route('/hello/')
@app.route('/helloWorld/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/error')
def error():
    return render_template('error.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if valid_login(request.form['name'], request.form['age']):
    #     a = request.form['question']
    #     print(a)
        return "%s is %s-year-old. Patrick Huston is %s's favorite softDes Ninja." % (request.form['name'], request.form['age'], request.form['name'])
    # return request.form['question']
    else:
        return render_template('error.html')


def valid_login(name, age):
    if name != "" and age != "":
        return True
    else:
        return False


@app.route('/user/<username>-<age>')
def show_user_profile(username, age):
    # show the user profile for that user
    return 'User %s is %s-year-old.' % (username, age)


if __name__ == '__main__':
    # url = 'http://127.0.0.5000'
    # webbrowser.open_new_tab(url)
    port = 5000
    url = "http://127.0.0.1:{0}".format(port)

    threading.Timer(1.25, lambda: webbrowser.open(url) ).start()

    app.run(port=port, debug=False)
    # app.run()
