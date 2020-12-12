import grpc
import time
import logging
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.errors import UniqueViolation, ForeignKeyViolation, InterfaceError
import psycopg2
from concurrent import futures
from os import getenv
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

import user_service_pb2_grpc
import user_service_pb2

host = getenv('POSTGRES_CONNECTION', 'localhost')
stock_list_loc = getenv('STOCK_LIST_LOCATION',  'stocks_list.csv')
reinit_db = bool(getenv('REINIT_DB', False))


def init_db(reinit=False):
    con = psycopg2.connect(host=host, user='postgres', password='postgres');
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = con.cursor();
    if reinit:
        logging.info('droping db')
        cursor.execute("DROP DATABASE IF EXISTS stocks;")
    cursor.execute("SELECT datname FROM pg_database WHERE datname = %s;", ('stocks',))
    if len(cursor.fetchall()) == 0:
        sqlCreateDB = f"create database stocks;"
        cursor.execute(sqlCreateDB)
    cursor.close();
    con.close()

    con = psycopg2.connect(dbname='stocks',host=host, user='postgres', password='postgres');
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = con.cursor();
    logging.info('creating tables')
    sqlCreateTableUser = "CREATE TABLE IF NOT EXISTS users(nick VARCHAR(256) PRIMARY KEY, hash VARCHAR(512) NOT NULL, token VARCHAR(512) NOT NULL, token_date timestamp NOT NULL);"
    sqlCreateTableStock = "CREATE TABLE IF NOT EXISTS stocks(code VARCHAR(10) PRIMARY KEY);"
    sqlCreateTableUserStock = '''CREATE TABLE IF NOT EXISTS
    user_stock (
    id serial PRIMARY KEY,
    nick VARCHAR (256) NOT NULL,
    code VARCHAR (10) NOT NULL,
    FOREIGN KEY (nick) REFERENCES users (nick),
    FOREIGN KEY (code) REFERENCES stocks (code),
    UNIQUE (nick, code)
    );
    '''
    for query in [sqlCreateTableUser, sqlCreateTableStock, sqlCreateTableUserStock]:
        cursor.execute(query)
    cursor.execute('select COUNT(*) from stocks')
    if cursor.fetchone()[0] == 0:
        logging.info('inserting stocks')
        with open(stock_list_loc, 'r') as f:
            for s in f:
                cursor.execute(f"INSERT INTO stocks VALUES ('{s.strip()}')")
    else:
        logging.info('stocks already presented')
    cursor.close()
    con.close()

class UserServicer(user_service_pb2_grpc.user_serviceServicer):
    def __init__(self):
        init_db(reinit_db)

    def AddStockToUser(self, request, context):
        conn = psycopg2.connect(host=host, dbname='stocks', user='postgres', password='postgres')
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        stock = request.stock_code.upper()
        user = request.user
        try:
            logging.debug(f"INSERT INTO user_stock(nick, code) VALUES ('{user}','{stock}')")
            cursor.execute(f"INSERT INTO user_stock(nick, code) VALUES ('{user}','{stock}')")
            cursor.close()
            conn.close()
            return user_service_pb2.OkAnswer(ok_code=1)
        except UniqueViolation:
            context.set_details('already added stock')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            cursor.close()
            conn.close()
            return user_service_pb2.OkAnswer()
        except ForeignKeyViolation:
            context.set_details('user or stock are not presented')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            cursor.close()
            conn.close()
            return user_service_pb2.OkAnswer()


    def RemoveStockFromUser(self, request, context):
        conn = psycopg2.connect(host=host, dbname='stocks', user='postgres', password='postgres')
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        stock = request.stock_code.upper()
        user = request.user
        logging.debug(f"DELETE FROM user_stock WHERE nick='{user}' AND code='{stock}'")
        cursor.execute(f"DELETE FROM user_stock WHERE nick='{user}' AND code='{stock}'")
        cursor.close()
        conn.close()
        return user_service_pb2.OkAnswer(ok_code=1)

    def GetStocks(self, request, context):
        conn = psycopg2.connect(host=host, dbname='stocks', user='postgres', password='postgres')
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        logging.debug(f"SELECT code from user_stock WHERE nick = '{request.user}'")
        cursor.execute(f"SELECT * from user_stock WHERE nick = '{request.user}'")
        ans = []
        for x in cursor.fetchall():
            ans.append(x[1])
        cursor.close()
        conn.close()
        return user_service_pb2.StockAnswer(codes=ans)

    def GetAllStocks(self, request, context):
        conn = psycopg2.connect(host=host, dbname='stocks', user='postgres', password='postgres')
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute('SELECT * from stocks')
        ans = []
        for x in cursor.fetchall():
            ans.append(x[0])
        cursor.close()
        conn.close()
        return user_service_pb2.StockAnswer(codes=ans)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_service_pb2_grpc.add_user_serviceServicer_to_server(UserServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(100500)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
