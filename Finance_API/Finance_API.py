import yfinance as yf
import time
from concurrent import futures
import grpc
import Finance_API_pb2
import Finance_API_pb2_grpc

import user_service_pb2
import user_service_pb2_grpc
from os import getenv


user_service_host = getenv('USER_SERVICE', 'localhost')


# stock_names = [('Apple Inc.', 'AAPL'),
#                ('Microsoft Corporation', 'MSFT'),
#                ('Amazon.com, Inc.', 'AMZN'),
#                ('Alphabet Inc.', 'GOOG'),
#                ('Facebook, Inc.', 'FB'),
#                ('Alibaba Group Holding Limited', 'BABA'),
#                ('Tesla, Inc.', 'TSLA'),
#                ('NVIDIA Corporation', 'NVDA'),
#                ('PayPal Holdings, Inc.', 'PYPL'),
#                ('Salesforce.com Inc', 'CRM'),
#                ('Intel Corporation', 'INTC'),
#                ('Advanced Micro Devices, Inc.', 'AMD')]

stock_names = []


class StocksLoaderServicer(Finance_API_pb2_grpc.StocksLoaderServicer):
    def get_stocks(self, request, context):
        tickers = yf.Tickers([x[1] for x in stock_names])
        for idx, ticker in enumerate(tickers.tickers):
            data = ticker.history(period='5d')
            last_quote = (data.tail(1)['Close'].iloc[0])
            if stock_names[idx][0] == '':
                stock_names[idx][0] = ticker.info['shortName']
            yield Finance_API_pb2.Stock(name=stock_names[idx][0], code=stock_names[idx][1], price=[last_quote])

    def get_stocks_history(self, request, context):
        stock_codes = request.codes.split()
        tickers = yf.Tickers(stock_codes)
        for idx, ticker in enumerate(tickers.tickers):
            data = ticker.history(period='5d')
            hist = data['Close'].tolist()
            yield Finance_API_pb2.Stock(name='', code=stock_codes[idx], price=hist)


def serve():
    with grpc.insecure_channel(user_service_host + ':50051') as channel:
        stub = user_service_pb2_grpc.user_serviceStub(channel)
        for code in stub.GetAllStocks(user_service_pb2.GetAllStocksRequest()).codes:
            stock_names.append(['', code])

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Finance_API_pb2_grpc.add_StocksLoaderServicer_to_server(
        StocksLoaderServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    #server.wait_for_termination()
    try:
        while True:
            time.sleep(100500)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
