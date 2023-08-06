import time
import socket
import sys
import operator

from config_files.quarch_config_parser import return_module_type_list
from quarchpy.user_interface import*
from quarchpy.user_interface import User_interface
try:
    from quarchpy.connection_specific.connection_USB import importUSB  # , USBConn
except:
    printText("System Compatibility issue - Is your Python architecture consistent with the Operating System?")
    pass
from quarchpy.device import quarchDevice, quarchArray
from quarchpy.connection_specific.connection_Serial import serialList, serial
from quarchpy.device.quarchArray import isThisAnArrayController
from quarchpy.connection_specific.connection_USB import TQuarchUSB_IF
from quarchpy.connection_specific import connection_ReST

# TODO: bodge bodge bodge
from quarchpy.utilities import TestCenter

'''
Merge two dictionaries and return the result
'''


def mergeDict(x, y):
    if (y is None):
        return x
    else:
        merged = x.copy()
        merged.update(y)
        return merged


'''
Scan for Quarch modules across all available COM ports
'''


def list_serial(debuPrint=False):
    serial_ports = serialList.comports()
    serial_modules = dict()

    for i in serial_ports:
        try:
            ser = serial.Serial(i[0], 19200, timeout=0.5)
            ser.write(b'*serial?\r\n')
            s = ser.read(size=64)
            serial_module = s.splitlines()[1]

            serial_module = str(serial_module).replace("'", "").replace("b", "")

            if "QTL" not in serial_module:
                serial_module = "QTL" + serial_module

            module = str(i[0]), str(serial_module)

            if serial_module[7] == "-" and serial_module[10] == "-":
                serial_modules["SERIAL:" + str(i[0])] = serial_module

            ser.close()
        except:
            pass
    return serial_modules


'''
Scan for all Quarch devices available over USB
'''


def list_USB(debuPrint=False):
    QUARCH_VENDOR_ID = 0x16d0
    QUARCH_PRODUCT_ID1 = 0x0449

    usb1 = importUSB()

    context = usb1.USBContext()
    usb_list = context.getDeviceList()

    if (debuPrint): printText(usb_list)

    usb_modules = dict()
    hdList = []

    for i in usb_list:
        if hex(i.device_descriptor.idVendor) == hex(QUARCH_VENDOR_ID) and hex(i.device_descriptor.idProduct) == hex(
                QUARCH_PRODUCT_ID1):
            try:
                i_handle = i.open()
            except:
                if (debuPrint): printText("FAIL - Module detected but handle will not open")
                usb_modules["USB:???"] = "LOCKED MODULE"
                continue

            try:
                module_sn = i_handle.getASCIIStringDescriptor(3)
                if "1944" in module_sn or "2098" in module_sn :  #use enclosure number instead of serial number
                    hdList.append(i)
            except:
                if (debuPrint): printText("FAIL - Module detected but unable to get serial number")
                usb_modules["USB:???"] = "LOCKED MODULE"
                continue

            try:
                if (debuPrint): printText(i_handle.getASCIIStringDescriptor(3) + " " + i_handle.getASCIIStringDescriptor(
                    2) + " " + i_handle.getASCIIStringDescriptor(1))
            except:
                if (debuPrint): printText("FAIL - Module detected but unable to get descriptors")
                usb_modules["USB:???"] = "LOCKED MODULE"
                continue

            if "QTL" not in module_sn:
                module_sn = "QTL" + module_sn.strip()
            else:
                module_sn = module_sn.strip()

            if (debuPrint): printText(module)

            usb_modules["USB:" + module_sn] = module_sn

            try:
                i_handle.close()
            except:
                continue

    # before returning the list of usb modules scan through the list for a 1944 create a quarch device and use sendCommand("*enclosure?")

    for module in hdList:

        QquarchDevice = None
        quarchDevice = None
        quarchDevice = module
        QquarchDevice = TQuarchUSB_IF(context)
        QquarchDevice.connection = quarchDevice
        QquarchDevice.OpenPort()
        time.sleep(0.02)  # sleep sometimes needed before sending comand directly after opening device
        QquarchDevice.SetTimeout(2000)
        serialNo = (QquarchDevice.RunCommand("*serial?")).replace("\r\n", "")
        enclNo = (QquarchDevice.RunCommand("*enclosure?")).replace("\r\n", "")

        keyToFind = "USB:QTL" + serialNo

        if keyToFind in usb_modules:
            del usb_modules[keyToFind]
            usb_modules["USB:QTL" + enclNo] = "QTL" + enclNo

        QquarchDevice.ClosePort()
        QquarchDevice.deviceHandle = None
    return usb_modules


