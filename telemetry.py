"""Send log messages to remote log aggregation servers."""
import threading
import requests
import os
import sys
from loguru import logger

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = os.environ.get('INFLUXDB_BUCKET')
org = os.environ.get('INFLUXDB_ORG')
token = os.environ.get('INFLUXDB_TOKEN')
url = os.environ.get('INFLUXDB_URL')

client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
)

write_api = client.write_api(write_options=SYNCHRONOUS)

p = influxdb_client.Point("exhibit_boot").tag("location", "Moneypalooza").field("exhibit_name", "jump_coins")
try:
    write_api.write(bucket=bucket, org=org, record=p)
except Exception as e:
    logger.warning(f"Error sending boot point to InfluxDB: {e}")

def send_point_in_thread(coin_name, jump_count):
    logging_thread = threading.Thread(target=send_point, args=(coin_name, jump_count))
    logging_thread.start()

def send_point(coin_name, jump_count):
    try:
        p = influxdb_client.Point("coin_jumps").tag("location", "Moneypalooza").field("coin_name", coin_name).field("jumps", jump_count)
        write_api.write(bucket=bucket, org=org, record=p)
    except Exception as e:
        logger.warning(f"Error sending point to InfluxDB: {e}")

def send_log_message(message):
    message_thread = threading.Thread(target=send_msg, args=(message,))
    message_thread.start()

def send_msg(message):
    logger.warning(f"telemetry.send_msg() not yet implemented, didn't send {message}")

if __name__ == "__main__":
    send_log_message(sys.argv[1])
