# Dockerfile
FROM python:3.11-slim

# Устанавливаем локали для поддержки UTF-8 (важно для кириллицы)
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]