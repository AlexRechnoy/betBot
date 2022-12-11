FROM python:3.9

# установка рабочей директории в контейнере
WORKDIR /code
# копирование файла зависимостей в рабочую директорию
COPY requirements.txt .
# установка зависимостей
RUN pip install -r requirements.txt

COPY . ./
CMD [ "python", "./main.py" ]