'''
List all Quarch devices found over LAN, using a UDP broadcast scan
'''
def list_network(target_conn="all", debugPring=False, lanTimeout=1, ipAddressLookup=None):
    # Create and configure the socket for broadcast.
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    mySocket.settimeout(lanTimeout)

    lan_modules = dict()

    specifiedDevice = None

    if ipAddressLookup is not None:
        # Attempts to find the device through UDP then REST
        specifiedDevice = lookupDevice(str(ipAddressLookup).strip(), mySocket, lan_modules )



    # Broadcast the message.
    mySocket.sendto(b'Discovery: Who is out there?\0\n', ('255.255.255.255', 30303))

    counter = 0

    # Receive messages until timeout.
    while True:
        network_modules = {}
        counter += 1
        # Receive raw message until timeout, then break.
        try:
            msg_received = mySocket.recvfrom(256)
        except:
            # check if any a device was targeted directly and allow parse
            if specifiedDevice is not None:
                msg_received = specifiedDevice
                specifiedDevice = None
            else:
                break
        cont = 0

        # print(msg_received)
        # Used split \r\n since values of 13 or 10 were looked at as /r and /n when using splitlines
        # This fixes for all cases except if 13 is followed by 10.
        splits = msg_received[0].split(b"\r\n")
        del splits[-1]
        for lines in splits:
            if cont <= 1:
                index = cont
                data = repr(lines).replace("'", "").replace("b", "")
                cont += 1
            else:
                index = repr(lines[0]).replace("'", "")
                data = repr(lines[1:]).replace("'", "").replace("b", "")

            network_modules[index] = data

        module_name = get_user_level_serial_number(network_modules)


        ip_module = msg_received[1][0].strip()

        try:
            # Add a QTL before modules without it.
            if "QTL" not in module_name.decode("utf-8"):
                module_name = "QTL" + module_name.decode("utf-8")
        except:
            # Add a QTL before modules without it.
            if "QTL" not in module_name:
                module_name = "QTL" + module_name

        # Checks if there's a value in the TELNET key.
        if (target_conn.lower() == "all" or target_conn.lower() == "telnet"):
            if network_modules.get("\\x8a") or network_modules.get("138"):
                # Append the information to the list.
                lan_modules["TELNET:" + ip_module] = module_name

        # Checks if there's a value in the REST key.
        if (target_conn.lower() == "all" or target_conn.lower() == "rest"):
            if network_modules.get("\\x84") or network_modules.get("132"):
                # Append the information to the list.
                lan_modules["REST:" + ip_module] = module_name

        # Checks if there's a value in the TCP key.
        if (target_conn.lower() == "all" or target_conn.lower() == "tcp"):
            if network_modules.get("\\x85") or network_modules.get("133"):
                # Append the information to the list.
                lan_modules["TCP:" + ip_module] = module_name

    mySocket.close()

    return lan_modules

