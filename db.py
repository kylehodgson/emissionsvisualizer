from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import json
from os import environ



def write_points(p) -> bool:
    token = environ.get('INFLUXDBTOKEN')
    username = environ.get('INFLUXDBUSER')
    password = environ.get('INFLUXDBPASSWORD')
    if not token:
        raise Exception(
            "Did not find InfluxDB credentials. Make sure INFLUXDBTOKEN is set.")
        
    with InfluxDBClient(url="http://localhost:8086", token=token) as c:
        with c.write_api(write_options=SYNCHRONOUS) as w:
            return w.write(bucket="home", org="Long Branch Flyer", record=p)