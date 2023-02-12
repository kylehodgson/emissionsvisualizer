import requests
import os
import datetime
import pytz
import db

class PurpleAir:
    APIKEY = ""
    SENSORURL="https://api.purpleair.com/v1/sensors/"
    SENSORID=""
    sensor_data=None
    def __init__(self, api_key="", sensor_id="") -> None:
        if not api_key:
            api_key = os.environ.get('PURPLEAPIKEY')
        if not sensor_id:
            sensor_id=os.environ.get('PURPLEAIRSENSORID')
        if not api_key or not sensor_id:
            raise Exception(
                "Did not find purple air credentials. Either provide "
                "the api key and sensor id while enstantiating PurpleAir, or make sure "
                "the PURPLEAPIKEY and PURPLEAIRSENSORID environment variables is set.")
        self.APIKEY=api_key
        self.SENSORID=sensor_id
    
    def get_measurements(self):
        resp=requests.get(self.SENSORURL+self.SENSORID,headers={'X-API-Key': self.APIKEY})
        self.sensor_data=resp.json()
        measurement_time=datetime.datetime.fromtimestamp(self.sensor_data['data_time_stamp'], tz=pytz.timezone('Canada/Eastern')).isoformat()
        return {
            "measurement": "purpleair",
            "fields": {
                "pm25_ug": self.sensor_data['sensor']['stats']['pm2.5'],
                "temperature": self.sensor_data['sensor']['temperature'],
                "humidity": self.sensor_data['sensor']['humidity']
            },
            "time": measurement_time,
            "tags": {
                "freq": 5*60
            }
        }
    
    def write(self,measurement: dict) -> bool:
        db.write_points([measurement])
    

if __name__ == "__main__":
    pa=PurpleAir()
    measurements=pa.get_measurements()
    ok=pa.write(measurements)
    print(f"OK was {ok}")