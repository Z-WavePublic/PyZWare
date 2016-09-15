from tkinter import *
from tkinter import messagebox
import xml.etree.ElementTree as ET
import zware
from threading import Thread
import time
import zwareGlobals

## 
#\mainpage ZWare Sample Client User Guide
#
#\section intro Introduction
#The ZWare Sample Client is an easy-to-use application which demonstrates a selection of the Z-Ware Web API to the user. The Client assists a Z-Wave supported device to communicate with a Z-Ware web server.
#\subsection prerequisites Prerequisites
#This guide describes how to setup and run the client on a PC.<br>
#\ref setup "Dependencies and Setup"
#\section function Functionality
#The ZWare Sample Client currently supports the following functionality:<br>1.Connect to either a ZWare local or portal server<br>2.Include a device to the network<br>3.Exclude a device from the network<br>4.Poll the network to get a list of nodes.<br>5.Poll the network to get the status of a binary switch (if any), binary sensor (if any) and multilevel sensor (if any) that is connected to the network and <br>6.Toggle a binary switch (if any) in the network to change it's current state using the application<br>
#\section details Details
#\ref connect "Connect to a network"<br>
#\ref poll_network "Polling the network"<br>
#\ref include_exclude "Including/Excluding a device"<br>
#\ref binary_switch "Working with Binary Switches"<br>
#\ref binary_sensor "Working with Binary Sensors"<br>
#\ref multilevel_sensor "Working with Multilevel Sensors"<br>
#\defgroup setup Dependencies and Setup
#@{
#\section dependencies Dependencies
#1.Ensure that the PC has a network connection.<br>2.Python 3 should be installed on the PC. The recommended version is 3.5.2.<br>3.Install the python library <b>requests</b> by going to the command line and running \verbatim python -m pip install requests \endverbatim If the library is not available python will download and install it.
#\section setup Setup
#1.Ensure that the ZWare web server and the ZIP Gateway (Z-Wave over Internet Protocol Gateway) are installed on the Raspberry Pi board provided to the user.<br>2.Refer to the respective documentation of the ZWare web server and the ZIP Gateway in order to correctly install and configure them for use with the ZWare Sample Client.<br>3.The ZIP Gateway should be connect to the ZWare server.<br>4.Ensure that a Z-Wave supported device is available for using with the client.
#@}
#\defgroup connect Connect to a network
#\defgroup poll_network Polling the network
#\defgroup include_exclude Include and Exclude a device
#\defgroup binary_switch Working with Binary Switch
#\defgroup binary_sensor Working with Binary Sensor
#\defgroup multilevel_sensor Working with Multilevel Sensor


#Application Entry point
def main():
	zware_client = Tk()
	zware_client.title("Z-Ware Sample Client")
	main_window(zware_client)
	zware_client.mainloop()

##
#\addtogroup connect
#@{
#\section modes Connection Modes
#The user can either connect to the board(<b>Board Connection</b>) or to the portal(<b>Portal Connection</b>.) Selecting either opens a new window based on the input type.<br>
#\subsection board Board Connection
#In this selection the user is communicating with ZWare in local mode i.e.,talking to ZWare in the board directly. In order to login to the server the user has to know it's IP address. The username and password is constant and hard-coded in the application. Once the user has entered a valid IP address the application will connect to the server.
#\subsection portal Portal Connection
#In this selection the user is communicating with the ZWare in portal mode i.e.,talking to the ZWare via a portal. In order to login the server the user should have registered a username and password with the server and configured it to connect to the zipgateway. The default URL for connecting in portal mode is <b>z-wave.sigmadesigns.com</b>. Once the user has entered a valid username and password the application will connect to the server.<br><br>On successfully connecting to the server (using the <b>register/login.php</b> page) in either mode the Application will display the current version (retrieved using the <b>zw_version</b> web api) of ZWare followed a list of nodes currently connected to the server.
#@}
def main_window(TK):
	boardConnection = create_button("Board Connection",TK,0,0)
	boardConnection.configure(command = lambda: board_connection())
	portalConnection = create_button("Portal Connection",TK,0,1)
	portalConnection.configure(command = lambda: portal_connection())

