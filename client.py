import socketio
import time
sio = socketio.Client(logger=True, engineio_logger=True)

@sio.event
def connect():
    print("Connected to the server!")
    # sio.emit('message', 'Hello, Server!')

@sio.event
def disconnect():
    print("Disconnected from the server.")

@sio.event
def response(data):
    print(f"Received response from server: {data}")

try:
    sio.connect("http://localhost:8000")
    sio.wait()
except socketio.exceptions.ConnectionError as e:
    print(f"Connection failed: {e}")

# input("Press Enter to disconnect...")


while not sio.sid:  
    time.sleep(0.1)

sid = sio.sid
print(f"SIO SID: {sid}")

import requests
response = requests.get(f'http://localhost:5000/client_message/{sid}')
print("Client message API response:", response.json())