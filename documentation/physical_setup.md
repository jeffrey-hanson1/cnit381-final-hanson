# Physical Network Setup

## Cabling Plan

| Device | Interface | Connected Device | Interface |
|---|---|---|---|
| Router1 | Gi0/0/0 | Router2 | Gi0/0/0 |
| Router1 | Gi0/0/1 | Router3 | Gi0/0/0 |
| Router2 | Gi0/0/1 | Router3 | Gi0/0/1 |
| Router2 | Gi0/0/2 | Switch1 | Gi1/0/1 |
| Switch1 | Gi1/0/24 | Switch2 | Gi1/0/24 |
| Switch1 | Gi1/0/2 | DEVASC | Network Adapter |

## Management Addresses

| Device | IP Address |
|---|---|
| Router1 | 10.0.12.1 |
| Router2 | 192.168.30.2 |
| Router3 | 10.0.23.2 |
| Switch1 | 192.168.30.11 |
| Switch2 | 192.168.30.12 |
| DEVASC | 192.168.30.100 |

DEVASC subnet mask: 255.255.255.0
DEVASC gateway: 192.168.30.2

## VLANs

- VLAN 10: DATA
- VLAN 20: VOICE
- VLAN 30: MANAGEMENT

## Pre-deployment Requirements

- Confirm physical interface availability.
- Confirm DEVASC management IP is unused.
- Configure management interfaces and SSH.
- Establish management VLAN and trunk connectivity.
- Establish initial return routes on Router1 and Router3.
- Verify connectivity to all five devices before running Ansible.
- Never store actual passwords in the public repository.

## Router1 Initial Console Configuration

Replace YOUR_NETWORK_PASSWORD with your actual lab password
at the physical console. Do not save the password in this file.

```text
enable
configure terminal
hostname Router1
ip domain-name cnit381.lab
username admin privilege 15 secret YOUR_NETWORK_PASSWORD
crypto key generate rsa modulus 2048
ip ssh version 2

line vty 0 4
login local
transport input ssh
exit

interface GigabitEthernet0/0/0
description Link to Router2
ip address 10.0.12.1 255.255.255.252
no shutdown
exit

ip route 192.168.30.0 255.255.255.0 10.0.12.2

end
write memory
```

### Router1 Verification

```text
show ip interface brief
show ip ssh
show ip route
```

The static management return route is temporary.
Remove it after EIGRP connectivity is verified.

## Router2 Initial Console Configuration

Replace YOUR_NETWORK_PASSWORD with the same lab password
used on Router1.

```text
enable
configure terminal
hostname Router2
ip domain-name cnit381.lab
username admin privilege 15 secret YOUR_NETWORK_PASSWORD
crypto key generate rsa modulus 2048
ip ssh version 2

line vty 0 4
login local
transport input ssh
exit

interface GigabitEthernet0/0/0
description Link to Router1
ip address 10.0.12.2 255.255.255.252
no shutdown
exit

interface GigabitEthernet0/0/1
description Link to Router3
ip address 10.0.23.1 255.255.255.252
no shutdown
exit

interface GigabitEthernet0/0/2
description Trunk to Switch1
no shutdown
exit

interface GigabitEthernet0/0/2.30
description Management VLAN Gateway
encapsulation dot1Q 30
ip address 192.168.30.2 255.255.255.0
exit

end
write memory
```

### Router2 Verification

```text
show ip interface brief
show ip ssh
show ip route
```

## Router3 Initial Console Configuration

Replace YOUR_NETWORK_PASSWORD with the same lab password
used on Router1 and Router2.

```text
enable
configure terminal
hostname Router3
ip domain-name cnit381.lab
username admin privilege 15 secret YOUR_NETWORK_PASSWORD
crypto key generate rsa modulus 2048
ip ssh version 2

line vty 0 4
login local
transport input ssh
exit

interface GigabitEthernet0/0/1
description Link to Router2
ip address 10.0.23.2 255.255.255.252
no shutdown
exit

ip route 192.168.30.0 255.255.255.0 10.0.23.1

end
write memory
```

### Router3 Verification

```text
show ip interface brief
show ip ssh
show ip route
```

The static management return route is temporary.
Remove it after EIGRP connectivity is verified.

## Switch1 Initial Console Configuration

Replace YOUR_NETWORK_PASSWORD with the same lab password
used on the routers.