def get_user_level_serial_number(network_modules):
    list_of_multi_module_units = ["1995"]  # List of modules that require enclosure number + Port to be displayed.

    # Filter the raw message to get the module and ip address.
    if "134" in network_modules.keys():
        module_name = network_modules.get("134").strip()                    # enclosure number only
        for module in list_of_multi_module_units:
            if module in module_name:
                module_name += "-" + network_modules.get("135").strip()     # enclosure number with port
                break
    elif "\\x86" in network_modules.keys():
        module_name = network_modules.get("\\x86").strip()  # enclosure number only
        for module in list_of_multi_module_units:
            if module in module_name:
                module_name += "-" + network_modules.get("\\x87").strip()     # enclosure number with port
                break
    else:
        if "131" in network_modules.keys():
            module_name = module_name = network_modules.get("131").strip()      # serial number
        elif "\\x83" in network_modules.keys():
            module_name = module_name = network_modules.get("\\x83").strip()  # serial number

    return module_name

def lookupDevice(ipAddressLookup, mySocket, lan_modules):
    try:
        printText("Ipaddress lookup " + ipAddressLookup)
        # For future reference, 0 is the C terminator for a string
        mySocket.sendto(b'Discovery: Who is out there?\0\n', (str(ipAddressLookup).strip(), 30303))
        specifiedDevice = mySocket.recvfrom(256)
        # Check to see if the response contains the connection protocol
        if ("\\x8a") or ("138") or ("\\x84") or ("132") or ("\\x85") or ("133") not in specifiedDevice:
            # If not allow it to fall-back to REST
            specifiedDevice = None
        else:
            # Exit as device was found correctly
            return specifiedDevice
    except Exception as e:
        printText("Error during UDP lookup " + str(e))
        printText("Is the IP address correct?\r\n")
        # Return if there's an error
        return None

    if specifiedDevice is None:
        try:
            restCon = connection_ReST.ReSTConn(str(ipAddressLookup).replace("\r\n", ""))
            restDevice = restCon.sendCommand("*serial?")
            if not str(restDevice).startswith("QTL"):
                restDevice = "QTL" + restDevice
            # Add the item to list
            lan_modules["REST:" + str(ipAddressLookup).replace("\r\n", "")] = restDevice

        except Exception as e:
            printText("Error During REST scan " + str(e))

        # Needs to return None so previous method will not attempt another lookup.
        return None

"""
                    Takes in the connection target and returns the serial number of a module found on the standard scan.
                    
                    Parameters
                    ----------
                    connectionTarget= : str
                        The connection target of the module you would like to know the serial number of.
                        
                    Returns
                    -------
                    ret_val : str
                        The Serial number of the supplied device.

"""
def getSerialNumberFromConnectionTarget(connectionTarget):
    myDict = scanDevices(favouriteOnly=False)
    for k,v in myDict.items():
        if k == connectionTarget:
            return v
    return None

"""
                    Takes in the connection type and serial number of a module and returns the connection target.
                    
                    Parameters
                    ----------
                    module_string= : str
                        The connection type and serial number combination eg. TCP:QTL1999-05-005.
                        
                    scan_dictionary= :dict, optional
                        A scan dictionary can be passed so that a scan does not need to take place on every call.
                        This would be advised if calling this for every item in a list of serial numbers.
                        
                    connection_preference= : list str, optional
                        The preference of which connection type to prioratise if none it given. 
                        Defaults to "USB", "TCP", "SERIAL", "REST", "TELNET" in that order.
                        
                    include_conn_type = : boolean, optional
                        Decided whether the connection type will appear in the return value eg. TCP:192.168.1.1 vs 192.168.1.1
                    
                    Returns
                    -------
                    ret_val : str
                        The Connection target of the supplied device.

"""
def get_connection_target(module_string ,scan_dictionary=None, connection_preference= None, include_conn_type = True):
    if connection_preference == None:
        connection_preference = ["USB", "TCP", "SERIAL", "REST", "TELNET"]
    module_string.replace("::", ":") #QIS/QPS format to QuarchPy format
    delimeter_pos = module_string.find(":")
    if delimeter_pos == -1:
        con_type = None
        serial_number = module_string
    else:
        con_type = module_string[:delimeter_pos]
        serial_number = module_string[delimeter_pos + 1:]
    if scan_dictionary is None:
        printText("Scanning for devices...")
        scan_dictionary = scanDevices(favouriteOnly=False,filterStr=[serial_number])

    ret_val="Fail Module Not Found"

    if con_type is None:
        connection_found = False
        for con_type in connection_preference:
            if connection_found is False:
                for k, v in scan_dictionary.items():
                    if k.__contains__(con_type):
                        ret_val = k
                        connection_found = True
    else:
        for k, v in scan_dictionary.items():
            if k.__contains__(con_type):
                ret_val=k

    if not include_conn_type and not ret_val.__contains__("Fail"):
        delimeter_pos = ret_val.find(":")
        ret_val = ret_val[delimeter_pos + 1:]

    return ret_val

