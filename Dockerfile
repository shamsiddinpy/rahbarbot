FROM python:3.10-slim

# Django uchun kerakli paketlarni o'rnatish
RUN apt-get update && apt-get install -y libpq-dev gcc python3-pip && apt-get clean

# Ishchi katalogni o'rnatish
WORKDIR /app

# Muhit o'zgaruvchilarini sozlash
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Requirementsni ko'chirish va o'rnatish
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN --mount=type=cache,id=custom-pip,target=/root/.cache/pip pip install -r requirements.txt

# Django loyihani ko'chirish
COPY . /app/

# Portni ochish
EXPOSE 8000

# Django migratsiya va Gunicorn serverni ishga tushurish uchun
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && gunicorn --bind 0.0.0.0:8000 root.wsgi:application"]
