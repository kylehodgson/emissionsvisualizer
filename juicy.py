import aiohttp
import asyncio
import datetime
import pytz
import pyjuicenet
from os import environ
import db

class JuiceNet:
  TOKEN=""

  def __init__(self) -> None: 
    self.TOKEN=environ.get('JN_API_KEY')
    if not self.TOKEN:
      raise Exception(
        "Set the environment variable JN_API_KEY to your JuiceNet API token. "\
        "You can find it here: https://home.juice.net/Manage")
    
  def write(self,measurements) -> bool:
    db.write_points(measurements)
  
  async def get_measurements(self):
    measurement_time=datetime.datetime.now(tz=pytz.timezone('Canada/Eastern')).isoformat()
    async with aiohttp.ClientSession() as session:
      api = pyjuicenet.Api(self.TOKEN, session)
      devices = await api.get_devices()
      measurements=[]
      for charger in devices:
        await charger.update_state()
        measurements.append({
          "measurement": "juicenet",
          "fields": {
            "charge_time": charger.charge_time, 
            "energy_added": charger.energy_added, 
            "voltage": charger.voltage, 
            "amps": charger.amps, 
            "watts": charger.watts, 
            "temperature_c": charger.temperature, 
            "status": charger.status,
            "charging_bool": True if charger.status.lower()=="Charging".lower() else False,
            "charging_mult": 1 if charger.status.lower()=="Charging".lower() else 0
          },
          "time": measurement_time,
          "tags": {
            "device_name": charger.name, 
            "device_id": charger.id, 
            "device_type": "evse",
            "device_brand": "enelx", 
            "device_model": "juicebox40 pro", 
            "status": charger.status
          }
        })
      return measurements


if __name__ == "__main__":
   jn=JuiceNet()
   measurements=asyncio.run(jn.get_measurements()) 
   ok=jn.write(measurements)
   print(f"ok was {ok}")
   


