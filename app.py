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


@app.route('/user/<string:page>/<string:page2>/')
@app.route('/user/<string:page>/')
def userFunctions(page,page2=""):

    if (page2 == "") :
        if (page == 'season'):
            return render_template('season.html')
        elif(page == 'profile'):
            return render_template('profile.html')
    else :
        if (page == 'season' and page2 =='add'):
            return render_template('season-new.html')

    return render_template('404.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error=e)

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html', error=e)


if __name__ == '__main__':
    app.run()
