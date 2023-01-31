import serial
import time
import matplotlib.pyplot as plt
import serial.tools.list_ports
import matplotlib.animation as animation

"""
DEPRECTAED IN FAVOR OF SERIAL STUDIO

This script is used to visualise data sent from the Teensy to the computer.
The data is sent in the following format:
    timestamp [group][label]:data [group][label]:data [group][label]:data
The data is then parsed and plotted in real-time.

The script will automatically search for the COM port of the Teensy.
If the Teensy is not found, the script will default to COM3.
"""

class subplot:
    def __init__(self, group, dataDicts, ln, ax):
        self.group = group
        self.dataDicts = dataDicts
        self.ln = ln
        self.ax = ax
    
#Search for the COM port of the Teensy
teensyPort = "COM4"
ports = list(serial.tools.list_ports.comports())
for p in ports: 
    if "Teensy" in p.description: 
        teensyPort = p.device
        break

print(f"Teensy found on port: {teensyPort}") 

# Set up serial communication with Teensy
ser = serial.Serial(teensyPort, 500000)

# Dictionary to store data
data_dict = {}

# Dictionary to store subplot information
plots = {}

def animate(i): #will be called in animation.FuncAnimation
    data = ser.readline().decode().strip().split(' ')
    print(data)
    for entry in data:
        group = entry.split('][')[0].strip('[')
        label_name = entry.split('][')[1].split(':')[0].strip(']') 
        label_data = entry.split(':')[1].strip(']')
        #check if label data can be converted to float
        try:
            label_data = float(label_data)
        except ValueError:
            continue

        plots[group].dataDicts[label_name].append(label_data)
        plots[group].ln.set_data([i for i in range(len(plots[group].dataDicts[label_name]))], plots[group].dataDicts[label_name])
        plots[group].ax.relim()
        plots[group].ax.autoscale_view()
        

data = ser.readline().decode().strip().split(' ')
for entry in data:
    group = entry.split('][')[0].strip('[')
    label_name = entry.split('][')[1].split(':')[0].strip(']') 
    label_data = entry.split(':')[1].strip(']')
    #check if label data can be converted to float
    try:
        label_data = float(label_data)
    except ValueError:
        continue

    #check if group exists in subplots
    if group not in plots:
        plots[group] = subplot(group, {label_name: [label_data]}, None, None)
    else:
        #check if label exists in subplots
        if label_name not in plots[group].dataDicts:
            plots[group].dataDicts[label_name] = [label_data]
        else:
            #update data
            plots[group].dataDicts[label_name].append(label_data)

fig, axs = plt.subplots(len(plots), 1)
for group in plots:
    for label in plots[group].dataDicts:
        #get index of group in plots
        index = list(plots.keys()).index(group)

        plots[group].ax = axs[index]
        plots[group].ax.legend()
        #create line for label
        plots[group].ln, = axs[index].plot(plots[group].dataDicts[label], label=label)

ani = animation.FuncAnimation(fig, animate, interval=100)
plt.show()

    
    
    