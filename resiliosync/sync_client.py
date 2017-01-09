import requests


class SyncClient:

    def __init__(self, **kwargs):
        self._host = kwargs.get('host', '192.168.56.102')
        self._port = kwargs.get('port', '8888')
        self._username = kwargs.get('username', 'root')
        self._password = kwargs.get('password', 'root')

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

    def _req(self, action, **kwargs):
        payloads = {
            **kwargs,
            'token': self._token,
            'action': action
        }
        return self._session.get(self.gui_url, params=payloads)

    # def set_user_identity(self, username: str)->bool:
    #     resp = self._req('setuseridentity', username=username)
    #     return resp.json()['status'] == 200

    def apply_license_link(self, license: str)->bool:
        resp = self._req('applylicenselink', link=license)
        return resp.json()['status'] == 200 and resp.json()['value']['error'] == 0

    def get_sync_folders(self)->dict:
        resp = self._req('getsyncfolders')
        return resp.json()

    def get_files_list(self, folder_id: str, path='')->dict:
        resp = self._req('getfileslist', folderid=folder_id, path=path)
        return resp.json()

    def remove_folder(self, folder_id)->bool:
        resp = self._req('removefolder', folderid=folder_id,
                         deletedirectory='true', fromalldevices='true')
        return resp.json()['status'] == 200

    def add_dir(self, dir: str)->str:
        resp = self._req('adddir', dir=dir)
        return resp.json()['path']

    def add_sync_folder(self, path: str, secret: str)->str:
        resp = self._req('addsyncfolder', path=path,
                         secret=secret, selectivesync=true)
        return resp.json()['value']['folderid']
