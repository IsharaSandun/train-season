#FR
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import os

from flask import Flask, render_template, request, url_for, redirect, session, flash, send_from_directory, send_file, \
    jsonify
from forms import RegisterForm
from dbconnect import Database
from passlib.hash import sha256_crypt

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
PRE_FOLDER = './uploads/pre/'
CLASSIFIER = './class/classifier.pkl'
MODEL_DIR = './model'
npy = ''
img_path = 'img.jpg'


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

@app.route('/recognize/')
def recognize():
    with tf.Graph().as_default():
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.6)
        sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
        with sess.as_default():
            pnet, rnet, onet = detect_face.create_mtcnn(sess, npy)

            minsize = 20  # minimum size of face
            threshold = [0.6, 0.7, 0.7]  # three steps's threshold
            factor = 0.709  # scale factor
            margin = 44
            frame_interval = 3
            batch_size = 1000
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
            prevTime = 0
            frame = cv2.imread(img_path, 0)

            frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)  # resize frame (optional)

            curTime = time.time() + 1  # calc fps
            timeF = frame_interval

            if (c % timeF == 0):
                find_results = []

                if frame.ndim == 2:
                    frame = facenet.to_rgb(frame)
                frame = frame[:, :, 0:3]
                bounding_boxes, _ = detect_face.detect_face(frame, minsize, pnet, rnet, onet, threshold, factor)
                nrof_faces = bounding_boxes.shape[0]
                print('Face Detected: %d' % nrof_faces)

                if nrof_faces > 0:
                    det = bounding_boxes[:, 0:4]
                    img_size = np.asarray(frame.shape)[0:2]

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
                        print(predictions)
                        best_class_indices = np.argmax(predictions, axis=1)
                        print("era", best_class_indices)
                        best_class_probabilities = predictions[np.arange(len(best_class_indices)), best_class_indices]
                        print(best_class_probabilities)

                        cv2.rectangle(frame, (bb[i][0], bb[i][1]), (bb[i][2], bb[i][3]), (0, 255, 0), 2)  # boxing face

                        # plot result idx under box
                        text_x = bb[i][0]
                        text_y = bb[i][3] + 20

                        if best_class_probabilities[0] > 0.7:
                            print('Result Indices: ', best_class_indices[0])
                            print(HumanNames)
                            for H_i in HumanNames:
                                # print(H_i)
                                if HumanNames[best_class_indices[0]] == H_i:
                                    result_names = HumanNames[best_class_indices[0]]
                                    print("Face Recognized: ",result_names)
                                    cv2.putText(frame, result_names, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                                1, (0, 0, 255), thickness=1, lineType=2)
                        else:
                            print('unknown')
                            cv2.putText(frame, 'Unknown', (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                                        (0, 0, 255), thickness=1, lineType=2)
                else:
                    print('Unable to align')
            cv2.imshow('Image', frame)


    return 'Recognize end'


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
