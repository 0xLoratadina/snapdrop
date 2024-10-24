import subprocess
import threading
import time

# Función para mostrar la salida en tiempo real de cada proceso
def stream_output(process, name):
    for line in iter(process.stdout.readline, b''):
        if line:
            print(f"[{name}] {line.decode().strip()}")

def start_pyro_naming_server():
    print("Iniciando el servidor de nombres de Pyro4...")
    naming_server_process = subprocess.Popen(['python', '-m', 'Pyro4.naming'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    time.sleep(3)  # Dar tiempo para que el servidor de nombres inicie correctamente
    return naming_server_process

def start_pyro_server():
    print("Iniciando el servidor Pyro4...")
    pyro_server_process = subprocess.Popen(['python', 'pyro_server.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return pyro_server_process

def start_flask_server():
    print("Iniciando el servidor Flask...")
    flask_server_process = subprocess.Popen(['python', 'server.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return flask_server_process

def main():
    try:
        # Iniciar el servidor de nombres de Pyro4
        naming_server_process = start_pyro_naming_server()

        # Iniciar el servidor Pyro4
        pyro_server_process = start_pyro_server()

        # Iniciar el servidor Flask
        flask_server_process = start_flask_server()

        print("Todos los servidores se han iniciado correctamente.")

        # Crear hilos para mostrar la salida de cada servidor
        threading.Thread(target=stream_output, args=(pyro_server_process, "Pyro4"), daemon=True).start()
        threading.Thread(target=stream_output, args=(flask_server_process, "Flask"), daemon=True).start()

        # Mantener los procesos corriendo
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\nDeteniendo servidores...")
        naming_server_process.terminate()
        pyro_server_process.terminate()
        flask_server_process.terminate()
        print("Servidores detenidos correctamente.")

if __name__ == '__main__':
    main()
