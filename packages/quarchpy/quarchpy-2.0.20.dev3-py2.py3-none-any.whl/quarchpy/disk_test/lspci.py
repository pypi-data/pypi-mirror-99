'''
Implements basic control over lspci utilities, so that we can identify and check the
status of PCIe devices on the host system
'''

import subprocess
import platform
import time
import os
import re
import sys
import ctypes
#from abc import ABC, abstractmethod
import abc
ABC = abc.ABCMeta('ABC', (object,), {})

from quarchpy.disk_test import driveTestConfig
from quarchpy.user_interface import*

#Class for others to 'extend'
class abstractLSPCI(ABC):

    @abc.abstractmethod
    def getPcieDeviceList(self):
        pass

    @abc.abstractmethod
    def getPcieDeviceDetailedInfo(self, deviceInfo, devicesToScan):
        pass

    def sortList(self, err, out):
        pcieDevices = {}

        # Handle error output
        if (err):
            raise ValueError("lspci error: " + err.decode('utf-8'))
        out = out.decode('utf-8')

        # Split the output into blocks of each device (paragraph)
        blocks = out.split('\r\n\r\n')
        for desc in blocks:
            # Split block into each line
            newDevice = {}
            for line in iter(desc.splitlines()):
                pos = line.find(':')
                if (pos != -1):
                    # Stop if we hit the end of the slot listings
                    if ("Summary of buses" in line):
                        break

                    # Add the dictionary item
                    newDevice[str(line[:pos]).lower()] = str(line[pos + 1:]).strip()
                    # Add the device descriptor as a sub dictionary of the main one
            if ("slot" in newDevice):
                pcieDevices[newDevice["slot"]] = newDevice

        # Return the list[line[:pos].lower()] = line[pos + 1:].strip()

        return pcieDevices

    @abc.abstractmethod
    def is_admin_mode(self):
        pass



