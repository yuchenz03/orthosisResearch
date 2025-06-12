import serial #pyserial library for port communication
import time
#python library for plotting graph
import matplotlib.pyplot as plt 
#python library for generating graph
from matplotlib.animation import FuncAnimation 

#linking to arduino
port = '/dev/cu.usbserial-10'  #arduino port
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
rawR = [] #raw data inputted from arduino
smoothedR = [] #smoothed data
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
    global startTime

    #ser.in_waiting gets the number of bytes in input buffer
    #if we get an input from the arduino board
    if ser.in_waiting:
        try:
            #ser.readline() gives binary code, so we decode using unicode 8bytes
            #edited to use ser.read to reduce latency between data and graph output
            line = ser.read(ser.in_waiting).decode('utf-8').strip()
            resistance = float(line)
            elapsed = time.time() - startTime

            times.append(elapsed)
            rawR.append(resistance)

            smooth = movingAverage(rawR, movingAvgNum)
            smoothedR.append(smooth)

            #clearing axes to resize according to time elapsed + data variance
            ax.clear()
            #uncomment for raw data
            #ax.plot(times, rawR, label='Raw Resistance', alpha=0.4)
            ax.plot(times, smoothedR, label='Smoothed Resistance', linewidth=2)

            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Resistance (ohms)")
            ax.set_title("Smoothed Conductive Foam Resistance Over Time")
            ax.legend(loc="upper right")

        except ValueError: #error handling for non-numeric arduino inputs
            pass
        

#setting up axes and plot
fig, ax = plt.subplots()
#refresh the plotted graph every 100 milliseconds using the update function
ani = FuncAnimation(fig, update, interval=100)
plt.tight_layout() #for layout 

#called when program is exiting
def on_close(event):
    print("Saving final graph as PDF...")
    #finalizing data to be saved in pdf
    ax.clear()
    ax.plot(times, smoothedR, label='Smoothed Resistance', color='blue')
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Resistance (ohms)")
    ax.set_title("Final Smoothed Resistance Plot")
    ax.legend()

    fig.savefig("ResistancePlot.pdf")
    print("Saved: ResistancePlot.pdf")
    ser.close() #closing serial port connection

#calls on_close when the matplotlib window is closed
fig.canvas.mpl_connect('close_event', on_close)

#opens matplotlib window
plt.show()