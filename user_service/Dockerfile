FROM python
WORKDIR /code
RUN apt update -y
RUN apt install build-essential
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "server.py"]
