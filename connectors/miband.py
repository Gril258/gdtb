#!/usr/bin/env python2
import struct
import time
import sys
import app

from app.core import Handler

from Crypto.Cipher import AES
from bluepy.btle import Peripheral, DefaultDelegate, ADDR_TYPE_RANDOM

from connectors.constants import AuthenticationConstants, HeartMonitorConstants, HardwareConstants

# MiBand2
#macAdress = "FF:BD:87:9D:70:7C"
# Amazefit Cor
#macAdress = "E5:2F:5A:BE:DC:CA"
# amazfit
macAdress = "d8:ec:bf:c7:8c:8b"

authServiceUUID = AuthenticationConstants.AUTHENTICATION_SERVICE
authCharUUID = AuthenticationConstants.AUTHENTICATION_CHARACTERISTICS
notificationsUUID = AuthenticationConstants.AUTHENTICATION_NOTIFICATIONS

heartMonitorServiceUUID = HeartMonitorConstants.HEART_MONITOR_SERVICE
heartMonitorControlCharacteristicUUID = HeartMonitorConstants.HEART_MONITOR_CONTROL_CHARACTERISTIC
heartRateMeasurementCharacteristicUUID = HeartMonitorConstants.HEART_RATE_MEASUREMENT_CHARACTERISTIC

hardwareServiceUUID = HardwareConstants.HARDWARE_SERVICE
sensorCharacteristicUUID = HardwareConstants.SENSOR_CHARACTERISTIC

class entrypoint(Handler):
    """docstring for entrypoint"""
    async def DoTask(self):
        print("TaskId - MIBAND!!!! = %s" % self.TaskId)
        print("TaskName = %s" % self.TaskName)
        print("TaskData = %s" % self.TaskData)
        self.TaskStatus = "running"
        main()
        await self.UpdateTask()
        return "done"

class Device(Peripheral):
    #key = b'\xf5\xd2\x29\x87\x65\x0a\x1d\x82\x05\xab\x82\xbe\xb9\x38\x59\xcf'
    key = b'\x89\x4a\x9e\x5c\x41\xa3\x3b\xab\x99\x03\x47\xfa\x1d\xee\xa1\x54'
    connectCount = 0

    def __init__(self, macAdress):
    
        while True: 
            try:
                Peripheral.__init__(self, macAdress, ADDR_TYPE_RANDOM)
                print("Connected")
                break
            except:
                if self.connectCount < 5:
                    self.connectCount += 1
                else:
                    sys.exit("Connection failed, try again")
                time.sleep(3)

        #for i in self.getServices():
        #   print(i)

        # Auth service and characteristic
        self.authService = self.getServiceByUUID(authServiceUUID)
        self.authCharacteristics = self.authService.getCharacteristics(authCharUUID)[0]
        self.notifDescriptor = self.authCharacteristics.getDescriptors(notificationsUUID)[0]

        # Heart measurement characteristic
        self.heartMonitorService = self.getServiceByUUID(heartMonitorServiceUUID)
        self.heartMonitorControlCharacteristic = self.heartMonitorService.getCharacteristics(heartMonitorControlCharacteristicUUID)[0]
        self.heartRateMeasurementCharacteristic = self.heartMonitorService.getCharacteristics(heartRateMeasurementCharacteristicUUID)[0]
        self.heartRateMeasurementDescriptor = self.heartRateMeasurementCharacteristic.getDescriptors(notificationsUUID)[0]

        # The other custom service
        self.hardwareService = self.getServiceByUUID(hardwareServiceUUID)
        self.sensorCharacteristic = self.hardwareService.getCharacteristics(sensorCharacteristicUUID)[0]
        print(self.sensorCharacteristic)

        self.authenticationsNotif(True)
        self.waitForNotifications(0.5)

    def authenticationsNotif(self, enable):
        if enable:
            print("Enabling auth notifications")
            self.notifDescriptor.write(b"\x01\x00", True)
            
            # This is needed for the Amazefit COR pairing!!!
            self.sendKey()
            self.waitForNotifications(2)
        elif not enable:
            print("Disabling auth notifications")
            self.notifDescriptor.write(b"\x00\x00", True)
        else:
            print("Changing authentication notifications failed")

    def authenticate(self):
        print("Authenticating...")
        self.setDelegate(AuthenticationDelegate(self))
        print("Requesting random key...")

        requestRandomKey = struct.pack('<2s', b'\x02\x00\x02')

        print("key request")
        for i in requestRandomKey:
            print(ord(i))
        
        self.authCharacteristics.write(requestRandomKey)
        self.waitForNotifications(5.0)

    def sendEncryptedKey(self, randomKey):
        sendEncKeyCommand = struct.pack('<2s', b"\x03\x00")
        command = sendEncKeyCommand + self.encryptKey(randomKey)

        sendCommand = struct.pack("<18s", command)

        print("Sending encrypted random key")
        print(sendCommand)
        self.authCharacteristics.write(sendCommand)
        self.waitForNotifications(5)

    def encryptKey(self, randomKey):
        print("Encrypting the key...")
        aes = AES.new(self.key, AES.MODE_ECB)
    
        return aes.encrypt(randomKey)

    # this fcuntion is called when the devices are paired I guess
    def sendKey(self):
        print("Sending a key...?")
        sendKeyCommand = struct.pack("<18s", b"\x01\x00" + self.key)
        self.authCharacteristics.write(sendKeyCommand)
        self.waitForNotifications(2)

    def getRealTimeHeartRate(self):
        print("Realtime heart rate measurement:")
        # First, we Need to turn one-shot and continuous heart measurements off
        # by sending 15 01 00 and 15 02 00 to Heart Rate Control
        # 15 01 00 for oneshot; 15 02 00 for continuous?
        self.heartMonitorControlCharacteristic.write(b"\x15\x01\x00", True)
        self.heartMonitorControlCharacteristic.write(b"\x15\x02\x00", True)
        # enabling gyroscope and and heart raw data  by sending 01 03 19 by sending command to sensor char
        self.sensorCharacteristic.write(b"\x01\x03\x19")
        # enabling Heart Rate notifications on by sendin 01 00 to Heart Measurement descriptor
        self.heartRateMeasurementDescriptor.write(b"\x01\x00", True)
        # starting continuous Heart Rate measurement by sending 15 01 01 to Heart Rate Control
        self.heartMonitorControlCharacteristic.write(b"\x15\x01\x01", True)
        # then, need to send 02 to sensor characteristics... don't know why
        self.sensorCharacteristic.write(b"\x02")

        t = time.time()
        while True:
            self.waitForNotifications(0.5)
            # Need to refresh the connection, otherwise it disconnects us
            if time.time() - t >= 12:
                self.heartMonitorControlCharacteristic.write(b"\x16", True)
                t = time.time()

    def getOneShotHeartRate(self):
        # Stop continuous and manual measuring
        print("Trying to get saved heart rate data")
        self.heartMonitorControlCharacteristic.write(b"\x15\x01\x00", True)
        self.heartMonitorControlCharacteristic.write(b"\x15\x02\x00", True)
        # Start manual measuring
        self.heartMonitorControlCharacteristic.write(b'\x15\x02\x01', True)

        self.waitForNotifications(30)


