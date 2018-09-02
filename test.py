from app import app
import unittest
import tensorflow as tf
import numpy as np
import packages.net as facenet


class FlaskTestCase(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_user_register_page_load(self):
        tester = app.test_client(self)
        response = tester.get('/register/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_user_login_page_load(self):
        tester = app.test_client(self)
        response = tester.get('/login/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def check_user_logging(self):
        tester = app.test_client(self)
        response = tester.get('/login/',data=dict(email='e@gmail.com',password='a'),follow_redirects=True)
        self.assertIn(b'incorrect', response.data)

    def check_user_logout(self):
        tester = app.test_client(self)
        response = tester.get('/logout/',follow_redirects=True)
        self.assertIn(b'session', response.data)


    def test_user_page(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["logged_in"] = True
                sess["user_type"] = 'user'
            response = client.get('/user/', content_type='html/text')
            self.assertEqual(response.status_code, 200)

    def test_user_profile_page(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["logged_in"] = True
                sess["user_type"] = 'user'
            response = client.get('/user/profile/', content_type='html/text')
            self.assertEqual(response.status_code, 200)

    def check_admin_logging(self):
        tester = app.test_client(self)
        response = tester.get('/admin/login/',data=dict(email='admin@gmail.com',password='a'),follow_redirects=True)
        self.assertIn(b'incorrect', response.data)

    def check_admin_logout(self):
        tester = app.test_client(self)
        response = tester.get('/logout/',follow_redirects=True)
        self.assertIn(b'session', response.data)


    def test_admin_home_page(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["logged_in"] = True
                sess["user_type"] = 'admin'
            response = client.get('/admin/', content_type='html/text')
            self.assertEqual(response.status_code, 200)

    def test_admin_profile_page(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["logged_in"] = True
                sess["user_type"] = 'admin'
            response = client.get('/admin/profile/', content_type='html/text')
            self.assertEqual(response.status_code, 200)

    def test_admin_user_view_page(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["logged_in"] = True
                sess["user_type"] = 'admin'
            response = client.get('/admin/user/1/', content_type='html/text')
            self.assertEqual(response.status_code, 200)



class TripletLossTest(unittest.TestCase):

    def testDemuxEmbeddings(self):
        batch_size = 3 * 12
        embedding_size = 16
        alpha = 0.2

        with tf.Graph().as_default():
            embeddings = tf.placeholder(tf.float64, shape=(batch_size, embedding_size), name='embeddings')
            anchor, positive, negative = tf.unstack(tf.reshape(embeddings, [-1, 3, embedding_size]), 3, 1)
            triplet_loss = facenet.triplet_loss(anchor, positive, negative, alpha)

            sess = tf.Session()
            with sess.as_default():
                np.random.seed(seed=666)
                emb = np.random.uniform(size=(batch_size, embedding_size))
                tf_triplet_loss = sess.run(triplet_loss, feed_dict={embeddings: emb})

                pos_dist_sqr = np.sum(np.square(emb[0::3, :] - emb[1::3, :]), 1)
                neg_dist_sqr = np.sum(np.square(emb[0::3, :] - emb[2::3, :]), 1)
                np_triplet_loss = np.mean(np.maximum(0.0, pos_dist_sqr - neg_dist_sqr + alpha))

                np.testing.assert_almost_equal(tf_triplet_loss, np_triplet_loss, decimal=5,
                                               err_msg='Triplet loss is incorrect')


if __name__ == '__main__':
    unittest.main()
