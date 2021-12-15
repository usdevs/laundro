# ADS deps
from plotext._utility import plot
from adafruit_ads1x15.ads1015 import ADS1015
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn
# rpi deps
import board
import busio
# cli and plot deps
import argparse
import plotext as plt


def get_all_ads(ads1x15: int):
    i2c = busio.I2C(board.SCL, board.SDA)
    i2c_dev_addrs = i2c.scan()

    if len(i2c_dev_addrs) == 0:
        raise Exception("No i2c devices found! Please check wiring/connection")

    def ads_constructor(i2c, addr): return ADS1015(
        i2c, address=addr) if ads1x15 == 0 else ADS1115(i2c, address=addr)
    return list(map(lambda addr: ads_constructor(i2c, addr), i2c_dev_addrs))


def poll_graph(list_of_ads, width):
    # 4 inputs per adc (row)
    # number of ads (col)
    plt.subplots(4, len(list_of_ads))

    def plot_subplot(r, c, val_lst):
        plt.subplot(r, c)  # access subplot
        plt.clp()  # clear previous tick's data
        plt.clc()  # clear color

        plt.xlabel("Ticks")
        plt.ylabel("Voltage")
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
                chan = AnalogIn(ads, pin_no)
                out_val = chan.voltage

                val_lst = store[idx][pin_no]
                val_lst.pop(0)
                val_lst.append(out_val)
                plot_subplot(pin_no + 1, idx + 1, val_lst)

        plt.sleep(0.05)
        plt.show()
        plt.clt()  # clear terminal

# rolling table 
def poll_table(r, c):
    # to be implemented
    
if __name__ == "__main__":
    '''
    Assumes that all ADS is of the same model
    '''
    parser = argparse.ArgumentParser(description="Poll ADS Channel Values")
    parser.add_argument('--func', help = "Representation(Table: poll_table, Graph: poll_graph)", 
                        default = 'poll_graph')
    parser.add_argument('--ads1x15', type=int,
                        help="ADS Model (1: ADS1115, 0: ADS1015)", default=0)
    parser.add_argument('--width', type=int,
                        help="Width of the graph (length of history)", default=20)
    
    args = parser.parse_args()
    func_type = globals()[args.func]
    
    func_type(get_all_ads(args.ads1x15), args.width)
