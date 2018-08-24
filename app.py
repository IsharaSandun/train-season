from flask import Flask,render_template,request,url_for,redirect,session
from forms import RegisterForm
from dbconnect import Database




app = Flask(__name__)
db = Database()


@app.route('/')
def home():
    print(db.checkDb())
    return render_template('starter.html')


@app.route('/login/')
def userLogin():
    return render_template('login.html')

@app.route('/register/', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        return 'register'

    return render_template('register.html',form=form)


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


@app.route('/admin/login/')
def adminLogin():
    return render_template('admin/login.html')


@app.route('/admin/')
@app.route('/admin/user/<int:id>/')
@app.route('/admin/<string:page>/<string:page2>/')
@app.route('/admin/<string:page>/')
def adminFunctions(page="",page2="",id=-1):

    if (id > 0):
        return render_template('admin/user-details.html')
    elif (page2 == "") :
        if (page == ''):
            return render_template('admin/users.html')
        elif(page == 'profile'):
            return render_template('admin/profile.html')
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
