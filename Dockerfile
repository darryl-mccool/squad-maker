FROM ubuntu:latest
MAINTAINER Ben Schreiber "Benobi1995@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python3-pip python3.7 build-essential
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]