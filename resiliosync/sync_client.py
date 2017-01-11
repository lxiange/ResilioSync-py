import requests
import time


class SyncClient:

    def __init__(self, host, port, username='root', password='root'):
        self._host = host
        self._port = port
        self._username = username
        self._password = password

        self.gui_url = 'http://{host}:{port}/gui/'.format(
            host=self._host,
            port=self._port,
        )
        self._init_session()

    def _init_session(self):
        """In case session being invalid, then we can reinit it."""
        self._session = requests.Session()
        self._session.auth = (self._username, self._password)
        self._token = self._apply_token()

    def _apply_token(self)->str:
        resp = self._session.get(self.gui_url + 'token.html').text
        return resp[44:108]

    @staticmethod
    def _time_stamp():
        return str(int(time.time() * 1000))

    def _req(self, action, **kwargs):
        payloads = {
            **kwargs,
            'token': self._token,
            'action': action,
            't': self._time_stamp(),
        }
        try:
            resp = self._session.get(self.gui_url, params=payloads)
            if resp.status_code != 200:
                # In case session timeout.
                self._init_session()
                resp = self._session.get(self.gui_url, params=payloads)
                if resp.status_code != 200:
                    raise Exception(resp.text + '\n\n' + str(payloads))
        except Exception as e:
            # TODO: handle it
            raise e

        return resp

    # def set_user_identity(self, username: str)->bool:
    #     resp = self._req('setuseridentity', username=username)
    #     return resp.json()['status'] == 200

    def apply_license_link(self, license: str)->bool:
        """Apply your Resilio Sync Pro license."""
        resp = self._req('applylicenselink', link=license)
        return resp.json()['status'] == 200 and resp.json()['value']['error'] == 0

    def get_sync_folders(self)->dict:
        """Get all synced folders from server."""
        resp = self._req('getsyncfolders')
        return resp.json()

    def get_files_list(self, folder_id: str, path='')->dict:
        """Get specified folder's filelist."""
        resp = self._req('getfileslist', folderid=folder_id, path=path)
        return resp.json()

    def remove_folder(self, folder_id, deletedirectory=True, fromalldevices=True)->bool:
        """Remove folder"""
        resp = self._req('removefolder', folderid=folder_id,
                         deletedirectory='true' if deletedirectory else 'false',
                         fromalldevices='true' if fromalldevices else 'false')
        return resp.json()['status'] == 200

    def add_dir(self, dir: str)->str:
        """Creat a new dir, just like `mkdir`
        Input:
            dir: full path, like `/mnt/sync/folders/your_dir_name`
        Output:
            dir + `/` : like `/mnt/sync/folders/your_dir_name/`
        """
        resp = self._req('adddir', dir=dir)
        return resp.json()['path']

    def add_sync_folder(self, path: str, secret: str, selectivesync=True)->str:
        """Add a sync key to given dir.
        Input:
            path: The path of the folder your want to restore data
            secret: The bt_sync key
            selectivesync: whether enable Selective Sync (need Pro license)
        Output:
            folderid: return the newly created sync folder's id
                    (This folderid is important, by which to control your folder.)
        """
        resp = self._req('addsyncfolder', path=path,
                         secret=secret,
                         selectivesync='true' if selectivesync else False)
        return resp.json()['value']['folderid']

    def get_secret_info(self, secret: str)->dict:
        """Get secret(bt_key)'s info, like r/w type."""
        resp = self._req('secret', secret=secret)
        return resp.json()

    def check_secret_valid(self, secret: str)->bool:
        """Check whether the secret(bt_key) is valid.
        Attention: It just check the format."""
        return self.get_secret_info(secret)['status'] == 200
