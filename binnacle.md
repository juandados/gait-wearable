# First Steps
## Install the Arduino IDE 
* following instructions from [here](https://www.arduino.cc/en/guide/linux).
* to give premissions over the usb port ```sudo chmod a+rw /dev/ttyUSB*``` Notice this should be run anytime the usb board is disconnected.
* To fix the no module named Serial error install pyserial ```pip install pyserial```
## Install the ESP32 board in arduino.
* Go to (file>>preferences), paste the board manager URL https://dl.espressif.com/dl/package_esp32_index.json
* Go to tools>>boards>>boards manager, search for ESP 32 and install (ESP32 by Espressif systems)
## Select the board
* When working with ESP-WROOM-32 board (schematics [here](/home/juan/Desktop/ESP32/SchematicsforESP32.pdf)), use the board Node32S (tools>>board>>Node32S).
* Select the port /dev/ttyUSB0 (tools>>port>>/dev/ttyUSB0).
* The upload speed is 921600 (tools>>upload speed>>921600).

# Bluethoot
## Arduino Side

```
//This example code is in the Public Domain (or CC0 licensed, at your option.)
//By Juan Chacon Based on (Evandro Copercini - 2018)
//
//This example creates a bridge between Serial and Classical Bluetooth (SPP)
//and also demonstrate that SerialBT have the same functionalities of a normal Serial

#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif
#define LED 2

BluetoothSerial SerialBT;
void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32test0"); //Bluetooth device name
  Serial.println("The device started, now you can pair it with bluetooth!");
  pinMode(LED, OUTPUT);
}

void loop() {
  SerialBT.println('0');
  delay(500);
  digitalWrite(LED, HIGH);
  delay(500);
  digitalWrite(LED, LOW);
}
```

## Python Side
### Connecting Bluethoot to a server [[ref]](https://github.com/pybluez/pybluez/blob/master/examples/simple/rfcomm-server.py#L10)
#### Install python bluetooth related modules
```
sudo apt-get update
sudo apt-get install python-pip python-dev ipython
sudo apt-get install bluetooth libbluetooth-dev
pip install pybluez
```
### Solving issue bluetooth.btcommon.BluetoothError: (2, 'No such file or directory')
Running bluetooth in compatibility mode:

by modifying /etc/systemd/system/dbus-org.bluez.service,

Changing `ExecStart=/usr/lib/bluetooth/bluetoothd` into `ExecStart=/usr/lib/bluetooth/bluetoothd -C`
Then adding the Serial Port Profile, executing: `sudo sdptool add SP`
Make sure you run the following after doing this:
1. `systemctl daemon-reload`
2. `service bluetooth restart`

**Note:** It seems that one can pair upto seven devices in bluetooth network, when scanning the available devices they could not be connected to another network.

### Paring Bluetooth Devices by terminal [[ref]](https://www.youtube.com/watch?v=F5-dV6ULeg8)
1. turn on the bluetooth device.
2. run the bluetooth controller: `sudo bluetoothctl`.
3. check bluetooth is on: `power on`.
4. register an agent: `agent on`.
5. check default agent: `default-agent`.
6. scan for available devices: (may take a while) `scan on`.
7. pair device: ``pair MAC ADDRESS``.
8. accept pairing.


# Option 1: Using bluetooth with python directly [[ref]](http://pages.iu.edu/~rwisman/c490/html/pythonandbluetooth.htm)
```python
from bluetooth import * 
client_socket=BluetoothSocket( RFCOMM )                                               
client_socket.connect(("24:6F:28:B0:2B:1A",1))                                        
while True:
    data = client_socket.recv(1024)                                                       
    print(data)
client_socket.close()
```

## Discovering devices with python
```python
from bluetooth import *
devices = discover_devices()
for device in devices:
    print([_ for _ in find_service(address=device) if 'RFCOMM' in _['protocol'] ])
```

# Option 2: Using bluetooth to serial map [[ref]](https://www.youtube.com/watch?v=rxExVsxI9jc)
With this method we are able to connect one device at a time making, it still does not convince me as requiere connect and disconect resources.
1. To get the devices details run `hcitool scan`
2. Using the device mask, connect it by running
`sudo rfcomm connect /dev/rfcommX 24:6F:28:96:A3:B2`
where X is the channel we want to use
3. Run the [blueSerial.py](/home/juan/Desktop/ESP32/blueSerial.py) file as sudo
` sudo /home/juan/anaconda3/bin/python3.7 blueSerial.py
Notice this example will uses to bluetooth devices and print the results
**Note**: Coolterm is an useful tool to test bluetooth connection
**Note**: When resources bussy ```sudo lsof | grep /dev/rfcomm*``` kill by PID: `kill -9 PID`


# Using the Accelerometer [[ref]](https://www.youtube.com/watch?v=wTfSfhjhAU0)[[ref2]](https://www.youtube.com/watch?v=UxABxSADZ6U)
This is based on the Jrowberg code, using the [MPU6050 library](https://github.com/jrowberg/i2cdevlib/tree/master/Arduino/MPU6050) and the [I2Cdev library](https://github.com/jrowberg/i2cdevlib/tree/master/Arduino/I2Cdev), this two libraries should be included going to **sketch>>include library>>add zip library...**
This are some modifications to the example 
```c++
#define SCL 4
#define SDA 15
#define INTERRUPT_PIN 2
#define LED_PIN 22
// comment Wire.begin() and wire.setClock(400000) by
Wire.begin(SDA, SCL, 400000);
// replace pinMode(INTERRUPT_PIN, INPUT); by
pinMode(INTERRUPT_PIN, INPUT_PULLUP);
```
after copying the example example>MPU6050>MP6090_DMP6 there are two errors to fix:
1. comment in file "~/Arduino/libraries/MPU6050_6Axis_MotionApps20.h" duplicated typedefs int8_t to uint32_t.
2. in the file "~/Arduino/libraries/MPU6050/MPU6050.cpp" add at the begining the variable BUFFER_LENGTH
```c++
#ifndef BUFFER_LENGTH
#define BUFFER_LENGTH 129
#endif
```
