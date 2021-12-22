import board
import busio
from adafruit_ads1x15.ads1015 import ADS1015
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.ads1x15 import Mode
from adafruit_ads1x15.analog_in import AnalogIn

import os
import time
import argparse
from influxdb import InfluxDBClient
from typing import Union, List, Tuple

INFLUX_HOST = os.getenv("INFLUX_HOST") or "localhost"
INFLUX_PORT = int(os.getenv("INFLUX_PORT") or "8086")
INFLUX_DB = os.getenv("INFLUX_DB") or "laundro-test"

db_client = InfluxDBClient(
    host=INFLUX_HOST, port=INFLUX_PORT, database=INFLUX_DB)
db_client.create_database(INFLUX_DB)


def log_ldr_value(voltage: float, raw_ads_val: int, ads_addr: int, ads_pin: int):
    MEASUREMENT_NAME = f"ldr-values-test"
    field_vals = {"voltage": voltage, "raw_ads_val": raw_ads_val}
    point = {"measurement": MEASUREMENT_NAME, "fields": field_vals}

    try:
        return db_client.write_points([point], tags={"ADS_ADDR": ads_addr, "ADS_PIN": ads_pin})
    except Exception as err:
        print(f"[log_ldr_value] Error: {err}")

    return


def get_ads_addr_pairs(ads1x15: int):
    i2c = busio.I2C(board.SCL, board.SDA)
    i2c_dev_addrs = i2c.scan()

    if len(i2c_dev_addrs) == 0:
        raise Exception("No i2c devices found! Please check wiring/connection")

    def ads_constructor(i2c, addr): return ADS1015(
        i2c, address=addr, mode=Mode.CONTINUOUS) if ads1x15 == 0 else ADS1115(i2c, address=addr, mode=Mode.CONTINUOUS)

    return list(map(lambda addr: (ads_constructor(i2c, addr), addr), i2c_dev_addrs))


def poll_to_influxdb(ads_addr_pairs: List[Tuple[Union[ADS1015, ADS1115], int]], poll_interval: float):
    print(
        f"Logging to {INFLUX_HOST}:{INFLUX_PORT}?db={INFLUX_DB} [{time.asctime(time.localtime())}]")
    while True:
        for ads, ads_addr in ads_addr_pairs:
            for pin_no in range(4):
                chan = AnalogIn(ads, pin_no)
                log_ldr_value(chan.voltage, chan.value, ads_addr, pin_no)
        time.sleep(poll_interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Poll to InfluxDB")
    parser.add_argument('--ads1x15', type=int,
                        help="ADS Model (1: ADS1115, 0: ADS1015)", default=0)
    parser.add_argument('--interval', type=float,
                        help="Poll Interval", default=0.5)
    args = parser.parse_args()

    poll_to_influxdb(get_ads_addr_pairs(args.ads1x15), args.interval)
