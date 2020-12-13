import grpc
import secrets
import logging
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from concurrent import futures
from os import getenv
import time
import hashlib

import auth_pb2
import auth_pb2_grpc
host = getenv('POSTGRES_CONNECTION', 'localhost')
tokens_lifetime_sec = int(getenv('TOKEN_LIFETIME', 300))

import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def find_hash(s):
    hashlib.md5(str(s).encode('utf-8')).hexdigest()

class Auth_Servicer(auth_pb2_grpc.authServicer):
    def GetToken(self, request, context):
        conn = psycopg2.connect(host=host, dbname='stocks', user='postgres', password='postgres')
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        passwd = find_hash(request.password)
        user = request.user
        logging.debug(f'got user {request.user} with pass: {request.password}')
        cursor.execute(f"SELECT COUNT(*) FROM users WHERE nick='{user}' and hash='{passwd}'")
        if cursor.fetchone()[0] == 0:
            context.set_details('no user with such password')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            cursor.close();
            conn.close();
            return auth_pb2.TokenAnswer()
        token = secrets.token_hex(64)
        cursor.execute(f'''UPDATE users
            SET token = '{token}',
            token_date = now()
            WHERE nick = '{user}'
            ''')
        logging.info(f'token refreshed for user {user}')
        cursor.close();
        conn.close();
        return auth_pb2.TokenAnswer(token=token)

    def CheckToken(self, request, context):
        conn = psycopg2.connect(host=host, dbname='stocks', user='postgres', password='postgres')
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        token = request.token
        cursor.execute(f"SELECT nick, now() - token_date FROM users WHERE token='{token}'")
        res = cursor.fetchall()
        if len(res) == 0:
            cursor.close();
            conn.close();
            context.set_details("token doesn't exist")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return auth_pb2.UserAnswer()
        res = res[0]
        user = res[0]
        left_time = res[1]
        if left_time.seconds < tokens_lifetime_sec:
            cursor.close();
            conn.close();
            return auth_pb2.UserAnswer(user=user)
        context.set_details("token outdated")
        context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
        cursor.close();
        conn.close();
        return auth_pb2.UserAnswer()

    def RegisterUser(self, request, context):
        conn = psycopg2.connect(host=host, dbname='stocks', user='postgres', password='postgres')
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        logging.debug(f'got user {request.user} with pass: {request.password}')
        passwd = find_hash(request.password)
        user = request.user
        cursor.execute(f"SELECT COUNT(*) FROM users WHERE nick='{user}'")
        if cursor.fetchone()[0] != 0:
            logging.info(f'user {user} already exist')
            context.set_details(f'user {user} already exist')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return auth_pb2.TokenAnswer()
        token = secrets.token_hex(64)
        cursor.execute(f"INSERT INTO users VALUES ('{user}', '{passwd}', '{token}', Now())")
        logging.info(f'registered {user}')
        cursor.close();
        conn.close();
        return auth_pb2.TokenAnswer(token=token)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_authServicer_to_server(Auth_Servicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
   # server.wait_for_termination()
    try:
        while True:
            time.sleep(100500)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
