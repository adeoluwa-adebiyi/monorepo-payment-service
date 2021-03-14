# FROM ubuntu:20.04

FROM python:3.6-buster

COPY . /home/app/src

WORKDIR /home/app/src

# RUN apt-get update

# RUN apt install -y python3-pip

RUN pip install -r requirements.txt

RUN python manage.py makemigrations

RUN sleep 10

RUN python manage.py migrate

EXPOSE 80

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]