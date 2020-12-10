import yfinance as yf
import time
from concurrent import futures
import grpc
from Finance_API import Finance_API_pb2_grpc
from Finance_API import Finance_API_pb2

stock_names = [('Apple Inc.', 'AAPL'),
               ('Microsoft Corporation', 'MSFT'),
               ('Amazon.com, Inc.', 'AMZN'),
               ('Alphabet Inc.', 'GOOG'),
               ('Facebook, Inc.', 'FB'),
               ('Alibaba Group Holding Limited', 'BABA'),
               ('Tesla, Inc.', 'TSLA'),
               ('NVIDIA Corporation', 'NVDA'),
               ('PayPal Holdings, Inc.', 'PYPL'),
               ('Salesforce.com Inc', 'CRM'),
               ('Intel Corporation', 'INTC'),
               ('Advanced Micro Devices, Inc.', 'AMD')]


class StocksLoaderServicer(Finance_API_pb2_grpc.StocksLoaderServicer):
    def get_stocks(self, request, context):
        tickers = yf.Tickers([x[1] for x in stock_names])
        for idx, ticker in enumerate(tickers.tickers):
            data = ticker.history(period='5d')
            last_quote = (data.tail(1)['Close'].iloc[0])
            yield Finance_API_pb2.Stock(name=stock_names[idx][0], code=stock_names[idx][1], price=[last_quote])

    def get_stocks_history(self, request, context):
        stock_codes = request.codes.split()
        tickers = yf.Tickers(stock_codes)
        for idx, ticker in enumerate(tickers.tickers):
            data = ticker.history(period='5d')
            hist = data['Close'].tolist()
            yield Finance_API_pb2.Stock(name='', code=stock_codes[idx], price=hist)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Finance_API_pb2_grpc.add_StocksLoaderServicer_to_server(
        StocksLoaderServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
