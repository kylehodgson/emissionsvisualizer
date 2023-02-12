import json
from simplemoer.client import WattTime
from influxdb import InfluxDBClient

def update_moer():
    write(get_moer())

def write(measurement: dict) -> bool:
    client=InfluxDBClient(host='localhost', port=8086)
    client.switch_database('pyexample')
    return client.write_points([measurement])

def get_moer():
    watt_time = WattTime()
    reading = watt_time.get_index()
    return {
        'measurement': "moer",
        'fields': {'percent': int(reading['percent'])},
        'time': reading['point_time'],
        'tags': {'ba': reading['ba'], 'freq': int(reading['freq'])}
    }

def print_moer():
    measurement=get_moer()
    print(f"measurement: {measurement}")

if __name__ == "__main__":
    moer=get_moer()
    print(f"moer was {moer}")
    ok=write(moer)
    print(f"ok was {ok}")