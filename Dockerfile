FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python3 python3-pip apache2

RUN pip3 install requests bs4

RUN mkdir Scanner
WORKDIR Scanner
COPY ./ ./
WORKDIR src

CMD ["./run.sh"]

