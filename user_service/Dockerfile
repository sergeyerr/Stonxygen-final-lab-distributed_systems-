FROM python:3.7
WORKDIR /code
RUN apt update -y
RUN apt install build-essential
RUN python -m pip install --upgrade pip
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "server.py"]