'''
Scans for Quarch modules across the given interface(s). Returns a dictionary of module addresses and serial numbers
'''


def filter_module_type(module_type_filter, found_devices):
    """
    Used in scandevices to filter modules by their type.
    Uses config files.

    :param module_type_filter: Acceptable values are 'Cable', 'Card', 'Drive', 'Power', 'Switch'
    :param found_devices: List of found devices passed from scan_devices
    :return: Returns all devices in found devices that are of 'module filter type'
    """
    accepted_qtl_numbers = return_module_type_list(module_type_filter)
    accepted_qtl_numbers = [x.lower() for x in accepted_qtl_numbers]
    filtered_devices = {}
    if not accepted_qtl_numbers:
        return {}
    for key, value in found_devices.items():
        if "qtl" in str(value).lower():
            qtl_num = str(value[str(value.lower()).index("qtl"):str(value).index("-")]).lower()
            if any(qtl_num in x for x in accepted_qtl_numbers):
                filtered_devices.update({key: value})
    return filtered_devices



'''
Scans for Quarch modules across the given interface(s). Returns a dictionary of module addresses and serial numbers
'''
def scanDevices(target_conn="all", lanTimeout=1, scanInArray=True, favouriteOnly=True,filterStr=None,
                module_type_filter=None, ipAddressLookup=None):
    foundDevices = dict()
    scannedArrays = list()

    if target_conn.lower() == "all":
        foundDevices = list_USB()
        foundDevices = mergeDict(foundDevices, list_serial())
        foundDevices = mergeDict(foundDevices, list_network("all", ipAddressLookup=ipAddressLookup, lanTimeout=lanTimeout))
        # print(foundDevices)

    if target_conn.lower() == "serial":
        foundDevices = list_serial()

    if target_conn.lower() == "usb":
        foundDevices = list_USB()

    if target_conn.lower() == "tcp" or target_conn.lower() == "rest" or target_conn.lower() == "telnet":
        foundDevices = list_network(target_conn, ipAddressLookup=ipAddressLookup, lanTimeout=lanTimeout)

    if (scanInArray):
        for k, v in foundDevices.items():
            if ("usb" not in k.lower()):
                if (k not in scannedArrays):
                    scannedArrays.append(k)
                    if (isThisAnArrayController(v)):
                        try:
                            scanDevice = quarchDevice(k)
                            scanArray = quarchArray(scanDevice)
                            scanDevices = scanArray.scanSubModules()
                            foundDevices = mergeDict(foundDevices, scanDevices)
                        except:
                            printText("Device in use.")
                            foundDevices[k] = "DEVICE IN USE"

    if (favouriteOnly):

        # Sort list in order of connection type preference. Can be changed by changing position in conPref list. This must be done so that it is in the correct format for picking the favourite connections.
        index = 0
        sortedFoundDevices = {}
        conPref = ["USB", "TCP", "SERIAL", "REST", "TELNET"]
        while len(sortedFoundDevices) != len(foundDevices):
            for k, v in foundDevices.items():
                if conPref[index] in k:
                    sortedFoundDevices[k] = v
            index += 1
        foundDevices = sortedFoundDevices

        # new dictionary only containing one favourite connection to each device.
        favConFoundDevices = {}
        index = 0
        for k, v in sortedFoundDevices.items():
            if (favConFoundDevices == {} or not v in favConFoundDevices.values()):
                favConFoundDevices[k] = v
        foundDevices = favConFoundDevices

    # Sort by alphabetic order of key
    sortedFoundDevices = {}
    sortedFoundDevices = sorted(foundDevices.items(), key=operator.itemgetter(1))
    foundDevices = dict(sortedFoundDevices)
    if filterStr != None:
        filteredDevices = {}
        for k, v in foundDevices.items():
            for j in filterStr:
                if (j in v or "LOCKED MODULE" in v): #show locked modules too incase the module you are looking for is on the system but is locked
                    filteredDevices[k] = v
        foundDevices = filteredDevices

    # used to filter module via type ( Power / Drive / ...)
    if module_type_filter:
        foundDevices = filter_module_type(module_type_filter, foundDevices)

    return foundDevices


