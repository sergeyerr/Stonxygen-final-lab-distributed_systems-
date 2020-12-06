FROM python
RUN pip install redis
WORKDIR /test
COPY redis-tests.py .
ENTRYPOINT ["sleep", "1000"]