---
id: networking
title: Networking
---

## Specs

Network card: [**BCM43438**](https://www.raspberry-pi-geek.com/Archive/2016/17/Raspberry-Pi-3-Model-B-in-detail#:~:text=The%20Broadcom%20BCM43438%20WiFi%2FBluetooth,not%20enabled%20on%20the%20Pi.)

:::caution
It does **not** support 5GHz
:::

## Connecting to a Wireless Network (Incomplete)

1. Add credentials
    ```bash
    wpa_passphrase <ssid> <password> >> /etc/wpa_supplicant/wpa_supplicant.conf
    ```
    :::warning
    This will also add the raw passphrase into the `.conf` file as a comment. A good practice would be to remove that line of comment
    :::

    :::note
    This would only work for **WPA** networks and not **WPA-Enterprise** networks (e.g. `NUS_STU`)
    :::
    
2. Reboot RPI
    ```bash
    sudo reboot
    ```

## References

- https://wiki.archlinux.org/title/wpa_supplicant

