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
docker run -d \
  --name ray_head \
  -p 6379:6379 \          # Puerto principal de Ray
  -p 8265:8265 \          # Dashboard de Ray (opcional)
  -p 10001:10001 \        # Puerto para objetos (object store)
  -p 5000:5000 \          # Puerto para api (object store)
  rayproject/ray


