# Menggunakan image dasar Python
FROM python:3.8-slim

# Menetapkan direktori kerja di dalam container
WORKDIR /app

# Menyalin file requirements.txt ke container
COPY requirements.txt .

# Install dependensi dari requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin semua file aplikasi ke container
COPY . .

# Menetapkan port untuk aplikasi Flask
EXPOSE 8080

# Menjalankan aplikasi dengan gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
