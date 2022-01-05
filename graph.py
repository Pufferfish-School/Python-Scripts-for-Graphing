import pandas as pd
from matplotlib import pyplot as plt
import os
import numpy as np


# Set path to be the folder containing the folders that contain the csvs
# path = r"C:/Users/14403/Desktop/Gerdt Lab/Currently Working On/processed-data/fluor_csvs/")
path = "/home/bkallus/Python-Scripts-for-Graphing/fluor_csvs/"

subdirs = os.listdir(path)
for subdir in subdirs: # For each experiment
    subfilenames = os.listdir(path + "/" + subdir)
    df_list = [] # Contains one DataFrame for each trial
    average_lists = [] # Contains one list of averages (to be plotted) for each trial
    std_lists = [] # Contains one list of standard deviations (to be plotted) for each trial

    for subfilename in subfilenames: # For each trial
        df = pd.read_csv(path + "/" + subdir + "/" + subfilename, sep=',', skiprows=3)
        for i, (name, data) in enumerate(df.iteritems()): # Find the first NaN
            if pd.isna(data[0]):
                last_val = data[0]
                break

        columns_to_drop = [df.columns[0]] # Drop the first column because it's just a timestamp
        if pd.isna(last_val): # If there is a NaN in the first row
            columns_to_drop += list(df.columns[i:]) # Cut off all the columns past the first one with a NaN in the first row

        df = df.drop(columns=columns_to_drop)
        df_list.append(df)

        average_list = []
        std_list = []
        for name, data in df.iterrows(): # For each row in the sliced csv
            average_list.append(data.sum() / len(data)) # Average the row and save it
            std_list.append(data.std())

        average_lists.append(average_list)
        std_lists.append(std_list)

    for i in range(len(average_lists)):
        plt.errorbar(x=list(range(len(average_lists[i]))), y=average_lists[i], yerr=std_lists[i], label=(subdir + " trial " + str(i + 1)))

    plt.legend()
    plt.savefig(fname = "graphs" + "/" + subdir + "_graph")
    plt.cla()