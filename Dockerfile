FROM python:3.11-alpine

LABEL org.opencontainers.image.source=https://github.com/alecks20/quack-media

VOLUME /app/uploads
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:80 --chdir=./"
COPY . .

EXPOSE 80

CMD ["gunicorn","app:app"]