from flask import Flask, request, jsonify, render_template, redirect, url_for, send_file
import os
import zipfile
import io
import user_agents
import socket
import Pyro4

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Conectar con el servidor Pyro
room_manager = Pyro4.Proxy("PYRONAME:room.manager")

# Obtener el tipo de dispositivo
def get_device_type(user_agent_string):
    ua = user_agents.parse(user_agent_string)
    if ua.is_mobile:
        return 'mobile'
    elif ua.is_tablet:
        return 'tablet'
    elif ua.is_pc:
        return 'desktop'
    else:
        return 'laptop'

# Obtener el nombre del dispositivo según la IP
def get_device_name(ip_address):
    try:
        return socket.gethostbyaddr(ip_address)[0]
    except socket.herror:
        return "Unknown Device"

# Página principal
@app.route('/')
def home():
    return render_template('index.html')

# Crear sala
@app.route('/create_room', methods=['POST'])
def create_room():
    owner_ip = request.remote_addr
    pin = room_manager.create_room(owner_ip)
    return jsonify({"pin": pin, "redirect_url": url_for('room_page', pin=pin)})

# Página de la sala
@app.route('/room/<int:pin>')
def room_page(pin):
    room_data = room_manager.get_room_data(pin)
    if 'error' in room_data:
        return "Sala no encontrada", 404
    return render_template('room.html', pin=pin, clients=room_data['clients'], files=room_data['files'], is_owner=(request.remote_addr == room_data['owner']))

# Unirse a sala
@app.route('/join_room', methods=['POST'])
def join_room():
    pin = int(request.json.get('pin'))
    user_agent = request.headers.get('User-Agent')
    device_type = get_device_type(user_agent)
    device_name = get_device_name(request.remote_addr)
    result = room_manager.join_room(pin, request.remote_addr, device_type, device_name)
    
    if result['status'] == 'success':
        return jsonify({"status": "success", "redirect_url": url_for('room_page', pin=pin)})
    else:
        return jsonify({"status": "error", "message": result['message']}), 404

# Subir archivo
@app.route('/upload_file/<int:pin>', methods=['POST'])
def upload_file(pin):
    room_data = room_manager.get_room_data(pin)
    if 'error' in room_data:
        return "Sala no encontrada", 404
    if request.remote_addr != room_data['owner']:
        return "No tienes permiso para subir archivos en esta sala.", 403
    if 'file' not in request.files:
        return "No hay archivo para subir.", 400
    file = request.files['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    room_manager.add_file(pin, file.filename)
    return redirect(url_for('room_page', pin=pin))

# Descargar archivo
@app.route('/download_file/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        zip_io = io.BytesIO()
        with zipfile.ZipFile(zip_io, mode='w', compression=zipfile.ZIP_DEFLATED) as temp_zip:
            temp_zip.write(file_path, arcname=filename)
        zip_io.seek(0)
        return send_file(zip_io, mimetype='application/zip', as_attachment=True, download_name=f'{filename}.zip')
    return "Archivo no encontrado", 404

# Obtener datos de la sala
@app.route('/get_room_data/<int:pin>', methods=['GET'])
def get_room_data(pin):
    room_data = room_manager.get_room_data(pin)
    return jsonify(room_data)

# Cerrar sala
@app.route('/close_room/<int:pin>', methods=['POST'])
def close_room(pin):
    room_data = room_manager.get_room_data(pin)
    if 'error' in room_data:
        return jsonify({"status": "error", "message": "Sala no encontrada"}), 404
    if request.remote_addr != room_data['owner']:
        return jsonify({"status": "error", "message": "No tienes permiso para cerrar esta sala"}), 403
    result = room_manager.close_room(pin)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)
