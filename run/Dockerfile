FROM stackbrew/debian:jessie
RUN apt-get install -qy python3
RUN apt-get install -qy python3-pip
ADD . /myapp
WORKDIR /myapp
RUN pip-3.3 install -r requirements.txt
RUN pip-3.3 install .
EXPOSE 5000
CMD myapp --port 8000