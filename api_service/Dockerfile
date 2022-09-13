FROM python:3.10-slim-buster

RUN mkdir /app && chmod +rwx /app

WORKDIR /app

RUN apt-get update && \
    apt-get -y dist-upgrade && \
    apt-get -y install bash 

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh
CMD ./run.sh
