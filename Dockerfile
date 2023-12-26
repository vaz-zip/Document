# Взять официальный базовый образ Python платформы Docker
FROM python:3.10.6
# Задать переменные среды
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Задать рабочий каталог
WORKDIR /code
# Установить зависимости
RUN pip3 install --upgrade pip
COPY requirements.txt /code/
RUN pip3 install -r requirements.txt

# Copy the Django project
COPY . /code/