```text
enable
configure terminal
hostname Switch1
ip domain-name cnit381.lab
username admin privilege 15 secret YOUR_NETWORK_PASSWORD
crypto key generate rsa modulus 2048
ip ssh version 2

line vty 0 15
login local
transport input ssh
exit

vlan 30
name MANAGEMENT
exit

interface Vlan30
description Management VLAN
ip address 192.168.30.11 255.255.255.0
no shutdown
exit

ip default-gateway 192.168.30.2

interface GigabitEthernet1/0/1
description Trunk to Router2
switchport mode trunk
switchport trunk allowed vlan 30
no shutdown
exit

interface GigabitEthernet1/0/24
description Trunk to Switch2
switchport mode trunk
switchport trunk allowed vlan 30
no shutdown
exit

interface GigabitEthernet1/0/2
description DEVASC Management Connection
switchport mode access
switchport access vlan 30
spanning-tree portfast
no shutdown
exit

end
write memory
```

### Switch1 Verification

```text
show ip interface brief
show vlan brief
show interfaces trunk
show ip ssh
ping 192.168.30.2
```

## Switch2 Initial Console Configuration

Replace YOUR_NETWORK_PASSWORD with the same lab password
used on the other four devices.

```text
enable
configure terminal
hostname Switch2
ip domain-name cnit381.lab
username admin privilege 15 secret YOUR_NETWORK_PASSWORD
crypto key generate rsa modulus 2048
ip ssh version 2

line vty 0 15
login local
transport input ssh
exit

vlan 30
name MANAGEMENT
exit

interface Vlan30
description Management VLAN
ip address 192.168.30.12 255.255.255.0
no shutdown
exit

ip default-gateway 192.168.30.2

interface GigabitEthernet1/0/24
description Trunk to Switch1
switchport mode trunk
switchport trunk allowed vlan 30
no shutdown
exit

end
write memory
```

### Switch2 Verification

```text
show ip interface brief
show vlan brief
show interfaces trunk
show ip ssh
ping 192.168.30.11
ping 192.168.30.2
```

## DEVASC Network Setup

1. Connect the laptop Ethernet adapter to Switch1 Gi1/0/2.
2. Configure the DEVASC VirtualBox network adapter in Bridged mode.
3. Select the physical Ethernet adapter connected to Switch1.
4. Configure the following IPv4 settings inside DEVASC:

- IP address: 192.168.30.100
- Subnet mask: 255.255.255.0
- Gateway: 192.168.30.2

Confirm the address is available before assigning it.
Record the original VM network settings before changing them.

## Connectivity Verification

Run the following commands from DEVASC:

```bash
ip addr
ip route
ping -c 4 192.168.30.2
ping -c 4 192.168.30.11
ping -c 4 192.168.30.12
ping -c 4 10.0.12.1
ping -c 4 10.0.23.2
```

Verify SSH access to all five devices:

```bash
ssh admin@10.0.12.1
ssh admin@192.168.30.2
ssh admin@10.0.23.2
ssh admin@192.168.30.11
ssh admin@192.168.30.12
```

Exit each SSH session before connecting to the next device.

## Start Ansible Verification

```bash
cd ~/cnit381-final-hanson
read -rsp "Network password: " NETWORK_PASSWORD
echo
export NETWORK_PASSWORD
ansible-playbook playbooks/01_verify_connectivity.yml
```

Confirm all five devices are reachable before proceeding
to the remaining playbooks.

## RESTCONF Setup on Switch1

After completing the Ansible playbooks, enable RESTCONF
on Switch1 using the following console commands:

```text
enable
configure terminal
ip http authentication local
ip http secure-server
restconf
end
write memory
```

## Postman GET Test

Method: GET

URL:
https://192.168.30.11/restconf/data/ietf-interfaces:interfaces

Authorization: Basic Auth
Username: admin
Password: Actual lab password

Headers:
Accept: application/yang-data+json
Content-Type: application/yang-data+json

Expected result: 200 OK

## Postman PUT Test

Method: PUT

URL:
https://192.168.30.11/restconf/data/ietf-interfaces:interfaces/interface=Loopback1

Use the same authentication and headers as the GET request.
Select Body, raw, JSON.
Paste the contents of restconf/loopback1.json.

Expected result: 201 Created

Confirm Loopback1 does not already exist before the PUT test.

## Switch1 CLI Verification

```text
show ip interface brief | include Loopback1
```

Expected IP address: 10.4.1.1

## Python RESTCONF Verification

From DEVASC, run:

```bash
cd ~/cnit381-final-hanson
python3 restconf/restconf-get.py
```

Expected result: Response [200] and JSON interface data.

Certificate verification may be disabled for the isolated
lab test if the switch uses a self-signed certificate.
Do not expose credentials in submission screenshots.

## RESTCONF Screenshot Evidence

- Successful Postman GET response
- Successful Postman PUT showing 201 Created
- Switch1 CLI showing Loopback1
- Successful Python RESTCONF GET response
