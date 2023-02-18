import json
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
import db
from pathlib import Path

def fmt_measurement_date_(isodate,h):
    d = datetime.fromisoformat(
        isodate + "T" +  fmt_twodigit_(h) + ":00"
    ).replace(
        tzinfo=ZoneInfo('Canada/Eastern')).astimezone(ZoneInfo('UTC'))
    return d.strftime("%Y-%m-%dT%H:%M")

def fmt_twodigit_(h):
    return str(h) if h >= 10 else "0"+str(h) 

if len(sys.argv) > 1:
   FILENAME=sys.argv[1]
   path=Path(FILENAME)
   if not path.is_file():
       raise FileNotFoundError(f"{FILENAME} is not a valid file")
else:
    raise FileNotFoundError("Please provide a filename as the argument.")    

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
                measurement_date=fmt_measurement_date_(isodate,h)
                measurement={
                    "measurement": "alectra",
                    "fields": {
                        "consumption_wh": float(cells[h+1].replace('"',''))*float(1000) # alectra CSV stores 1 AM in column B, numeric 1.
                    },
                    "time": measurement_date,
                 
                    "tags": {}
                }
                measurements.append(measurement)


ok=db.write_points(measurements)
print(f"OK was {ok}")
