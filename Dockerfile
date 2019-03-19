FROM python:3.7
ADD . /auth-api
WORKDIR /auth-api
RUN pip3 install -r requirements.txt
CMD python3 app.py