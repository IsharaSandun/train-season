# FR
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from flask import Flask, render_template, request, url_for, redirect, session, flash, send_from_directory, send_file, \
    jsonify
from forms import RegisterForm, AdminLoginForm, AddNewSeason
from dbconnect import Database
from passlib.hash import sha256_crypt, md5_crypt
from functools import wraps

# for facial recognition
from packages.preprocess import preprocesses
from packages.classifier import training
import pickle
import time
import cv2
import numpy as np
import tensorflow as tf
from scipy import misc
from packages import facenet, detect_face

app = Flask(__name__)
app.secret_key = 'my screcret key'
db = Database()
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
TRAIN_FOLDER = './uploads/train/'
TEST_FOLDER = './uploads/test/'
PRE_FOLDER = './uploads/pre/'
CLASSIFIER = './class/classifier.pkl'
MODEL_DIR = './model'
npy = ''


def login_required_user(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session.get('logged_in') == True and 'user_type' in session and session.get(
                'user_type') == 'user':
            return f(*args, **kwargs)
        else:
            flash("You need to login first", category='e_msg')
            return redirect(url_for('userLogin'))

    return wrap


def login_required_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session.get('logged_in') == True and 'user_type' in session and session.get(
                'user_type') == 'admin':
            return f(*args, **kwargs)
        else:
            flash("You need to login first", category='e_msg')
            return redirect(url_for('adminLogin'))

    return wrap


def logged_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session.get('logged_in') == True and 'user_type' in session and session.get(
                'user_type') == 'admin':
            return redirect(url_for('adminFunctions'))
        else:
            return f(*args, **kwargs)

    return wrap


def logged_user(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session.get('logged_in') == True and 'user_type' in session and session.get(
                'user_type') == 'admin':
            return redirect(url_for('userFunctions'))
        else:
            return f(*args, **kwargs)

    return wrap


@app.route('/')
def home():
    return render_template('home.html')


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


@app.route('/recognize/')
def recognize(filename="img.png"):
    image_path = TEST_FOLDER + filename
    with tf.Graph().as_default():
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.6)
        sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
        with sess.as_default():
            pnet, rnet, onet = detect_face.create_mtcnn(sess, npy)

            minsize = 20  # minimum size of face
            threshold = [0.6, 0.7, 0.7]  # three steps's threshold
            factor = 0.709  # scale factor
            frame_interval = 3
            image_size = 182
            input_image_size = 160

            HumanNames = os.listdir(TRAIN_FOLDER)
            HumanNames.sort()

            print('Loading feature extraction model')
            facenet.load_model(MODEL_DIR)

            images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
            embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
            phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
            embedding_size = embeddings.get_shape()[1]

            classifier_filename_exp = os.path.expanduser(CLASSIFIER)
            with open(classifier_filename_exp, 'rb') as infile:
                (model, class_names) = pickle.load(infile)

            c = 0

            print('Start Recognition!')
            frame = cv2.imread(image_path, 0)

            frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)  # resize frame (optional)

            timeF = frame_interval

            if (c % timeF == 0):

                if frame.ndim == 2:
                    frame = facenet.to_rgb(frame)
                frame = frame[:, :, 0:3]
                bounding_boxes, _ = detect_face.detect_face(frame, minsize, pnet, rnet, onet, threshold, factor)
                nrof_faces = bounding_boxes.shape[0]
                print('Face Detected: %d' % nrof_faces)

                if nrof_faces > 0:
                    det = bounding_boxes[:, 0:4]

                    cropped = []
                    scaled = []
                    scaled_reshape = []
                    bb = np.zeros((nrof_faces, 4), dtype=np.int32)

                    for i in range(nrof_faces):
                        emb_array = np.zeros((1, embedding_size))

                        bb[i][0] = det[i][0]
                        bb[i][1] = det[i][1]
                        bb[i][2] = det[i][2]
                        bb[i][3] = det[i][3]

                        # inner exception
                        if bb[i][0] <= 0 or bb[i][1] <= 0 or bb[i][2] >= len(frame[0]) or bb[i][3] >= len(frame):
                            print('face is too close')
                            continue

                        cropped.append(frame[bb[i][1]:bb[i][3], bb[i][0]:bb[i][2], :])
                        cropped[i] = facenet.flip(cropped[i], False)
                        scaled.append(misc.imresize(cropped[i], (image_size, image_size), interp='bilinear'))
                        scaled[i] = cv2.resize(scaled[i], (input_image_size, input_image_size),
                                               interpolation=cv2.INTER_CUBIC)
                        scaled[i] = facenet.prewhiten(scaled[i])
                        scaled_reshape.append(scaled[i].reshape(-1, input_image_size, input_image_size, 3))
                        feed_dict = {images_placeholder: scaled_reshape[i], phase_train_placeholder: False}
                        emb_array[0, :] = sess.run(embeddings, feed_dict=feed_dict)
                        # print("emb_array",emb_array)
                        predictions = model.predict_proba(emb_array)
                        print("Predictions ", predictions)
                        best_class_indices = np.argmax(predictions, axis=1)
                        best_class_probabilities = predictions[np.arange(len(best_class_indices)), best_class_indices]
                        print("Best Predictions ", best_class_probabilities)

                        if best_class_probabilities[0] > 0.6:
                            print('Result Indices: ', best_class_indices[0])
                            print(HumanNames)
                            for H_i in HumanNames:
                                # print(H_i)
                                if HumanNames[best_class_indices[0]] == H_i:
                                    result_names = HumanNames[best_class_indices[0]]
                                    print("Face Recognized: ", result_names)
                                    return str(result_names)
                        else:
                            print('Not Recognized')
                            return False
                else:
                    print('Unable to align')
                    return False

    return False


