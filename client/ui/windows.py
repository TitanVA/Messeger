import time
from PyQt5 import QtCore, QtWidgets

from client.ui.login_ui import Ui_Login_Dialog as login_ui_class
from client.ui.contacts_ui import Ui_ContactsWindow as contacts_ui_class
from client.ui.chat_ui import Ui_ChatMainWindow as chat_ui_class


class LoginWindow(QtWidgets.QDialog):
    """Login Window (user interface)"""

    def __init__(self, parent=None):
        """
        :param auth_instance: instance of client.client_proto.ClientAuth
        :param parent: default None
        """
        super().__init__(parent)
        #self.username = None
        #self.password = None
        #self.auth_instance = auth_instance

        self.ui = login_ui_class()
        self.ui.setupUi(self)


class ContactsWindow(QtWidgets.QMainWindow):
    """Contacts Window (user interface)"""

    def __init__(self, parent=None):
        """

        :param client_instance: instance of client.client_proto.ChatClientProtocol
        :param user_name: client's username
        :param chat_ins: instance of ChatWindow
        :param parent:
        """
        super().__init__(parent)

        self.ui = contacts_ui_class()
        self.ui.setupUi(self)