def board_connection():
	boardWindow,mainFrame,debugFrame,zwareGlobals.debugData,debugScrollBar = init_connection_window("Board Connection")
	boardIpName = create_label("Board IP address",mainFrame,0,0)
	boardIpData = create_entry(mainFrame,0,1)
	boardConnect = create_button("Connect",mainFrame,1,0)
	boardConnect.configure(command = lambda: connected_to_server(mainFrame,boardIpData.get()))
	close = create_button("Close",mainFrame,1,1)
	close.configure(command = lambda: close_window(boardWindow))

def portal_connection():
	portalWindow,mainFrame,debugFrame,zwareGlobals.debugData,debugScrollBar = init_connection_window("Portal Connection")
	zwareGlobals.debugData.insert(INSERT,"Portal URL is z-wave.sigmadesigns.com\n")
	portalUsername = create_label("Username",mainFrame,0,0)
	portalUsernameData = create_entry(mainFrame,0,1)
	portalPassword = create_label("Password",mainFrame,1,0)
	portalPasswordData = create_entry(mainFrame,1,1)
	portalPasswordData.configure(show="*")
	portalConnect = create_button("Connect",mainFrame,2,0)
	portalConnect.configure(command = lambda: connected_to_server(mainFrame,"z-wave.sigmadesigns.com",portalUsernameData.get(),portalPasswordData.get()))
	close = create_button("Close",mainFrame,2,1)
	close.configure(command = lambda: close_window(portalWindow))

def connected_to_server(Frame,ipAddress="z-wave.sigmadesigns.com",username="sigma",password="sigmadesigns"):
	boardIp = 'https://' + ipAddress + '/'
	r = zware.zw_init(boardIp,username,password)
	v = r.findall('./version')[0]
	loginOutput = "Connected to zware version: " + v.get('app_major') + '.' + v.get('app_minor') + '\n'
	zwareGlobals.debugData.insert(INSERT, loginOutput)
	includeDevice = create_button("Include Device",Frame,3,0)
	includeDevice.configure(command = lambda: device_inclusion(includeDevice))
	excludeDevice = create_button("Exclude Device",Frame,3,1)
	excludeDevice.configure(command = lambda:  device_exclusion(excludeDevice))
	zwareGlobals.binarySwitchButton = create_button("Toggle Switch",Frame,4,1)
	zwareGlobals.binarySwitchButton.configure(command = lambda: binary_switch_action())
	zwareGlobals.binarySwitchButton.grid_remove()
	getNodeList = create_button("Node details",Frame,4,0)
	getNodeList.configure(command = lambda: node_list_action())
	client_init()
	node_list_action()
	create_thread()
	zwareGlobals.debugData.see(END)


