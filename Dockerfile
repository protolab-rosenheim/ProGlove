FROM python:3.6.3

WORKDIR /usr/src/app

COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python3", "proglove"]