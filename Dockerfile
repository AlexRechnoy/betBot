	
FROM python:3.9
# установка рабочей директории в контейнере
WORKDIR /code

# копирование файла зависимостей в рабочую директорию
COPY requirements.txt .
# установка зависимостей
RUN pip install -r requirements.txt

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . ./
CMD [ "python", "./main.py" ]