##
#\addtogroup include_exclude
#@{
#\section include Including a device to the network
#Once the user is logged in succesfully they can include a Z-Wave supported device to the network. This is triggered using the "Include Device" button. On clicking this button the user is prompted to initiate the device and start the inclusion process. The inclusion is done using the <b>zwnet_add</b> web api. Once this is done succesfully the client will display that the device is connected to the network followed by polling the network to get the latest node list.
#\section exclude Excluding a device from the network
#Once the user is logged in succesfully they can exclude a Z-Wave supported device from the network. This is achieved using the "Exclude Device" button. On clicking the user is prompted to initiate the device and start the exclusion process. The exclusion is also done using the <b>zwnet_add</b> web api however with a different input parameter than the inclusion process. Once this is done succesfully the client will display that the device is removed from the network followed by polling the network to get the latest node list.
#\section confirmation Inclusion and Exclusion Confirmation
#Once the inclusion or exclusion process has been initiated the client continuously tracks the last completed operation in the server using the <b>zwnet_get_operation</b> web api. Once the server confirms that the last completed operation was either the inclusion or exclusion the client will confirm that the device has been included or excluded in the network.
#@}
def device_inclusion(Button):
	zwareGlobals.debugData.insert(INSERT,"Including device to the network....\n")
	Button['state'] = 'disabled'
	result = messagebox.askokcancel("Include Device","Initiate your device and select \"OK\" to add it to the network\n")
	if result == 1:
		zwareGlobals.debugData.focus_force()
		r = zware.zw_add_remove(2)
		zware.zw_net_comp(2)
		zwareGlobals.debugData.insert(INSERT,"Device has been successfully added to the network\n")
		poll_node_list(True)
		enable_disable_binary_switch()
	else:
		zwareGlobals.debugData.focus_force()
		zwareGlobals.debugData.insert(INSERT,"Device Inclusion cancelled\n")
	zwareGlobals.debugData.see(END)
	Button['state'] = 'normal'

def device_exclusion(Button):
	zwareGlobals.debugData.insert(INSERT,"Excluding device from the network....\n")
	Button['state'] = 'disabled'
	result = messagebox.askokcancel("Exclude Device","Initiate your device and select \"OK\" to remove it from the network\n")
	if result == 1:
		zwareGlobals.debugData.focus_force()
		r = zware.zw_add_remove(3)
		zware.zw_net_comp(3)
		zwareGlobals.debugData.insert(INSERT,"Device has been successfully removed from the network\n")
		poll_node_list(True)
		enable_disable_binary_switch()
	else:
		zwareGlobals.debugData.focus_force()
		zwareGlobals.debugData.insert(INSERT,"Device Exclusion cancelled\n")
	zwareGlobals.debugData.see(END)
	Button['state'] = 'normal'

##
#\addtogroup poll_network
#@{
#\section polling Network Polling
#The client polls the network both automatically in the background as well as on user prompt with the "Node Details" button. On polling succesfully the client displays a list of nodes along with all available endpoints connected to them. It also displays a list of all the Command Classes supported by each endpoint. This is achieved using:<br>1. The Client queries for available nodes using the <b>zwnet_get_node_list</b> web api.<br>2. On succesfully retrieving the node list the client queries for available endpoints for each node using the <b>zwnet_get_ep_list</b> web api.<br>3. Subsequently for each endpoint it will query for the supporting command classes using the <b>zwnet_get_if_list</b> web api. Once all data has been retrieved it will either be a:)Be displayed to the user if they had clicked on the "Node Details" button or b:)Be used for further background polling of devices.
#\section tracking Tracking Devices
#The client will constantly be polling the network for tracking devices and their state values. In the present version this support is provided for Binary Switches, Binary Sensors and Multilevel Sensors. For example whenever a binary switch is added or removed from a network the client will display this information to the user. This is achieved using the polling web-apis mentioned above along with identifying the binary switch using it's interface id.
#@}
def poll_node_list(buttonPress):
	for interface in zwareGlobals.device_interface_list:
		zwareGlobals.device_dictionary_list[interface]['tempFoundDevice'] = 0
	r = zware.zw_api('zwnet_get_node_list')
	nodes = r.findall('./zwnet/zwnode')
	for node in range(len(nodes)):
		if buttonPress:
			zwareGlobals.debugData.insert(INSERT,'node[' + str(node) + '] '+ "id:"+nodes[node].get('id') + "\n")
		r2 = zware.zw_api('zwnode_get_ep_list', 'noded=' + nodes[node].get('desc'))
		eps = r2.findall('./zwnode/zwep')
		for ep in range(len(eps)):
			if buttonPress:
				zwareGlobals.debugData.insert(INSERT,'\tendpoint name: ' + eps[ep].get('name') + "\n")
			epid = eps[ep].get('id')
			r3 = zware.zw_api('zwep_get_if_list', 'epd=' + eps[ep].get('desc'))
			intfs = r3.findall('./zwep/zwif')
			if buttonPress:
				zwareGlobals.debugData.insert (INSERT,"\t\tSupported Command Classes: \n")			
			for intf in range(len(intfs)):
				if (intfs[intf].get('name') != "Unknown"):
					if buttonPress:
						zwareGlobals.debugData.insert(INSERT,'\t\t' + intfs[intf].get('name')  + "\n")
					ifid = int(intfs[intf].get('id'))
					ifd = int(intfs[intf].get('desc'))
					for interface in zwareGlobals.device_interface_list:
						if ifid == interface:
							zwareGlobals.device_dictionary_list[interface]['ifdDevice'] = ifd
							zwareGlobals.device_dictionary_list[interface]['tempFoundDevice'] = 1
	for interface in zwareGlobals.device_interface_list:
		if zwareGlobals.device_dictionary_list[interface]['tempFoundDevice'] != zwareGlobals.device_dictionary_list[interface]['foundDevice']:
			zwareGlobals.device_dictionary_list[interface]['previouslyFoundDevice'] = zwareGlobals.device_dictionary_list[interface]['foundDevice']
		zwareGlobals.device_dictionary_list[interface]['foundDevice'] = zwareGlobals.device_dictionary_list[interface]['tempFoundDevice']

