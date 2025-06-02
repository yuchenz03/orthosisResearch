# Bistable Orthosis Sensor Research
## Research Goals
This summer, I will be working in the Interactive Structures Lab at CMU's HCI Institute as a research assistant, mentored by Professor Alexandra Ion and Yuyu Lin. The project I will be working on continues research previously done on bistable orthoses for finger joints. Specifically, I will be working on adding sensors to the existing orthosis device and classifying collected data using machine learning models to gain information about the patient’s usage of the device and their recovery trajectory.

We will be collecting data via the use of conductive foam attached to the inner linings of the bistable orthosis brace. The two pieces of rehabilitation data we will be attempting to extract will be swelling of the joint and the amount of time the patient's brace is in either a flexible or stiff state.

# Files
### singleSensory.py
When an arduino board is attached to the laptop, this program reads the resistance from a single piece of conductive foam and outputs it into a graph. When the program is exited/ the plot window is closed, the final graph is saved as a PDF named "ResistancePlot.pdf". 
