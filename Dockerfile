FROM ubuntu
RUN apt-get update
RUN export DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y tzdata=2018d-1
RUN ln -fs /usr/share/zoneinfo/Europe/Moscow /etc/localtime 
RUN dpkg-reconfigure -f noninteractive tzdata

FROM python:3.9
# установка рабочей директории в контейнере
WORKDIR /code

# копирование файла зависимостей в рабочую директорию
COPY requirements.txt .
# установка зависимостей
RUN pip install -r requirements.txt


COPY . ./
CMD [ "python", "./main.py" ]