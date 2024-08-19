import os
import json
import socket
import threading
import fcntl
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

# Set the path for config.json in a separate config directory
CONFIG_DIR = "/config"
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

# Ensure the config directory exists
os.makedirs(CONFIG_DIR, exist_ok=True)

current_pc = None  # Track the currently selected PC
config_lock = threading.Lock()  # Lock for thread-safe config access

# Load configuration from the config file
def load_config():
    with config_lock:
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return None
        return None

# Save configuration to the config file and reload it
def save_config(config):
    try:
        with open(CONFIG_FILE, 'w') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            json.dump(config, f, indent=4)
            fcntl.flock(f, fcntl.LOCK_UN)
        reload_config()
    except Exception as e:
        raise e

# Reload the configuration from the file
def reload_config():
    global config
    config = load_config()

# Reload config before each request to ensure consistency across workers
@app.before_request
def before_request():
    global config
    config = load_config()

# Load initial configuration
config = load_config()

# Route for the home page
@app.route('/')
def index():
    if config is None:
        return redirect(url_for('configure'))
    return render_template('index.html', current_pc=current_pc)

# Route for the configuration page
@app.route('/configure', methods=['GET', 'POST'])
def configure():
    if request.method == 'POST':
        kvm_ip = request.form['kvm_ip']
        kvm_port = int(request.form['kvm_port'])
        new_config = {
            "KVM_IP": kvm_ip,
            "KVM_PORT": kvm_port
        }
        save_config(new_config)
        return redirect(url_for('index'))
    return render_template('configure.html')

# Route to handle switching PCs
@app.route('/switch', methods=['POST'])
def switch_pc():
    global current_pc
    if config is None:
        return jsonify({"message": "Configuration not set."}), 500
    
    pc_number = request.json.get('pc_number')
    command = get_command_for_pc(pc_number)
    
    if command:
        retries = 3
        while retries > 0:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(20)  # Set a longer timeout
                    s.connect((config['KVM_IP'], config['KVM_PORT']))
                    s.sendall(command)
                current_pc = pc_number
                return jsonify({"message": f"Switched to PC{pc_number}"})
            except socket.timeout:
                retries -= 1
                if retries == 0:
                    return jsonify({"message": "Failed to switch to PC due to timeout."}), 500
                time.sleep(2)  # Wait before retrying
            except Exception as e:
                return jsonify({"message": f"Failed to switch to PC{pc_number}: {str(e)}"}), 500
    else:
        return jsonify({"message": "Invalid PC number"}), 400

# Function to get the command bytes for each PC
def get_command_for_pc(pc_number):
    commands = {
        1: [0xAA, 0xBB, 0x03, 0x01, 0x01, 0xEE],
        2: [0xAA, 0xBB, 0x03, 0x01, 0x02, 0xEE],
        3: [0xAA, 0xBB, 0x03, 0x01, 0x03, 0xEE],
        4: [0xAA, 0xBB, 0x03, 0x01, 0x04, 0xEE],
        5: [0xAA, 0xBB, 0x03, 0x01, 0x05, 0xEE],
        6: [0xAA, 0xBB, 0x03, 0x01, 0x06, 0xEE],
        7: [0xAA, 0xBB, 0x03, 0x01, 0x07, 0xEE],
        8: [0xAA, 0xBB, 0x03, 0x01, 0x08, 0xEE],
    }
    return bytes(commands.get(pc_number, []))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090, debug=False)

