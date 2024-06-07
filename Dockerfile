FROM python:3.9-alpine

WORKDIR /app

ADD ./requirements.txt ./

RUN pip install -r requirements.txt

add . ./

CMD python main.py