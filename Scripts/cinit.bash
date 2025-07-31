#!/bin/bash

# Actualiza paquetes e instala Docker desde repositorio de Ubuntu
sudo apt update -y
sudo apt install -y docker.io

# Habilita y arranca el servicio Docker
sudo systemctl enable docker
sudo systemctl start docker

# Permite al usuario ubuntu usar docker sin sudo
sudo usermod -aG docker ubuntu

# Espera que Docker esté completamente listo
sleep 5

# Ejecuta el contenedor con política de reinicio
docker run -d -p 8080:80 --restart unless-stopped bayronj/rayclientvf:latest
