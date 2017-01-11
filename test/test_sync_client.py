import unittest
import resiliosync


class TestSyncClient(unittest.TestCase):

    def setUp(self):
        self.sync_client = resiliosync.SyncClient('192.168.56.102', 8888)

    def test_apply_token(self):
        token = self.sync_client._token
        self.assertEqual(64, len(token))
        self.assertEqual(token[-5:], 'AAAAA')

    def test_get_files_list(self):
        files_list = self.sync_client.get_files_list('12514058833974463344')
        self.assertIsNot(files_list, None)

if __name__ == "__main__":
    unittest.main()
