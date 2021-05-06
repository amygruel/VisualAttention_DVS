import os
import tonic 
import tonic.transforms as tr
import numpy as np
import csv
import argparse
import datetime


# set up PARSER 
parser = argparse.ArgumentParser(description="Import samples from specific categories of DVS128 Gesture and save them as csv")
parser.add_argument("categories", metavar="C", type=int, nargs="+", help="Wanted category, defined by an integer between 1 and 11")
parser.add_argument("--different_samples","-d", help="Get different samples for a specific category called many times (True by default)", action='store_true', default=True)
parser.add_argument("--same_samples","-s", help="Get the same sample for a specific category called many times", action='store_true')
parser.add_argument("--loop","-l", help="Create a csv with same category L times", nargs=1, metavar="L", type=int, default=[1])
parser.add_argument("--hyperparameters","-hp", help="Run the hyperparametrization during HP loops", nargs=1, metavar="HP", type=int, default=[3])
args = parser.parse_args()


## FUNCTIONS
def getSpikes(category, sample, spikes, samples_time):
    nom_file = "DVS128_data/Category"+str(category)+"_Sample"+str(sample)+".csv"
    print(nom_file)
    print(datetime.datetime.now())
    data_file = open(nom_file, "r")
    pixel = 0
    for line in data_file:
        pixel_data = [samples_time[-1]+int(p) for p in line.split(";") if p not in ("","\n")]
        spikes[pixel] += pixel_data
        pixel += 1
    data_file.close()
    
    print(datetime.datetime.now())
    bigger_ts = sample_lengths_file['Category'+str(category)+'_Sample'+str(sample)]
    print(datetime.datetime.now())
    
    print("Bigger timestamp:", bigger_ts)
    samples_time.append(samples_time[-1]+bigger_ts)
    print(samples_time)
    print(datetime.datetime.now())
    print("")
    return (spikes, samples_time)

def displayInfo(simu, category, sample):
    print("// Video "+str(simu)+" for category "+str(category)+"\nSample: "+str(sample))

def getStatsCategory(cat):
    #The DVS128 Gesture dataset samples are organized as follows : 
    stats = {
        'Category 1': 97, 
        'Category 2': 98, 
        'Category 3': 98, 
        'Category 4': 98, 
        'Category 5': 98, 
        'Category 6': 98, 
        'Category 7': 98, 
        'Category 8': 98, 
        'Category 9': 98, 
        'Category 10': 98, 
        'Category 11': 98
    }

    return stats["Category "+str(cat)]



## MAIN

# read samples
sample_lengths_file = {}
file_sl = open("DVS128_data/sample_lengths.csv","r")
for line in file_sl:
    line=line.split(";")
    sample_lengths_file[line[0]] = int(line[1])
file_sl.close()

# main loop
spikes = [[] for pixel in range(int(128*128/4))]
samples_time = [0]
if args.same_samples:
    args.different_samples = False

nb_sim = 1
for category in args.categories:
    if args.same_samples :
        sample = np.random.randint(low=1, high=getStatsCategory(category)+1)

        displayInfo(nb_sim, category, sample)
        spikes, samples_time = getSpikes(category, sample, spikes, samples_time)
        t_max = samples_time[-1]

        while nb_sim <= args.loop[0]:
            nb_sim += 1
            displayInfo(nb_sim, category, sample)
            for pixel in range(len(spikes)):
                pixel_data = [samples_time[-1] + e for e in spikes[pixel] if e <=t_max] 
                spikes[pixel] += pixel_data
            samples_time.append(samples_time[-1] + t_max)
            print(samples_time)
            print("Bigger timestamp:", t_max)
            print("")

    elif args.different_samples :
        samples = list(range(1, getStatsCategory(category)+1))
        for l in range(args.loop[0]):
            sample = np.random.choice(samples)
            samples.remove(sample)
            if len(samples) == 0:
                samples=list(range(1, getStatsCategory(category)+1))

            displayInfo(nb_sim, category, sample)
            nb_sim += 1
            
            spikes, samples_time = getSpikes(category, sample, spikes, samples_time)


# writing data into csv
print("Writing files...")

gesture_data = open("data/gesture_data.csv","w")
for pixel in spikes:
    gesture_data.write(";".join([str(e) for e in pixel]))
    gesture_data.write(";\n")
gesture_data.close()

os.system('csvtool transpose -t ";" -u ";" data/gesture_data.csv > data/T_gesture_data.csv')
os.system('mv data/T_gesture_data.csv data/gesture_data.csv')
print("Sample(s) have been saved as data/gesture_data.csv")

print(len(samples_time))
samples_data = open("data/samples_time.csv", "w")
samples_data.write(";".join([str(sample) for sample in samples_time]))
samples_data.close()
print("Times of the sample(s) have been saved as data/samples_time.csv")