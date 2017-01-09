import unittest
import resiliosync


class TestSyncClient(unittest.TestCase):

    def setUp(self):
        self.sync_client = resiliosync.SyncClient()

    def test_apply_token(self):
        token = self.sync_client._token
        self.assertEqual(64, len(token))
        self.assertEqual(token[-5:], 'AAAAA')

    def test_get_files_list(self):
        files_list = self.sync_client.get_files_list('17272499736134150978')
        self.assertIsNot(files_list, None)

if __name__ == "__main__":
    unittest.main()
