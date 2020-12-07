import grpc
import Finance_API_pb2_grpc
import Finance_API_pb2
import time


def update_stocks(stub):
    for stock in stub.get_stocks(Finance_API_pb2.Get_stocks_request()):
        print(stock.name + " " + stock.code + " " + str(stock.price))


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = Finance_API_pb2_grpc.StocksLoaderStub(channel)

        while True:
            update_stocks(stub)
            time.sleep(20)


if __name__ == '__main__':
    run()
