import json
import datetime
import pytz
import db

#FILENAME="4959131128_2023-02-0615.29.39.csv"
#FILENAME="4959131128_2023-02-0720.56.49.csv"
FILENAME="4959131128_2023-02-1123.45.00.csv"
headers=[]
measurements=[]
with open(FILENAME, 'r') as f:
    for line in f:
        if not headers: 
            headers.append(line)
        elif len(line.split(",")) > 20:
            cells=line.split(",")
            isodate=cells[0].replace('"','')
            
            for h in range(0,24):
                measurement_date=datetime.datetime.fromisoformat(
                    isodate + "T" + 
                    (str(h) if h >= 10 else "0"+str(h)) +
                    ":00")
                measurement={
                    "measurement": "alectra",
                    "fields": {
                        "consumption_kwh": float(cells[h+1].replace('"','')) # alectra CSV stores 1 AM in column B, numeric 1.
                    },
                    "time": measurement_date,
                 
                    "tags": {}
                }
                measurements.append(measurement)

db.write_points(measurements)
