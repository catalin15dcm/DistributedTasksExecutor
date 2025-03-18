import unittest
import json
from master import app

class MasterNodeTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_submit_task(self):
        response = self.app.post('/submit', json={'task': '1+2'})
        data = json.loads(response.data)
        print(data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('job_id', data)
        self.assertFalse(data['finished'])

    def test_get_job_status_not_found(self):
        response = self.app.get('/job/invalid_id')
        data = json.loads(response.data)
        print(data)
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)

    def test_register_worker(self):
        response = self.app.post('/worker', json={'worker_name': 'worker_1'})
        data = json.loads(response.data)
        print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'Worker registered')

if __name__ == '__main__':
    unittest.main()
