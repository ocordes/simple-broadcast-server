import unittest
import server as tested_app
import json


# stolen from https://github.com/ozada/flask-app-github-actions
#
#

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        tested_app.app.config['TESTING'] = True
        self.app = tested_app.app.test_client()

    def test_get_ping_endpoint(self):
        r = self.app.get('/ping')
        self.assertEqual(r.data, b'pong')


if __name__ == '__main__':
    unittest.main()
