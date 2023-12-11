FROM python:3.10.0-alpine

RUN adduser -D sudden

WORKDIR /home/sudden

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY server.py config.py app.db boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP server.py

RUN chown -R sudden:sudden ./
USER sudden

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]