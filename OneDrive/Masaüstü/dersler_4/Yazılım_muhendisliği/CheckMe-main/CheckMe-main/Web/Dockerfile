FROM node:20-alpine

WORKDIR /app

# Bağımlılık yönetimi için sadece package.json kopyala
COPY package*.json ./

# Bağımlılıkları yükle
RUN npm install

# Geri kalan her şeyi kopyala
COPY . .

EXPOSE 3000

# Next.js'i development modunda başlat
CMD ["npm", "run", "dev"]