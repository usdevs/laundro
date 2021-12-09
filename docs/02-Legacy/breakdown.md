---
id: breakdown
title: Breakdown
---

Legacy Repo: https://github.com/usdevs/laundry-pi 

_TODO_

## class Pin (`pin.py`)

Each `Pin` object represents a pin on the **raspberry pi** (not the Analog to Digital Conveter (ADC)), and has the following properties and methods:


| Properties                                      | Info                                                                                                 |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `id (int) `                                       | Unique ID to every pin (should be unique across RPis too)                                             |
| `adc (adafruit_ads1x15.ads1115.ADS.ADS1115)`      | Represents one ADC module. (ADC Module that the pin connects to)                         |
| `adc_pin (adafruit_ads1x15.ads1115.ADS.P0/1/2/3)` | Represents a pin on the ADC module. (ADC pin that pin connects to)                     |
| `threshold (int, optional)`                       | Light threshold. The pin is on if the light value is below this threshold. `Default = 32000`          | 
| `record_values (boolean)`                         | Whether to record light value readings. Readings are recorded in a csv file named `pin-<pin ID>.csv`. |


| (Instance) Methods              | Info                                                                                                              | Returns          |
| -------------------- | ----------------------------------------------------------------------------------------------------------------- | ---------------- |
| `is_on_single(self)` | Checks if this pin is currently on, based on 1 reading at the moment. This may return off if the pin is blinking. | tuple(bool, int) | 
| `is_on(self)`        | True if this pin is on or blinking, False otherwise. The pin will appear off if it is disconnected.               | bool             |

**Notes:**
- `is_on(self)` takes 20 readings over 2 seconds (every 0.1 seconds) and returns `True` if at least one detects the pin as on.
- `is_on(self)` logs pin and values to the logger
- if `record_values` is True, `is_on(self)` records light valuers onto the corresponding csv file on the pi.

## `config.py`

Stores some config values:

| Name             | Desc.                                                                                                                                                    |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `FIRESTORE_CERT` | The path to the JSON file containing the Firestore certificate. Used to create a new `FirestoreManager`                                                  |
| `PI_ID`          | Value is either `1` or `2`, is an identifier that determines which pins to update. Is called by `get_pins(id)` in `main.py` for a list of `Pin` objects. |
| `LOGDIR`         | Directory path to save log files in. Called in `utils.init_logger(logdir="", logger_name=None)`                                                          | 
