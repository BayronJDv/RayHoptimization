#!/bin/bash

# Actualiza paquetes e instala Docker desde repositorio de Ubuntu
sudo apt update -y
sudo apt install -y docker.io

# Habilita y arranca el servicio Docker
sudo systemctl enable docker
sudo systemctl start docker

# (Opcional) Permite al usuario ubuntu usar docker sin sudo
sudo usermod -aG docker ubuntu

# Espera que Docker esté completamente listo
sleep 5

# Ejecuta el contenedor con la variable de entorno
docker run -d -p 8080:80 \
  -e API_URL="https://api.tu-produccion.com" \
  tu-imagen-react:ports

#reemplazar la imagen segun sea el caso 
# client = bayronj/rayclientv4:latest
# api = bayronj/rayapi:latest
# worker = bayronj/rayworker:latest
