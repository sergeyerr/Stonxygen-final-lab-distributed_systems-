FROM python
WORKDIR /tests
RUN pip install redis 
RUN pip install pika
RUN pip install psycopg2
COPY example_app.py .
ENTRYPOINT ["python", "example_app.py"]
