FROM python:3.11-slim

WORKDIR /app

# Gerekli sistem paketleri (git, valgrind, derleme araçları ve make)
RUN apt-get update && apt-get install -y \
    git \
    valgrind \
    build-essential \
    make \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıklarını yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY bin/ /usr/local/bin/
RUN chmod +x /usr/local/bin/* || true
COPY . .

# API sunucusunu başlat
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]