def node_list_action():
	zwareGlobals.debugData.insert(INSERT,'Getting node details...\n')
	poll_node_list(True)
	zwareGlobals.debugData.insert(INSERT,'Finished getting node details\n')
	enable_disable_binary_switch()
	zwareGlobals.debugData.see(END)

##
#\addtogroup binary_switch
#@{
#\section polling_switch Polling Binary Switch state
#On polling for node list the client will also track device and their state values. This is applicable to Binary Switches in this version. Once a binary switch is found in the network the client will retrieve the switch's last known state from the server. This is achieved using the <b>zwif_switch</b> web api and the necessary input parameter for getting a BINARY_SWITCH_REPORT from the server. Every time the binary switch's state changes it will send out a report to the server which will be stored as the last known state in the server.
#\section toggle_switch Toggle Binary Switch
#Whenever a binary switch is detected in the network the "Toggle Switch" button will be visible in the client. Note that this is possible when a)polling the network and detecting a binary switch or b)Including a binary switch using the client.<br> Once the button is visible the user can manually change the state of the binary switch by clicking on the button. For example if the switch is turned off and the user presses the button it will be turned on. This is achieved using the <b>zwif_switch</b> web api and the necessary input parameter for doing a BINARY_SWITCH_SET to the server.
#\section Stop Binary Switch tracking
#Whenever a binary switch is removed from the network the client will inform this to the user. Once the switch is removed the "Toggle Switch" button will be no longer be visible in the client. The removal can happen either using the client's "Exclude Device" button or by removing the switch from the network manually by the user. In either case the information will be relayed to the user by the client.
#@}
def poll_binary_switch():
	if zwareGlobals.device_dictionary_list[zwareGlobals.BINARY_SWITCH_INTERFACE]['foundDevice'] == 1:
		zware.zwif_switch_api(zwareGlobals.device_dictionary_list[zwareGlobals.BINARY_SWITCH_INTERFACE]['ifdDevice'], 1)
		v = int(zware.zwif_switch_api(zwareGlobals.device_dictionary_list[zwareGlobals.BINARY_SWITCH_INTERFACE]['ifdDevice'], 3).get('state'))
		if zwareGlobals.device_dictionary_list[zwareGlobals.BINARY_SWITCH_INTERFACE]['previouslyFoundDevice'] == 0:
			zwareGlobals.debugData.insert(INSERT,"Polling: Switch found in network\n")
			enable_disable_binary_switch()
			zwareGlobals.device_dictionary_list[zwareGlobals.BINARY_SWITCH_INTERFACE]['previouslyFoundDevice'] = 1
			if v == 255:
				zwareGlobals.debugData.insert(INSERT,"Polling: Switch is turned on\n")
			else:
				zwareGlobals.debugData.insert(INSERT,"Polling: Switch is turned off\n")
			zwareGlobals.device_dictionary_list[zwareGlobals.BINARY_SWITCH_INTERFACE]['defaultState'] = v
		if zwareGlobals.device_dictionary_list[zwareGlobals.BINARY_SWITCH_INTERFACE]['defaultState'] != v:
			if v == 255:
				zwareGlobals.debugData.insert(INSERT,"Polling: Switch has been turned on\n")
			else:
				zwareGlobals.debugData.insert(INSERT,"Polling: Switch has been turned off\n")
			zwareGlobals.device_dictionary_list[zwareGlobals.BINARY_SWITCH_INTERFACE]['defaultState'] = v
	elif zwareGlobals.device_dictionary_list[zwareGlobals.BINARY_SWITCH_INTERFACE]['previouslyFoundDevice'] == 1:
			zwareGlobals.debugData.insert(INSERT,"Polling: Switch removed from network\n")
			enable_disable_binary_switch()
			zwareGlobals.device_dictionary_list[zwareGlobals.BINARY_SWITCH_INTERFACE]['previouslyFoundDevice'] = 0
	zwareGlobals.debugData.see(END)

