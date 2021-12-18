# ADS deps
from adafruit_ads1x15.ads1015 import ADS1015
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.ads1x15 import Mode
from adafruit_ads1x15.analog_in import AnalogIn
# rpi deps
import board
import busio
# cli and plot deps
import time
import argparse
import plotext as plt
from enum import Enum


class ADSDataType (Enum):
    VOLTAGE = "VOLTAGE"
    ADS_VALUE = "ADS_VALUE"

    def __str__(self):
        return self.value


def get_all_ads(ads1x15: int):
    # i2c
    i2c = busio.I2C(board.SCL, board.SDA)
    i2c_dev_addrs = i2c.scan()

    if len(i2c_dev_addrs) == 0:
        raise Exception("No i2c devices found! Please check wiring/connection")

    def ads_constructor(i2c, addr): return ADS1015(
        i2c, address=addr, mode=Mode.CONTINUOUS) if ads1x15 == 0 else ADS1115(i2c, address=addr, mode=Mode.CONTINUOUS)
    return list(map(lambda addr: ads_constructor(i2c, addr), i2c_dev_addrs))


def get_raw_adc_value(ads, pin_no):
    return AnalogIn(ads, pin_no).value


def get_voltage(ads, pin_no):
    return AnalogIn(ads, pin_no).voltage


def get_log_value(ads, pin_no, dtype: ADSDataType):
    if dtype == ADSDataType.VOLTAGE:
        return get_voltage(ads, pin_no)
    elif dtype == ADSDataType.ADS_VALUE:
        return get_raw_adc_value(ads, pin_no)

    return -1


def poll_graph(list_of_ads, width, dtype: ADSDataType):
    # 4 inputs per adc (row)
    # number of ads (col)
    plt.subplots(4, len(list_of_ads))

    def plot_subplot(r, c, val_lst):
        plt.subplot(r, c)  # access subplot
        plt.clp()  # clear previous tick's data
        plt.clc()  # clear color

        plt.xlabel("Ticks")
        plt.ylabel(dtype.value)
        plt.xticks(x_ticks)

        plt.title(f"ADS_{c-1} A{r-1}")
        plt.plot(x_ticks, val_lst, marker="dot", color=r)

    # store
    store = dict(zip(range(0, len(list_of_ads)), [
        [[0]*width for j in range(4)] for i in range(len(list_of_ads))]))
    x_ticks = range(0, width+1)

    while True:
        for idx, ads in enumerate(list_of_ads):
            for pin_no in range(4):
                val_lst = store[idx][pin_no]
                val_lst.pop(0)
                val_lst.append(get_log_value(ads, pin_no, dtype))

                plot_subplot(pin_no + 1, idx + 1, val_lst)

        plt.sleep(0.05)  # reduces screen flickering
        plt.show()
        plt.clt()  # clear terminal


def poll_table(list_of_ads, dtype: ADSDataType):
    # TODO handle multiple ADS
    # for now we will always just log the ads in idx 0
    chosen_ads = list_of_ads[0]
    TABLE_ROW_TEMPLATE = '| 0: {0:^6} | 1: {1:^6} | 2: {2:^6} | 3: {3:^6} |'
    while True:
        out_vals = [get_log_value(chosen_ads, pin_idx, dtype)
                    for pin_idx in range(4)]
        if dtype == dtype.VOLTAGE:
            out_vals = list(map(lambda x: round(x, 3), out_vals))

        print(TABLE_ROW_TEMPLATE.format(*out_vals))
        time.sleep(0.5)  # make it readable


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Poll ADS Channel Values")
    parser.add_argument('poll_type', type=str, help="graph / table")
    parser.add_argument('--ads1x15', type=int,
                        help="ADS Model (1: ADS1115, 0: ADS1015)", default=0)
    parser.add_argument('--width', type=int,
                        help="Width of the graph (length of history)", default=20)
    parser.add_argument('--dtype', type=ADSDataType,
                        help="VOLTAGE / ADC_VALUE", default=ADSDataType.VOLTAGE, choices=list(ADSDataType))

    args = parser.parse_args()
    if args.poll_type == "graph":
        poll_graph(get_all_ads(args.ads1x15), args.width, args.dtype)
    elif args.poll_type == "table":
        poll_table(get_all_ads(args.ads1x15), args.dtype)
