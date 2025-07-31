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
docker run -d -it \
  --name ray-worker \
  --network host \
  --restart unless-stopped \
  bayronj/raywork:latest

# Conecta el worker al head de Ray
docker exec -it ray-worker bash -c "ray start --address=10.0.142.121:6379 && tail -f /dev/null"
