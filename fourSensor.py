import serial #pyserial library for port communication
import time
#python library for plotting graph
import matplotlib.pyplot as plt 
#python library for generating graph
from matplotlib.animation import FuncAnimation 

#linking to arduino
port = '/dev/cu.usbserial-110'  #arduino port
baudRate = 9600 #number of signals to recieve per second
resistance = 20000.0 #fixed resistor resistance

#data is too noisy; using moving average to make data look smoother
movingAvgNum = 10 #number of points used to generate moving average

#opening serial port
ser = serial.Serial(port, baudRate) #open serial port
#allowing time for arduino to reset after port opened to prevent errors/ wrong data
time.sleep(2)


#initializing global variables
times = []
rawR = [[], [], [], []] #raw data inputted from arduino
smoothedR = [[], [], [], []] #smoothed data
startTime = time.time()

#function to generate smoothed data
#data: list of data points; 
#avgNum: number of data points to average from
def movingAverage(data, avgNum):
    if len(data) < avgNum:
        return sum(data) / len(data)
    else:
        return sum(data[-avgNum:]) / avgNum
    
    
#function to update the graph
#frame: int passed in by FuncAnimation that increments each time the animation
#updates.
def update(frame):
    #ser.in_waiting gets the number of bytes in input buffer
    #if we get an input from the arduino board
    if ser.in_waiting:
        try:
            line = ser.readline().decode('utf-8').strip()
            parts = line.split(",")
            if len(parts) != 4:
                return  #if data doesn't contain 4 readings then return

            #changing readings from strings to floats + storing in list
            readings = [float(p) for p in parts]
            elapsed = time.time() - startTime
            times.append(elapsed)

            #looping through 4 readings of resistance
            for i in range(4):
                rawR[i].append(readings[i])
                smooth = movingAverage(rawR[i], movingAvgNum)
                smoothedR[i].append(smooth)
                axs[i].clear()
                axs[i].plot(times, smoothedR[i], label=f'A{i}', color=f'C{i}')
                axs[i].set_ylabel("Resistance (ohms)")
                axs[i].legend(loc='upper right')

            axs[3].set_xlabel("Time (s)")
            fig.suptitle("Smoothed Conductive Foam Resistance Over Time from 4 Foam Sensors")

        except ValueError:
            pass

#setting up axes and plot
fig, axs = plt.subplots()
#refresh the plotted graph every 100 milliseconds using the update function
ani = FuncAnimation(fig, update, interval=100)
plt.tight_layout() #for layout 

#called when program is exiting
def on_close(event):
    print("Saving final plot to 4ResistanceGraph.pdf...")
    for i in range(4):
        axs[i].clear()
        axs[i].plot(times, smoothedR[i], label=f'Foam {i+1}', color=f'C{i}')
        axs[i].set_ylabel("Resistance (ohms)")
        axs[i].legend(loc='upper right')
    axs[3].set_xlabel("Time (s)")
    fig.suptitle("Final Smoothed Resistance Plot")
    fig.savefig("4ResistanceGraph.pdf")
    ser.close()
    print("Saved: 4ResistanceGraph.pdf")

fig.canvas.mpl_connect('close_event', on_close)
plt.show()
