import asyncio

from bleak import BleakClient, BleakScanner
from bleak.assigned_numbers import CharacteristicPropertyName
from bleak.backends import device
from bleak.backends.service import BleakGATTService
from bleak.exc import BleakError


async def scan_ble_devices() -> None:
    """
    Prints out all the BLE devices available for connection.
    Prints out their name and Bluetooth MAC Address
    """
    print("Scanning...")
    devices: list[device.BLEDevice] = await BleakScanner.discover()

    if not devices:
        print("No BLE devices found")
        return

    print(f"Found {len(devices)} devices")
    for d in devices:
        print(f"  Name: {d.name if d.name else 'N/A'}, Address: {d.address}")

async def get_all_charcateristics(address : str) -> None:
    """
    Prints out all the data on what queries can be made to the given device.\n
        'address' paramater is the Bluetooth MAC Address
    """
    # Connect
    async with BleakClient(address) as client:
        # If the Connection failed
        if not client.is_connected:
            print("Failed to connect")
            return

        # Connected
        print(f"Connected to {client.name if client.name else client.address}")
        print("Services")
        # List through the services
        for service in client.services:
            print(f"UUID: {service.uuid}")
            print(f"Handle: {service.handle}")
            print(f"Description: {service.description}")
            print("    Characterists:")
            # List through the characteristics
            for characteristic in service.characteristics:
                print(f"        UUID: {characteristic.uuid}")
                print(f"        Handle: {characteristic.handle}")
                print(f"        Description: {characteristic.description}")
                print(f"        Max Write Size: {characteristic.max_write_without_response_size}")
                print("        Descriptiors:")
                # List through the descriptors of these characteristics
                for desc in characteristic.descriptors:
                    print(f"            UUID: {desc.uuid}")
                    print(f"            Handle: {desc.handle}")
                    print(f"            Description: {desc.description}")
                    print()
                print("        Properties:")
                #List through the descriptor's properties
                for prop in characteristic.properties:
                    print(f"            {prop}")
                print()
            print("-" * 20)

def notification_handler(sender, data):
    print(f"Notification from {sender}: {data}")

async def get_all_characteristic_values(address : str, service_handle : int) -> None:
    """
    Gets all the characteristic values of a certain service on a device\n
    Only gets the value of characteristics with the 'read' property\n
        'address' is the Bluetooth MAC Address of the device\n
        'service_handle' should be the handle of the service
    """
    # Connect
    async with BleakClient(address, use_cached_services=False, pair=True) as client:
        # If not Connected
        if not client.is_connected:
            print("Failed to connect")
            return

        print(f"Connected to {client.name if client.name else client.address}")

        # Get the service
        targeted_service : BleakGATTService
        for service in client.services:
            if service.handle != service_handle:
                continue

            print(f"Found service: {service_handle}\n")
            targeted_service = service
            break
        else:
            print(f"Could not find service: {service_handle}")
            return

        # Now we can read each characteristic
        for characteristic in targeted_service.characteristics:
            # PRint basic info
            print(f"Characteristic: {characteristic.handle}")
            print(f"Description: {characteristic.description}")

            # Check the characteristic supports read first
            can_read : bool = "read" in characteristic.properties
            if not can_read:
                print("Does not support read")
                #continue

            # Read from charcateristic
            try:
                char_value = await client.read_gatt_char(characteristic.uuid)
                print(f"value: {char_value}")
            except BleakError as e:
                print(f"Error Reading: {str(e)}")

            print()

async def test():
     async with BleakClient("FD:D3:9D:E7:40:E0") as client:
         print(client.is_connected)
         await asyncio.sleep(1)
         print(client.is_connected)
         e = await client.read_gatt_char("11a70301-f691-4b93-a6f4-0968f5b648f8")
         print(e)

if __name__ == "__main__":
    asyncio.run(test())
