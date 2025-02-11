import Pyro4
import random

@Pyro4.expose
class RoomManager:
    def __init__(self):
        self.active_rooms = {}
        self.connected_clients = {}

    def create_room(self, owner_ip):
        pin = random.randint(10000, 99999)
        self.active_rooms[pin] = {"owner": owner_ip, "files": [], "clients": []}
        print(f"Sala {pin} creada por {owner_ip}")
        return pin

    def join_room(self, pin, ip, device_type, device_name):
        if pin in self.active_rooms:
            client = {"ip": ip, "device": device_type, "name": device_name}
            self.active_rooms[pin]["clients"].append(client)
            self.connected_clients[ip] = client
            print(f"{device_name} ({ip}) se unió a la sala {pin}")
            return {"status": "success", "message": "Unido correctamente"}
        else:
            return {"status": "error", "message": "Sala no encontrada"}

    def add_file(self, pin, filename):
        if pin in self.active_rooms:
            self.active_rooms[pin]["files"].append(filename)
            print(f"Archivo {filename} añadido a la sala {pin}")
        else:
            print(f"Sala {pin} no encontrada al intentar añadir archivo.")

    def get_room_data(self, pin):
        if pin in self.active_rooms:
            return {
                "files": self.active_rooms[pin]["files"],
                "clients": self.active_rooms[pin]["clients"],
                "owner": self.active_rooms[pin]["owner"]
            }
        else:
            return {"error": "Sala no encontrada"}

    def close_room(self, pin):
        if pin in self.active_rooms:
            del self.active_rooms[pin]
            print(f"Sala {pin} cerrada")
            return {"status": "success", "message": f"Sala {pin} cerrada correctamente"}
        else:
            return {"status": "error", "message": "Sala no encontrada"}

def main():
    daemon = Pyro4.Daemon()  
    ns = Pyro4.locateNS()  
    uri = daemon.register(RoomManager)  
    ns.register("room.manager", uri)   
    print("Servidor Pyro RoomManager iniciado.")
    daemon.requestLoop()

if __name__ == '__main__':
    main()
