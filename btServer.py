#!/usr/bin/env python3
"""PyBluez simple example inquiry.py
Performs a simple device inquiry followed by a remote name request of each
discovered device
Author: Albert Huang <albert@csail.mit.edu>
$Id: inquiry.py 401 2006-05-05 19:07:48Z albert $
"""

import bluetooth

print("Performing inquiry...")

nearby_devices = bluetooth.discover_devices(duration=1, lookup_names=True,
                                            flush_cache=True, lookup_class=False)

print("Found {} devices".format(len(nearby_devices)))

counter = 1 
for addr, name in nearby_devices:
    try:
        print("{}.   {} - {}".format(counter, addr, name))
    except UnicodeEncodeError:
        print("{}.   {} - {}".format(counter, addr, name.encode("utf-8", "replace")))
    counter += 1

device_number = int(input("select device number:"))
print(nearby_devices[device_number-1])
bt_addr = nearby_devices[device_number-1][0]

# Create Connection
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = [_ for _ in bluetooth.find_service(address=bt_addr) if 'RFCOMM' in _['protocol']][0]['port']
server_sock.bind((bt_addr, bluetooth.PORT_ANY))
server_sock.listen(1) # What this parameter means?
print("s1")
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            # protocols=[bluetooth.OBEX_UUID]
                            )
print("s2")
client_sock, address = server_sock.accept()
print("s3")
data = client_sock.recv(1024)
print('data:{}'.format(data))
client_sock.close()
server_sock.close()
