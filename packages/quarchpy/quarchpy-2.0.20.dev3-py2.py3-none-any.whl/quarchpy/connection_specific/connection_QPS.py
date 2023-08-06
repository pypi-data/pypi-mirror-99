import sys
import socket
import time
import datetime
import subprocess
import os
import random
import time


class QpsInterface:
    def __init__(self, host='127.0.0.1', port=9822):
        self.host = host
        self.port = port
        
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        time.sleep(1)
        self.recv()
        time.sleep(1)


    def recv(self):
        if sys.hexversion >= 0x03000000:
            response = self.client.recv(4096)
            i = 0
            for b in response:                                          # end buffer on first \0 character/value
                if b > 0:
                    i += 1
                else:
                    break;
            
            return response[:i].decode('utf-8', "ignore")
        else:            
            return self.client.recv(4096)


    def send(self, data):
        if sys.hexversion >= 0x03000000:
            self.client.send( data.encode() )
        else:
            self.client.send( data )


    def sendCmdVerbose(self, cmd):
        cmd = cmd + "\r\n"

        self.send(cmd)

        response = self.recv().strip()
        while response.rfind('\r\n>') == -1:
            response += self.recv().strip()

        pos = response.rfind('\r\n>')
        return response[:pos]


    def connect(self, targetDevice):
        self.sendCmdVerbose("$connect " + targetDevice)
        time.sleep(0.3)


    def disconnect(self, targetDevice):
        self.sendCmdVerbose("$disconnect")

    def scanIP(self, ipAddress, sleep=10):
        """
        Triggers QPS to look at a specific IP address for a quarch module

        Parameters
        ----------
        QpsConnection : QpsInterface
            The interface to the instance of QPS you would like to use for the scan.
        ipAddress : str
            The IP address of the module you are looking for eg '192.168.123.123'
        sleep : int, optional
            This optional variable sleeps to allow the network to scan for the module before allowing new commands to be sent to QPS.
        """
        ipAddress = "TCP::" + ipAddress

        self.send("$scan " + ipAddress)
        # logging.debug("Starting QPS IP Address Lookup")
        time.sleep(
            sleep)  # Time must be allowed for QPS to Scan. If another scan request is sent it will time out and throw an error.

    def getDeviceList(self, scan = True):
        deviceList = []
        scanWait = 2
        foundDevices = "1"
        foundDevices2 = "2"
        if scan:
            devString = self.sendCmdVerbose('$scan')
            time.sleep(scanWait)
            while foundDevices not in foundDevices2:
                foundDevices = self.sendCmdVerbose('$list')
                time.sleep(scanWait)
                foundDevices2 = self.sendCmdVerbose('$list')
        else:
            foundDevices = self.sendCmdVerbose('$list')

        response = self.sendCmdVerbose( "$list" )

        time.sleep(2)

        response2 = self.sendCmdVerbose( "$list" )

        while (response != response2):
            response = response2
            response2 = self.sendCmdVerbose( "$list" )
            time.sleep(1)
        if "no device" in response.lower() or "no module" in response.lower():
            return [response.strip()]
        #check if a response was received and the first char was a digit
        if( len(response) > 0 and response[0].isdigit ):
            sa = response.split()
            for s in sa:
                #checks for invalid chars
                if( ")" not in s and ">" not in s ):
                    #append to list if conditions met
                    deviceList.append( s )

        #return list of devices
        return deviceList

    
