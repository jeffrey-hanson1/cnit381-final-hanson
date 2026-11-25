import ipaddress
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "configs"


def validate_devices(devices):
    used_ips = {}
    errors = []

    for device in devices:
        for interface in device["interfaces"]:
            if "ip" not in interface:
                continue

            location = (
                f'{device["hostname"]} {interface["name"]}'
            )

            try:
                address = ipaddress.IPv4Interface(interface["ip"])
                ip = str(address.ip)

                if ip in used_ips:
                    errors.append(
                        f"Duplicate IP {ip}: "
                        f"{used_ips[ip]} and {location}"
                    )
                else:
                    used_ips[ip] = location

            except ValueError:
                errors.append(
                    f'Invalid IP {interface["ip"]} on {location}'
                )

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        sys.exit(1)

    print("IP validation passed.")


def main():
    with open(BASE_DIR / "devices.yml") as file:
        devices = yaml.safe_load(file)["devices"]

    validate_devices(devices)

    env = Environment(
        loader=FileSystemLoader(str(BASE_DIR)),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True
    )

    env.filters["ip_address"] = (
        lambda value: str(ipaddress.IPv4Interface(value).ip)
    )

    env.filters["subnet_mask"] = (
        lambda value: str(ipaddress.IPv4Interface(value).netmask)
    )

    template = env.get_template("template.j2")
    OUTPUT_DIR.mkdir(exist_ok=True)

    for device in devices:
        config = template.render(device=device)
        output = OUTPUT_DIR / f'{device["hostname"]}.cfg'
        output.write_text(config + "\n")
        print(f"Generated: {output.name}")

    print("Configuration generation completed successfully.")


if __name__ == "__main__":
    main()
