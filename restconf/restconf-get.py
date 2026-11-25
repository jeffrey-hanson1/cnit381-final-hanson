import os
import getpass
import requests
import urllib3

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)

switch_ip = "192.168.30.11"
username = "admin"

password = os.getenv("NETWORK_PASSWORD")
if not password:
    password = getpass.getpass("Device password: ")

url = (
    f"https://{switch_ip}/restconf/data/"
    "ietf-interfaces:interfaces"
)

headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

try:
    response = requests.get(
        url,
        auth=(username, password),
        headers=headers,
        verify=False,
        timeout=30
    )

    print(response)
    response.raise_for_status()
    print(response.json())

except requests.exceptions.RequestException as error:
    print(f"RESTCONF request failed: {error}")
    raise SystemExit(1)
