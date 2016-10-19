import csv

reader = csv.reader(file("r3.csv", "rb"))
writer = csv.writer(file("airport_gz_passenger_predict.csv","wb"))
for pc,wi,sl in reader:
    try:
        p = round(float(pc), 1)
        writer.writerow((p,wi,sl))
    except:
        writer.writerow((pc,wi,sl))
    
