# Wedding Phone Service

[![Python](https://img.shields.io/static/v1?label=built+with&message=Python+3.11&color=2b5b84)](https://www.python.org/)

An app to record audio guest book entries with a retro phone.




## Run on Raspberry Pi as a Service

This section explains how to manage the `wedding-phone.service` using systemctl.

### Clone the repository

Clone this repository to your Raspberry Pi. And setup a new service file.

```bash
sudo nano /etc/systemd/system/wedding-phone.service
```

Add the following content to the service file and make sure to change the `ExecStart` line to point to the location of `run.py` on your Pi.

```ini
[Unit]
Description=Run Python Script on Boot
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/wedding/Development/gpio-test/run.py
WorkingDirectory=/home/wedding/Development/gpio-test
StandardOutput=inherit
StandardError=inherit
Restart=always
User=wedding

[Install]
WantedBy=multi-user.target
```

### Connect the GPIO pins

Connect the receiver pins to the GPIO pins as follows:

- GPIO 4 --> Pull-down resistor (10kΩ) --> GND
- GPIO 4 --> switch side 1
- switch side 2 --> 3.3V

### Use USB Sound Card

Use a USB Sound Card to connect the reciever microphone and speaker.

For example the [Icy Box IB-AC527](https://www.digitec.ch/de/s1/product/icy-box-ib-ac527-usb-20-soundkarte-5724945)

### Starting the Service

To start the wedding-phone service, use the following command:

```bash
sudo systemctl start wedding-phone.service
```

### Stopping the Service

To stop the wedding-phone service, use the following command:

```bash
sudo systemctl stop wedding-phone.service
```

### Checking the Service Status

To check the status of the wedding-phone service, use the following command:

```bash
sudo systemctl status wedding-phone.service
```

### Enabling the Service on Boot

To enable the wedding-phone service to start automatically on boot, use the following command:

```bash
sudo systemctl enable wedding-phone.service
```

### Disabling the Service on Boot

To disable the wedding-phone service from starting automatically on boot, use the following command:

```bash
sudo systemctl disable wedding-phone.service
```

### Restarting the Service on `run.py` Change

If you need to make changes to the script, remember to restart the service:

```bash
sudo systemctl restart wedding-phone.service
```

### Viewing Logs

To view the logs of the wedding-phone service, use the following command:

```bash
sudo journalctl -u wedding-phone.service
```

