FROM ubuntu:18.04

RUN apt-get update && apt-get upgrade -y 

RUN apt-get install \
    git\ 
    golang-go \
    nano \
    python3 \
    python3-pip\
    -y
RUN pip3 install \
    requests

COPY . /ATM_Controller

WORKDIR /ATM_Controller

RUN go get -u github.com/gorilla/mux

RUN go run test_webserver.go & 