class AuthenticationDelegate(DefaultDelegate):

    def __init__(self, device):
        DefaultDelegate.__init__(self)
        self.device = device

    def handleNotification(self, handle, data):
        if(handle == self.device.authCharacteristics.getHandle()):
            print("Response: hnd + data " + str(handle), data)
        # Handling MiBand2 response at Auth handle (84)
        # first 3? bytes are the auth response
            if data[:3] == b"\x10\x01\x01":
                print("Recieved: Auth initialized!")

            elif data[:3] == b"\x10\x01\x04":
                print("Recieved: Auth key send failed")

            elif data[:3] == b"\x10\x02\x01":
                print("Recieved: Request random key OK")
                
                randomKey = data[3:]

                self.device.sendEncryptedKey(randomKey)

            elif data[:3] == b"\x10\x02\x04":
                print("Recieved: Error random number error")

            elif data[:3] == b"\x10\x03\x01":
                print("Recieved: Authorization complete")
                time.sleep(0.5)

                # Sending message notification to alert service
                # test thing - need to test if the connection won't drop
                # ------------------------------------------------------
                alertService = self.device.getServiceByUUID("00001802-0000-1000-8000-00805f9b34fb")
                alertCharacteristic = alertService.getCharacteristics("00002a06-0000-1000-8000-00805f9b34fb")[0]
                alertTypeMessage = b'\x01'
                
                """i=0
                while True:
                  i = i + 1
                  alertCharacteristic.write(alertTypeMessage)
                  time.sleep(3)
                  if i == 5:
                    break
                """

                self.device.getRealTimeHeartRate()
                #self.device.getOneShotHeartRate()
                time.sleep(5)

            elif data[:3] == b"\x10\x03\x04":
                print("Recieved: Encrypted key error")
                self.device.sendKey()

            else:
                print("Unknown response")
                print("data: " + data)
                for i in data:
                    print(str(ord(i)))
                print(data[:3])
        
        elif (handle == self.device.heartRateMeasurementCharacteristic.getHandle()):
            #print("Heart rate: " + struct.unpack('HHHHHHH', data[2:]))
            print("Heart rate: " + str(ord(data[1])))


        else:
            print("Response from different handle")
            print("Handle: " + str(handle))
            print("Respose data: " + data)



def main():

    print('Connecting to ' + macAdress)
    connectedDevice = Device(macAdress)
    connectedDevice.setSecurityLevel(level="medium")

    connectedDevice.authenticate()

    connectedDevice.disconnect()


if __name__ == "__main__":
    main()

# authentication service    - 0000fee1-0000-1000-8000-00805f9b34fb
# authentication cahracteristic - 00000009-0000-3512-2118-0009af100700
# notification descriptor       - 0x2902

#_send_key_cmd = struct.pack('<18s', b'\x01\x08' + _KEY)
#_send_rnd_cmd = struct.pack('<2s', b'\x02\x08')
#_send_enc_key = struct.pack('<2s', b'\x03\x08')
