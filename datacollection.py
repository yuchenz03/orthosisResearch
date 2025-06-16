import csv
import serial #pyserial library for port communication
import time

#linking to arduino
port = '/dev/cu.usbserial-10'  #arduino port
baudRate = 9600 #number of signals to recieve per second
resistance = 20000.0 #fixed resistor resistance
numSensors = 4 #number of sensors to use

#initializing global variables
times = []
rawR = [[], [], [], []] #raw data inputted from arduino
#ranging from 3 to 8 seconds of data collected, incrementing per 0.5
dataWindows = [60,70,80,90,100,110,120,130,140,150,160] 
startTime = time.time()

#looping func to generate data
def recieveData():
    print("Starting data collection...")
    #ser.in_waiting gets the number of bytes in input buffer
    #if we get an input from the arduino board
    # print("Calibrating sensors... (0/4)")
    # time.sleep(15)
    # print("Calibrating sensors... (1/4)")
    # time.sleep(15)
    # print("Calibrating sensors... (2/4)")
    # time.sleep(15)
    # print("Calibrating sensors... (3/4)")
    # time.sleep(10)
    # print("Switch in 5 seconds")
    # time.sleep(1)
    # print("4 seconds")
    # time.sleep(1)
    # print("3 seconds")
    # time.sleep(1)
    # print("2 seconds")
    # time.sleep(1)
    # print("1 seconds")
    # time.sleep(1)
    #checking that the amount of elapsed time is accurate
    # assert(time.time() - startTime < 61 and time.time() - startTime > 59)
    
    #opening serial port
    ser = serial.Serial(port, baudRate) #open serial port
    #allowing time for arduino to reset after port opened to prevent errors/ wrong data
    time.sleep(2)
    
    print("Switch now!")
    readings = []
    while (time.time() - startTime) <= 60 + (dataWindows[-1]//20):
        if ser.in_waiting:
            try:
                line = ser.read(ser.in_waiting).decode('utf-8').strip()
                fourreadings = line.split("\r\n")
                for reading in fourreadings:
                    parts = reading.split(",")
                    assert(len(parts) == 4)
                    readings += parts
                print(readings)
                #changing readings from strings to floats + storing in list
                elapsed = time.time() - startTime
                times.append(elapsed)

                #looping through 4 readings of resistance
                for i in range(4):
                    rawR[i].append(readings[i])
            except ValueError:
                print("ValueError - check arduino output format")
                return
    print("Completed data collection.")
    

def main():
    recieveData()
    switchtype = input("0: stiff->flexible, 1: flexible->stiff, 2: none >> ")
    
    for i in range(len(dataWindows)):
        finalData = [dataWindows[i], switchtype] #1D array of data points
        for j in range(numSensors):
            #20 data points per second, take following n seconds
            finalData += rawR[j][:dataWindows[i]]
        filename = 'data'+str(dataWindows[i])+'.csv'
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(finalData)

main()
'''
probably best way to do this is by setting first value as 0 or something in the
middle such that the min value would never fall below zero, then compare the 
fluctuations?? basically normalize the values before doing anything

something from lab meeting this morning: could measure the absolute change from the
baseline and the baseline exponentially decaying avergae

note to self for tmr: ur gonna have to change the way that you wait - you need to 
still collect data otherwise ur gonna get the multiple inputs thing again
'''