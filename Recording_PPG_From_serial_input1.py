import time
import json
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

name = "ppg"
age = 24
weight = 80
ppg = []

index = 0
data_length = 500

#PPG_Record = {"Name":"", "Age":"", "Weight":"", "PPG data": ""}

PPG_Record = {"Age":"", "PPG data": ""}

def animate(i, dataList, ser):
    ser.write(b'g')                                     # Transmit the char 'g' to receive the Arduino data point
    Data_string = ser.readline().decode('ascii')        # Decode receive Arduino data as a formatted string
    #print(i)                                           # 'i' is a incrementing variable based upon frames = x argument

    try:
        Data_float = float(Data_string)           # Convert to float
        dataList.append(Data_float)              # Add to the list holding the fixed number of points to animate
        ppg.append(Data_float)
        print(Data_float)

    except:                                             # Pass if data point is bad
        pass

    dataList = dataList[-50:]                           # Fix the list size so that the animation plot 'window' is x number of points

    if len(ppg) == data_length:
#        PPG_Record.update({"Name":name, "Age":age, "Weight":weight, "PPG data":ppg})
        PPG_Record.update({"Age":age, "PPG data":ppg})

        print(PPG_Record)
        # Save Json Record
        newfile = open("ppg.json", 'w')#after recording change the file extension to txt for the anlysis
        json.dump(PPG_Record, newfile)
        newfile.close()

        ser.close()

    ax.clear()                                          # Clear last data frame
    ax.plot(dataList)                                   # Plot new data frame

    ax.set_ylim([1600, 5000])                            # Set Y axis limit of plot
    ax.set_title("PPG Signal")                          # Set title of figure
    ax.set_ylabel("Value")                              # Set title of y axis

dataList = []                                           # Create empty list variable for later use

fig = Figure(figsize = (3, 3), dpi = 100)
#fig = plt.figure()
ax = fig.add_subplot(111)

ser = serial.Serial("COM4", 115200)                     # Establish Serial object with COM port and BAUD rate to match Arduino Port/rate
time.sleep(2)                                           # Time delay for Arduino Serial initialization
                                                        # Matplotlib Animation Fuction that takes takes care of real time plot.
                                                        # Note that 'fargs' parameter is where we pass in our dataList and Serial object.
ani = animation.FuncAnimation(fig, animate, frames=1000, fargs=(dataList, ser), interval=100)

plt.show()                                              # Keep Matplotlib plot persistent on screen until it is closed
#ser.close()                                            # Close Serial connection when plot is closed

# Open Json Record
# file = open("path", 'r')
# print(json.load(file))
