FROM python
WORKDIR /app 
copy . .
RUN pip install flask
ENTRYPOINT ["python", "server.py"]