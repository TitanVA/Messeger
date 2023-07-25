"""файл для запуска клиентского приложения в цикле"""
from argparse import ArgumentParser
from asyncio import ensure_future, get_event_loop, run, create_task

from client.utils.client_proto import ChatClientProtocol, ClientAuth
from client.client_config import DB_PATH, PORT


class ConsoleClientApp:
    """Console Client"""

    def __init__(self, parsed_args, db_path):
        self.args = parsed_args
        self.db_path = db_path
        self.ins = None

    def main(self):
        # create event loop
        loop = get_event_loop()
        print(f"ох 1 - {loop}")
        #for signame in ('SIGINT', 'SIGTERM'):
            #loop.add_signal_handler(getattr(signal, signame), loop.stop)

        # authentication process
        auth = ClientAuth(db_path=self.db_path)
        while True:
            usr = self.args["user"] or input('username: ')
            passwrd = self.args["password"] or input('password: ')
            auth.username = usr
            auth.password = passwrd
            is_auth = auth.authenticate()
            if is_auth:
                break
            else:
                print('wrong username/password')

        # Each client will create a new protocol instance
        tasks = []
        client_ = ChatClientProtocol(db_path=self.db_path,
                                     loop=loop,
                                     username=usr,
                                     password=passwrd)
        # connect to our server
        try:
            coro = loop.create_connection(lambda: client_, self.args["addr"], self.args["port"])
            print(f"ох 2 - {coro}")
            transport, protocol = loop.run_until_complete(coro)
            print(f"ох 3 - {transport, protocol}")
        except ConnectionRefusedError:
            print('Error. wrong server')
            exit(1)

        # Serve requests until Ctrl+C
        try:
            task = loop.create_task(client_.get_from_console())  # create Task from coroutine
            print(f"ох 4 - {task}")
            tasks.append(task)
            loop.run_until_complete(task)
            #await task
            #run(task)

        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(e)

        finally:
            loop.close()


def parse_and_run():
    def parse_args():
        parser = ArgumentParser(description="Client settings")
        parser.add_argument("--user", default="user1", type=str)
        parser.add_argument("--password", default="123", type=str)
        parser.add_argument("--addr", default="127.0.0.1", type=str)
        parser.add_argument("--port", default=PORT, type=int)
        parser.add_argument('--nogui', action='store_true')
        return vars(parser.parse_args())

    args = parse_args()

    if args['nogui']:
        # start consoles server
        a = ConsoleClientApp(args, DB_PATH)
        a.main()


if __name__ == '__main__':
    parse_and_run()
