FROM python:3.8-alpine
MAINTAINER Ken H <docker@kenh.fr>

# Add Tini
RUN apk add --update tini
RUN apk --no-cache add binutils musl-dev

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 1234

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["gunicorn", "-w 3", "-b :1234", "pytilt-api:app"]
