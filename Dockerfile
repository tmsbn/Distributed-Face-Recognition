FROM dalloriam/python-dlib
ADD . /myapp
WORKDIR /myapp
#RUN apt-get update
#RUN apt-get install -y software-properties-common
#RUN add-apt-repository ppa:george-edison55/cmake-3.x
#RUN apt-get update
#RUN apt-get install cmake
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python3 ${SYSTEM_TYPE}.py