def binary_switch_action():
	if zwareGlobals.device_dictionary_list[zwareGlobals.BINARY_SWITCH_INTERFACE]['foundDevice'] == 0:
		zwareGlobals.debugData.insert(INSERT,"No switch is found in network\n")
	else:
		ifd = zwareGlobals.device_dictionary_list[zwareGlobals.BINARY_SWITCH_INTERFACE]['ifdDevice']
		if zwareGlobals.device_dictionary_list[zwareGlobals.BINARY_SWITCH_INTERFACE]['defaultState'] == 0:
			zware.zwif_switch_api(ifd, 1)
			zware.zwif_switch_api(ifd, 4, "&value=1")
			v = int(zware.zwif_switch_api(ifd, 2).get('state'))
			zwareGlobals.device_dictionary_list[zwareGlobals.BINARY_SWITCH_INTERFACE]['defaultState'] = v
			if v == 255:
				zwareGlobals.debugData.insert(INSERT,"Switch has been turned on\n")
			else:
				zwareGlobals.debugData.insert(INSERT,"Switch could not be turned on\n")
		else:
			zware.zwif_switch_api(ifd, 1)
			zware.zwif_switch_api(ifd, 4, "&value=0")
			v = int(zware.zwif_switch_api(ifd, 2).get('state'))
			zwareGlobals.device_dictionary_list[zwareGlobals.BINARY_SWITCH_INTERFACE]['defaultState'] = v
			if v == 0:
				zwareGlobals.debugData.insert(INSERT,"Switch has been turned off\n")
			else:
				zwareGlobals.debugData.insert(INSERT,"Switch could not be turned off\n")	
	zwareGlobals.debugData.see(END)

def enable_disable_binary_switch():
	if zwareGlobals.device_dictionary_list[zwareGlobals.BINARY_SWITCH_INTERFACE]['foundDevice'] == 0:
		zwareGlobals.binarySwitchButton.grid_remove()
	else:
		zwareGlobals.binarySwitchButton.grid()
