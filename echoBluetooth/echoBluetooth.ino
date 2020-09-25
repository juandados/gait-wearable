//This example code is in the Public Domain (or CC0 licensed, at your option.)
//By Evandro Copercini - 2018
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
  SerialBT.begin("ESP32test21apr"); //Bluetooth device name
  Serial.println("The device started, now you can pair it with bluetooth!");
  pinMode(LED, OUTPUT);
}

void loop() {
  SerialBT.print(millis());
  SerialBT.print("\t");
  SerialBT.print("555");
  SerialBT.println("\t");
  delay(1);
  /*
  delay(500);
  digitalWrite(LED, HIGH);
  delay(500);
  digitalWrite(LED, LOW);
  */
}
