# D-Link-DDNS-IP-Updater
A Python script that updates the public IP address to the D-Link DDNS service.

## Motivation
If you have a D-Link router and your Internet service provider (ISP) applies carrier-grade NAT (or large-scale NAT), the IP address your router got assigned 
is from the Shared Address Space (100.64.0.0/10). Thus, a home server in your private network is not reachable from the outside. 
The public IP address is different and may change independently from the IP address your router got assigned. 
Therefore, the dynamic DNS solutions offered by D-Link are obsolete, since your router does not realize when your public IP address changes.
Depending on the ISP, it might be possible to access your services in your private network through your public IP address. 
If that is the case, you only have to update your public IP address to the D-Link DDNS service whenever it changes.
I therefore wrote a Python script that fetches the public IP address and sends it to the D-Link DDNS service.

## Installation

Clone this repository
```
	git clone https://github.com/philip-raschke/D-Link-DDNS-IP-Updater.git
```

Install dependencies
```
	apt-get install python python-dev libffi-dev
```

Run the setup.py
```
	python setup.py install
```

Write your D-Link DDNS credentials into the credentials file
```
	username
	password
```

Run the Python script to update your IP address
```
	python ip-updater.py
```
