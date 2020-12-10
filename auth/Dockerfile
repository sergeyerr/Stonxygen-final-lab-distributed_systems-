FROM python:3.7
WORKDIR /code
RUN python -m pip install --upgrade pip
RUN pip install grpcio~=1.19.0 protobuf psycopg2
COPY . .
ENTRYPOINT ["python", "server.py"]
