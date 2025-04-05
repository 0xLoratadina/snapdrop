# SnapDrop

This project implements a simple file-sharing platform. It allows users to create and join rooms where files can be uploaded and shared between connected devices. The project uses Pyro4 for room management and Flask for the web interface.

## Project Structure

- `index.html` – The main page where users can create or join rooms by entering a PIN.
- `room.html` – The room page that displays uploaded files and connected clients. It also allows the room owner to upload files.
- `pyro_server.py` – Manages rooms, clients, and files using Pyro4.
- `server.py` – A Flask server that interacts with the Pyro4 server to manage the web interface, allowing room creation/joining and handling file uploads/downloads.
- `start_servers.py` – A script that starts both the Pyro4 name server and the Flask server in separate threads.

## Key Features

1. **Room Management**: Users can create rooms, which generate a unique PIN that other users can use to join.
2. **File Upload/Download**: Room owners can upload files, and all connected clients can download them.
3. **Client Connection**: Clients are identified by device type (mobile, tablet, desktop) and IP address.
4. **Real-Time Updates**: The room page automatically refreshes to show newly uploaded files and newly connected clients.
5. **Room Closure**: The room owner can close the room, which deletes all files and disconnects all clients.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/DrBabaBoy/snapdrop.git
    cd snapdrop-clone
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    The `requirements.txt` file should include:
    - Flask
    - Pyro4
    - user-agents

3. Set up the project directory structure:

    ```bash
    mkdir uploads
    ```

4. Start the servers:

    ```bash
    python start_servers.py
    ```

    This will start:
    - The Pyro4 name server
    - The Pyro4 room management server
    - The Flask web server

5. Access the web interface by visiting `http://localhost:5000`.

## How It Works

### 1. Creating a Room

Users can create a room by clicking the "Create Room" button on the main page. A PIN will be generated for the room, and the user will be redirected to the room page where files can be uploaded.

### 2. Joining a Room

Other users can join a room by entering the room's PIN on the main page. Once inside, they can see the list of connected clients and the files available for download.

### 3. File Upload

Only the room owner can upload files. These files will be visible to all other connected clients in the room and can be downloaded by clicking the "Download" button next to each file.

### 4. Real-Time Updates

The room page refreshes automatically every 5 seconds to display new connected clients and uploaded files.

### 5. Closing the Room

The room owner can close the room, which deletes all files and disconnects all clients.

## Contributing

If you'd like to contribute to this project, feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License.
