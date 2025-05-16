import tkinter as tk
import serial
import threading

# Change this to your serial port name
# On Windows, it might be like 'COM3'
# On Linux/Mac, it might be like '/dev/ttyUSB0'
SERIAL_PORT = 'COM3'  
BAUD_RATE = 9600      # Common baud rate for USB serial devices, adjust if needed

card_id = ""

def read_from_serial():
    global card_id
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            while True:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    card_id = line
                    # Update label in main thread
                    root.after(0, lambda: label.config(text=f"Card ID: {card_id}"))
    except serial.SerialException as e:
        root.after(0, lambda: label.config(text=f"Serial error: {e}"))

root = tk.Tk()
root.title("Wave ID Card Reader")

label = tk.Label(root, text="Waiting for card scan...", font=("Arial", 24))
label.pack(padx=20, pady=20)

# Run the serial reading in a separate thread to not block the GUI
thread = threading.Thread(target=read_from_serial, daemon=True)
thread.start()

root.mainloop()