##
#\addtogroup binary_sensor
#@{
#\section polling_sensor Polling Binary Sensor State
#On polling for node list the client will also track device and their state values. This is applicable to Binary Sensors in this version. Once a binary sensor is found in the network the client will retrieve the sensor's last known state from the server. This is achieved using the <b>zwif_bsensor</b> web api and the necessary input parameter for getting a BINARY_SENSOR_REPORT from the server. Every time the binary sensor's state changes it will send out a report to the server which will be stored as the last known state in the server. Additionally along with the value the client will also display the sensor type.
#@}
def poll_binary_sensor():
	if zwareGlobals.device_dictionary_list[zwareGlobals.BINARY_SENSOR_INTERFACE]['foundDevice'] == 1:
		zware.zwif_bsensor_api(zwareGlobals.device_dictionary_list[zwareGlobals.BINARY_SENSOR_INTERFACE]['ifdDevice'], 1)
		r = zware.zwif_bsensor_api(zwareGlobals.device_dictionary_list[zwareGlobals.BINARY_SENSOR_INTERFACE]['ifdDevice'], 3)
		v = int(r.get('state'))
		t = r.get('type')
		binary_sensor_type = "Polling: Binary Sensor type:" + t + "\n"
		if zwareGlobals.device_dictionary_list[zwareGlobals.BINARY_SENSOR_INTERFACE]['previouslyFoundDevice'] == 0:
			zwareGlobals.debugData.insert(INSERT,"Polling: Binary Sensor found in network\n")
			zwareGlobals.device_dictionary_list[zwareGlobals.BINARY_SENSOR_INTERFACE]['previouslyFoundDevice'] = 1
			if v == 255:
				zwareGlobals.debugData.insert(INSERT,binary_sensor_type)
				zwareGlobals.debugData.insert(INSERT,"Polling: Binary Sensor has detected an event\n")
			else:
				zwareGlobals.debugData.insert(INSERT,binary_sensor_type)
				zwareGlobals.debugData.insert(INSERT,"Polling: Binary Sensor is idle\n")
			zwareGlobals.device_dictionary_list[zwareGlobals.BINARY_SENSOR_INTERFACE]['defaultState'] = v
		if v == 255:
			zwareGlobals.debugData.insert(INSERT,binary_sensor_type)
			zwareGlobals.debugData.insert(INSERT,"Polling: Binary Sensor has detected an event\n")
			zwareGlobals.device_dictionary_list[zwareGlobals.BINARY_SENSOR_INTERFACE]['defaultState'] = v
	elif zwareGlobals.device_dictionary_list[zwareGlobals.BINARY_SENSOR_INTERFACE]['previouslyFoundDevice'] == 1:
			zwareGlobals.debugData.insert(INSERT,"Polling: Binary Sensor removed from network\n")
			zwareGlobals.device_dictionary_list[zwareGlobals.BINARY_SENSOR_INTERFACE]['previouslyFoundDevice'] = 0
	zwareGlobals.debugData.see(END)

