# Sistema de Gestión Bancaria Distribuida

Aplicación web para gestionar operaciones bancarias en un entorno de base de datos distribuida y heterogénea. Usa dos bases Oracle y una MongoDB con fragmentación horizontal por región y replicación mediante Kafka.

## Descripción

Este proyecto implementa una arquitectura distribuida heterogénea para simular un sistema bancario en múltiples regiones. Se compone de:

- **Nodo 1 (Región A)**: Oracle DB (datos de Región A)
- **Nodo 2 (Región B)**: Oracle DB (datos de Región B)
- **Nodo 3 (Nodo de Replicación)**: MongoDB

Los datos están fragmentados por región y se replican automáticamente al nodo MongoDB usando Apache Kafka.  
La aplicación web interactúa únicamente con el Nodo 1 y permite realizar operaciones CRUD sobre sucursales y préstamos, con replicación activa a MongoDB.

## Getting Started

### Pre-requisitos

* Tener instalado [Docker](https://www.docker.com/) y [Docker Compose](https://docs.docker.com/compose/)

### Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tuusuario/banco-distribuido.git
   cd banco-distribuido
    ```

2. Levanta todos los servicios:

   ```bash
   docker-compose up --build
   ```

3. En otra terminal, inicializa las bases Oracle (creación de tablas, triggers y datos iniciales) ejecutando:

   ```bash
   python oracle_init.py
   ```

   Este script se conecta a Oracle Región A y Región B y configura las tablas necesarias para sucursales, préstamos, etc., además de crear los triggers que activan la replicación con Kafka.

3. Accede a la aplicación en tu navegador:

   ```
   http://localhost:5000
   ```

Esto iniciará:

* Las bases Oracle para las regiones A y B
* El contenedor de MongoDB
* Kafka y Zookeeper
* La aplicación Flask conectada a Oracle Región A
* El producer y consumer Kafka que replica los datos en MongoDB

## Autores

* [Andrea Burciaga](https://github.com/andrea441)
* Luis Moncayo
* Alan Morales

## Licencia

Este proyecto está licenciado bajo la licencia MIT.
