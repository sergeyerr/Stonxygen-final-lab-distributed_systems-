import grpc
import secrets
import logging
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from concurrent import futures

import auth_pb2
import auth_pb2_grpc
host = 'localhost'
tokens_lifetime_sec = 300


class Auth_Servicer(auth_pb2_grpc.authServicer):
    def __init__(self):
        self.conn = psycopg2.connect(host = host, dbname='stocks', user='postgres', password='postgres')
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.conn.cursor()

    def GetToken(self, request, context):
        passwd = hash(request.password)
        user = request.user
        self.cursor.execute(f"SELECT COUNT(*) FROM users WHERE nick='{user}' and hash='{passwd}'")
        if self.cursor.fetchone()[0] == 0:
            context.set_details('no user with such password')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return auth_pb2.token_answer()
        token = secrets.token_hex(64)
        self.cursor.execute(f'''UPDATE users
            SET token = '{token}',
            token_date = now()
            WHERE nick = '{user}'
            ''')
        logging.info(f'token refreshed for user {user}')
        return auth_pb2.token_answer(token=token)

    def CheckToken(self, request, context):
        token = request.token
        self.cursor.execute(f"SELECT now() - token_date FROM users WHERE token='{token}'")
        res = self.cursor.fetchall()
        if len(res) == 0:
            context.set_details("token doesn't exist")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return auth_pb2.ok_answer()
        res = res[0]
        left_time = res[0]
        if left_time.seconds < tokens_lifetime_sec:
            return auth_pb2.ok_answer(ok_code=1)
        context.set_details("token outdated")
        context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
        return auth_pb2.ok_answer()

    def RegisterUser(self, request, context):
        passwd = hash(request.password)
        user = request.user
        self.cursor.execute(f"SELECT COUNT(*) FROM users WHERE nick='{user}'")
        if self.cursor.fetchone()[0] != 0:
            logging.info(f'user {user} already exist')
            context.set_details(f'user {user} already exist')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return auth_pb2.token_answer()
        token = secrets.token_hex(64)
        self.cursor.execute(f"INSERT INTO users VALUES ('{user}', '{passwd}', '{token}', Now())")
        logging.info(f'registered {user}')
        return auth_pb2.token_answer(token=token)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_authServicer_to_server(Auth_Servicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()


if __name__ == '__main__':
    serve()
