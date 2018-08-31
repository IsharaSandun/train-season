from app import app
import unittest
import tensorflow as tf
import numpy as np
import packages.facenet as facenet


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

    # Ensure the login behave correctly when given the correct credentials
    def test_user_dashboard_page_load(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login/',
            data=dict(email="e@gmail.com", password="a"),
            follow_redirects=True
        )
        self.assertTrue(b'You just logged in..', response.data)
        self.assertTrue(response.status_code, 202)

        def test_user_dashboard_page_load(self):
            tester = app.test_client(self)
            response = tester.get('/user/', content_type='html/text')
            self.assertEqual(response.status_code, 200)

    def test_user_season_add_page_load(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login/',
            data=dict(email="e@gmail.com", password="a"),
            follow_redirects=True
        )
        self.assertTrue(b'You just logged in..', response.data)
        self.assertTrue(response.status_code, 202)

        def test_user_season_add_page_load(self):
            tester = app.test_client(self)
            response = tester.get('/user/season/add/', content_type='html/text')
            self.assertEqual(response.status_code, 200)

    def test_user_profile_page_load(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login/',
            data=dict(email="e@gmail.com", password="a"),
            follow_redirects=True
        )
        self.assertTrue(b'You just logged in..', response.data)
        self.assertTrue(response.status_code, 202)

        def test_user_profile_page_load(self):
            tester = app.test_client(self)
            response = tester.get('/user/profile/', content_type='html/text')
            self.assertEqual(response.status_code, 200)


    def test_admin_login_page_load(self):
        tester = app.test_client(self)
        response = tester.get('/admin/login/', content_type='html/text')
        self.assertEqual(response.status_code, 200)


    def test_user_profile_page_load(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login/',
            data=dict(email="e@gmail.com", password="a"),
            follow_redirects=True
        )
        self.assertTrue(b'You just logged in..', response.data)
        self.assertTrue(response.status_code, 202)


        def test_user_profile_page_load(self):
            tester = app.test_client(self)
            response = tester.post(
                '/login/',
                data=dict(email="e@gmail.com", password="a"),
                follow_redirects=True
            )
            self.assertTrue(b'You just logged in..', response.data)
            self.assertTrue(response.status_code, 202)


    def test_admin_dashboard_page_load(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login/',
            data=dict(email="admin@gmail.com", password="a"),
            follow_redirects=True
        )
        self.assertTrue(b'You just logged in..', response.data)
        self.assertTrue(response.status_code, 202)

        def test_admin_dashboard_page_load(self):
            tester = app.test_client(self)
            response = tester.get('/admin/', content_type='html/text')
            self.assertEqual(response.status_code, 200)



    def test_admin_dashboard_page_load(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login/',
            data=dict(email="admin@gmail.com", password="a"),
            follow_redirects=True
        )
        self.assertTrue(b'You just logged in..', response.data)
        self.assertTrue(response.status_code, 202)

        def test_admin_profile_page_load(self):
            tester = app.test_client(self)
            response = tester.get('/admin/', content_type='html/text')
            self.assertEqual(response.status_code, 200)



    def test_admin_view_user_page_load(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login/',
            data=dict(email="admin@gmail.com", password="a"),
            follow_redirects=True
        )
        self.assertTrue(b'You just logged in..', response.data)
        self.assertTrue(response.status_code, 202)
        def test_admin_view_user_page_load(self):
            tester = app.test_client(self)
            response = tester.get('/admin/user/1/', content_type='html/text')
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
