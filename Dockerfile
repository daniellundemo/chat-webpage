FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev ssh git cron

COPY crontab-git /etc/cron.d/crontab-git
COPY id_rsa /root/.ssh/id_rsa

RUN chmod 0644 /etc/cron.d/crontab-git
RUN crontab /etc/cron.d/crontab-git

RUN ssh-keyscan github.com >> /root/.ssh/known_hosts
RUN chmod 700 /root/.ssh/id_rsa
RUN git clone git@github.com:daniellundemo/chat-webpage.git

WORKDIR /chat-webpage

RUN git pull
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

EXPOSE 4000/tcp

CMD [ "server.py" ]