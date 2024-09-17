# Wedding Phone Service

This README explains how to manage the `wedding-phone.service` using systemctl.

## Starting the Service

To start the wedding-phone service, use the following command:

```bash
sudo systemctl start wedding-phone.service
```

## Stopping the Service

To stop the wedding-phone service, use the following command:

```bash
sudo systemctl stop wedding-phone.service
```

## Checking the Service Status

To check the status of the wedding-phone service, use the following command:

```bash
sudo systemctl status wedding-phone.service
```

## Enabling the Service on Boot

To enable the wedding-phone service to start automatically on boot, use the following command:

```bash
sudo systemctl enable wedding-phone.service
```

## Disabling the Service on Boot

To disable the wedding-phone service from starting automatically on boot, use the following command:

```bash
sudo systemctl disable wedding-phone.service
```

## Restarting the Service on `run.py` Change

If you need to make changes to the script, remember to restart the service:

```bash
sudo systemctl restart wedding-phone.service
```

## Viewing Logs

To view the logs of the wedding-phone service, use the following command:

```bash
sudo journalctl -u wedding-phone.service
```

