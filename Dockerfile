FROM python:3.10-slim

# Django uchun kerakli paketlarni o'rnatish
RUN apt-get update && apt-get install -y libpq-dev && apt-get clean

# Ishchi katalogni o'rnatish
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Requirementsni ko'chirish va o'rnatish
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Django loyihani ko'chirish
COPY . /app/

# Portni ochish
EXPOSE 8000

# Django migratsiya va serverni ishga tushirish uchun
CMD python3 manage.py makemigrations && python3 manage.py migrate  && python manage.py runserver 0.0.0.0:8000
