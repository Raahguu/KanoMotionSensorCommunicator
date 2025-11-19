import asyncio

from bleak import BleakClient, BleakScanner
from bleak.assigned_numbers import CharacteristicPropertyName
from bleak.backends import device


async def scan_ble_devices() -> None:
    print("Scanning...")
    devices: list[device.BLEDevice] = await BleakScanner.discover()

    if not devices:
        print("No BLE devices found")
        return

    print(f"Found {len(devices)} devices")
    for d in devices:
        print(f"  Name: {d.name if d.name else 'N/A'}, Address: {d.address}")

async def get_all_charcateristics(address : str) -> None:
    async with BleakClient(address) as client:
        if not client.is_connected:
            print("Failed to connect")
            return

        print(f"Connected to {client.name if client.name else client.address}")
        print("Services")
        for service in client.services:
            print(f"UUID: {service.uuid}")
            print(f"Handle: {service.handle}")
            print(f"Description: {service.description}")
            print("    Characterists:")
            for characteristic in service.characteristics:
                print(f"        UUID: {characteristic.uuid}")
                print(f"        Handle: {characteristic.handle}")
                print(f"        Description: {characteristic.description}")
                print("        Descriptiors:")
                for desc in characteristic.descriptors:
                    print(f"            UUID: {desc.uuid}")
                    print(f"            Handle: {desc.handle}")
                    print(f"            Description: {desc.description}")
                    print()
                print("        Properties:")
                for prop in characteristic.properties:
                    print(f"            {prop}")
                print()
            print("-" * 20)



if __name__ == "__main__":
    asyncio.run(get_all_charcateristics("FD:D3:9D:E7:40:E0"))
