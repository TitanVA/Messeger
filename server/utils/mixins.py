from server.database.controller import ClientMessages
from server.database.models import CBase

from json import dumps, loads
from server.server_config import ENCODING


class DbInterfaceMixin:
    def __init__(self, db_path):
        self._cm = ClientMessages(db_path, CBase, echo=False)  # init DB

    def add_client(self, username, info=None):
        return self._cm.add_client(username, info)

    def get_client_by_username(self, username):
        return self._cm.get_client_by_username(username)

    def add_client_history(self, client_username, ip_addr='8.8.8.8'):
        return self._cm.add_client_history(client_username, ip_addr)

    def set_user_online(self, client_username):
        return self._cm.set_user_online(client_username)


class ConvertMixin:
    def _dict_to_bytes(self, msg_dict):
        """
        Преобразование словаря в байты
        :param msg_dict: словарь
        :return: bytes
        """
        # Проверям, что пришел словарь
        if isinstance(msg_dict, dict):
            jmessage = dumps(msg_dict)  # Преобразуем словарь в json
            bmessage = jmessage.encode(ENCODING)  # Переводим json в байты
            return bmessage
        else:
            raise TypeError

    def _bytes_to_dict(self, msg_bytes):
        """
        Получение словаря из байтов
        :param msg_bytes: сообщение в виде байтов
        :return: словарь сообщения
        """
        # Если переданы байты
        if isinstance(msg_bytes, bytes):

            jmessage = msg_bytes.decode(ENCODING)  # Декодируем
            message = loads(jmessage)  # Из json делаем словарь

            # Если там был словарь
            if isinstance(message, dict):
                return message  # Возвращаем сообщение
            else:
                raise TypeError  # Нам прислали неверный тип
        else:
            raise TypeError  # Передан неверный тип
