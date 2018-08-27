#FR
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import os, base64, re

from flask import Flask, render_template, request, url_for, redirect, session, flash, send_from_directory, send_file, \
    jsonify
from forms import RegisterForm
from dbconnect import Database
from passlib.hash import sha256_crypt

# for facial recognition
from packages.preprocess import preprocesses
from packages.classifier import training

app = Flask(__name__)
app.secret_key = 'my screcret key'
db = Database()
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# TRAIN_FOLDER = os.path.join(APP_ROOT, 'uploads/train/')
# PRE_FOLDER = os.path.join(APP_ROOT, 'uploads/pre/')
TRAIN_FOLDER = './uploads/train/'
PRE_FOLDER = './uploads/pre/'
CLASSIFIER = './class/classifier.pkl'
MODEL_DIR = './model'


@app.route('/')
def home():
    return render_template('starter.html')


@app.route('/login/')
def userLogin():
    return render_template('login.html')


@app.route('/register/', methods=['GET'])
def register():
    form = RegisterForm(request.form)
    return render_template('register.html', form=form)

@app.route('/train/')
def train():
    print("Training Start")
    obj = training(PRE_FOLDER, MODEL_DIR, CLASSIFIER)
    get_file = obj.main_train()
    print('Saved classifier model to file "%s"' % get_file)
    return 'train end'


@app.route('/init/')
def init():
    obj = preprocesses(TRAIN_FOLDER, PRE_FOLDER)
    nrof_images_total, nrof_successfully_aligned = obj.collect_data()

    print('Total number of images: %d' % nrof_images_total)
    print('Number of successfully aligned images: %d' % nrof_successfully_aligned)
    return 'init align images'


@app.route('/do_reg/', methods=['POST'])
def doRegister():
    form = RegisterForm(request.form)
    print("form validate", form.validate())
    if request.method == 'POST' and form.validate():

        fname = form.firstName.data
        lname = form.lastName.data
        email = form.email.data
        tp = form.tel.data
        password = sha256_crypt.encrypt(str(form.password.data))

        check_user = db.checkUserExists(email)
        print("check user ", check_user)
        if (not check_user):
            user_id = db.regNewUser(fname, lname, tp, email, password)

            if (user_id > 0):

                target = os.path.join(TRAIN_FOLDER, str(user_id) + '/')
                if not os.path.isdir(target):
                    os.mkdir(target)

                for file in request.files.getlist('img'):
                    print(file)
                    filename = str(user_id) + "-" + file.filename
                    print(filename)
                    destination = "/".join([target, filename])
                    print(destination)
                    file.save(destination)

                obj = preprocesses(TRAIN_FOLDER, PRE_FOLDER)
                nrof_images_total, nrof_successfully_aligned = obj.collect_data()

                print('Total number of images: %d' % nrof_images_total)
                print('Number of successfully aligned images: %d' % nrof_successfully_aligned)

                print("Training Start")
                obj = training(PRE_FOLDER, MODEL_DIR, CLASSIFIER)
                get_file = obj.main_train()
                print('Saved classifier model to file "%s"' % get_file)

                flash('User registeration succeeded please log in', 's_msg')
                return jsonify(success=["User Registration Success"],value=True)

            else:
                # flash('User registration failed!', 'e_msg')
                return jsonify(error=["User registration failed!"])
        else:
            # flash('User Exists, Please try different email', category='e_msg')
            return jsonify(error=["User Exists, Please try different email!"])

    return jsonify(form_error=form.errors)

    # return redirect(url_for('register'))


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    target = os.path.join(APP_ROOT, 'uploads/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)

    if request.method == 'POST':
        count = 0
        username = request.form['user'];
        print(request.form)
        for file in request.files.getlist('img'):
            print(file)
            count = count + 1
            # filename = '00' + str(count) + '.png'
            filename = file.filename
            print(filename)
            destination = "/".join([target, filename])
            print(destination)
            file.save(destination)

        return "file uploaded"

    return "ooooooppppppssss"


@app.route('/user/<string:page>/<string:page2>/')
@app.route('/user/<string:page>/')
def userFunctions(page, page2=""):
    if (page2 == ""):
        if (page == 'season'):
            return render_template('season.html')
        elif (page == 'profile'):
            return render_template('profile.html')
    else:
        if (page == 'season' and page2 == 'add'):
            return render_template('season-new.html')

    return render_template('404.html')


@app.route('/admin/login/')
def adminLogin():
    return render_template('admin/login.html')


@app.route('/admin/')
@app.route('/admin/user/<int:id>/')
@app.route('/admin/<string:page>/<string:page2>/')
@app.route('/admin/<string:page>/')
def adminFunctions(page="", page2="", id=-1):
    if (id > 0):
        return render_template('admin/user-details.html')
    elif (page2 == ""):
        if (page == ''):
            return render_template('admin/users.html')
        elif (page == 'profile'):
            return render_template('admin/profile.html')
    else:
        if (page == 'season' and page2 == 'add'):
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
