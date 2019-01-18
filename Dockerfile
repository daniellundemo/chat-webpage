FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev ssh

RUN mkdir /root/.ssh

COPY requirements.txt /app/requirements.txt
COPY id_rsa /root/.ssh/id_rsa

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

EXPOSE 4000/tcp

CMD [ "server.py" ]