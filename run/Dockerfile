FROM python:3
ADD . /myapp
WORKDIR /myapp
RUN pip install -r requirements.
EXPOSE 5000
CMD python3 ${SYSTEM_TYPE}.py