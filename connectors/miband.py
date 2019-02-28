#!/usr/bin/env python2
import struct
import time
import sys
import app

from Crypto.Cipher import AES
from bluepy.btle import Peripheral, DefaultDelegate, ADDR_TYPE_RANDOM

from constants import AuthenticationConstants

# MiBand2
#macAdress = "FF:BD:87:9D:70:7C"

#macAdress = "DB:EA:52:5D:C5:C4"
macAdress = "FF:BD:87:9D:70:7C"

#macAdress = "DB:EA:52:5D:C5:C4"
macAdress = "D8:EC:BF:C7:8C:8B"
# Amazefit Cor
#macAdress = "E5:2F:5A:BE:DC:CA"

authServiceUUID = AuthenticationConstants.AUTHENTICATION_SERVICE
authCharUUID = AuthenticationConstants.AUTHENTICATION_CHARACTERISTICS
notificationsUUID = AuthenticationConstants.AUTHENTICATION_NOTIFICATIONS

@app.core.hander.DoTask()
def start():
    print("doing task")
    return "did it"

class entrypoint(app.core.Handler):
    """docstring for entrypoint"""
    async def DoTask(self):
        print("TaskId - MIBAND!!!! = %s" % self.TaskId)
        print("TaskName = %s" % self.TaskName)
        print("TaskData = %s" % self.TaskData)
        self.TaskStatus = "running"
        call = "%s(self.TaskData)"
        result = eval(call)
        await self.UpdateTask()
        return "done"

class Device(Peripheral):
    #key = b'\xf5\xd2\x29\x87\x65\x0a\x1d\x82\x05\xab\x82\xbe\xb9\x38\x59\xcf'
    key = b'\x89\x4a\x9e\x5c\x41\xa3\x3b\xab\x99\x03\x47\xfa\x1d\xee\xa1\x54'

    def __init__(self, macAdress):
        Peripheral.__init__(self, macAdress, ADDR_TYPE_RANDOM)
        print("Connected")
        self.authService = self.getServiceByUUID(authServiceUUID)
        self.authCharacteristics = self.authService.getCharacteristics(authCharUUID)[0]
        self.notifDescriptor = self.authCharacteristics.getDescriptors(notificationsUUID)[0]
        self.authenticationsNotif(True)
        self.waitForNotifications(0.5)

    def authenticationsNotif(self, enable):
        if enable:
            print("Enabling auth notifications")
            self.notifDescriptor.write(b"\x01\x00", True)
        elif not enable:
            print("Disabling auth notifications")
            self.notifDescriptor.write(b"\x00\x00", True)
        else:
            print("Changing authentication notifications failed")

    def authenticate(self):
        print("Authenticating...")
        self.setDelegate(AuthenticationDelegate(self))
        print("Requesting random key...")

        requestRandomKey = struct.pack('<2s', b'\x02\x00')
        
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

class AuthenticationDelegate(DefaultDelegate):

    def __init__(self, device):
        DefaultDelegate.__init__(self)
        self.device = device

    def handleNotification(self, handle, data):
        if(handle == self.device.authCharacteristics.getHandle()):
            print("HANDLE: %s || DATA: %s" % (handle, data))
        # Handling MiBand2 response at Auth handle (84)
        # first 3? bytes are the auth response
            if data[:3] == b"\x10\x01\x01":
                print("Recieved: Auth initialized!")

            elif data[:3] == b"\x10\x01\x04":
                print("Recieved: Auth key send failed")

            elif data[:3] == b"\x10\x02\x01":
                print("Recieved: Request random key OK")
                
                randomKey = data[3:]
                print(randomKey)
                self.device.sendEncryptedKey(randomKey)

            elif data[:3] == b"\x10\x02\x04":
                print("Recieved: Error random number error")

            elif data[:3] == b"\x10\x03\x01":
                print("Recieved: Authorization complete")
                time.sleep(0.5)

                # Sending message notification to alert service
                # test thing - need to test if the connection won't drop
                # ------------------------------------------------------
                #alertService = self.device.getServiceByUUID("00001802-0000-1000-8000-00805f9b34fb")
                #alertCharacteristic = alertService.getCharacteristics("00002a06-0000-1000-8000-00805f9b34fb")[0]
                #alertTypeMessage = b'\x01'

                alertService = self.device.getServiceByUUID("00001800-0000-1000-8000-00805f9b34fb")
                #alertCharacteristic = alertService.getCharacteristics("00002a00-0000-1000-8000-00805f9b34fb")[0]
                #alertCharacteristic1 = alertService.getCharacteristics("00002a01-0000-1000-8000-00805f9b34fb")[0]
                #alertCharacteristic2 = alertService.getCharacteristics("00002a04-0000-1000-8000-00805f9b34fb")[0]
                #alertCharacteristic3 = alertService.getCharacteristics("00002a05-0000-1000-8000-00805f9b34fb")[0]
                i = 1
                while i < 128:
                    w = self.device.readCharacteristic(i)
                    ch = self.device.getCharacteristics(i)
                    i += 1
                    print("%s --- %s" % (w, ch[0]))
                alertTypeMessage = b'\x01'
                print(alertCharacteristic)
                print(alertCharacteristic1)
                print(alertCharacteristic2)
                print(alertCharacteristic3)
                alertCharacteristic.write(alertTypeMessage)
                self.device.waitForNotifications(2)
                
                i=0
                while True:
                  i = i + 1
                  alertCharacteristic.write(alertTypeMessage)
                  time.sleep(3)
                  if i == 5:
                    break
                # Measuring the heart rate onetime/realtime
                # Get the heart rate service and its characteristics
                # --------------------------------------------------
                #heartRateService = self.device.getServiceByUUID("0000180d-0000-1000-8000-00805f9b34fb")
                #heartRateControlCharacteristic = heartRateService.getCharacteristics("00002a39-0000-1000-8000-00805f9b34fb")[0]
                #print(heartRateControlCharacteristic)

            elif data[:3] == b"\x10\x03\x04":
                print("Recieved: Encrypted key error")
                self.device.sendKey()

            else:
                print("Unknown response")
                print data
                print data[:3]
        else:
            print("nothing2")

