import csv
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import accuracy_score

features = []
labels = []
with open("Crawled_data.csv") as csvfile:
    reader = csv.reader(csvfile)
    for i in reader:
        features.append(i[2:-1])
        labels.append(i[-1])

train_features = features[:50]
train_labels = labels[:50]

test_features = features[50:]
test_labels = labels[50:]

clf = RandomForestClassifier()
clf.fit(train_features, train_labels)
result_list = []

for i in range(len(test_features)):
    result = clf.predict([(test_features[i])])
    print ("predicted result", result)
    print ('label', test_labels[i])
    result_list.append(result)

print ("accuracy", accuracy_score(result_list, test_labels))

