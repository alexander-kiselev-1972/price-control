FROM python:3.9.5

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/



RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV TZ Europe/Praga

RUN python manage.py makemigrations
RUN python manage.py migrate




CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

