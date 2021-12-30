# Testing

The following test datasets contains LDR values from a **full wash cycle** (30 mins). Data were collected from a single washer from the _9th floor laundry room_.

## Raw InfluxDB dump

- [`ldr-values-raw`](https://drive.google.com/drive/folders/1AGChMASJA0ACT4ZQWbuUTe3YbAWQlNpB?usp=sharing)

- [`legacy-snapshot-raw`](https://drive.google.com/drive/folders/196ZlssDv5WDiKMFu0Ar49-DvXsVDt1_2?usp=sharing)

Restore the dump into local instance of InfluxDB with the following commands

> **Ensure that local version of influxdb is `1.x.x`**

```bash
# db with raw ldr values from all 4 input pins of the ADS

influx restore -portable -db laundro-test ./ldr-values-raw

# db with raw ldr values from 2 active pins of ADS
# + on/off indicator generated from legacy stack (threshold is set at 15000 raw ADS channel value)

influx restore -portable -db laundro-legacy-test ./legacy-snapshot-raw
```

## `pandas.Dataframe` pickle

Data is extracted from the raw InfluxDB dump (**laundro-test** db) into a `.pkl` file that can be deserialize back into a `pandas.Dataframe`

**1st Wash cycle** ([wash-cycle-1.pkl](./data/wash-cycle-1.pkl))

- Pin positions

  - **Pin 0: Door Lock Indicator**
  - **Pin 1: Spin Indicator**

- Timestamp (with a bit of a buffer at start and end)
  - **Start: `2021-12-23 05:15:54`** (`2021-12-23 13:15:54 GMT+8`)
  - **End: `2021-12-23 05:45:00`** (`2021-12-23 13:45:00 GMT+8`)

```
Dimensions: [8596 rows x 5 Columns]

                             time ADS_ADDR ADS_PIN  raw_ads_val   voltage
0     2021-12-23T05:15:55.615711Z       72       0         6080  1.900058
1     2021-12-23T05:15:55.886560Z       72       1        32752  4.094125
2     2021-12-23T05:15:55.940863Z       72       2         4608  0.816025
3     2021-12-23T05:15:55.993361Z       72       3         5248  0.740023
4     2021-12-23T05:15:56.555476Z       72       0        23456  1.048032
```

**2nd Wash cycle** ([wash-cycle-2.pkl](./data/wash-cycle-2.pkl))

- Pin positions

  - **Pin 0: Door Lock Indicator**
  - **Pin 1: Spin Indicator**

- Timestamp (with a bit of a buffer at start and end)
  - **Start: `2021-12-23 07:31:32`** (`2021-12-23 15:31:32 GMT+8`)
  - **End: `2021-12-23 08:07:00`** (`2021-12-23 16:07:00 GMT+8`)

```
Dimensions: [10307 rows x 5 Columns]
                              time ADS_ADDR ADS_PIN  raw_ads_val   voltage
0      2021-12-23T07:31:33.971408Z       72       0        12528  0.888027
1      2021-12-23T07:31:34.030930Z       72       1          336  0.040001
2      2021-12-23T07:31:34.124149Z       72       2         5472  0.636019
3      2021-12-23T07:31:34.241946Z       72       3         5376  1.054032
4      2021-12-23T07:31:34.808506Z       72       0        23344  0.984030
```

## Goal

**To find a generic way to determine if the system is current in a wash cycle or in idle mode without the use of hard-coded threshold.**