class WindowsLSPCI ( abstractLSPCI ):
    def __init__(self):
        pass

    def is_admin_mode(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    '''
    Get basic information on all PCIe devices on the system.  Returned as a dictionary of dictionaries
    {nn:nn.n: {ELEMENT:DATA}}
    This is a fast way to scan the bus and see what is there before possible interrogating devices in more detail (device status and similar)
    '''
    def getPcieDeviceList(self):

        dir_path = os.path.dirname(os.path.realpath(__file__))
        lspciPath = os.path.join(dir_path, "pciutils", "lspci.exe")

        # call lspci to get a list of all devices and basic details in parable form
        proc = subprocess.Popen([lspciPath, '-Mmmvvnn'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Execute the process
        out, err = proc.communicate()

        # will supply a dictionary - calls base class
        retValues = self.sortList(err, out)

        # {'00:00.0': {'slot': '00:00.0', 'class': 'Host bridge [0600]' ... } }
        return retValues

    '''
    Lists all PCIe devices on the bus

    mappingMode=True to allow lspci mapping mode to scan beyond switches
    filterDrives=True to try and filter out 'non drives' (switches and similar)
    '''
    def getPcieDevices(self, mappingMode, filterDrives=False):
        pcieDevices = []
        dir_path = os.path.dirname(os.path.realpath(__file__))
        lspciPath = os.path.join(dir_path, "pciutils", "lspci.exe")

        # Choose mapping mode to use
        if mappingMode == True:
            proc = subprocess.Popen([lspciPath, '-M'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            proc = subprocess.Popen([lspciPath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Execute the process
        out, err = proc.communicate()
        # Handle error output
        if (err):
            printText("ERROR: " + err.decode('utf-8'))
        out = out.decode('utf-8')

        # Add valid device lines to the list
        for pciStr in iter(out.splitlines()):
            matchObj = re.match('[0-9a-fA-F]+:[0-9a-fA-F]+.[0-9a-fA-F]', pciStr)
            try:
                matchStr = matchObj.group(0)
            except:
                matchStr = ""
            if (len(matchStr) > 0):
                if pciStr.find('##') == -1:
                    if (filterDrives == False):
                        pcieDevices.append(pciStr)
                    else:
                        # TODO: check if this looks like a non-storage item and skip
                        pcieDevices.append(pciStr)
        # Return the list
        return pcieDevices

    '''
    Gets more detailed device information on one or more PCIe bus devices.  Each device info requires a seperate lcpci call
    Optionally pass in the info dictionary from getPcieDeviceInfo() in order to fill in the additional details
    devicesToScan is a CSV list of PCIe slot addresses.
    '''
    def getPcieDeviceDetailedInfo(self, deviceInfo=None, devicesToScan="all"):

        # Setup the info structure, filling it if an 'all' selection is given but it is currently empty
        if (deviceInfo == None and devicesToScan == "all"):
            deviceInfo = self.getPcieDeviceInfo()
        elif (deviceInfo == None):
            deviceInfo = {}
            devicesToScan = devicesToScan[5:]

        dir_path = os.path.dirname(os.path.realpath(__file__))

        # Run the lspci command
        lspciPath = os.path.join(dir_path, "pciutils", "lspci.exe")

        # call lspci to get detailed information on devices
        proc = subprocess.Popen([lspciPath, '-vvvs', devicesToScan], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Execute the process
        out, err = proc.communicate()

        retValue = self.sortDeviceInfo(err, out, deviceInfo, devicesToScan)

        return retValue

    '''
    Returns the link status and speed of the device specified
    '''
    def getPcieLinkStatus(self, deviceStr, mappingMode):

        dir_path = os.path.dirname(os.path.realpath(__file__))

        lspciPath = os.path.join(dir_path, "pciutils", "lspci.exe")

        if str(deviceStr).lower().startswith("pcie:"):
            deviceStr = deviceStr[5:]

        if mappingMode == False:
            proc = subprocess.Popen([lspciPath, '-vv', '-s ' + deviceStr], stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        else:
            proc = subprocess.Popen([lspciPath, '-M', '-vv', '-s ' + deviceStr], stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)

        # Execute the process
        out, err = proc.communicate()
        # Handle error output
        if (err):
            printText("ERROR: " + err.decode('utf-8'))
        out = out.decode('utf-8')

        # Locate the link status section
        strPos = out.find('LnkSta:')
        out = out[strPos:]

        try:
            # Get the link speed
            matchObj = re.search('Speed (.*?) ', out)
            linkSpeed = matchObj.group(0)
            linkSpeed = linkSpeed.replace("Speed ", "").replace(",", "").strip()
            # Get the link width
            matchObj = re.search('Width (.*?) ', out)
            linkWidth = matchObj.group(0)
            linkWidth = linkWidth.replace("Width ", "").replace(",", "").strip()
        # If the selected device does not have these parameters, fail here
        except:
            linkSpeed = "UNKNOWN"
            linkWidth = "UNKNOWN"
            # driveTestConfig.testCallbacks["TEST_LOG"](None, time.time(), "error", "Device does not report link
            # speed/width", os.path.basename( __file__) + " - " + sys._getframe().f_code.co_name, { "textDetails":
            # "deviceName " + deviceStr + " is not suitable for link test"})

        return linkSpeed, linkWidth


    def getPcieDeviceInfo(self):
        #stubbing for the time being
        return None


class LinuxLSPCI ( abstractLSPCI ):
    def __init__(self):
        pass

    def is_admin_mode(self):
        if os.getuid() == 0:
            return True
        else:
            return False

    '''
    Get basic information on all PCIe devices on the system.  Returned as a dictionary of dictionaries
    {nn:nn.n: {ELEMENT:DATA}}
    This is a fast way to scan the bus and see what is there before possible interrogating devices in more detail (device status and similar)
    '''

    def getPcieDeviceList(self):

        # call lspci to get a list of all devices and basic details in parable form
        proc = subprocess.Popen(["lspci","-mmvvvnn"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Execute the process
        out, err = proc.communicate()

        # will supply a dictionary - calls base class
        return self.sortList(err, bytes(out))

    def getPcieDevices(self, mappingMode, filterDrives=False):
        pcieDevices = []
        lspciPath = os.path.join(os.getcwd(), "pciutils", "lspci.exe")

        # Choose mapping mode to use
        if mappingMode == True:
            proc = subprocess.Popen(["lspci", '-M'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            proc = subprocess.Popen(["lspci"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Execute the process
        out, err = proc.communicate()
        # Handle error output
        if (err):
            printText("ERROR: " + err.decode('utf-8'))
        out = out.decode('utf-8')

        # Add valid device lines to the list
        for pciStr in iter(out.splitlines()):
            matchObj = re.match('[0-9a-fA-F]+:[0-9a-fA-F]+.[0-9a-fA-F]', pciStr)
            try:
                matchStr = matchObj.group(0)
            except:
                matchStr = ""
            if (len(matchStr) > 0):
                if pciStr.find('##') == -1:
                    if (filterDrives == False):
                        pcieDevices.append(pciStr)
                    else:
                        # TODO: check if this looks like a non-storage item and skip
                        pcieDevices.append(pciStr)
        # Return the list
        return pcieDevices

    '''
    Gets more detailed device information on one or more PCIe bus devices.  Each device info requires a seperate lcpci call
    Optionally pass in the info dictionary from getPcieDeviceInfo() in order to fill in the additional details
    devicesToScan is a CSV list of PCIe slot addresses.
    '''
    def getPcieDeviceDetailedInfo(self, deviceInfo=None, devicesToScan="all"):

        # Setup the info structure, filling it if an 'all' selection is given but it is currently empty
        if (deviceInfo == None and devicesToScan == "all"):
            deviceInfo = self.getPcieDeviceInfo()
        elif (deviceInfo == None):
            deviceInfo = {}
            devicesToScan = devicesToScan[5:]

        # call lspci to get detailed information on devices
        proc = subprocess.Popen(["lspci", '-vvvs', devicesToScan], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Execute the process
        out, err = proc.communicate()

        retValue = self.sortDeviceInfo(err, out, deviceInfo, devicesToScan)

        return retValue

    '''
        Returns the link status and speed of the device specified
        '''

    def getPcieLinkStatus(self, deviceStr, mappingMode):
        lspciPath = os.path.join(os.getcwd(), "pciutils", "lspci.exe")

        if str(deviceStr).startswith("pcie:"):
            deviceStr = deviceStr[5:]

        if mappingMode == False:
            proc = subprocess.Popen(["lspci", '-vv', '-s', deviceStr], stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        else:
            proc = subprocess.Popen(["lspci", '-M', '-vv', '-s', deviceStr], stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)

        # Execute the process
        out, err = proc.communicate()
        # Handle error output
        if (err):
            printText("ERROR: " + err.decode('utf-8'))
        out = out.decode('utf-8')

        # Locate the link status section
        strPos = out.find('LnkSta:')
        out = out[strPos:]

        try:
            # Get the link speed
            matchObj = re.search('Speed (.*?) ', out)
            linkSpeed = matchObj.group(0)
            linkSpeed = linkSpeed.replace("Speed ", "").replace(",", "").strip()
            # Get the link width
            matchObj = re.search('Width (.*?) ', out)
            linkWidth = matchObj.group(0)
            linkWidth = linkWidth.replace("Width ", "").replace(",", "").strip()
        # If the selected device does not have these parameters, fail here
        except:
            linkSpeed = "UNKNOWN"
            linkWidth = "UNKNOWN"

        return linkSpeed, linkWidth

    def getPcieDeviceInfo(self):
        #stubbing for the time being
        return None


    def sortList(self, err, out):
        pcieDevices = {}

        # Handle error output
        if (err):
            raise ValueError("lspci error: " + err.decode('utf-8'))
        out = out.decode('utf-8')

        # Split the output into blocks of each device (paragraph)
        blocks = out.split("\n\n")
        for desc in blocks:
            # printText(desc)
            # Split block into each line
            newDevice = {}
            for line in iter(desc.splitlines()):
                pos = line.find(':')
                if (pos != -1):
                    # Stop if we hit the end of the slot listings
                    if ("Summary of buses" in line):
                        break

                    # Add the dictionary item
                    newDevice[line[:pos].lower()] = line[pos + 1:].strip()


            # Add the device descriptor as a sub dictionary of the main one
            if ("slot" in newDevice):
                pcieDevices[newDevice["slot"]] = newDevice

        # Return the list
        return pcieDevices
