from flask import Flask,render_template,request,url_for,redirect,session

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('starter.html')


if __name__ == '__main__':
    app.run()
