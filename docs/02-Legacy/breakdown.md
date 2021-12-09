---
id: breakdown
title: Breakdown
---

Legacy Repo: https://github.com/usdevs/laundry-pi 

_TODO_
# Setup
_TODO:_ To Update

From [legacy repo](https://github.com/usdevs/laundry-pi):

### 1. Install dependencies 
`pip install` :
- firebase-admin
- Adafruit-Blinka
- Adafruit-ADS1x15

### 2. Setup device specific configuration in config.py
1. Generate another firestore cert, and save it somewhere on the RPi
2. Copy `config.py.example` as `config.py` and fill in it in appropriately.
    `FIRESTORE_CERT` refers to the path to the firestore cert file we generated
    above.

### 3. Add tasks to crontab
`crontab -e` then add:
- `@reboot cd path/to/laundro && python3 runner.py main.py main` (start the main
  script when the RPi boots up)
- `* * * * * cd path/to/laundro && git pull && git log --pretty=oneline -1 |
  python3 flagger.py` (check Github for updates every minute)
---
# How it Works:
### 1. `crontab` tasks from setup:
```
crontab -e
@reboot cd path/to/laundro && python3 runner.py main.py main
* * * * * cd path/to/laundro && git pull && git log --pretty=oneline -1 | python3 flagger.py
```

- `runner.py main.py main` is set to run every time the rpi is booted up
  - This runs `main.py` (_TODO_: can't tell if it's `main.py` or `main()` in `main.py`) in a process, and restarts it every time the process ends (when an error is raised).
- Second line checks for github updates every minute.
### 2. `main.py`

`main.py` calls `main()`. If `main` encounters an error (possibly from firebase), it then runs `local_main`, which is essentially `main` without any firebase-related things.

`main`:
1. Initiates a `logger`
2. Initiates a `FirestoreManager`
3. Gets the list of pins
4. Creates a firestore documents for the pins and rpi, if it doesn't exist already
5. Gets initial pin readings
    - For each `pin`, its status (`bool`, on or off) is stored in a dictionary `prev_on`.
    ```python
    for p in pins:
      ...
      on = p.is_on()
      prev_on[p.id] = on
      ...
    ```
    - For each pin, get the previous time when it was updated from firebase with `current = firestore.get_pin_data(p.id)`
    - If _pin values did not change_ within 30 mins (washing machine) or 45 mins (dryer), ignore this reading.
      - Otherwise update the `pin` document on firebase.

6. Enters a `while(True)` loop for data collection.
    - Note: Each run of the loop takes around 25 seconds (it actually takes 21(?) seconds, but 25 is assumed in the script)
      - 2 seconds x 9 pins + 1 second sleep + 2 seconds firebase/logs ~ 21 seconds 

    - Every 6 minutes (24 runs), update the `lastSeen` time for the RPi to the current time.
    - For every pin,

    1. Check if its machine is on with `p.is_on()` (Note: takes 2 seconds _per pin_, singlethreaded. This monitors the pin state over 2 seconds, so it accounts for blinking.)
    2. Check if the pin has changed by comparing it with the dict `prev_on`.
    3. If the pin has changed, update firestore and `prev_on`.
    4. Check if there are any updates from GitHub with `if flag.flagged():`
        - restart main script if there are updates
    5. `time.sleep(1)` I don't know why we are sleeping for 1 second, but it is there I guess
---
# Files
## `main.py`
- The project uses the [`adafruit_ads1x15` module](https://github.com/adafruit/Adafruit_CircuitPython_ADS1x15).


Contains methods:
| Method          | Desc                                                                            | Returns     |
| --------------- | ------------------------------------------------------------------------------- | ----------- |
| `get_pins(pi_id)` | Returns an array of `Pin`s associated with each Raspberry Pi.                   | `list[Pin]` |
| `main()`          | Main Script                                                                     | `None`      |
| `local_main()`    | Debugging for Main Script. This checks the pins, but does not update firestore. | `None`      |

`get_pins(pi_id)` returns the following list of `Pin` objects:
If `pi_id == 1`, returns

| Class | Pin id | ADC ID | ADC Pin id | record_values | threshold       |
| ----- | ------ | ------ | ---------- | ------------- | --------------- |
| Pin   | 1      | `ads1`   | `ADS.P0`     | `True`          | `32000` (Default) |
| Pin   | 2      | `ads1`   | `ADS.P1`     | `True`          | `32000` (Default) |
| Pin   | 3      | `ads1`   | `ADS.P2`     | `True`          | `32000` (Default) |
| Pin   | 4      | `ads1`   | `ADS.P3`     | `True`          | `32000` (Default) |
| Pin   | 5      | `ads2`   | `ADS.P0`     | `True`          | `20000`           |
| Pin   | 6      | `ads2`   | `ADS.P1`     | `True`          | `32000` (Default) |
| Pin   | 7      | `ads2`   | `ADS.P2`     | `True`          | `32000` (Default) |
| Pin   | 8      | `ads2`   | `ADS.P3`     | `True`          | `32000` (Default) |
| Pin   | 9      | `ads3`   | `ADS.P0`     | `True`          | `25000`           |

If `pi_id == 2`, returns

| Class | Pin id | ADC ID | ADC Pin id | record_values | threshold         |
| ----- | ------ | ------ | ---------- | ------------- | ----------------- |
| Pin   | 10     | `ads1` | `ADS.P0`   | `True`        | `15000`           |
| Pin   | 11     | `ads1` | `ADS.P1`   | `True`        | `32000` (Default) |
| Pin   | 12     | `ads1` | `ADS.P2`   | `True`        | `32000` (Default) |
| Pin   | 13     | `ads1` | `ADS.P3`   | `True`        | `21000`           |
| Pin   | 14     | `ads2` | `ADS.P0`   | `True`        | `32000` (Default) |
| Pin   | 15     | `ads2` | `ADS.P1`   | `True`        | `32000` (Default) |
| Pin   | 16     | `ads2` | `ADS.P2`   | `True`        | `32000` (Default) |
| Pin   | 17     | `ads2` | `ADS.P3`   | `True`        | `32000` (Default) |
| Pin   | 18     | `ads3` | `ADS.P0`   | `True`        | `32000` (Default) |

Otherwise, raises an error.

**Notes:**
`ads1`, `ads2` and `ads3` are ADS ids hardcoded as:
```
ads1 = ADS.ADS1115(i2c, address=0x48)
ads2 = ADS.ADS1115(i2c, address=0x49)
ads3 = ADS.ADS1115(i2c, address=0x4a)
```
As their name implies, `ADS.P0`, `ADS.P1`, `ADS.P2` and `ADS.P3` corresponds to the pin values 0, 1, 2, and 3 respectively, and are `int` values `0`, `1`, `2`, and `3`.
### Log Files
`main.py` writes logs with the `logging` module to the directory `~/laundro_logs/<pi ID>/`.

A log file can be read with live updates using:
```
tail -f <name of log file>
```

`all.log` contains all log messages, `info.log` contains only INFO level and above log messages. Practically speaking, log messages for individual sensor readings will be in `all.log` and not `info.log`.

## `flagger.py` and `runner.py`
_TODO_ but the previous repo says that it is a small ecosystem to update the code on the pi every time a new comit is made.

Importantly, `runner.py` takes a `module path` and `function` and runs `function` in a process. Upon the process terminating, `module path` is reloaded and the new `function` is run in a new process. **This is used to run main.py**

## class FireStoreManager (`firestore_manager.py`)
_TODO_
## class Pin (`pin.py`)

Each `Pin` object represents a pin on the **raspberry pi** (not the Analog to Digital Conveter (ADC)), and has the following properties and methods:


| Properties                                        | Info                                                                                                  |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `id (int) `                                       | Unique ID to every pin (should be unique across RPis too)                                             |
| `adc (adafruit_ads1x15.ads1115.ADS.ADS1115)`      | Represents one ADC module. (ADC Module that the pin connects to)                                      |
| `adc_pin (adafruit_ads1x15.ads1115.ADS.P0/1/2/3)` | Represents a pin on the ADC module. (ADC pin that pin connects to)                                    |
| `threshold (int, optional)`                       | Light threshold. The pin is on if the light value is below this threshold. `Default = 32000`          |
| `record_values (boolean)`                         | Whether to record light value readings. Readings are recorded in a csv file named `pin-<pin ID>.csv`. |


| (Instance) Methods   | Info                                                                                                              | Returns          |
| -------------------- | ----------------------------------------------------------------------------------------------------------------- | ---------------- |
| `is_on_single(self)` | Checks if this pin is currently on, based on 1 reading at the moment. This may return off if the pin is blinking. | tuple(bool, int) |
| `is_on(self)`        | True if this pin is on or blinking, False otherwise. The pin will appear off if it is disconnected.               | bool             |

To test whether the pin is on (detecting light), an analog pin value is read via 
```
light_value = adafruit_ads1x15.analog_in.AnalogIn(adc, adc_pin).value
```
and the light is on if `light_value < self.threshold`.

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
