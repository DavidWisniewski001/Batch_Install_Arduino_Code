import tkinter as tk
from tkinter import filedialog
import subprocess
import serial
import time

# Define the serial port and baud rate
serial_port = '/dev/ttyUSB0'  # Change this to your serial port
baud_rate = 9600  # Change this to match your microcontroller's baud rate

# Function to upload code using PlatformIO
def upload_code(code_path, board='arduino'):
    # Run PlatformIO command to upload the code
    cmd = f'platformio run --target upload --environment {board}'
    subprocess.run(cmd, shell=True)

# Function to communicate with the microcontroller
def communicate_with_microcontroller():
    try:
        # Open the serial port
        ser = serial.Serial(serial_port, baud_rate, timeout=1)
        status_label.config(text=f'Serial port {serial_port} opened successfully.')
        
        # Wait for the microcontroller to initialize
        time.sleep(2)

        # Send a message to the microcontroller
        message = "Hello, microcontroller!"
        ser.write(message.encode())

        # Read response from the microcontroller
        response = ser.readline().decode().strip()
        status_label.config(text=f'Response from microcontroller: {response}')

        # Close the serial port
        ser.close()
        status_label.config(text='Serial port closed.')

    except serial.SerialException as e:
        status_label.config(text=f'Error opening serial port: {e}')

# Function to handle button click for uploading code
def upload_code_click():
    code_path = filedialog.askdirectory()
    if code_path:
        upload_code(code_path)
        status_label.config(text='Arduino code uploaded successfully.')

# Create the GUI window
window = tk.Tk()
window.title("Arduino Code Uploader")

# Create and place the upload button
upload_button = tk.Button(window, text="Upload Arduino Code", command=upload_code_click)
upload_button.pack(pady=10)

# Create a label for status messages
status_label = tk.Label(window, text="")
status_label.pack()

# Create and place the communicate button
communicate_button = tk.Button(window, text="Communicate with Microcontroller", command=communicate_with_microcontroller)
communicate_button.pack(pady=10)

# Run the GUI main loop
window.mainloop()