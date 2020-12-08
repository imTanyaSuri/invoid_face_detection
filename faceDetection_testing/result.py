import csv
total=0
with open('DEMO7.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        if row[1]=='1':
            total+=1
print(str(total)+' '+str(total/3153))