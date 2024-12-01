FROM python:3.9-buster

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn
RUN pip install mysqlclient

COPY app app
COPY instance instance
COPY migrations migrations
COPY gunicorn.sh gunicorn.sh

RUN chmod +x gunicorn.sh

EXPOSE 3000

ENV FLASK_APP app

ENTRYPOINT ["./gunicorn.sh"]
