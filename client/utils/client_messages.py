from datetime import datetime as dt


class JimClientMessage:
    """Client's requests protocol"""
    def auth(self, username, password):
        """
        Authorization message

        :param username:
        :param password:
        :return: dict with data
        """
        data = {
            "action": "authenticate",
            "time": dt.now().timestamp(),
            "user": {
                "account_name": username,
                "password": password
            }
        }
        return data

    def presence(self, sender, status="Yep, I am here!"):
        """
        Presence message, which notify server that client is online.
        :param sender: username
        :param status: some text
        :return: dict with data
        """
        data = {
            "action": "presence",
            "time": dt.now().timestamp(),
            "type": "status",
            "user": {
                "account_name": sender,
                "status": status
            }
        }
        return data
