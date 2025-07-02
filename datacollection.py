import csv
import serial # pyserial library for port communication
import time

# linking to arduino
port = '/dev/cu.usbserial-10'  # arduino port
baudRate = 9600 # number of signals to recieve per second
resistance = 20000.0 # fixed resistor resistance
numSensors = 4 # number of sensors to use

# initializing global variables
times = []
rawR = [[], [], [], []] # raw data inputted from arduino
# ranging from 3 to 8 seconds of data collected, incrementing per 0.5
dataWindows = [60,70,80,90,100,110,120,130,140,150,160] 

# looping func to generate data
def recieveData():
    global times, rawR
    times = []
    rawR = [[], [], [], []]
    print("Starting data collection...")
    
    # ser.in_waiting gets the number of bytes in input buffer
    # if we get an input from the arduino board
    # uncomment to allow time for calibration when first putting on brace
    # print("Calibrating sensors... (0/4)")
    # time.sleep(15)
    # print("Calibrating sensors... (1/4)")
    # time.sleep(15)
    # print("Calibrating sensors... (2/4)")
    # time.sleep(15)
    print("Calibrating sensors... ")
    time.sleep(10)
    print("Switch in 5 seconds")
    time.sleep(1)
    print("4 seconds")
    time.sleep(1)
    print("3 seconds")
    time.sleep(1)
    # checking that the amount of elapsed time is accurate
    # assert(time.time() - startTime < 61 and time.time() - startTime > 59)
    
    # opening serial port
    ser = serial.Serial(port, baudRate) # open serial port
    # allowing time for arduino to reset after port opened to prevent errors/ wrong data
    print("2 seconds")
    time.sleep(1)
    print("1 seconds")
    time.sleep(1)
    
    print("Switch now!")
    startTime = time.time()
    # add 60 seconds onto time on right if calibration wanted
    while (time.time() - startTime) <= (dataWindows[-1]//20):
        if ser.in_waiting:
            try:
                line = ser.read(ser.in_waiting).decode('utf-8').strip()
                fourreadings = line.split("\r\n")
                for reading in fourreadings:
                    parts = reading.split(",")
                    
                    # handles the case where input 4's decimal place doesn't
                    # come in the same line as other values.
                    if "." not in parts[3]: 
                        while not ser.in_waiting:
                            pass
                        decimalpoint = ser.read(ser.in_waiting).decode('utf-8').strip()
                        parts[3] = parts[3]+decimalpoint
                        
                elapsed = time.time() - startTime
                times.append(elapsed)
 
                # looping through 4 readings of resistance to store raw values
                for i in range(4):
                    rawR[i].append(parts[i])
            except ValueError:
                print("ValueError - check arduino output format")
                return
    print("Completed data collection.")
    ser.close()
    

def main():
    again = True
    while again == True:
        typeslist = [0,1,2,0,2,1]
        for i in range(len(typeslist)):
            if typeslist[i] == 0:
                print("stiff to flexible")
            elif typeslist[i] == 1:
                print("flexible to stiff")
            elif typeslist[i] == 2:
                print("none")
            recieveData()
            # switchtype = input("0: stiff->flexible, 1: flexible->stiff, 2: none >> ")
            switchtype = typeslist[i]
            for i in range(len(dataWindows)):
                finalData = [switchtype] #1D array of data points
                for j in range(numSensors):
                    # 20 data points per second, take following n seconds
                    finalData += rawR[j][:dataWindows[i]]
                filename = 'prototype3data/data'+str(dataWindows[i])+'.csv'
                with open(filename, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(finalData)
        againin = input("again? y or enter for yes >>")
        if againin != "y" and againin != "Y" and againin != "":
            again = False

main()