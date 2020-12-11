import pika, sys, os
import json
import grpc
import Finance_API_pb2
import Finance_API_pb2_grpc
import redis
import socket
import user_service_pb2
import user_service_pb2_grpc
from os import getenv

stat_expiration_time = getenv('STAT_EXPIRATION_TIME', '30')
user_service_host = getenv('USER_SERVICE', 'localhost')
finance_api_host = getenv('FINANCE_API', 'localhost')
rabbitmq_host = getenv('RABBIT_MQ_HOST', 'localhost')


def get_user_stocks(user):
    ans = ''
    with grpc.insecure_channel(user_service_host + ':50051') as channel:
        stub = user_service_pb2_grpc.user_serviceStub(channel)
        for code in stub.GetStocks(user_service_pb2.GetUserStocksRequest(user=user)).codes:
            ans += code + ' '
    # calling GetStocks(user) of Sergey's service
    # expecting list of stock codes ['AAPL', 'MSFT',..] or (better) string 'AAPL MSFT ..'
    ans = ans[:-1]
    return ans


# getting prices history through gRPC using Finance_API
# returns dictionary {'code1': [prices], ..}
def get_prices_history(stocks):
    prices_history = {}
    with grpc.insecure_channel(finance_api_host + ':50051') as channel:
        stub = Finance_API_pb2_grpc.StocksLoaderStub(channel)
        for stock_hist in stub.get_stocks_history(Finance_API_pb2.Stock_Codes(codes=stocks)):
            prices_history[stock_hist.code] = stock_hist.price

    #print(prices_history)
    return prices_history


def calc_stat_for_stock(stocks_with_prices, stock_code):
    diffs = {}
    days_cnt = None
    for key, value in stocks_with_prices.items():
        if days_cnt is None:
            days_cnt = len(value)

        diffs[key] = []
        for i in range(1, days_cnt):
            diffs[key].append((value[i]-value[i-1])/value[i-1])

    avgs = [0]*(days_cnt-1)
    for key, value in diffs.items():
        for i in range(len(value)):
            avgs[i] += value[i]

    for i in range(len(avgs)):
        avgs[i] /= len(stocks_with_prices)

    res = 0
    for i, diff in enumerate(diffs[stock_code]):
        res += diff/avgs[i]
    res /= (days_cnt-1)
    return res


def save_to_redis(user, stock_code, the_stat):
    redis_conn = redis.Redis()
    redis_conn.set(user + "_" + stock_code, the_stat, ex=int(stat_expiration_time))


def respond_by_socket(address):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('127.0.0.1', 7777))  # use address variable!
        s.sendall(b'Stat calculated and saved')
        data = s.recv(1024)
    print('Received', repr(data))


def callback(ch, method, properties, body):
    msg = json.loads(body)
    user = msg["user"]
    stock_code = msg["stock_code"]
    address = msg["address"]

    stocks = get_user_stocks(user)  # expecting list of stock codes ['AAPL', 'MSFT',..] or (better) string 'AAPL MSFT ..'

    stocks_with_prices = get_prices_history(stocks)

    the_stat = calc_stat_for_stock(stocks_with_prices, stock_code)
    print(the_stat)
    save_to_redis(user, stock_code, the_stat)

    respond_by_socket(address)


def main():
    credentials = pika.credentials.PlainCredentials('rabbit', 'rabbit', erase_on_connect=False)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