@app.route('/init/')
def init():
    obj = preprocesses(TRAIN_FOLDER, PRE_FOLDER)
    nrof_images_total, nrof_successfully_aligned = obj.collect_data()

    print('Total number of images: %d' % nrof_images_total)
    print('Number of successfully aligned images: %d' % nrof_successfully_aligned)
    return 'init align images'


@app.route('/logout/')
def logout():
    user_type = session.get('user_type')

    session.clear()
    flash('Your have been Logged out', category='i_msg')

    if user_type == 'user':
        return redirect(url_for('userLogin'))
    return redirect(url_for('adminLogin'))


@app.route('/login/')
@logged_user
def userLogin():
    return render_template('login.html')


def random_name():
    name = md5_crypt.encrypt(str(time.time())).split("$")[2]
    return name


@app.route('/do_login/', methods=['POST'])
def doLogin():
    target = os.path.join(APP_ROOT, 'uploads/test/')
    if not os.path.isdir(target):
        os.mkdir(target)

    filename = random_name() + ".png"
    destination = "/".join([target, filename])

    if request.method == 'POST':

        username = request.form.get('email')
        password = request.form.get('password')
        if username == '' and password == '':
            print(request.files.getlist('img'))
            for file in request.files.getlist('img'):
                print(filename)
                file.save(destination)

            result = recognize(filename)
            os.remove(destination)
            if result is False:
                return jsonify(result=False)

            user_details = db.getUserById(result)
            session['logged_in'] = True
            session['user_type'] = 'user'
            session['username'] = user_details['email']
            session['user_id'] = user_details['id']

            return jsonify(result=True)

        else:

            user_pw = db.getUserPassword(username)
            if user_pw is not False:
                if sha256_crypt.verify(password, db.getUserPassword(username)):
                    user_details = db.getUserByEmail(username)
                    session['logged_in'] = True
                    session['user_type'] = 'user'
                    session['username'] = username
                    session['user_id'] = user_details['id']

                    return jsonify(result=True)

                return jsonify(result=False)

            return jsonify(result=False)

    return jsonify(result=False)


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
                return jsonify(success=["User Registration Success"], value=True)

            else:
                # flash('User registration failed!', 'e_msg')
                return jsonify(error=["User registration failed!"])
        else:
            # flash('User Exists, Please try different email', category='e_msg')
            return jsonify(error=["User Exists, Please try different email!"])

    return jsonify(form_error=form.errors)


### USER FUNCTIONS ###

@app.route('/user/season/')
@app.route('/user/')
@login_required_user
def userFunctions():
    user_id = session.get('user_id')
    old_seasons = db.getSeasonByUserInactive(user_id)
    active_season = db.getSeasonByUserActive(user_id)

    return render_template('season.html', old_seasons=old_seasons, active_season=active_season)


@app.route('/user/season/add/', methods=['POST', 'GET'])
@login_required_user
def user_season_add():
    locations = db.getLocationList()
    location_list = [('', '-- Please Select --')]
    for loc in locations:
        location_list.append((loc['id'], loc['name']))

    choices_list = [(1, 'First Class'), (2, 'Second Class'), (3, 'Third Class')]

    form = AddNewSeason(request.form)
    form.location_from.choices = location_list
    form.location_to.choices = location_list
    form.season_class.choices = choices_list

    if request.method == 'POST':
        location_from = form.location_from.data
        location_to = form.location_to.data
        season_class = form.season_class.data

        if location_to == location_from:
            flash('Both locations cannot be same', category='e_msg')

    return render_template('season-new.html', locations=locations, form=form)


@app.route('/user/profile/')
@login_required_user
def user_profile():
    return render_template('profile.html')


### END USER FUNCTIONS ###


@app.route('/pass/<string:hash>/')
def hashing(hash=""):
    print(hash)
    return sha256_crypt.encrypt(hash)


@app.route('/admin/login/', methods=['POST', 'GET'])
@logged_admin
def adminLogin():
    form = AdminLoginForm(request.form)

    if request.method == 'POST' and form.validate():
        username = form.email.data
        password = form.password.data

        admin_pw = db.getAdminPassword(username)
        if admin_pw is not False:
            if sha256_crypt.verify(password, admin_pw):
                session['logged_in'] = True
                session['user_type'] = 'admin'
                session['username'] = username

                return redirect(url_for('adminFunctions'))

        flash("Invalid Login Credentials!", category='e_msg')

    return render_template('admin/login.html', form=form)


### ADMIN FUNCTIONS ###

@app.route('/admin/')
@login_required_admin
def adminFunctions():
    pending_users = db.getPendingUsers()
    active_users = db.getActiveUsers()

    return render_template('admin/users.html', pending_users=pending_users, active_users=active_users)


@app.route('/admin/user/<int:id>/')
@login_required_admin
def admin_user_details(id):
    return render_template('admin/user-details.html')


@app.route('/admin/profile/')
@login_required_admin
def admin_profile():
    return render_template('admin/profile.html')


@app.route('/admin/season/add')
@login_required_admin
def admin_user_season_add():
    return render_template('season-new.html')


@app.route('/admin/user/approve/<int:id>')
@login_required_admin
def approve_users(id):
    if not db.approveUser(id):
        flash('Failed to approve the user', category='e_msg')
    flash('User approved', category='s_msg')

    return redirect(url_for('adminFunctions'))


@app.route('/admin/user/approve/<int:id>/trash/')
@login_required_admin
def trash_users(id):
    if not db.trashUser(id):
        flash('Failed to delete user', category='e_msg')
    flash('Successfully user removed', category='s_msg')
    return redirect(url_for('adminFunctions'))


### END ADMIN FUNCTIONS ###


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error=e)


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html', error=e)


if __name__ == '__main__':
    app.run()
