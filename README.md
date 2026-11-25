# CNIT 381 Final Project - Network Automation

## Student Information
- Student: Jeffrey Hanson
- Course: CNIT 381
- Semester: Fall 2026
- University: University of Wisconsin-Stout

## Project Overview

This project automates the configuration and management of three Cisco ISR 4331 routers and two Catalyst 3650 switches. Ansible provides automated device configuration, EIGRP routing, VLAN configuration, network services, and configuration backups. RESTCONF provides programmatic access to switch interfaces. Docker and GitHub Actions provide automated configuration generation and IP address validation.

## Network Topology

The network uses a triangular router topology with EIGRP AS 100 and three VLANs.

| Device | Management IP |
|---|---|
| Router1 | 10.0.12.1 |
| Router2 | 192.168.30.2 |
| Router3 | 10.0.23.2 |
| Switch1 | 192.168.30.11 |
| Switch2 | 192.168.30.12 |

| VLAN | Name | Subnet |
|---|---|---|
| 10 | DATA | 192.168.10.0/24 |
| 20 | VOICE | 192.168.20.0/24 |
| 30 | MANAGEMENT | 192.168.30.0/24 |

## Prerequisites

- DEVASC virtual machine
- Ansible
- Python 3
- Docker
- Git
- Postman
- SSH connectivity to all five Cisco devices

## Authentication

Device passwords are supplied through an environment variable and are not stored in the public repository.

```bash
read -s -p "Device password: " NETWORK_PASSWORD
export NETWORK_PASSWORD
echo
```

## Ansible Automation

Run the following playbooks in order after establishing initial management connectivity.

```bash
ansible-playbook playbooks/01_verify_connectivity.yml
ansible-playbook playbooks/02_base_config.yml
ansible-playbook playbooks/03_eigrp_config.yml
ansible-playbook playbooks/04_vlan_config.yml
ansible-playbook playbooks/05_services_config.yml
ansible-playbook playbooks/06_backup_config.yml
```

| Playbook | Purpose |
|---|---|
| 01 | Verify device connectivity |
| 02 | Configure hostnames, interfaces and banners |
| 03 | Configure EIGRP and router loopbacks |
| 04 | Configure VLANs and trunk interfaces |
| 05 | Configure NTP and buffered logging |
| 06 | Back up running configurations |

## RESTCONF

Switch1 is used for RESTCONF operations.

GET endpoint:

```text
https://192.168.30.11/restconf/data/ietf-interfaces:interfaces
```

PUT endpoint:

```text
https://192.168.30.11/restconf/data/ietf-interfaces:interfaces/interface=Loopback1
```

The PUT request uses the JSON payload in
`restconf/loopback1.json` to create Loopback1.

Run the Python GET script:

```bash
python3 restconf/restconf-get.py
```

## Docker Configuration Pipeline

```bash
cd config-pipeline
docker build -t config-pipeline .
docker run --rm config-pipeline
cd ..
```

The pipeline validates IP addresses, detects duplicates,
and generates device configurations using YAML and Jinja2.

## GitHub Actions

The CI workflow automatically validates and generates
network configurations on pushes and pull requests.

An intentional duplicate IP address was introduced to
verify that the workflow correctly detects invalid
configurations. The duplicate was corrected and the
workflow subsequently passed.

## Documentation

- [Network Diagram](documentation/network_diagram.pdf)
- [Project Whitepaper](documentation/whitepaper.pdf)
- [Testing Results](documentation/testing_results.md)

## Project Status

- Ansible playbooks prepared
- RESTCONF scripts prepared
- Python and JSON syntax validated
- Docker configuration pipeline tested
- GitHub Actions failure and recovery verified
- Branch and pull request completed
- Network diagram prepared
- Whitepaper draft prepared
- Physical equipment deployment and testing pending

