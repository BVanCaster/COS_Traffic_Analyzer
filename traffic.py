import csv
import collections
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import homogeneity_score, homogeneity_completeness_v_measure
from sklearn.cluster import KMeans

def main():
    files = ['AnnualTrafficVolume.csv', 'AnnualTrafficVolume (1).csv', 'AnnualTrafficVolume (2).csv', 
             'AnnualTrafficVolume (3).csv', 'AnnualTrafficVolume (4).csv', 'AnnualTrafficVolume (5).csv',
             'AnnualTrafficVolume (6).csv', 'AnnualTrafficVolume (7).csv']
    with open(files[0], 'r') as f:
        header = f.readline().split(',')
        # station id, data, direction, 24 hr cols, formatted date
    raw_data = retrieve_data('master_traffic_data.csv')

    # Determining if there's clustering along the two stations / by month?
    
    # visualizing the data
    #plot_stations(raw_data)
    # plot_months(raw_data)

    # Try a k-means classification on hours
    time_data, labels = create_hours_data(raw_data)
    k_clustering(time_data, labels)    

def compile_files(filenames):
    for f in filenames:
        with open(f, 'r') as csv_file:
            with open('master_traffic_data.csv', 'a') as master_file:
                header = csv_file.readline()
                for line in csv_file.readlines():
                    master_file.write(line)

def retrieve_data(file):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        data = []
        for line in reader:
            data.append(line)
    return data

def plot_stations(data):
    station1, station2 = [], []
    dates1, dates2 = [], []
    for point in data:
        if point[0] == '000520':
            station1.append(sum([int(x) for x in point[3:27]]))
            dates1.append(point[1])
        else:
            station2.append(sum([int(x) for x in point[3:27]]))
            dates2.append(point[1])
    plt.scatter(dates1, station1)
    plt.scatter(dates2, station2)
    plt.show()

def plot_months(data):
    months = []
    sums = []
    for point in data:
        months.append(point[1][4:6])
        sums.append(sum([int(x) for x in point[3:27]]))
    plt.scatter(months, sums)
    plt.show()

def create_hours_data(data):
    new_data, labels = [], []
    for point in data:
        for x in range(3, 27):
            new_data.append(point[x])
            labels.append(x-3)
    return new_data, labels

def k_clustering(time_data, labels):
    krange = range(1, 25)
    exps = {}
    for k in krange:
        exps[k] = {}
        # various label comparisons
        exps[k]['kmeans'] = km = KMeans(n_clusters=k,n_init='auto').fit(np.array(time_data).reshape(-1, 1))
        hcv = homogeneity_completeness_v_measure(np.array(labels),km.labels_)
        exps[k]['h'],exps[k]['c'],exps[k]['v'] = hcv
    plt.plot(krange,[exps[k]['h'] for k in krange],label='h score')
    plt.plot(krange,[exps[k]['c'] for k in krange],label='c score')
    plt.plot(krange,[exps[k]['v'] for k in krange],label='v score')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
