# Bistable Orthosis Sensor Research
## Research Goals
This summer, I will be working in the Interactive Structures Lab at CMU's HCI Institute as a research assistant, mentored by Professor Alexandra Ion and Yuyu Lin. The project I will be working on continues research previously done on bistable orthoses for finger joints. Specifically, I will be working on adding sensors to the existing orthosis device and classifying collected data using machine learning models to gain information about the patient’s usage of the device and their recovery trajectory.

We will be collecting data via the use of conductive foam attached to the inner linings of the bistable orthosis brace. The two pieces of rehabilitation data we will be attempting to extract will be swelling of the joint and the amount of time the patient's brace is in either a flexible or stiff state.

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