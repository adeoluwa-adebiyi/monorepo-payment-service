FROM ubuntu:20.04

COPY . /home/app/src

WORKDIR /home/app/src

RUN apt-get update

RUN apt install -y python3-pip

RUN pip3 install -r requirements.txt

RUN python3 manage.py makemigrations

RUN python3 manage.py migrate

EXPOSE 80

CMD ["python3", "manage.py", "runserver", "0.0.0.0:80"]