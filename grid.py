import json
import datetime
import pytz
import requests
from influxdb import InfluxDBClient

class GridWatch:
    URL='https://live.gridwatch.ca/WebServices/GridWatchWebApp.asmx/GetHomeViewData_v2'
    response=object
    response_plain=""
    
    def write(self,measurement: dict) -> bool:
        client=InfluxDBClient(host='localhost', port=8086)
        client.switch_database('pyexample')
        return client.write_points([measurement])
    
    def get_measurements(self):
        self.response_plain=requests.get(self.URL)
        self.response=self.response_plain.json()
        measurement_time=self.reading_time_() 
        return {
            'measurement': "gridwatch",
            'fields': {
                'emissions_tons': int(self.response['totalCo2e'].replace(',','')),
                'co2e_g_kwh': int(self.response['co2eIntensity'].replace(',','')),
                'nuclear_mw_generated': int(self.response['nuclearOutput'].replace(',','')),
                'nuclear_gen_percent': float(self.response['nuclearPercentage'].replace(',','')),
                'hydro_mw_generated': int(self.response['hydroOutput'].replace(',','')),
                'hydro_gen_percent': float(self.response['hydroPercentage'].replace(',','')),
                'gas_mw_generated': int(self.response['gasOutput'].replace(',','')),
                'gas_gen_percent': float(self.response['gasPercentage'].replace(',','')),
                'wind_mw_generated': int(self.response['windOutput'].replace(',','')),
                'wind_gen_percent': float(self.response['windPercentage'].replace(',','')),
                'solar_mw_generated': int(self.response['solarOutput'].replace(',','')),
                'solar_gen_percent': float(self.response['solarPercentage'].replace(',','')),
                'biofuel_mw_generated': int(self.response['biofuelOutput'].replace(',','')),
                'biofuel_gen_percent': float(self.response['biofuelPercentage'].replace(',',''))
            },
            'time': measurement_time,
            'tags': {'freq': 60*60, 'ba': 'IESO_NORTH'}
        }

    def reading_time_(self)->str:
        month_lookup={
            "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, 
            "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12 }
        now=datetime.datetime.now()                                   #  0   1   2  3  4  5 6  7
        tokens=self.response['timeOfReading'].replace(',','').split() # "Sat Feb 4, 11 AM - 12 PM"
        reading_month=month_lookup[tokens[1]]
        reading_day=int(tokens[2])
        reading_hour_start=int(tokens[3]) if int(tokens[3])==12 or tokens[4]=="AM" else int(tokens[3])+12 # convert to 24 hour time
        reading_year=now.year-1 if now.month==1 and reading_month==12 else now.year # handle new years day getting last year's readings
        
        reading_time= datetime.datetime(
            year=reading_year, 
            month=reading_month, 
            day=reading_day, 
            hour=reading_hour_start,
            tzinfo=pytz.timezone('Canada/Eastern')
            ).isoformat()
        
        print(f"at {now} calculated reading time {reading_time} from string {self.response['timeOfReading']}")
        return reading_time

if __name__ == "__main__":
   gw=GridWatch()
   measurements=gw.get_measurements()
   print(f"measurements:{measurements}")
   ok=gw.write(measurements)
   print(f"ok was {ok}")
