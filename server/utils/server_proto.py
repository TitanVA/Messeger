from asyncio import Protocol
from hashlib import pbkdf2_hmac
from binascii import hexlify

from server.utils.server_messages import JimServerMessage
from server.utils.mixins import ConvertMixin, DbInterfaceMixin


class ChatServerProtocol(Protocol, ConvertMixin, DbInterfaceMixin):
    """ A Server Protocol listening for subscriber messages """

    def __init__(self, db_path, connections, users):
        super().__init__(db_path)
        self.connections = connections
        self.users = users
        self.jim = JimServerMessage()

        # useful temp variables
        self.user = None
        self.transport = None

    def connection_made(self, transport):
        """ Called when connection is initiated """

        self.connections[transport] = {
            'peername': transport.get_extra_info('peername'),
            'username': '',
            'transport': transport
        }
        self.transport = transport

    def authenticate(self, username, password):
        # check user in DB
        if username and password:
            usr = self.get_client_by_username(username)
            dk = pbkdf2_hmac('sha256', password.encode('utf-8'),
                                     'salt'.encode('utf-8'), 100000)
            hashed_password = hexlify(dk)

            if usr:
                # existing user
                if hashed_password == usr.password:
                    # add client's history row
                    self.add_client_history(username)
                    return True
                else:
                    return False
            else:
                # new user
                print('new user')
                self.add_client(username, hashed_password)
                # add client's history row
                self.add_client_history(username)
                return True
        else:
            return False

    def data_received(self, data):
        """The protocol expects a json message in bytes"""

        _data = self._bytes_to_dict(data)
        print(_data)

        if _data:
            try:

                if _data['action'] == 'presence':  # received presence msg
                    if _data['user']['account_name']:

                        print(self.user, _data['user']['status'])
                        resp_msg = self.jim.response(code=200)
                        self.transport.write(self._dict_to_bytes(resp_msg))
                    else:
                        resp_msg = self.jim.response(code=500,
                                                     error='wrong presence msg')
                        self.transport.write(self._dict_to_bytes(resp_msg))

                elif _data['action'] == 'authenticate':
                    # todo complete this
                    if self.authenticate(_data['user']['account_name'],
                                         _data['user']['password']):

                        # add new user to temp variables
                        if _data['user']['account_name'] not in self.users:
                            print(f'self.users - {self.users}')
                            self.user = _data['user']['account_name']
                            print(f'self.user - {self.user}')
                            self.connections[self.transport][
                                'username'] = self.user
                            print(f'self.connections - {self.connections}')
                            self.users[_data['user']['account_name']] = \
                                self.connections[self.transport]
                            print(f'self.users - {self.users}')
                            self.set_user_online(_data['user']['account_name'])

                        resp_msg = self.jim.probe(self.user)
                        self.users[_data['user']['account_name']][
                            'transport'].write(self._dict_to_bytes(resp_msg))
                    else:
                        resp_msg = self.jim.response(code=402,
                                                     error='wrong login/password')
                        self.transport.write(self._dict_to_bytes(resp_msg))

            except Exception as e:
                resp_msg = self.jim.response(code=500, error=e)
                self.transport.write(self._dict_to_bytes(resp_msg))

        else:
            resp_msg = self.jim.response(code=500,
                                         error='Вы отправили сообщение '
                                               'без имени или данных'
                                         )
            self.transport.write(self._dict_to_bytes(resp_msg))
