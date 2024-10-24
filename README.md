# SnapDrop

Este proyecto implementa una plataforma simple para compartir archivos. Permite a los usuarios crear y unirse a salas donde se pueden cargar y compartir archivos entre dispositivos conectados. El proyecto utiliza Pyro4 para la gestión de salas y Flask para la interfaz web.

## Estructura del Proyecto

- `index.html` - La página principal donde los usuarios pueden crear o unirse a salas proporcionando un PIN.
- `room.html` - La página de la sala que muestra los archivos subidos y los clientes conectados. También permite la carga de archivos por parte del propietario de la sala.
- `pyro_server.py` - Gestiona las salas, clientes y archivos utilizando Pyro4.
- `server.py` - Un servidor Flask que interactúa con el servidor Pyro4 para gestionar la interfaz web, permitiendo crear/unirse a salas y manejar la carga/descarga de archivos.
- `start_servers.py` - Un script que inicia tanto el servidor de nombres Pyro4 como el servidor Flask en hilos separados.

## Características Principales

1. **Gestión de Salas**: Los usuarios pueden crear salas, las cuales generan un PIN único que otros usuarios pueden utilizar para unirse a la sala.
2. **Carga/Descarga de Archivos**: Los propietarios de las salas pueden subir archivos, y todos los clientes conectados pueden descargarlos.
3. **Conexión de Clientes**: Los clientes son identificados por el tipo de dispositivo (móvil, tableta, escritorio) y su dirección IP.
4. **Actualización en Tiempo Real**: La página de la sala se actualiza automáticamente para mostrar archivos recién subidos y nuevos clientes conectados.
5. **Cierre de Salas**: El propietario de la sala puede cerrar la sala, lo que elimina todos los archivos y desconecta a todos los clientes.

## Instalación

1. Clona el repositorio:

    ```bash
    git clone https://github.com/DrBabaBoy/snapdrop.git
    cd snapdrop-clone
    ```

2. Instala las dependencias necesarias:

    ```bash
    pip install -r requirements.txt
    ```

    El archivo `requirements.txt` debería incluir:
    - Flask
    - Pyro4
    - user-agents

3. Configura la estructura del directorio del proyecto:

    ```bash
    mkdir uploads
    ```

4. Inicia los servidores:

    ```bash
    python start_servers.py
    ```

    Esto iniciará:
    - El servidor de nombres Pyro4
    - El servidor de gestión de salas Pyro4
    - El servidor web Flask

5. Accede a la interfaz web visitando `http://localhost:5000`.

## Cómo Funciona

### 1. Crear una Sala

Los usuarios pueden crear una sala haciendo clic en el botón "Crear Sala" en la página principal. Se generará un PIN para la sala, y el usuario será redirigido a la página de la sala donde podrá cargar archivos.

### 2. Unirse a una Sala

Otros usuarios pueden unirse a una sala ingresando el PIN de la sala en la página principal. Una vez dentro, podrán ver la lista de clientes conectados y los archivos disponibles para descargar.

### 3. Subida de Archivos

Solo el propietario de la sala puede subir archivos. Estos archivos serán visibles para todos los demás clientes conectados en la sala, y se podrán descargar haciendo clic en el botón "Descargar" junto a cada archivo.

### 4. Actualizaciones en Tiempo Real

La página de la sala se actualiza automáticamente cada 5 segundos para mostrar los nuevos clientes conectados y archivos subidos.

### 5. Cierre de la Sala

El propietario de la sala puede cerrarla, lo que eliminará todos los archivos y desconectará a todos los clientes.

## Contribuir

Si deseas contribuir a este proyecto, no dudes en enviar issues o pull requests.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT.
