import csv
import numpy as np
from sklearn.calibration import LinearSVC
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.model_selection import LeaveOneOut, cross_val_score
from sklearn.neighbors import KNeighborsClassifier

from sklearn.preprocessing import StandardScaler

def main():
    # Create master data array
    # One entry is [YYYY, MM, DD, HR, count]
    data, labels = np.array(wrangle_data(retrieve_data('master_traffic_data.csv')))
    scaler = StandardScaler().fit(data)
    data = scaler.transform(data)
    # cols = ['year', 'month', 'day', 'hour', 'station', 'count']
    loo_classification(data, labels)

def retrieve_data(file):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        data = []
        for line in reader:
            data.append(line)
    return data

def wrangle_data(raw_data):
    data = []
    labels = []
    for line in raw_data:
        for i in range(0, 24):
            date = line[1]
            # YYYY, MM, DD, HR, station #, count
            data.append([int(date[:4]), int(date[4:6]), int(date[6:]), i, int(line[0]), int(line[i+3])])
            labels.append(data[0])
    return data, labels

def loo_classification(data, labels):
    classifiers = [LinearDiscriminantAnalysis(), \
              QuadraticDiscriminantAnalysis(), \
               KNeighborsClassifier(1), \
               LinearSVC()]

    tags = ['Linear', 'Quad Disc Analysis', 'KNeighbors', 'Linear SVC']

    for cls, tag in zip(classifiers, tags):
        score = np.mean(cross_val_score(cls, data, labels, cv=LeaveOneOut()))*100
        print(tag, score)

if __name__ == "__main__":
    main()
