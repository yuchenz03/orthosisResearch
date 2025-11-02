# Bistable Orthosis Sensor Research

## Research Goals

This summer, I will be working in the Interactive Structures Lab at CMU's HCI Institute as a research assistant, mentored by Professor Alexandra Ion and Yuyu Lin. The project I will be working on continues research previously done on bistable orthoses for finger joints. Specifically, I will be working on adding sensors to the existing orthosis device and classifying collected data using machine learning models to gain information about the patient’s usage of the device and their recovery trajectory.

We will be collecting data via the use of conductive foam attached to the inner linings of the bistable orthosis brace. The two pieces of rehabilitation data we will be attempting to extract will be swelling of the joint and the amount of time the patient's brace is in either a flexible or stiff state.

## Data Folders

### prototype1data

This folder contains data from the first prototype of the orthotic brace containing sensors. This prototype had tiny clips on two adjacent corners of each of the four conductive foam pieces that measure resistance. Overall, this method didn't work very well - due to the fragility of the design, the wires and clips kept breaking or snapping during the process of collecting data. Furthermore, after further testing the conductive foam, we found that the readings were more sensitive when larger clips were used and hence had a larger area of contact with the foam.

### prototype2data

This folder contains data collected from the second prototype of the orthotic brace containing sensors. This prototype had two wires that "clipped" the sides of the foam to ensure a higher area of contact.

### prototype3data

This folder contains data collected from the third prototype of the orthotic brace containing sensors. The only difference bewteen prototype 2 and 3 is that non-conductive tape was added on the surface of the conductive foams to reduce noise data from occuring due to the skin being a conductive material that touches the wires instead of the foam.
For the first 96 readings, I recorded the switches with minimal movement when not switching. For the next 54 values, I recorded switches where after switching, I continued applying pressure in the same direction of the switch in readings where we recorded switching for varying amounts of time. This mimics movements such as grasping a large object or switching states in order to pinch a small object. During readings where there were supposed to be no switches, I recorded data where I pressed hard surfaces for varying amounts of time without switching states. This mimics movement such as pressing buttons or typing.

### prototype3databasic

The first 96 readings from prototype3data. Used for testing purposes.

# Files

### singleSensory.py

When an arduino board is attached to the laptop, this program reads the resistance from a single piece of conductive foam and outputs it into a graph. When the program is exited/ the plot window is closed, the final graph is saved as a PDF named "ResistancePlot.pdf". The data is smoothed using a moving average of 10 data values when there is a sufficient amount of data points.

### singleSensory.ino

Code to be run in the Arduino IDE after connecting the arduino board to format the data from one sensor properly. Returns the resistance of the foam in ohms, where each new reading is printed on a new line.

### fourSensory.py

When an arduino board is attached to the laptop, this program reads the resistance from four piece of conductive foam and outputs it into a graph. When the program is exited/ the plot window is closed, the final graph is saved as a PDF named "4ResistanceGraph.pdf". Each data point is smoothed using a moving average of 10 data values when there is a sufficient amount of data points.

### fourSensory.ino

Code to be run in the Arduino IDE after connecting the arduino board to format the data from four sensors properly. Returns the resistance of the foam in ohms, where the readings of four sensors are outputted on a single line in the order and format {A0},{A1},{A2},{A3} and next four readings are printed on a new line.

### datacollection.py

Code that takes in n seconds of serial data input then appends collected data into the datak.csv files, where k is the number of data points used to store the state switching. Values of k to be determined. Data is appended in the following format:
switchtype,sensor1data1,sensor1data2,...,sensor1datak,sensor2data1,...,sensor2datak,sensor3data1,...,sensor3datak,sensor4data1,sensor4datak
Each time the code is run, one new data point is generated (one new line in the csv file).

### classifyswitch.py

Uses data in some datak.csv (where k is a number) and uses it to train a random forest classifier. It then prints out the true and predicted values of each data point, and whether the prediction was correct or not.

### angularVel.ino

Arduino code that uses A1 and A4, which take in two values of Y-acceleration from two different GY-61 accelerometers, and computes the angular velocity in degrees/second, and the difference between those two angles.
