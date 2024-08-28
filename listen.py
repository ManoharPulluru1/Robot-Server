import socketio
import time
import RPi.GPIO as GPIO

# GPIO Setup
GPIO.setmode(GPIO.BOARD)  # Use BOARD numbering scheme
GPIO.cleanup()  # Clean up any previous configurations

# Define GPIO pins for forward and backward movement
Forward = 26
Backward = 20

# Setup GPIO pins
GPIO.setup(Forward, GPIO.OUT)
GPIO.setup(Backward, GPIO.OUT)

# Define functions for starting and stopping movement
def start_forward():
    GPIO.output(Forward, GPIO.HIGH)
    print("Moving Forward")

def stop_forward():
    GPIO.output(Forward, GPIO.LOW)
    print("Stopped Moving Forward")

def start_reverse():
    GPIO.output(Backward, GPIO.HIGH)
    print("Moving Backward")

def stop_reverse():
    GPIO.output(Backward, GPIO.LOW)
    print("Stopped Moving Backward")

# Socket.IO client setup
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to the server")

@sio.event
def disconnect():
    print("Disconnected from the server")

@sio.event
def reconnect():
    print("Reconnected to the server")

# Handle press events
@sio.on("press_new")
def press_new(data):
    temp_press = data['direction1']
    print(temp_press)
    if temp_press == 'top':
        start_forward()  # Start moving forward continuously
    elif temp_press == 'bottom':
        start_reverse()  # Start moving backward continuously
    print("temp_press:", temp_press)

# Handle release events
@sio.on("release_new")
def release_new(data):
    temp_release = data['direction1']
    print(temp_release)
    if temp_release == 'top':
        stop_forward()  # Stop moving forward
    elif temp_release == 'bottom':
        stop_reverse()  # Stop moving backward
    print("temp_release:", temp_release)

# Connect to the server
server_url = 'http://localhost:4000'
print(f"Connecting to {server_url}...")
sio.connect(server_url)

print("Listening for events...")
try:
    sio.wait()
except KeyboardInterrupt:
    print("Script interrupted by user")
    sio.disconnect()
    # GPIO.cleanup()  # Clean up GPIO on exit
