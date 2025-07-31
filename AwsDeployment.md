# Despliegue de Arquitectura AWS con Cliente, Load Balancer y Clúster Privado

Este documento describe los pasos necesarios para implementar una arquitectura distribuida en AWS con una separación clara entre los servicios /api, /client, /workers.

---

## 🧱 Estructura General

- **VPC** con dos subredes:
  - Subred Pública (para Cliente y Load Balancer)
  - Subred Privada (para Head Node y Workers)
- **Application Load Balancer (ALB)** para enrutar tráfico externo al nodo principal (Head).
- **Elastic IP** para acceso fijo desde el exterior.
- **Instancias EC2** para Cliente, Head Node y Workers.

---

## 🛠️ Pasos para Implementar

### 1. Crear VPC y Subredes
- Crear una **VPC personalizada**.
- Crear **una subred pública** y **una subred privada** en la misma región (por ejemplo, `us-east-1a`).
- Activar `Auto-assign public IPv4` en la subred pública.

### 2. Crear Internet Gateway
- Crear un **Internet Gateway** y asociarlo a la VPC.
- Editar la **tabla de rutas** de la subred pública para enrutar tráfico `0.0.0.0/0` hacia el Internet Gateway.

### 3. Lanzar Instancias EC2
- **Cliente**:
  - En la subred pública.
  - Asignar una **Elastic IP**.
- **Head Node**:
  - En la subred privada.
  - Sin IP pública.
- **Workers**:
  - En la subred privada.
  - Sin IP pública.
- Asignar roles IAM y claves SSH según necesidad.

### 4. Configurar Elastic IP
- Asociar la **Elastic IP** al Cliente.

### 5. Configurar Application Load Balancer (ALB)
- Crear un **ALB**:
  - Escoger la VPC creada.
  - Asociarlo a la subred pública.
- Crear un **Target Group** para el Head Node.
- Configurar un **Listener HTTP/HTTPS** para enrutar solicitudes hacia el target group.

### 6. Configurar Grupos de Seguridad
- **Cliente**: permitir SSH (`puerto 22`) desde tu IP.
- **ALB**: permitir tráfico HTTP/HTTPS (`puertos 80/443`) desde Internet.
- **Head Node**: permitir tráfico solo desde el ALB.
- **Workers**: permitir tráfico solo desde el Head Node (por ejemplo, puertos personalizados para RPC/comunicación interna).

---

## 📌 Notas

- la arquitectura puede ser mejorada lanzando mas intancias de tipo y api, añadiendolas al grupo de destino del ALB 