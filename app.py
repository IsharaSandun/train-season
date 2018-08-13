from flask import Flask,render_template,request,url_for,redirect,session

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('starter.html')


@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/register/')
def register():
    return render_template('register.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run()
