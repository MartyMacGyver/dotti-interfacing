/*
   Based on Neil Kolban example for IDF: https://github.com/nkolban/esp32-snippets/blob/master/cpp_utils/tests/BLE%20Tests/SampleScan.cpp
   Ported to Arduino ESP32 by Evandro Copercini
*/

#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>
#include <cstring>


int scanTime = 30; //In seconds
BLEAdvertisedDevice currentDevice;
BLEScan * pBLEScan;
const char targetName [] = "Dotti";
bool deviceFound = false;

// The remote service we wish to connect to.
static BLEUUID serviceUUID("0000fff0-0000-1000-8000-00805f9b34fb");
// The characteristic of the remote service we are interested in.
static BLEUUID    charUUID("0000fff3-0000-1000-8000-00805f9b34fb");

static BLEAddress *pServerAddress;
static boolean connected = false;
static BLERemoteCharacteristic* pRemoteCharacteristic;

class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
  void onResult(BLEAdvertisedDevice advertisedDevice) {
    if (advertisedDevice.haveServiceUUID() && !std::strcmp(advertisedDevice.getName().c_str(), targetName)) {
      currentDevice = advertisedDevice;
      pBLEScan->stop();
      deviceFound = true;
    }
  }
};

static void notifyCallback(
  BLERemoteCharacteristic* pBLERemoteCharacteristic,
  uint8_t* pData,
  size_t length,
  bool isNotify) {
    Serial.print("Notify callback for characteristic ");
    Serial.print(pBLERemoteCharacteristic->getUUID().toString().c_str());
    Serial.print(" of data length ");
    Serial.println(length);
}

bool connectToServer(BLEAddress pAddress) {
    Serial.print("Forming a connection to ");
    Serial.println(pAddress.toString().c_str());
    
    BLEClient*  pClient  = BLEDevice::createClient();
    Serial.println(" - Created client");

    // Connect to the remove BLE Server.
    pClient->connect(pAddress);
    Serial.println(" - Connected to server");

    // Obtain a reference to the service we are after in the remote BLE server.
    BLERemoteService* pRemoteService = pClient->getService(serviceUUID);
    if (pRemoteService == nullptr) {
      Serial.print("Failed to find our service UUID: ");
      Serial.println(serviceUUID.toString().c_str());
      return false;
    }
    Serial.println(" - Found our service");


    // Obtain a reference to the characteristic in the service of the remote BLE server.
    pRemoteCharacteristic = pRemoteService->getCharacteristic(charUUID);
    if (pRemoteCharacteristic == nullptr) {
      Serial.print("Failed to find our characteristic UUID: ");
      Serial.println(charUUID.toString().c_str());
      return false;
    }
    Serial.println(" - Found our characteristic");

    // Read the value of the characteristic.
    std::string value = pRemoteCharacteristic->readValue();
    Serial.print("The characteristic value was: ");
    Serial.println(value.c_str());

    pRemoteCharacteristic->registerForNotify(notifyCallback);
    return true;
}

void setup() {
  Serial.begin(115200);
  Serial.println("Scanning...");
  BLEDevice::init("MyESP32");
  pBLEScan = BLEDevice::getScan(); //create new scan
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setActiveScan(true); //active scan uses more power, but get results faster
  BLEScanResults foundDevices = pBLEScan->start(scanTime);
  Serial.print("Devices found: ");
  Serial.println(foundDevices.getCount());
  Serial.println("Scan done!");
}

void loop() {
  if (deviceFound) {
    Serial.printf("Advertised Device: %s \n", currentDevice.toString().c_str());
    Serial.printf("Name: %s \n", currentDevice.getName().c_str());
    Serial.printf("Manufacturer: %s \n", currentDevice.getManufacturerData().c_str());
    Serial.printf("MAC Address: %s \n", currentDevice.getAddress().toString().c_str());
    Serial.printf("Service UUID: %s \n", currentDevice.getServiceUUID().toString().c_str());
    delay(1000);
    pServerAddress = new BLEAddress(currentDevice.getAddress());
    if (connectToServer(*pServerAddress)) {
      Serial.println("We are now connected to the BLE Server.");
      connected = true;
      int cnt = 0;
      while(1) {
        uint8_t pixel_idx = random(0, 64);
        uint8_t color_r = random(0, 2) * 255;
        uint8_t color_g = random(0, 2) * 255;
        uint8_t color_b = random(0, 2) * 255;
        Serial.printf("%d: Pixel %d: #%02X%02X%02X\n", cnt, pixel_idx, color_r, color_g, color_b);
        int cmdBytesLen = 6;
        uint8_t cmdBytes [cmdBytesLen] = {0x07, 0x02, (uint8_t)(pixel_idx + 1), color_r, color_g, color_b};
        //uint8_t cmdBytes [cmdBytesLen] = {0x06, 0x01, color_r, color_g, color_b};
        //uint8_t cmdBytes [cmdBytesLen] = {0x06, 0x01, uint8_t(cnt), 0, 0};
        pRemoteCharacteristic->writeValue(cmdBytes, cmdBytesLen);
        delay(100);
        cnt += 1;
      }
    } else {
      Serial.println("We have failed to connect to the server; there is nothin more we will do.");
    }
  }
  else {
    Serial.printf("Target device not found");
  }
  while (true) {
    delay(2000);
  }
}

