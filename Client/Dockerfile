# Etapa 1: Build con Node
FROM node:18 AS builder

WORKDIR /app
COPY . .
RUN npm install
RUN npm run build

# Etapa 2: Servir con Nginx
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

# Construir la imagen:
# docker build -t bayronj/rayclient .
#comando para correr la imagen
#   docker run -d -p 8080:80 \
#   bayronj/rayclientv5