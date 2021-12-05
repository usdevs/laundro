---
id: setting-up
title: Setting Up
---

## Specs

Model: [**Raspberry PI 3 Model B V1.2 2015**](https://www.raspberrypi.com/products/raspberry-pi-3-model-b/)

_This is the model that we currently have on our hands, but we are definitely not limited to just this specific model. There will be a chance for us to explore the feasibility to pivot towards [RPI Zero](https://www.raspberrypi.com/products/raspberry-pi-zero/) depending on our approach_

## OS

RPI boots from a SD card (we will mostly be dealing with `16GB/32GB` cards). You can either use the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) or manually install the OS images by downloading and installing them [here](https://www.raspberrypi.com/software/operating-systems/).

There are a couple of choices for the OS image, some comes with a GUI while some are just lightweight OS that we will interact with mainly through the command line/terminal.

:::info
For linux enthusiasts, RPI can also boot [Ubuntu Desktop](https://ubuntu.com/download/raspberry-pi).
:::

**Considering the nature of the project, we will likely not deploy it with a OS that comes with a GUI since it will be wasted storage. However in the process of development feel free to use whatever fits your needs.**

### Installation

| OS Images                                                 | Description                  | Size (as of `v5.10`) |
| --------------------------------------------------------- | ---------------------------- | -------------------- |
| **Raspberry Pi OS with desktop**                          | GUI ✅                       | `1148MB`             |
| **Raspberry Pi OS with desktop and recommended software** | Bulkier version of the above | `3045MB`             |
| **Raspberry Pi OS Lite**                                  | GUI ❌                       | `463MB`              |

:::note
There are also legacy versions of the above OS images that are available for download on the same website. However, I do not think that it will matter as of now for this project.
:::

The installation process is quite simple.

1. Get a SD Card and a SD card reader
2. Download the imager (if you prefer a interface) or the OS image manually
3. Write it to your SD card
4. Mount the SD card to RPI
5. (Optional) _Pray it works_

:::warning
I will not recommend using the imager on a M1 as it does not seem like it is [not fully compatible](https://github.com/raspberrypi/rpi-imager/issues/235) yet.

[_Sadly I found this out the hard way._](/blog/2021/12/04/rpi-imager-crash)
:::

## Default Login

- Username: **pi**
- Password: **raspberry**

## References

- https://www.raspberrypi.com/documentation/computers/getting-started.html
