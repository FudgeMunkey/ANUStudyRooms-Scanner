FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python3 python3-pip apache2

RUN pip3 install requests bs4

# Set the Date/Time of the machine
RUN ln -fs /usr/share/zoneinfo/Australia/Sydney > /etc/localtime
RUN apt-get install -y tzdata
RUN echo "Australia/Sydney" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

RUN mkdir Scanner
WORKDIR Scanner
COPY ./ ./
WORKDIR src

CMD ["./run.sh"]

