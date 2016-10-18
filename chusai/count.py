import csv

reader = csv.reader(file('./WIFI_AP_Passenger_Records_chusai_1stround.csv','rb'))
data = []
for line in reader:
    data.append(line)

print ("Read Over")
tags = set()
times = set()
for WIFIAPTag, passengerCount, timeStamp in data[1:]:
    tags.add(WIFIAPTag)
    times.add(timeStamp)
