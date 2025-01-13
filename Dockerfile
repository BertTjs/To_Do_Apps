# Gunakan base image Python versi ringan
FROM python:3.9-slim

# Tetapkan direktori kerja di dalam container
WORKDIR /app

# Salin semua file proyek ke direktori kerja container
COPY . /app

# Install semua dependensi aplikasi
RUN pip install --no-cache-dir -r requirements.txt

# Ekspos port 5000 (port default Flask)
EXPOSE 5000

# Jalankan aplikasi
CMD ["python", "app.py"]
