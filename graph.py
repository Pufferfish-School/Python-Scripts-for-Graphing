import pandas
from matplotlib import pyplot as plt
import os

path = "C:\\Users\\14403\\Desktop\\Gerdt Lab\\Currently Working On\\processed-data\\fluor_csvs\\"
filenames = os.listdir(path)

for filename in filenames:
	subfilenames = os.listdir(path + filename)
	df_list = []
	averages = []
	names = []

	for subfilename in subfilenames:
		average_list = []
		df = pandas.read_csv(path + filename + "\\" + subfilename, sep=',', skiprows=3)
		i = 0
		for (name, data) in df.iteritems():
			if pandas.isna(data[0]):
				last_val = data[0]
				break
			i += 1

		if pandas.notna(last_val):
			break

		df_list.append(df.drop(columns=df.columns[i:]))

		for (name, data) in df.iterrows():
			average_list.append(data[1:].sum() / (len(data) - 1))

		names.append(subfilename)

		averages.append(average_list)

	trial_count = 0
	for listy in averages:
		trial_count += 1
		plt.plot(listy, label = filename + " trial " + str(trial_count))
	plt.legend()
	plt.savefig(fname = filename + "_graph")
	plt.cla()