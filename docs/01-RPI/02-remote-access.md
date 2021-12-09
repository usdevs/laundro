---
id: remote-access
title: Remote Access (SSH)
---

## Primer on SSH

The intuition behind SSH (Secure Shell) is quite straight-forward. Built on the public-key cryptography system, the way you prove your identity would be through a pair of public and private keys that you will possess. To access a remote SSH server (in this case our RPI), your public key (`pubKey`) would need to be in the list of `authorized_keys` on the remote server. Subsequently, you would use your private key (`privKey`) to authenciate yourself for the server to grant you authorization.

**Authenication Process**

> The actual process is more complicated than this, this is meant to just give a sufficient intuition on how this works

1. Client attempts to the remote server by informing the server which `pubKey` it should use for the auth process
2. Remote server generates a random string and encrypts it using your `pubKey`
3. Client receives the encrypted string
4. Client attempts to decrypt it using its `privKey`
5. Client sends the decrypted (_the actual process have some additional steps_) package back to the server
6. Server checks that it corresponds and grant authorization accordingly

## Set up

Before we can SSH into the RPI, there are some set up that we will need to do on both client (You) and server (RPI) side. This mainly involves the client setting up its SSH client and allow SSH access on the server.

### Remote Server (RPI)

After a flash OS install, SSH is not enabled by default.

**To enable the SSH server**

```bash
sudo raspi-config
```

1. Navigate to **Interface Options**
2. Navigate to **P2 SSH**
3. Enable it

:::info
Another way would be to add a file named `ssh`/`ssh.txt` in the `boot` drive of the PI.

You can add it to the OS image before flashing to the PI.
:::

### Client (You)

There are couple of GUI-based SSH clients out there (e.g. `PuTTY`) or you can opt for just the command-line based `OpenSSH` client.

> `OpenSSH` have been integrated into `win` as a built-in

The following would be a simple guide for those that opt for the `OpenSSH` client.

> I believe GUI-based clients should already handle all these things for you.

1. **Generate your SSH key pair (`pubKey` and `privKey`)**
   ```bash
   ssh-keygen
   ```
2. **It will subsequently prompt you to save the keys generated (its a readable text file) to the `*/.ssh/id_rsa` files (path prefix would differ based on OS)**

   - `*/.ssh/id_rsa`: `privKey`
   - `*/.ssh/id_rsa.pub`: `pubKey`

3. **Set a passphrase**

   - You will need to give this passphrase everytime you want to use your `privKey` (treat this as a master password)

4. **At the end of the process you will get a summary**

   ```
   Your identification has been saved in /Users/shenyihong/.ssh/id_rsa
   Your public key has been saved in /Users/shenyihong/.ssh/id_rsa.pub
   The key fingerprint is:
   SHA256:kiUhzyvccIKx07jmzAj512lhMCfEue7F2o+vzMxg7x0 shenyihong@Shens-MBP
   The key's randomart image is:
   +---[RSA 3072]----+
   |  ..o..          |
   |   Bo+ .         |
   |  = B.* .        |
   | . +.X =         |
   |o o.o.B S        |
   |.B  .+o+         |
   |. =.+++ E        |
   |   ooO.o .       |
   |     .X++        |
   +----[SHA256]-----+
   ```

   :::info
   The randomart image is generated using your `pubKey`. This is useful for verification as instead of comparing the `pubKey` stored on the server character by character, you can simply compare the randomart image.
   :::

**Right now, we have the SSH server and client side set up individually, next we will need to set up a connection between the RPI and the client to copy our `pubKey` to the server.**

## SSH via LAN (Direct Connection)

> Basically we are just directly connecting a ethernet cable between the client and the server (RPI)

:::note
The IP address on RPI's `eth0` interface should be static. This means on each connection, the IP address of the RPI should remain the same
:::

1. Find out which network interface you are using to connect to the RPI (using `ifconfig`)
2. Get the network address and the subnet mask
3. Discovering the IP address of the RPI

   - **Without** a keyboard attached to RPI
     1. We will need to scan our network inteface for the presence of a RPI device
     2. Install `nmap`
     3. `nmap -sn <net-addr>/<mask>`
     4. Inspect result of scan for a RPI device
        - Since it is a direct connection, we will likely pick up just one device which should correspond to the RPI

   :::warning
   Depending on the size of the `netmask`, the scan can take quite a while

   I would advise if it is a 16-bit mask, just give up and get a keyboard.
   :::

   - **With** a keyboard attached to RPI
     - We simply just need to grab the RPI's IP address
     ```bash
     ifconfig | grep -A 3 eth0
     ```
     - Inspect the IP address under `inet` (this is the RPI IP address)

4. Copy your `pubKey` to the RPI

   ```bash
   ssh-copy-id pi@<rpi-ip-addr>
   ```

   - You will be prompted for the password for the `pi` user
     - If there is not change of password, it will be the [default login](/RPI/setting-up#default-login)

5. You are all done
   ```bash
   ssh pi@<rpi-ip-addr>
   ```

## SSH via USB

| RPI Model                        | Compatibility |
| -------------------------------- | ------------- |
| Raspberry Pi Zero W v1.1         | ✅            |
| Raspberry PI 3 Model B V1.2 2015 | ❌            |

:::info
Only RPI that has [USB OTG](https://en.wikipedia.org/wiki/USB_On-The-Go) support is compatible with this method.
:::

To access the RPI via USB, we will need to configure it to be **Ethernet Gadget**.

> To configure the RPI to be booted up as a Ethernet Gadget we will mainly be editing files in the `/boot` of the RPI. You can access the content of the `/boot` by either reading the SD card directly or access it via SSH using other methods.

1. Edit `/boot/config.txt`

   ```bash
   echo "dwcoverlay=dwc2" >> /boot/config.txt
   ```

2. Edit `/boot/cmdline.txt`

   - **After `rootwait` (the last word on the first line) add a space and then `modules-load=dwc2,g_ether`**

3. Enable **SSH** (refer [here](#remote-server-rpi))

4. Boot the RPI and connect it using a **OTG USB cable** (USB A-male to Micro B)

   :::info
   The cable that you usually read data off your Android phone is most likely a OTG USB cable
   :::

   :::warning
   Cables that you use to **charge** devices is **likely not** a OTG USB cable
   :::

5. Verify that cilent can detect the RPI as a **RNDIS** device

   ```bash
   ioreg -p IOUSB
   ```

   :::note
   For `win` users, you might need install to a RNDIS driver first before you can recongize the RPI

   For some older versions of `win`, you will probably need to install [Bonjour](https://support.apple.com/kb/dl999). This is because old `win` versions does not resolve `.local` (see below) by default
   :::

6. Verify connection

   ```bash
   ping raspberrypi.local
   ```

7. You are done

   ```bash
   ssh pi@raspberrypi.local
   ```

## SSH via OHS/NUS Network

_TODO_

## Reference

- https://www.digitalocean.com/community/tutorials/ssh-essentials-working-with-ssh-servers-clients-and-keys
- https://www.raspberrypi.com/documentation/computers/remote-access.html
- https://learn.adafruit.com/turning-your-raspberry-pi-zero-into-a-usb-gadget/ethernet-gadget
