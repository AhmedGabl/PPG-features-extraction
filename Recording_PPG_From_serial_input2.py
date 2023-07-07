#record ppg signal 
import serial
import numpy as np

# Serial port settings
port = 'COM1'  # Replace with the appropriate serial port
baudrate = 9600
timeout = 1

# Open the serial port
ser = serial.Serial(port, baudrate, timeout=timeout)

# Read and process the serial data
buffer = ""
data = []
num_samples = 0

while True:
    # Read a line from the serial port
    line = ser.readline().decode().strip()

    # Check if the line contains valid data
    if line.startswith("PPG:"):
        try:
            # Extract the PPG value from the line
            ppg_value = float(line.split(":")[1])
            data.append(ppg_value)
            num_samples += 1
            buffer += line + "\n"

            # Check stability and validity every 100 samples
            if num_samples % 100 == 0:
                signal = np.array(data)

                # Check stability condition (e.g., standard deviation)
                if np.std(signal) < 0.1:
                    print("Signal is stable")

                # Check validity condition (e.g., range check)
                if np.all((signal >= 0)) :
                    print("Signal is valid")

        except (ValueError, IndexError):
            print("Invalid data")

    # Check if the line is an end signal
    elif line == "END":
        break

# Close the serial port
ser.close()

# Save the PPG signal as a text file
filename = "ppg.txt"
with open(filename, "w") as file:
    file.write(buffer)

print(f"PPG signal saved to {filename}")