'''
Prints out a list of Quarch devices nicely onto the terminal, numbering each unit
'''


def listDevices(scanDictionary):
    if not scanDictionary:
        printText("No quarch devices found to display")
    else:
        x = 1
        for k, v in scanDictionary.items():
            printText('{0:>3}'.format(str(x)) + " - " + '{0:<18}'.format(
                v) + "\t" + k)  # add padding to keep responses in line
            x += 1


'''
Requests the user to select one of the devices in the given list
'''


def userSelectDevice(scanDictionary=None, scanFilterStr=None,favouriteOnly=True, message=None, title=None, nice=False, additionalOptions = None, target_conn="all"):
    if User_interface.instance != None and User_interface.instance.selectedInterface == "testcenter":
        nice = False
    if message is None: message = "Please select a quarch device"
    if title is None: title = "Select a Device"

    while (True):
        # Scan first, if no list is supplied
        if (scanDictionary is None):
            printText("Scanning for devices...")
            scanDictionary = scanDevices(filterStr=scanFilterStr, favouriteOnly=favouriteOnly, target_conn=target_conn)

        if len(scanDictionary)<1:
            scanDictionary["***No Devices Found***"]="***No Devices Found***"


        if nice: #Prepair the data for niceListSelection using displayTable().
            if additionalOptions is None: additionalOptions = ["Rescan","Quit"]
            tempList = []
            tempEl = []
            for k, v in scanDictionary.items():
                tempEl = []
                tempEl.append(v)
                charPos = k.find(":")
                tempEl.append(k)
                tempList.append(tempEl)
            adOp =[]
            for option in additionalOptions:
                adOp.append([option]*2) # Put option in all columns
                #adOp.append([option,"-"])
            userStr = listSelection(title, message, tempList, additionalOptions=adOp, indexReq=True, nice=nice, tableHeaders=["Selection", "Description"])
            userStr = userStr[2] #With the data formatted in this way the ConnTarget will always be in userStr[2]

        else: # Prepare data for old style selection or testCenter
            devicesString = []
            for k, v in scanDictionary.items():
                charPos = k.find(":")
                devicesString.append(k + '=' + v + ": " + k[:charPos])
            devicesString = ','.join(devicesString)
            if additionalOptions is None :
                additionalOptions = "Rescan=Rescan,Quit=Quit"
            userStr = listSelection(title=title,message=message,selectionList=devicesString, additionalOptions=additionalOptions)

        # Process the user response
        if (userStr.lower() in 'quit'):
            return "quit"
        elif (userStr.lower() in 'rescan'):
            scanDictionary = None
            favouriteOnly = True
        elif (userStr.lower() in 'all conn types'):
            scanDictionary = None
            favouriteOnly = False
        else:
            # Return the address string of the selected module
            return userStr