##
#\addtogroup multilevel_sensor
#@{
#\section polling_msensor Polling Multilevel Sensor Data
#On polling for node list the client will also track device and their state values. This is applicable to Multilevel Sensors in this version. Once a multilevel sensor is found in the network the client will retrieve the sensor's last known value from the server. This is achieved using the <b>zwif_sensor</b> web api and the necessary input parameter for getting a MULTILEVEL_SENSOR_REPORT from the server. Every time the multilevel sensor's value changes it will send out a report to the server which will be stored as the last known value in the server. Additionally along with the value the client will also display the sensor type, precision and unit.
#@}
def poll_multilevel_sensor():
	if zwareGlobals.device_dictionary_list[zwareGlobals.MULTILEVEL_SENSOR_INTERFACE]['foundDevice'] == 1:
		zware.zwif_sensor_api(zwareGlobals.device_dictionary_list[zwareGlobals.MULTILEVEL_SENSOR_INTERFACE]['ifdDevice'], 1)
		r = zware.zwif_sensor_api(zwareGlobals.device_dictionary_list[zwareGlobals.MULTILEVEL_SENSOR_INTERFACE]['ifdDevice'], 3)
		v = r.get('value')
		t = r.get('type')
		p = int(r.get('precision'))
		u = r.get('unit')
		multilevel_poll_data = "Polling:Multilevel Sensor Type:" + t + "," + "Value:" + v + "," + "Precision:" + p + "," + "Unit:" + u + "\n"		
		if zwareGlobals.device_dictionary_list[zwareGlobals.MULTILEVEL_SENSOR_INTERFACE]['previouslyFoundDevice'] == 0:
			zwareGlobals.debugData.insert(INSERT,"Polling: Multilevel Sensor found in network\n")
			zwareGlobals.device_dictionary_list[zwareGlobals.MULTILEVEL_SENSOR_INTERFACE]['previouslyFoundDevice'] = 1
			zwareGlobals.debugData.insert(INSERT,multilevel_poll_value)
			zwareGlobals.device_dictionary_list[zwareGlobals.MULTILEVEL_SENSOR_INTERFACE]['defaultState'] = v
		if zwareGlobals.device_dictionary_list[zwareGlobals.MULTILEVEL_SENSOR_INTERFACE]['defaultState'] != v:
			zwareGlobals.debugData.insert(INSERT,"Polling: Multilevel Sensor Updated\n")
			zwareGlobals.debugData.insert(INSERT,multilevel_poll_value)
			zwareGlobals.device_dictionary_list[zwareGlobals.MULTILEVEL_SENSOR_INTERFACE]['defaultState'] = v
	elif zwareGlobals.device_dictionary_list[zwareGlobals.MULTILEVEL_SENSOR_INTERFACE]['previouslyFoundDevice'] == 1:
			zwareGlobals.debugData.insert(INSERT,"Polling: Multilevel Sensor removed from network\n")
			zwareGlobals.device_dictionary_list[zwareGlobals.MULTILEVEL_SENSOR_INTERFACE]['previouslyFoundDevice'] = 0
	zwareGlobals.debugData.see(END)

#Background polling
def poll_server():
	while zwareGlobals.runPollingThread:
		poll_node_list(False)
		poll_binary_switch()
		poll_binary_sensor()
		poll_multilevel_sensor()
		time.sleep(2)


#GUI Rendering and Code Cleaning
def client_init():
	zwareGlobals.runPollingThread = True

def create_thread():
	userThread = Thread(target=poll_server)
	userThread.daemon = True
	userThread.start()

def create_window(windowName):
	userWindow = Toplevel()
	userWindow.title(windowName)
	return userWindow

def create_frame(container):
	userFrame = Frame(container)
	userFrame.pack()
	return userFrame

def create_text(container,rowNumber,columnNumber):
	userText = Text(container)
	userText.grid(row=rowNumber,column=columnNumber)
	return userText

def create_scrollbar(container,rowNumber,columnNumber):
	userScrollBar = Scrollbar(container)
	userScrollBar.grid(row=rowNumber,column=columnNumber,sticky=(N,S,E,W))
	return userScrollBar

def create_label(labelName,container,rowNumber,columnNumber):
	userLabel = Label(container, text=labelName)
	userLabel.grid(row=rowNumber,column=columnNumber,sticky=(N, S, E, W))
	return userLabel

def create_entry(container,rowNumber,columnNumber):
	userEntry = Entry(container)
	userEntry.grid(row=rowNumber,column=columnNumber,sticky=(N, S, E, W))
	return userEntry

def create_button(buttonName,container,rowNumber,columnNumber):
	userButton = Button(container, text = buttonName)
	userButton.grid(row=rowNumber, column=columnNumber, sticky=(N, S, E, W))
	return userButton

def close_window(Toplevel):
	Toplevel.destroy()
	zwareGlobals.runPollingThread = False

def init_connection_window(windowName):
	connectionWindow = create_window(windowName)
	frame1 = create_frame(connectionWindow)
	frame2 = create_frame(connectionWindow)
	userData = create_text(frame2,0,0)
	userScrollBar = create_scrollbar(frame2,0,1)
	userScrollBar.configure(command=userData.yview)
	userData['yscrollcommand'] = userScrollBar.set
	return connectionWindow,frame1,frame2,userData,userScrollBar

main()
