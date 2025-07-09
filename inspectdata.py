import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# change this depending on what file is being used
filepath = "prototype3data/data120.csv"
numpoints = 120  # number of readings per sensor
delay = 50       # from Arduino, 50ms delay between readings (for plotting)
numsensors = 4
switchtypes_list = [0, 1, 2]

rowrangetoplot = (0,150)  # specify row range to plot (inclusive)

df = pd.read_csv(filepath, header=None)
switchtypes = df.iloc[:, 0].astype(int)
data = df.iloc[:, 1:]

# configuring x-axis so that it shows seconds on the bottom line
tickpos = list(range(1, 7))
ticklabels = [str(t) for t in tickpos]

# plotting the 4 axes:
fig, axes = plt.subplots(numsensors, len(switchtypes_list), figsize=(18, 12), sharex=True, sharey=False)

# Function to normalize data per sensor
def normalizedata(row, numpoints, numsensors):
    normalizedrow = row.copy()
    for sensor in range(numsensors):
        start = sensor * numpoints
        end = start + numpoints
        sensorblock = row[start:end]
        meanval = np.mean(sensorblock)
        normalizedrow[start:end] = sensorblock - meanval
    return normalizedrow

for sensor in range(numsensors):
    for col, switchtype in enumerate(switchtypes_list):
        ax = axes[sensor, col]

        # filter rows within specified range and switchtype
        mask = (switchtypes == switchtype) & \
               (df.index >= rowrangetoplot[0]) & \
               (df.index <= rowrangetoplot[1])
        indices = df.index[mask].tolist()

        # skip if no data in this range for this switchtype
        if not indices:
            ax.set_title(f"Sensor {sensor + 1} | Switchtype {switchtype} (No Data)")
            continue

        rows = data.iloc[indices, :]
        rowindices = indices

        for groupidx, rowid in enumerate(rowindices):
            row = rows.iloc[groupidx, :].values.astype(float)
            row = normalizedata(row, numpoints, numsensors)

            startcol = sensor * numpoints
            endcol = startcol + numpoints
            if endcol > len(row):
                endcol = len(row)

            readings = row[startcol:endcol]

            # for x axis
            time = np.arange(0, len(readings) * delay, delay) / 1000

            # use CSV line number for labeling
            # ax.plot(time, readings, alpha=0.7, label=f"Line {rowid + 1}")
            ax.plot(time, readings, alpha=0.7, label=None)

        ax.set_title(f"Sensor {sensor + 1} | Switchtype {switchtype}")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Reading Value")
        ax.grid(True)
        ax.set_xlim(0, 6)
        ax.set_xticks(tickpos)
        ax.set_xticklabels(ticklabels)

        # making a legend
        ax.legend(fontsize='x-small', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()
