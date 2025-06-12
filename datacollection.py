import serial #pyserial library for port communication
import time

#linking to arduino
port = '/dev/cu.usbserial-10'  #arduino port
baudRate = 9600 #number of signals to recieve per second
resistance = 20000.0 #fixed resistor resistance

#data is too noisy; using moving average to make data look smoother
movingAvgNum = 10 #number of points used to generate moving average
dataWindow = 4000

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
    

#looping func to generate data
def updateData():
    #ser.in_waiting gets the number of bytes in input buffer
    #if we get an input from the arduino board
    if ser.in_waiting:
        try:
            line = ser.read(ser.in_waiting).decode('utf-8').strip()
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
        except ValueError:
            pass
