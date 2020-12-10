FROM python:3.7
WORKDIR /code
RUN python -m pip install --upgrade pip
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "Finance_API.py"]
