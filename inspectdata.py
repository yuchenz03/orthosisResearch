import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# change this depending on what file is being used
filepath = "prototype3data/data120.csv"  
k = 120 # number of readings per sensor

delay = 50  # from the arduino code we have a 50ms delay between readings (used for plotting)
numsensors = 4
switchtypes_list = [0, 1, 2]

lastntrialstoshow = 10  # number of most recent trials to keep for plotting 
                        # note: this is n trials per subplot, so 10 indicates 
                        # the last 90 trials will be plotted

df = pd.read_csv(filepath, header=None)
switchtypes = df.iloc[:, 0].astype(int)
data = df.iloc[:, 1:]  # data without switchtypes

# configuring x-axis so that it shows seconds on the bottom line
tickpos = list(range(1, 7))
ticklabels = [str(t) for t in tickpos]

# plotting the 4 axes:
fig, axes = plt.subplots(numsensors, len(switchtypes_list), figsize=(18, 12), sharex=True, sharey=False)

for sensor in range(numsensors):
    for col, switchtype in enumerate(switchtypes_list):
        ax = axes[sensor, col]

        mask = (switchtypes == switchtype)
        indices = df.index[mask].tolist()

        # Keep only the last num_trials_to_keep rows with this switchtype
        if len(indices) > lastntrialstoshow:
            indices = indices[-lastntrialstoshow:]

        rows = data.iloc[indices, :]
        row_indices = indices

        for groupidx, rowid in enumerate(row_indices):
            startcol = sensor * k
            endcol = startcol + k
            if endcol > rows.shape[1]:
                endcol = rows.shape[1]
            readings = rows.iloc[groupidx, startcol:endcol].values.astype(float)
            
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
