#Copyright 2014-2018 Silicon Laboratories Inc.
#The licensor of this software is Silicon Laboratories Inc.  Your use of this software is governed by the terms of  Silicon Labs Z-Wave Development Kit License Agreement.  A copy of the license is available at www.silabs.com.  

from tkinter import *
from tkinter import messagebox
from zware import *
from threading import Thread
import time
import string

class zwareClientClass:
	BINARYSWITCHINTERFACE = 37
	BINARYSENSORINTERFACE = 48
	MULTILEVELSENSORINTERFACE = 49
	MAXSMARTSTARTDEVICES = 32
	runPollingThread = True
	debugData = None
	binarySwitchButton = None
	smartStartList = {}
	smartStartData = {}
	deviceDictionaryList = {}
	deviceInterfaceList = [BINARYSWITCHINTERFACE,BINARYSENSORINTERFACE,MULTILEVELSENSORINTERFACE]
	zware = None

	def __init__(self,zwareObject):
		self.zware = zwareObject
		for interface in self.deviceInterfaceList:
			self.deviceDictionaryList[interface] = {}
			self.deviceDictionaryList[interface]['defaultState'] = -1
			self.deviceDictionaryList[interface]['foundDevice'] = 0
			self.deviceDictionaryList[interface]['tempFoundDevice'] = 0	
			self.deviceDictionaryList[interface]['previouslyFoundDevice'] = 0
			self.deviceDictionaryList[interface]['ifdDevice'] = 0
		for iterator in range(self.MAXSMARTSTARTDEVICES):
			self.smartStartList[iterator] = {}
			self.smartStartList[iterator]['dsk'] = ""
			self.smartStartList[iterator]['bootMode'] = ""
			self.smartStartList[iterator]['grantKeys'] = ""
			self.smartStartList[iterator]['plStatus'] = ""
			self.smartStartList[iterator]['deviceName'] = ""
			self.smartStartList[iterator]['deviceLocation'] = ""
			self.smartStartList[iterator]['productType'] = ""
			self.smartStartList[iterator]['productId'] = ""
			self.smartStartList[iterator]['genericClass'] = ""
			self.smartStartList[iterator]['specificClass'] = ""
			self.smartStartList[iterator]['installerIcon'] = ""
			self.smartStartList[iterator]['vendor'] = ""
			self.smartStartList[iterator]['applicationVersion'] = ""
			self.smartStartList[iterator]['subVersion'] = ""
			self.smartStartList[iterator]['interval'] = ""
			self.smartStartList[iterator]['uuidNumericFormat'] = ""
			self.smartStartList[iterator]['uuid'] = ""
		self.smartStartData['dsk'] = ""
		self.smartStartData["deviceName"] = ""
		self.smartStartData["deviceLocation"] = ""
		self.smartStartData["genericLocation"] = ""
		self.smartStartData["specificLocation"] = ""
		self.smartStartData["installerIcon"] = ""
		self.smartStartData["vendor"] = ""
		self.smartStartData["productId"] = ""
		self.smartStartData["productType"] = ""
		self.smartStartData["applicationVersion"] = ""
		self.smartStartData["subVersion"] = ""
		self.smartStartData["interval"] = ""
		self.smartStartData["uuid"] = ""
		self.smartStartData["uuidFormat"] = StringVar()
		self.smartStartData["uuidNumericFormat"] = 0
		self.smartStartData["status"] = IntVar()
		self.smartStartData["s20GrantKey"] = IntVar()
		self.smartStartData["s21GrantKey"] = IntVar()
		self.smartStartData["s22GrantKey"] = IntVar()
		self.smartStartData["s0GrantKey"] = IntVar()
		self.smartStartData["bootMode"] = IntVar()

	def clear_smart_start_data(self):
		self.smartStartData['dsk'] = ""
		self.smartStartData["deviceName"] = ""
		self.smartStartData["deviceLocation"] = ""
		self.smartStartData["genericLocation"] = ""
		self.smartStartData["specificLocation"] = ""
		self.smartStartData["installerIcon"] = ""
		self.smartStartData["vendor"] = ""
		self.smartStartData["productId"] = ""
		self.smartStartData["productType"] = ""
		self.smartStartData["applicationVersion"] = ""https://www.stack.nl/~dimitri/doxygen/manual/doxygen_usage.html
		self.smartStartData["subVersion"] = ""
		self.smartStartData["interval"] = ""
		self.smartStartData["uuidFormat"].set("")
		self.smartStartData["uuidNumericFormat"] = 0
		self.smartStartData["uuid"] = ""
		self.smartStartData["status"].set(0)
		self.smartStartData["s20GrantKey"].set(0)
		self.smartStartData["s21GrantKey"].set(0)
		self.smartStartData["s22GrantKey"].set(0)
		self.smartStartData["s0GrantKey"].set(0)
		self.smartStartData["bootMode"].set(1)
	
	def clear_smart_start_info_for_device(self,iterator):
		if iterator == "all_devices":
			for i in range(self.MAXSMARTSTARTDEVICES):
				self.smartStartList[i]['dsk'] = ""
				self.smartStartList[i]['bootMode'] = ""
				self.smartStartList[i]['grantKeys'] = ""
				self.smartStartList[i]['plStatus'] = ""
				self.smartStartList[i]['deviceName'] = ""
				self.smartStartList[i]['deviceLocation'] = ""
				self.smartStartList[i]['productType'] = ""
				self.smartStartList[i]['productId'] = ""
				self.smartStartList[i]['genericClass'] = ""
				self.smartStartList[i]['specificClass'] = ""
				self.smartStartList[i]['installerIcon'] = ""
				self.smartStartList[i]['vendor'] = ""
				self.smartStartList[i]['applicationVersion'] = ""
				self.smartStartList[i]['subVersion'] = ""
				self.smartStartList[i]['interval'] = ""
				self.smartStartList[i]['uuidNumericFormat'] = ""
				self.smartStartList[i]['uuid'] = ""
		else:
			i = int(iterator)
			self.smartStartList[i]['dsk'] = ""
			self.smartStartList[i]['bootMode'] = ""
			self.smartStartList[i]['grantKeys'] = ""
			self.smartStartList[i]['plStatus'] = ""
			self.smartStartList[i]['deviceName'] = ""
			self.smartStartList[i]['deviceLocation'] = ""
			self.smartStartList[i]['productType'] = ""
			self.smartStartList[i]['productId'] = ""
			self.smartStartList[i]['genericClass'] = ""
			self.smartStartList[i]['specificClass'] = ""
			self.smartStartList[i]['installerIcon'] = ""
			self.smartStartList[i]['vendor'] = ""
			self.smartStartList[i]['applicationVersion'] = ""
			self.smartStartList[i]['subVersion'] = ""
			self.smartStartList[i]['interval'] = ""
			self.smartStartList[i]['uuidNumericFormat'] = ""
			self.smartStartList[i]['uuid'] = ""
	
	##
	#\addtogroup connect
	#@{
	#\section modes Connection Modes
	#The user can either connect to the board(<b>Board Connection</b>) or to the portal(<b>Portal Connection</b>.) Selecting either opens a login frame based on the input type.<br>
	#\subsection board Board Connection
	#In this selection the user is communicating with ZWare in local mode i.e.,talking to ZWare in the board directly. In order to login to the server the user has to know it's IP address. The username and password is constant and hard-coded in the application. Once the user has entered a valid IP address the application will connect to the server.
	#\subsection portal Portal Connection
	#In this selection the user is communicating with the ZWare in portal mode i.e.,talking to the ZWare via a portal. In order to login the server the user should have registered a username and password with the server and configured it to connect to the zipgateway. The default URL for connecting in portal mode is <b>z-ware.silabs.com</b>. Once the user has entered a valid username and password the application will connect to the server.<br><br>On successfully connecting to the server in either mode the Application will display the current version of ZWare followed a list of nodes currently connected to the server.
	#@}
	def main_window(self,TK):
		initialFrame = self.create_frame(TK)
		buttonFrame = self.create_frame(TK)
		debugFrame = self.create_frame(TK)
		self.debugData = self.create_text(debugFrame,0,0)
		userScrollBar = self.create_scrollbar(debugFrame,0,1)
		userScrollBar.configure(command=self.debugData.yview)
		self.debugData['yscrollcommand'] = userScrollBar.set
		boardConnection = self.create_button("Board Connection",initialFrame,0,0)
		boardConnection.configure(command = lambda: self.connection_start(initialFrame,buttonFrame,"board"))
		portalConnection = self.create_button("Portal Connection",initialFrame,0,1)
		portalConnection.configure(command = lambda: self.connection_start(initialFrame,buttonFrame,"portal"))

	def connection_start(self,initialFrame,buttonFrame,connectionType):
		self.disable_frame(initialFrame)
		if connectionType == "board":
			boardIpName = self.create_label("Board IP address",buttonFrame,0,0)
			boardIpData = self.create_entry(buttonFrame,0,1)
			boardConnect = self.create_button("Connect",buttonFrame,1,0)
			boardConnect.configure(command = lambda: self.connected_to_server(boardConnect,buttonFrame,boardIpData.get()))
			close = self.create_button("Close connection",buttonFrame,1,1)
			close.configure(command = lambda: self.close_connection(boardConnect,initialFrame,buttonFrame))
		elif connectionType == "portal":
			self.debugData.insert(INSERT,"Portal URL is z-ware.silabs.com\n")
			portalUsername = self.create_label("Username",buttonFrame,0,0)
			portalUsernameData = self.create_entry(buttonFrame,0,1)
			portalPassword = self.create_label("Password",buttonFrame,1,0)
			portalPasswordData = self.create_entry(buttonFrame,1,1)
			portalPasswordData.configure(show="*")
			portalConnect = self.create_button("Connect",buttonFrame,2,0)
			portalConnect.configure(command = lambda: self.connected_to_server(portalConnect,buttonFrame,"z-ware.silabs.com",portalUsernameData.get(),portalPasswordData.get()))
			close = self.create_button("Close connection",buttonFrame,2,1)
			close.configure(command = lambda: self.close_connection(portalConnect,initialFrame,buttonFrame))

	def connected_to_server(self,Button,Frame,ipAddress,username="user",password="smarthome"):
		if ipAddress == "":
			self.debugData.delete('1.0', END)
			self.debugData.insert(INSERT, "Please enter a valid IP address\n")
			return
		boardIp = 'https://' + ipAddress + '/'
		r = self.zware.zw_init(boardIp,username,password)
		v = r.findall('./version')[0]
		loginOutput = "Connected to zware version: " + v.get('app_major') + '.' + v.get('app_minor') + '\n'
		self.debugData.insert(INSERT, loginOutput)
		Button['state'] = 'disabled'
		includeDevice = self.create_button("Include Device",Frame,3,0)
		includeDevice.configure(command = lambda: self.device_inclusion(includeDevice))
		includeDeviceSecurely = self.create_button("Include S2 Device",Frame,3,1)
		includeDeviceSecurely.configure(command = lambda: self.device_inclusion_secure(includeDeviceSecurely))
		excludeDevice = self.create_button("Exclude Device",Frame,5,0)
		excludeDevice.configure(command = lambda:  self.device_exclusion(excludeDevice))
		getNodeList = self.create_button("Node details",Frame,5,1)
		getNodeList.configure(command = lambda: self.node_list_action())
		smartStart = self.create_button("Smart Start",Frame,6,0)
		smartStart.configure(command = lambda: self.smart_start())
		self.binarySwitchButton = self.create_button("Toggle Switch",Frame,6,1)
		self.binarySwitchButton.configure(command = lambda: self.binary_switch_action())
		self.binarySwitchButton.grid_remove()
		self.client_init()
		self.node_list_action()
		self.create_thread()
		self.debugData.see(END)

	##
	#\addtogroup include_exclude
	#@{
	#\section include Including a device to the network
	#Once the user is logged in succesfully they can include a Z-Wave supported device to the network. This is triggered using the "Include Device" button. On clicking this button the user is prompted to initiate the device and start the inclusion process. Once this is done succesfully the client will display that the device is connected to the network followed by polling the network to get the latest node list.
	#\section secure_include Including a secure device to the network
	#Once the user is logged in succesfully they can include a Z-Wave supported S2 device to the network. This is triggered using the "Include S2 Device" button. On clicking this button the user is prompted to initiate the device and start the secure inclusion process. During this inclusion process the user will be first prompted to select the grant keys appropriate to the device. Once this is done the user may be asked to enter the first 5 digits of the device's DSK. If done correctly the device will be securely included in the network.
	#\section exclude Excluding a device from the network
	#Once the user is logged in succesfully they can exclude a Z-Wave supported device from the network. This is achieved using the "Exclude Device" button. On clicking the user is prompted to initiate the device and start the exclusion process. Once this is done succesfully the client will display that the device is removed from the network followed by polling the network to get the latest node list.
	#\section confirmation Inclusion and Exclusion Confirmation
	#Once the inclusion or exclusion process has been initiated the client continuously tracks the last completed operation in the server. Once the server confirms that the last completed operation was either the inclusion or exclusion the client will confirm that the device has been included or excluded in the network.
	#@}
	def device_inclusion(self,Button):
		self.debugData.insert(INSERT,"Including device to the network....\n")
		Button['state'] = 'disabled'
		result = messagebox.askokcancel("Include Device","Initiate your device and select \"OK\" to add it to the network\n")
		if result == 1:
			self.debugData.focus_force()
			r = self.zware.zw_add_remove(2)
			self.zware.zw_net_comp(2)
			self.debugData.insert(INSERT,"Device has been successfully added to the network\n")
			self.poll_node_list(True)
			self.enable_disable_binary_switch()
		else:
			self.debugData.focus_force()
			self.debugData.insert(INSERT,"Device Inclusion cancelled\n")
		self.debugData.see(END)
		Button['state'] = 'normal'

	def device_inclusion_secure(self,Button):
		self.debugData.insert(INSERT,"Including device securely to the network....\n")
		Button['state'] = 'disabled'
		result = messagebox.askokcancel("Include Device","Initiate your device and select \"OK\" to add it to the network\n")
		if result == 1:
			self.debugData.focus_force()
			r = self.zware.zw_add_remove(2)
			self.zware.zw_net_op_sts(11)
			grantKey = self.zware.zw_net_get_grant_keys()
			grantKeyWindow = self.create_window("grant_Keys")
			grantKeyWindow.s20GrantKey = BooleanVar()
			grantKeyWindow.s21GrantKey = BooleanVar()
			grantKeyWindow.s22GrantKey = BooleanVar()
			grantKeyWindow.s0GrantKey = BooleanVar()
			if (int(grantKey) & 1) == 1:
				grantKeyWindow.s20GrantKey.set(True)
			if (int(grantKey) & 2) == 2:
				grantKeyWindow.s21GrantKey.set(True)
			if (int(grantKey) & 4) == 4:
				grantKeyWindow.s22GrantKey.set(True)
			if (int(grantKey) & 128) == 128:
				grantKeyWindow.s0GrantKey.set(True)
			self.create_checkbox("Security 2 Class 0 - Unauthenticated",grantKeyWindow.s20GrantKey,grantKeyWindow,1,0)
			self.create_checkbox("Security 2 Class 1 - Authenticated",grantKeyWindow.s21GrantKey,grantKeyWindow,1,1)
			self.create_checkbox("Security 2 Class 2 - Access Control",grantKeyWindow.s22GrantKey,grantKeyWindow,2,0)
			self.create_checkbox("Security 0 - Unauthenticated",grantKeyWindow.s0GrantKey,grantKeyWindow,2,1)
			okButton = self.create_button("OK",grantKeyWindow,3,0,)
			okButton.configure(command = lambda: self.set_grant_keys(grantKeyWindow,grantKeyWindow.s20GrantKey,grantKeyWindow.s21GrantKey,grantKeyWindow.s22GrantKey,grantKeyWindow.s0GrantKey))
			cancelButton = self.create_button("Cancel",grantKeyWindow,3,1)
			cancelButton.configure(command = lambda: self.grantKeyWindow.destroy())
			grantKeyWindow.protocol("WM_DELETE_WINDOW", grantKeyWindow.destroy)
		else:
			self.debugData.focus_force()
			self.debugData.insert(INSERT,"Device Inclusion cancelled\n")
		self.debugData.see(END)
		Button['state'] = 'normal'

	def set_grant_keys(self,grantWindow,s20grantKey,s21grantKey,s22grantKey,s0grantKey):
		userSelectedGrantKeys = 0
		dsk = ""
		if s20grantKey.get() == True:
			userSelectedGrantKeys += 1
		if s21grantKey.get() == True:
			userSelectedGrantKeys += 2
		if s22grantKey.get() == True:
			userSelectedGrantKeys += 4
		if s0grantKey.get() == True:
			userSelectedGrantKeys += 128
		grantWindow.destroy()
		self.zware.zw_net_set_grant_keys(str(userSelectedGrantKeys))
		if userSelectedGrantKeys == 1 or userSelectedGrantKeys == 129 or userSelectedGrantKeys == 128:
			self.debugData.insert(INSERT,"S2 Grant keys is correct. Continuing secure inclusion\n")
			self.zware.zw_net_comp(2)
			self.debugData.insert(INSERT,"S2 Device has been successfully added to the network\n")
			self.poll_node_list(True)
			self.enable_disable_binary_switch()
		elif userSelectedGrantKeys > 1:
			self.debugData.insert(INSERT,"S2 Grant keys is correct. Continuing secure inclusion\n")
			self.zware.zw_net_op_sts(12)
			dsk = self.zware.zw_net_add_s2_get_dsk()
			dskWindow = self.create_window("DSK")
			dskUserInput = self.create_entry(dskWindow,0,0)
			dskAutoFill = self.create_label(dsk,dskWindow,0,1)
			dskSend = self.create_button("OK",dskWindow,1,0)
			dskSend.configure(command = lambda: self.dsk_verify_and_send(dskWindow,dskUserInput.get(),dsk))
			dskWindow.protocol("WM_DELETE_WINDOW", dskWindow.destroy)
		elif userSelectedGrantKeys == 0:
			self.debugData.insert(INSERT,"S2 Grant Keys is incorrect. Aborting secure inclusion.\n")
			r = self.zware.zw_abort()

	def dsk_verify_and_send(self,dsk_input_window,dskUserInput,receivedDSK):
		generatedDSK = dskUserInput + receivedDSK
		dsk_input_window.destroy()
		self.zware.zw_net_set_dsk(generatedDSK)
		self.zware.zw_net_comp(2)
		self.debugData.insert(INSERT,"S2 Device has been successfully added to the network\n")
		self.poll_node_list(True)
		self.enable_disable_binary_switch()

	##
	#\addtogroup smartstart
	#@{
	#\section introduction	Introduction
	#Once the user is logged in to the network they can manage smart start devices in the network. This is done by selecting the "Smart Start" button. This opens a new window which allows the user to<br>1.Register a smart start device to a network and <br>2.Get Smart start device details<br>
	#\section register Registering a smartstart device to the network
	#This can be done by clicking on the "Register Smart start Device" button. The user can enter the required values and click on the "Register Device" button. If everything is correct the device will be registered to the network. The next time the device is turned on it will be automatically included into the network if it has been registered that way. Only the DSK is mandatory for registerting a device to the network. The user can click on the "Help" button to find out the details regarding the different options available when registering a device to the network.
	#\section get_smart_start_details Get Smart start device details.
	#This can be done by clicking on the "Get Smart start Devices details" button. It will show a list of the smart start devices registered in the network identified by the their DSK. The user has the option to <br>1.Edit the device which opens up the Register window again populated with the devices' existing values which the user can update and then click the "Update Device" button to complete the process.<br>2.Delete the selected device from the smart start registry in the network and <br>3.Delete all devices from the smart start registry in the network<br>
	#@}
	def smart_start(self):
		smartStartMainWindow = self.create_window("Smart Start")
		smartStartMainWindow.protocol("WM_DELETE_WINDOW", lambda: smartStartMainWindow.destroy())
		smartStartButtonWindow = self.create_frame(smartStartMainWindow)
		smartStartRegisterWindow = self.create_frame(smartStartMainWindow)
		registerDevice = self.create_button("Register Smart start Device",smartStartButtonWindow,0,1)
		registerDevice.configure(command = lambda: self.register_smart_start_device(smartStartRegisterWindow,"Register",0))
		getSmartStartDevicesList = self.create_button("Get Smart start Devices details",smartStartButtonWindow,0,2)
		getSmartStartDevicesList.configure(command = lambda: self.get_smart_start_devices_list(smartStartRegisterWindow))

	def smart_start_register_info(self,smartStartRegisterWindow):
		smartStartHelpWindow = self.create_window("Smart Start Register Help")
		smartStartHelpWindow.protocol("WM_DELETE_WINDOW", lambda: smartStartHelpWindow.destroy())
		denotesMandatory = self.create_label("* denotes mandatory",smartStartHelpWindow,0,0)
		denotesNumeric = self.create_label("** denotes numeric data",smartStartHelpWindow,1,0)
		denotesHexadecimal = self.create_label("*** denotes hexadecimal data",smartStartHelpWindow,2,0)
		dskSample = self.create_label("DSK sample: 31568-37020-48769-65093-50278-41501-00891-24720",smartStartHelpWindow,3,0)
		uuidInfo = self.create_label("UUID data length must be either be 16 or 32 or 36 (for GUID)",smartStartHelpWindow,4,0)
		uuidInfo3 = self.create_label("UUID format <GUID> data sample: 58D5E212-165B-4CA0-909B-C86B9CEE0111",smartStartHelpWindow,5,0)

	def register_smart_start_default(self,smartStartRegisterWindow,windowType,deviceIterator):
		self.clear_frame(smartStartRegisterWindow)
		provisioningDevice = self.create_label("Provisioning Device",smartStartRegisterWindow,0,1)
		dsk = self.create_label("DSK*",smartStartRegisterWindow,1,0)
		self.smartStartData["dsk"] = self.create_entry(smartStartRegisterWindow,1,1)
		deviceName = self.create_label("Device Name",smartStartRegisterWindow,2,0)
		self.smartStartData["deviceName"] = self.create_entry(smartStartRegisterWindow,2,1)
		deviceLocation = self.create_label("Device Location",smartStartRegisterWindow,3,0)
		self.smartStartData["deviceLocation"] = self.create_entry(smartStartRegisterWindow,3,1)
		productType = self.create_label("Product Type",smartStartRegisterWindow,5,1)
		genericClass = self.create_label("Generic Device Class**",smartStartRegisterWindow,6,0)
		self.smartStartData["genericClass"] = self.create_entry(smartStartRegisterWindow,6,1)
		specificClass = self.create_label("Specific Device Class**",smartStartRegisterWindow,7,0)
		self.smartStartData["specificClass"] = self.create_entry(smartStartRegisterWindow,7,1)
		installerIcon = self.create_label("Installer Icon**",smartStartRegisterWindow,8,0)
		self.smartStartData["installerIcon"] = self.create_entry(smartStartRegisterWindow,8,1)
		productId = self.create_label("Product Id",smartStartRegisterWindow,10,1)
		vendor = self.create_label("Vendor**",smartStartRegisterWindow,11,0)
		self.smartStartData["vendor"] = self.create_entry(smartStartRegisterWindow,11,1)
		productId = self.create_label("Product Id**",smartStartRegisterWindow,12,0)
		self.smartStartData["productId"] = self.create_entry(smartStartRegisterWindow,12,1)
		productType = self.create_label("Product Type**",smartStartRegisterWindow,13,0)
		self.smartStartData["productType"] = self.create_entry(smartStartRegisterWindow,13,1)
		applicationVersion = self.create_label("Application Version**",smartStartRegisterWindow,14,0)
		self.smartStartData["applicationVersion"] = self.create_entry(smartStartRegisterWindow,14,1)
		subVersion = self.create_label("Sub Version**",smartStartRegisterWindow,15,0)
		self.smartStartData["subVersion"] = self.create_entry(smartStartRegisterWindow,15,1)
		interval = self.create_label("Interval**",smartStartRegisterWindow,17,0)
		self.smartStartData["interval"] = self.create_entry(smartStartRegisterWindow,17,1)
		uuidFormat = self.create_label("UUID Format",smartStartRegisterWindow,18,0)
		self.create_drop_down_list(self.smartStartData["uuidFormat"],smartStartRegisterWindow,"sn:","UUID:","<GUID>",18,1)
		uuid = self.create_label("UUID***",smartStartRegisterWindow,19,0)
		self.smartStartData["uuid"] = self.create_entry(smartStartRegisterWindow,19,1)
		status = self.create_label("Status",smartStartRegisterWindow,20,0)
		self.create_radiobutton("Pending",self.smartStartData["status"],0,smartStartRegisterWindow,20,1)
		self.create_radiobutton("Ignored",self.smartStartData["status"],3,smartStartRegisterWindow,20,2)
		grantKeys = self.create_label("Grant Keys",smartStartRegisterWindow,21,0)
		self.create_checkbox("Security 2 Class 0 - Unauthenticated",self.smartStartData["s20GrantKey"],smartStartRegisterWindow,21,1)
		self.create_checkbox("Security 2 Class 1 - Authenticated",self.smartStartData["s21GrantKey"],smartStartRegisterWindow,22,1)
		self.create_checkbox("Security 2 Class 2 - Access Control",self.smartStartData["s22GrantKey"],smartStartRegisterWindow,23,1)
		self.create_checkbox("Security 0 - Unauthenticated",self.smartStartData["s0GrantKey"],smartStartRegisterWindow,24,1)
		bootMode = self.create_label("Boot Mode",smartStartRegisterWindow,25,0)
		self.create_radiobutton("Smart Start Bootstrapping mode",self.smartStartData["bootMode"],1,smartStartRegisterWindow,25,1)
		self.create_radiobutton("S2 Bootstrapping mode",self.smartStartData["bootMode"],0,smartStartRegisterWindow,25,2)
		cancel = self.create_button("Cancel",smartStartRegisterWindow,27,1)
		if windowType == "Register":
			registerDevice = self.create_button("Register Device",smartStartRegisterWindow,27,0)
			registerDevice.configure(command = lambda: self.add_device_provisioning_list(smartStartRegisterWindow,"Register",0))
			cancel.configure(command = lambda: self.cancel_operation(smartStartRegisterWindow,"Register"))
		elif windowType == "Update":
			registerDevice = self.create_button("Update Device",smartStartRegisterWindow,27,0)
			registerDevice.configure(command = lambda: self.add_device_provisioning_list(smartStartRegisterWindow,"Update",deviceIterator))
			cancel.configure(command = lambda: self.cancel_operation(smartStartRegisterWindow,"Update"))
		smartStartInfo = self.create_button("Help",smartStartRegisterWindow,27,2)
		smartStartInfo.configure(command = lambda: self.smart_start_register_info(smartStartRegisterWindow))
		

	def cancel_operation(self,smartStartRegisterWindow,windowType):
		self.clear_frame(smartStartRegisterWindow)
		if windowType == "Register":
			messagebox.showinfo("SmartStart","Device Registration cancelled",parent=smartStartRegisterWindow)
		elif windowType == "Update":
			messagebox.showinfo("SmartStart","Device Update cancelled",parent=smartStartRegisterWindow)
		self.register_smart_start_device(smartStartRegisterWindow,"Register",0)

	def register_smart_start_device(self,smartStartRegisterWindow,windowType,deviceIterator):
		currentDSK = ""
		currentStatus = 0
		currentBootMode = 0
		currentGrantKeys = 0
		currentDeviceName = ""
		currentDeviceLocation = ""
		currentProductType = ""
		currentProductId = ""
		currentGenericClass = ""
		currentSpecificClass = ""
		currentInstallerIcon = ""
		currentVendor = ""
		currentApplicationVersion = ""
		currentSubVersion = ""
		currentUuidFormat = ""
		currentUuid = ""
		currentInterval = ""
		self.clear_smart_start_data()
		if windowType == "Register":
			self.register_smart_start_default(smartStartRegisterWindow,"Register",0)
		elif windowType == "Update":
			self.register_smart_start_default(smartStartRegisterWindow,"Update",deviceIterator)
			for i in range(self.MAXSMARTSTARTDEVICES):
				if i == deviceIterator.get():
					currentDSK = self.smartStartList[i]['dsk']
					currentStatus = int(self.smartStartList[i]['plStatus'])
					currentBootMode = int(self.smartStartList[i]['bootMode'])
					if self.smartStartList[i]['grantKeys'] != None:
						currentGrantKeys = int(self.smartStartList[i]['grantKeys'])
					if self.smartStartList[i]['deviceName'] != None:
						currentDeviceName = self.smartStartList[i]['deviceName']
					if self.smartStartList[i]['deviceLocation'] != None:
						currentDeviceLocation = self.smartStartList[i]['deviceLocation']
					if self.smartStartList[i]['productType'] != None:
						currentProductType = self.smartStartList[i]['productType']
					if self.smartStartList[i]['productId'] != None:
						currentProductId = self.smartStartList[i]['productId']
					if self.smartStartList[i]['genericClass'] != None:
						currentGenericClass = self.smartStartList[i]['genericClass']
					if self.smartStartList[i]['specificClass'] != None:
						currentSpecificClass = self.smartStartList[i]['specificClass']
					if self.smartStartList[i]['installerIcon'] != None:
						currentInstallerIcon = self.smartStartList[i]['installerIcon']
					if self.smartStartList[i]['vendor'] != None:
						currentVendor = self.smartStartList[i]['vendor']
					if self.smartStartList[i]['applicationVersion'] != None:
						currentApplicationVersion = self.smartStartList[i]['applicationVersion']
					if self.smartStartList[i]['subVersion'] != None:
						currentSubVersion = self.smartStartList[i]['subVersion']
					if self.smartStartList[i]['uuidNumericFormat'] != None:
						currentUuidFormat = self.smartStartList[i]['uuidNumericFormat']
					if self.smartStartList[i]['uuid'] != None:
						currentUuid = self.smartStartList[i]['uuid']
					if self.smartStartList[i]['interval'] != None:
						currentInterval = self.smartStartList[i]['interval']
					break
			self.smartStartData["dsk"].insert(0,currentDSK)
			self.smartStartData["status"].set(currentStatus)
			self.smartStartData["bootMode"].set(currentBootMode)
			self.smartStartData["deviceName"].insert(0,currentDeviceName)
			self.smartStartData["deviceLocation"].insert(0,currentDeviceLocation)
			self.smartStartData["productType"].insert(0,currentProductType)
			self.smartStartData["productId"].insert(0,currentProductId)
			self.smartStartData["genericClass"].insert(0,currentGenericClass)
			self.smartStartData["specificClass"].insert(0,currentSpecificClass)
			self.smartStartData["installerIcon"].insert(0,currentInstallerIcon)
			self.smartStartData["vendor"].insert(0,currentVendor)
			self.smartStartData["applicationVersion"].insert(0,currentApplicationVersion)
			self.smartStartData["subVersion"].insert(0,currentSubVersion)
			self.smartStartData["uuid"].insert(0,currentUuid)
			self.smartStartData["interval"].insert(0,currentInterval)
			if currentUuidFormat != "":
				if currentUuidFormat == "2" or currentUuidFormat == "3":
					self.smartStartData["uuidFormat"].set("sn:")
				if currentUuidFormat == "4" or currentUuidFormat == "5":
					self.smartStartData["uuidFormat"].set("UUID")
				if currentUuidFormat == "6":
					self.smartStartData["uuidFormat"].set("<GUID>")
			if currentGrantKeys != 0:
				if ((currentGrantKeys | 1) == currentGrantKeys):
					self.smartStartData["s20GrantKey"].set(1)
				if ((currentGrantKeys | 2) == currentGrantKeys):
					self.smartStartData["s21GrantKey"].set(1)
				if ((currentGrantKeys | 4) == currentGrantKeys):
					self.smartStartData["s22GrantKey"].set(1)
				if ((currentGrantKeys | 128) == currentGrantKeys):
					self.smartStartData["s0GrantKey"].set(1)

	def add_device_provisioning_list(self,smartStartRegisterWindow,windowType,deviceIterator):
		grantKeys = 0
		grantKeyString = ""
		uuidNumericFormatString = ""
		if windowType == "Update":
			result = self.zware.zw_net_provisioning_list_remove(self.smartStartList[deviceIterator.get()]['dsk'])
			if result != "":
				messagebox.showinfo("SmartStart delete device","Error updating device from the smart start registry",parent=smartStartRegisterWindow)
				self.register_smart_start_device(smartStartRegisterWindow,"Register",0)
				return

		if len(self.smartStartData["dsk"].get()) == 0:
				messagebox.showinfo("SmartStart Register device","DSK cannot be empty",parent=smartStartRegisterWindow)
				return
		dskSplit = self.smartStartData["dsk"].get().split("-")
		if len(dskSplit) != 8:
			messagebox.showinfo("SmartStart Register device","DSK is invalid",parent=smartStartRegisterWindow)
			return
		for dskString in dskSplit:
			if len(dskString) != 5:
				messagebox.showinfo("SmartStart Register device","DSK is invalid",parent=smartStartRegisterWindow)
				return
			if dskString.isdigit() == False:
				messagebox.showinfo("SmartStart Register device","DSK is invalid",parent=smartStartRegisterWindow)
				return
		if self.smartStartData["genericClass"].get() != "":
			if self.smartStartData["genericClass"].get().isdigit() == False:
				messagebox.showinfo("SmartStart Register device","Generic class should be numeric only",parent=smartStartRegisterWindow)
				return
		if self.smartStartData["specificClass"].get() != "":
			if self.smartStartData["specificClass"].get().isdigit() == False:
				messagebox.showinfo("SmartStart Register device","Specific class should be numeric only",parent=smartStartRegisterWindow)
				return
		if self.smartStartData["installerIcon"].get() != "":
			if self.smartStartData["installerIcon"].get().isdigit() == False:
				messagebox.showinfo("SmartStart Register device","Installer icon should be numeric only",parent=smartStartRegisterWindow)
				return
		if self.smartStartData["vendor"].get() != "":
			if self.smartStartData["vendor"].get().isdigit() == False:
				messagebox.showinfo("SmartStart Register device","Vendor should be numeric only",parent=smartStartRegisterWindow)
				return
		if self.smartStartData["applicationVersion"].get() != "":
			if self.smartStartData["applicationVersion"].get().isdigit() == False:
				messagebox.showinfo("SmartStart Register device","Application Version should be numeric only",parent=smartStartRegisterWindow)
				return
		if self.smartStartData["subVersion"].get() != "":
			if self.smartStartData["subVersion"].get().isdigit() == False:
				messagebox.showinfo("SmartStart Register device","Sub Version should be numeric only",parent=smartStartRegisterWindow)
				return
		if self.smartStartData["interval"].get() != "":
			if self.smartStartData["interval"].get().isdigit() == False:
				messagebox.showinfo("SmartStart Register device","Interval should be numeric only",parent=smartStartRegisterWindow)
				return
		if self.smartStartData["productType"].get() != "":
			if self.smartStartData["productType"].get().isdigit() == False:
				messagebox.showinfo("SmartStart Register device","Product Type should be numeric only",parent=smartStartRegisterWindow)
				return
			if (self.smartStartData["genericClass"].get() == "") or (self.smartStartData["specificClass"].get() == "") or (self.smartStartData["installerIcon"].get() == ""):
				messagebox.showinfo("SmartStart Register device","If product type is specified please also specify the generic class, specific class and installer icon",parent=smartStartRegisterWindow)
				return
		if self.smartStartData["productId"].get() != "":
			if self.smartStartData["productId"].get().isdigit() == False:
				messagebox.showinfo("SmartStart Register device","Product Id should be numeric only",parent=smartStartRegisterWindow)
				return
			if (self.smartStartData["vendor"].get() == "") or (self.smartStartData["productType"].get() == "") or (self.smartStartData["applicationVersion"].get() == "") or (self.smartStartData["subVersion"].get() == ""):
				messagebox.showinfo("SmartStart Register device","If product id is specified please also specify the vendor, product type, application version and sub version",parent=smartStartRegisterWindow)
				return
		if self.smartStartData["uuidFormat"].get() == "sn:" or self.smartStartData["uuidFormat"].get() == "UUID:":
			if len(self.smartStartData["uuid"].get()) != 16 and len(self.smartStartData["uuid"].get()) != 32:
				messagebox.showinfo("SmartStart Register device","UUID data length must be either be 16 or 32 or 36 (for GUID)",parent=smartStartRegisterWindow)
				return
			if all(char in string.hexdigits for char in self.smartStartData["uuid"].get()) == False:
				messagebox.showinfo("SmartStart Register device","UUID data must be hexadecimal only",parent=smartStartRegisterWindow)
				return
			if self.smartStartData["uuidFormat"].get() == "sn:":
				self.smartStartData["uuidNumericFormat"] = 2
			else:
				self.smartStartData["uuidNumericFormat"] = 4
			if len(self.smartStartData["uuid"].get()) == 16:
				self.smartStartData["uuidNumericFormat"] = self.smartStartData["uuidNumericFormat"] + 1
		if self.smartStartData["uuidFormat"].get() == "<GUID>":
			if len(self.smartStartData["uuid"].get()) != 36:
				messagebox.showinfo("SmartStart Register device","UUID data length must be either be 16 or 32 or 36 (for GUID)",parent=smartStartRegisterWindow)
				return
			guidSplit = self.smartStartData["uuid"].get().split("-")
			if len(guidSplit) != 5:
				messagebox.showinfo("SmartStart Register device","GUID format is invalid",parent=smartStartRegisterWindow)
				return
			if len(guidSplit[0]) != 8 or len(guidSplit[1]) != 4 or len(guidSplit[2]) != 4 or len(guidSplit[3]) != 4 or len(guidSplit[4]) != 12:
				messagebox.showinfo("SmartStart Register device","GUID format is invalid",parent=smartStartRegisterWindow)
				return
			for guid in guidSplit:
				if all(char in string.hexdigits for char in guid) == False:
					messagebox.showinfo("SmartStart Register device","UUID data must be hexadecimal only",parent=smartStartRegisterWindow)
					return
			self.smartStartData["uuidNumericFormat"] = 6
		if self.smartStartData["s20GrantKey"].get() == 1:
			grantKeys += 1
		if self.smartStartData["s21GrantKey"].get() == 1:
			grantKeys += 2
		if self.smartStartData["s22GrantKey"].get() == 1:
			grantKeys += 4
		if self.smartStartData["s0GrantKey"].get() == 1:
			grantKeys += 128
		if grantKeys != 0:
			grantKeyString = str(grantKeys)
		if self.smartStartData["uuidNumericFormat"] != 0:
			uuidNumericFormatString = str(self.smartStartData["uuidNumericFormat"])
		provisioning_list_add_value = self.zware.zw_net_provisioning_list_add(self.smartStartData["dsk"].get(),str(self.smartStartData["bootMode"].get()),grantKeyString,self.smartStartData["interval"].get(),self.smartStartData["deviceName"].get(),self.smartStartData["deviceLocation"].get(),self.smartStartData["applicationVersion"].get(),self.smartStartData["subVersion"].get(),self.smartStartData["vendor"].get(),self.smartStartData["productId"].get(),self.smartStartData["productType"].get(),str(self.smartStartData["status"].get()),self.smartStartData["genericClass"].get(),self.smartStartData["specificClass"].get(),self.smartStartData["installerIcon"].get(),uuidNumericFormatString,self.smartStartData["uuid"].get())
		if provisioning_list_add_value == "":
			if windowType == "Register":
				messagebox.showinfo("Register Device","Device succesfully added to smart start registry",parent=smartStartRegisterWindow)
			elif windowType == "Update":
				messagebox.showinfo("Update Device","Device succesfully updated in smart start registry",parent=smartStartRegisterWindow)
			self.register_smart_start_device(smartStartRegisterWindow,"Register",0)
			
	def delete_smart_start_device_details(self,smartStartDetailsWindow,deviceDSKIterator):
		deviceIterator = int(deviceDSKIterator.get())
		result = messagebox.askokcancel("Delete Device","Select \"OK\" to remove device from the smart start registry\n",parent=smartStartDetailsWindow)
		if result == 1:
			result = self.zware.zw_net_provisioning_list_remove(self.smartStartList[deviceIterator]['dsk'])
			if result == "":
				self.clear_smart_start_info_for_device(str(deviceIterator))
				self.get_smart_start_devices_list(smartStartDetailsWindow)
			else:
				messagebox.showinfo("SmartStart delete device","Error removing device from the smart start registry",parent=smartStartDetailsWindow)

	def delete_all_smart_start_devices_details(self,smartStartDetailsWindow):
		result = messagebox.askokcancel("Delete all Devices","Select \"OK\" to remove all devices from the smart start registry\n",parent=smartStartDetailsWindow)
		if result == 1:
			result = self.zware.zw_net_provisioning_list_remove_all()
			if result == "":
				self.clear_smart_start_info_for_device("all_devices")
				self.get_smart_start_devices_list(smartStartDetailsWindow)
			else:
				messagebox.showinfo("SmartStart delete all device","Error removing all devices from the smart start registry",parent=smartStartDetailsWindow)

	def get_smart_start_devices_list(self,smartStartDetailsWindow):
		self.clear_frame(smartStartDetailsWindow)
		devices_info = self.zware.zw_net_provisioning_list_list_get()
		deviceIterator = 0
		for device in devices_info:
				self.smartStartList[deviceIterator]['dsk'] = device.get('dsk')
				self.smartStartList[deviceIterator]['deviceName'] = device.get('name')
				self.smartStartList[deviceIterator]['deviceLocation'] = device.get('loc')
				self.smartStartList[deviceIterator]['productType'] = device.get('pid_product_type')
				self.smartStartList[deviceIterator]['productId'] = device.get('pid_product_id')
				self.smartStartList[deviceIterator]['genericClass'] = device.get('ptype_generic')
				self.smartStartList[deviceIterator]['specificClass'] = device.get('ptype_specific')
				self.smartStartList[deviceIterator]['installerIcon'] = device.get('ptype_icon')
				self.smartStartList[deviceIterator]['vendor'] = device.get('pid_manufacturer_id')
				self.smartStartList[deviceIterator]['applicationVersion'] = device.get('pid_app_version')
				self.smartStartList[deviceIterator]['subVersion'] = device.get('pid_app_sub_version')
				self.smartStartList[deviceIterator]['interval'] = device.get('interval')
				self.smartStartList[deviceIterator]['uuidNumericFormat'] = device.get('uuid_format')
				self.smartStartList[deviceIterator]['uuid'] = device.get('uuid_data')
				self.smartStartList[deviceIterator]['bootMode'] = device.get('boot_mode')
				self.smartStartList[deviceIterator]['grantKeys'] = device.get('grant_keys')
				self.smartStartList[deviceIterator]['plStatus'] = device.get('pl_status')
				deviceIterator = deviceIterator + 1
		if deviceIterator == 0:
			self.create_label("No Smart start devices registered",smartStartDetailsWindow,0,0)
		else:
			smartStartDetailsWindow.dskVariable = IntVar()
			smartStartDetailsWindow.dskVariable.set(0)
			list_iterator = 1
			for i in range(self.MAXSMARTSTARTDEVICES):
				if self.smartStartList[i]['dsk'] != "":
					self.create_radiobutton(self.smartStartList[i]['dsk'],smartStartDetailsWindow.dskVariable,i,smartStartDetailsWindow,list_iterator,0)
					list_iterator = list_iterator + 1
			editDevice = self.create_button("Edit Device",smartStartDetailsWindow,list_iterator,0)
			editDevice.configure(command = lambda: self.register_smart_start_device(smartStartDetailsWindow,"Update",smartStartDetailsWindow.dskVariable))
			deleteDevice = self.create_button("Delete Device",smartStartDetailsWindow,list_iterator,1)
			deleteDevice.configure(command = lambda: self.delete_smart_start_device_details(smartStartDetailsWindow,smartStartDetailsWindow.dskVariable))
			deleteAllDevices = self.create_button("Delete All Devices",smartStartDetailsWindow,list_iterator,2)
			deleteAllDevices.configure(command = lambda: self.delete_all_smart_start_devices_details(smartStartDetailsWindow))

	def device_exclusion(self,Button):
		self.debugData.insert(INSERT,"Excluding device from the network....\n")
		Button['state'] = 'disabled'
		result = messagebox.askokcancel("Exclude Device","Initiate your device and select \"OK\" to remove it from the network\n")
		if result == 1:
			self.debugData.focus_force()
			r = self.zware.zw_add_remove(3)
			self.zware.zw_net_comp(3)
			self.debugData.insert(INSERT,"Device has been successfully removed from the network\n")
			self.poll_node_list(True)
			self.enable_disable_binary_switch()
		else:
			self.debugData.focus_force()
			self.debugData.insert(INSERT,"Device Exclusion cancelled\n")
		self.debugData.see(END)
		Button['state'] = 'normal'

	##
	#\addtogroup poll_network
	#@{
	#\section polling Network Polling
	#The client polls the network both automatically in the background as well as on user prompt with the "Node Details" button. On polling succesfully the client displays a list of nodes along with all available endpoints connected to them. It also displays a list of all the Command Classes supported by each endpoint. This is achieved using:<br>1. The Client queries for available nodes.<br>2. On succesfully retrieving the node list the client queries for available endpoints for each node.<br>3. Subsequently for each endpoint it will query for the supporting command classes. Once all data has been retrieved it will either be a:)Be displayed to the user if they had clicked on the "Node Details" button or b:)Be used for further background polling of devices.
	#\section tracking Tracking Devices
	#The client will constantly be polling the network for tracking devices and their state values. In the present version this support is provided for Binary Switches, Binary Sensors and Multilevel Sensors. For example whenever a binary switch is added or removed from a network the client will display this information to the user. This is achieved using the polling web-apis mentioned above along with identifying the binary switch using it's interface id.
	#@}
	def poll_node_list(self,buttonPress):
		for interface in self.deviceInterfaceList:
			self.deviceDictionaryList[interface]['tempFoundDevice'] = 0
		r = self.zware.zw_api('zwnet_get_node_list')
		nodes = r.findall('./zwnet/zwnode')
		for node in range(len(nodes)):
			if buttonPress:
				self.debugData.insert(INSERT,'node[' + str(node) + '] '+ "id:"+nodes[node].get('id') + "\n")
			r2 = self.zware.zw_api('zwnode_get_ep_list', 'noded=' + nodes[node].get('desc'))
			eps = r2.findall('./zwnode/zwep')
			for ep in range(len(eps)):
				if buttonPress:
					self.debugData.insert(INSERT,'\tendpoint name: ' + eps[ep].get('name') + "\n")
				epid = eps[ep].get('id')
				r3 = self.zware.zw_api('zwep_get_if_list', 'epd=' + eps[ep].get('desc'))
				intfs = r3.findall('./zwep/zwif')
				if buttonPress:
					self.debugData.insert (INSERT,"\t\tSupported Command Classes: \n")			
				for intf in range(len(intfs)):
					if (intfs[intf].get('name') != "Unknown"):
						if buttonPress:
							self.debugData.insert(INSERT,'\t\t' + intfs[intf].get('name')  + "\n")
						ifid = int(intfs[intf].get('id'))
						ifd = int(intfs[intf].get('desc'))
						for interface in self.deviceInterfaceList:
							if ifid == interface:
								self.deviceDictionaryList[interface]['ifdDevice'] = ifd
								self.deviceDictionaryList[interface]['tempFoundDevice'] = 1
		for interface in self.deviceInterfaceList:
			if self.deviceDictionaryList[interface]['tempFoundDevice'] != self.deviceDictionaryList[interface]['foundDevice']:
				self.deviceDictionaryList[interface]['previouslyFoundDevice'] = self.deviceDictionaryList[interface]['foundDevice']
			self.deviceDictionaryList[interface]['foundDevice'] = self.deviceDictionaryList[interface]['tempFoundDevice']

	def node_list_action(self):
		self.debugData.insert(INSERT,'Getting node details...\n')
		self.poll_node_list(True)
		self.debugData.insert(INSERT,'Finished getting node details\n')
		self.enable_disable_binary_switch()
		self.debugData.see(END)

	##
	#\addtogroup binary_switch
	#@{
	#\section polling_switch Polling Binary Switch state
	#On polling for node list the client will also track device and their state values. This is applicable to Binary Switches in this version. Once a binary switch is found in the network the client will retrieve the switch's last known state from the server. Every time the binary switch's state changes it will send out a report to the server which will be stored as the last known state in the server.
	#\section toggle_switch Toggle Binary Switch
	#Whenever a binary switch is detected in the network the "Toggle Switch" button will be visible in the client. Note that this is possible when a)polling the network and detecting a binary switch or b)Including a binary switch using the client.<br> Once the button is visible the user can manually change the state of the binary switch by clicking on the button. For example if the switch is turned off and the user presses the button it will be turned on.
	#\section Stop Binary Switch tracking
	#Whenever a binary switch is removed from the network the client will inform this to the user. Once the switch is removed the "Toggle Switch" button will be no longer be visible in the client. The removal can happen either using the client's "Exclude Device" button or by removing the switch from the network manually by the user. In either case the information will be relayed to the user by the client.
	#@}
	def poll_binary_switch(self):
		if self.deviceDictionaryList[self.BINARYSWITCHINTERFACE]['foundDevice'] == 1:
			self.zware.zwif_switch_api(self.deviceDictionaryList[self.BINARYSWITCHINTERFACE]['ifdDevice'], 1)
			v = int(self.zware.zwif_switch_api(self.deviceDictionaryList[self.BINARYSWITCHINTERFACE]['ifdDevice'], 3).get('state'))
			if self.deviceDictionaryList[self.BINARYSWITCHINTERFACE]['previouslyFoundDevice'] == 0:
				self.debugData.insert(INSERT,"Polling: Switch found in network\n")
				self.enable_disable_binary_switch()
				self.deviceDictionaryList[self.BINARYSWITCHINTERFACE]['previouslyFoundDevice'] = 1
				if v == 255:
					self.debugData.insert(INSERT,"Polling: Switch is turned on\n")
				else:
					self.debugData.insert(INSERT,"Polling: Switch is turned off\n")
				self.deviceDictionaryList[self.BINARYSWITCHINTERFACE]['defaultState'] = v
			if self.deviceDictionaryList[self.BINARYSWITCHINTERFACE]['defaultState'] != v:
				if v == 255:
					self.debugData.insert(INSERT,"Polling: Switch has been turned on\n")
				else:
					self.debugData.insert(INSERT,"Polling: Switch has been turned off\n")
				self.deviceDictionaryList[self.BINARYSWITCHINTERFACE]['defaultState'] = v
		elif self.deviceDictionaryList[self.BINARYSWITCHINTERFACE]['previouslyFoundDevice'] == 1:
				self.debugData.insert(INSERT,"Polling: Switch removed from network\n")
				self.enable_disable_binary_switch()
				self.deviceDictionaryList[self.BINARYSWITCHINTERFACE]['previouslyFoundDevice'] = 0
		if self.runPollingThread:
			self.debugData.see(END)

	def binary_switch_action(self):
		timer = 0
		if self.deviceDictionaryList[self.BINARYSWITCHINTERFACE]['foundDevice'] == 0:
			self.debugData.insert(INSERT,"No switch is found in network\n")
		else:
			ifd = self.deviceDictionaryList[self.BINARYSWITCHINTERFACE]['ifdDevice']
			if self.deviceDictionaryList[self.BINARYSWITCHINTERFACE]['defaultState'] == 0:
				self.zware.zwif_switch_api(ifd, 1)
				self.zware.zwif_switch_api(ifd, 4, "&value=1")
				timer = 0
				v = int(self.zware.zwif_switch_api(ifd, 2).get('state'))
				while (v == 0) and (timer < 10):
					v = int(self.zware.zwif_switch_api(ifd, 2).get('state'))
					time.sleep(2)
					timer = timer + 1
				self.deviceDictionaryList[self.BINARYSWITCHINTERFACE]['defaultState'] = v
				if v == 255:
					self.debugData.insert(INSERT,"Switch has been turned on\n")
				else:
					self.debugData.insert(INSERT,"Switch could not be turned on\n")
			else:
				self.zware.zwif_switch_api(ifd, 1)
				self.zware.zwif_switch_api(ifd, 4, "&value=0")
				timer = 0			
				v = int(self.zware.zwif_switch_api(ifd, 2).get('state'))
				while (v == 255) and (timer < 10):
					v = int(self.zware.zwif_switch_api(ifd, 2).get('state'))
					time.sleep(2)
					timer = timer + 1
				self.deviceDictionaryList[self.BINARYSWITCHINTERFACE]['defaultState'] = v
				if v == 0:
					self.debugData.insert(INSERT,"Switch has been turned off\n")
				else:
					self.debugData.insert(INSERT,"Switch could not be turned off\n")	
		self.debugData.see(END)

	def enable_disable_binary_switch(self):
		if self.deviceDictionaryList[self.BINARYSWITCHINTERFACE]['foundDevice'] == 0:
			self.binarySwitchButton.grid_remove()
		else:
			self.binarySwitchButton.grid()
	##
	#\addtogroup binary_sensor
	#@{
	#\section polling_sensor Polling Binary Sensor State
	#On polling for node list the client will also track device and their state values. This is applicable to Binary Sensors in this version. Once a binary sensor is found in the network the client will retrieve the sensor's last known state from the server. Every time the binary sensor's state changes it will send out a report to the server which will be stored as the last known state in the server. Additionally along with the value the client will also display the sensor type.
	#@}
	def poll_binary_sensor(self):
		if self.deviceDictionaryList[self.BINARYSENSORINTERFACE]['foundDevice'] == 1:
			self.zware.zwif_bsensor_api(self.deviceDictionaryList[self.BINARYSENSORINTERFACE]['ifdDevice'], 1)
			r = self.zware.zwif_bsensor_api(self.deviceDictionaryList[self.BINARYSENSORINTERFACE]['ifdDevice'], 3)
			v = int(r.get('state'))
			t = r.get('type')
			binary_sensor_type = "Polling: Binary Sensor type:" + t + "\n"
			if self.deviceDictionaryList[self.BINARYSENSORINTERFACE]['previouslyFoundDevice'] == 0:
				self.debugData.insert(INSERT,"Polling: Binary Sensor found in network\n")
				self.deviceDictionaryList[self.BINARYSENSORINTERFACE]['previouslyFoundDevice'] = 1
				if v == 255:
					self.debugData.insert(INSERT,binary_sensor_type)
					self.debugData.insert(INSERT,"Polling: Binary Sensor has detected an event\n")
				else:
					self.debugData.insert(INSERT,binary_sensor_type)
					self.debugData.insert(INSERT,"Polling: Binary Sensor is idle\n")
				self.deviceDictionaryList[self.BINARYSENSORINTERFACE]['defaultState'] = v
			if v == 255:
				self.debugData.insert(INSERT,binary_sensor_type)
				self.debugData.insert(INSERT,"Polling: Binary Sensor has detected an event\n")
				self.deviceDictionaryList[self.BINARYSENSORINTERFACE]['defaultState'] = v
		elif self.deviceDictionaryList[self.BINARYSENSORINTERFACE]['previouslyFoundDevice'] == 1:
				self.debugData.insert(INSERT,"Polling: Binary Sensor removed from network\n")
				self.deviceDictionaryList[self.BINARYSENSORINTERFACE]['previouslyFoundDevice'] = 0
		if self.runPollingThread:
			self.debugData.see(END)

	##
	#\addtogroup multilevel_sensor
	#@{
	#\section polling_msensor Polling Multilevel Sensor Data
	#On polling for node list the client will also track device and their state values. This is applicable to Multilevel Sensors in this version. Once a multilevel sensor is found in the network the client will retrieve the sensor's last known value from the server. Every time the multilevel sensor's value changes it will send out a report to the server which will be stored as the last known value in the server. Additionally along with the value the client will also display the sensor type, precision and unit.
	#@}
	def poll_multilevel_sensor(self):
		if self.deviceDictionaryList[self.MULTILEVELSENSORINTERFACE]['foundDevice'] == 1:
			self.zware.zwif_sensor_api(self.deviceDictionaryList[self.MULTILEVELSENSORINTERFACE]['ifdDevice'], 1)
			r = self.zware.zwif_sensor_api(self.deviceDictionaryList[self.MULTILEVELSENSORINTERFACE]['ifdDevice'], 3)
			v = r.get('value')
			t = r.get('type')
			p = int(r.get('precision'))
			u = r.get('unit')
			multilevel_poll_data = "Polling:Multilevel Sensor Type:" + t + "," + "Value:" + v + "," + "Precision:" + p + "," + "Unit:" + u + "\n"		
			if self.deviceDictionaryList[self.MULTILEVELSENSORINTERFACE]['previouslyFoundDevice'] == 0:
				self.debugData.insert(INSERT,"Polling: Multilevel Sensor found in network\n")
				self.deviceDictionaryList[self.MULTILEVELSENSORINTERFACE]['previouslyFoundDevice'] = 1
				self.debugData.insert(INSERT,multilevel_poll_value)
				self.deviceDictionaryList[self.MULTILEVELSENSORINTERFACE]['defaultState'] = v
			if self.deviceDictionaryList[self.MULTILEVELSENSORINTERFACE]['defaultState'] != v:
				self.debugData.insert(INSERT,"Polling: Multilevel Sensor Updated\n")
				self.debugData.insert(INSERT,multilevel_poll_value)
				self.deviceDictionaryList[self.MULTILEVELSENSORINTERFACE]['defaultState'] = v
		elif self.deviceDictionaryList[self.MULTILEVELSENSORINTERFACE]['previouslyFoundDevice'] == 1:
				self.debugData.insert(INSERT,"Polling: Multilevel Sensor removed from network\n")
				self.deviceDictionaryList[self.MULTILEVELSENSORINTERFACE]['previouslyFoundDevice'] = 0
		if self.runPollingThread:
			self.debugData.see(END)

	#Background polling
	def poll_server(self):
		while self.runPollingThread:
			self.poll_node_list(False)
			self.poll_binary_switch()
			self.poll_binary_sensor()
			self.poll_multilevel_sensor()
			time.sleep(2)

	#GUI Rendering and Code Cleaning
	def client_init(self):
		self.runPollingThread = True

	def create_thread(self):
		userThread = Thread(target=self.poll_server)
		userThread.daemon = True
		userThread.start()

	def create_window(self,windowName):
		userWindow = Toplevel()
		userWindow.title(windowName)
		return userWindow

	def create_frame(self,container):
		userFrame = Frame(container)
		userFrame.pack()
		return userFrame

	def clear_frame(self,frame):
		for widget in frame.winfo_children():
			widget.destroy()

	def disable_frame(self,frame):
		for widget in frame.winfo_children():
			widget.configure(state='disable')

	def enable_frame(self,frame):
		for widget in frame.winfo_children():
			widget.configure(state='active')

	def create_text(self,container,rowNumber,columnNumber):
		userText = Text(container)
		userText.grid(row=rowNumber,column=columnNumber,sticky=(N,S,E,W))
		return userText

	def create_scrollbar(self,container,rowNumber,columnNumber):
		userScrollBar = Scrollbar(container)
		userScrollBar.grid(row=rowNumber,column=columnNumber,sticky=(N,S,E,W))
		return userScrollBar

	def create_label(self,labelName,container,rowNumber,columnNumber):
		userLabel = Label(container, text=labelName)
		userLabel.grid(row=rowNumber,column=columnNumber,sticky=(N,S,E,W))
		return userLabel

	def create_radiobutton(self,buttonName,buttonVariable,buttonValue,container,rowNumber,columnNumber):
		Radiobutton(container,text=buttonName,variable=buttonVariable,value=buttonValue).grid(row=rowNumber,column=columnNumber,sticky=(N,S,E,W))

	def create_checkbox(self,checkboxName,checkboxVariable,container,rowNumber,columnNumber):
		userCheckBox = Checkbutton(container,text=checkboxName,variable=checkboxVariable)
		userCheckBox.grid(row=rowNumber,column=columnNumber,sticky=(N,S,E,W))
		return userCheckBox

	def create_drop_down_list(self,dropDownListVariable,container,listitem1,listitem2,listitem3,rowNumber,columnNumber):
		OptionMenu(container,dropDownListVariable,listitem1,listitem2,listitem3).grid(row=rowNumber,column=columnNumber,sticky=(N,S,E,W))

	def create_entry(self,container,rowNumber,columnNumber):
		userEntry = Entry(container)
		userEntry.grid(row=rowNumber,column=columnNumber,sticky=(N,S,E,W))
		return userEntry

	def create_button(self,buttonName,container,rowNumber,columnNumber):
		userButton = Button(container, text = buttonName)
		userButton.grid(row=rowNumber, column=columnNumber,sticky=(N,S,E,W))
		return userButton

	def close_window(self,Toplevel):
		Toplevel.destroy()
		self.runPollingThread = False

	def close_child_window_and_refocus_main_window(self,childWindow,mainWindow):
		childWindow.destroy()
		mainWindow.deiconify()

	def close_connection(self,Button,initialFrame,buttonFrame):
		Button['state'] = 'normal'
		self.enable_frame(initialFrame)
		self.clear_frame(buttonFrame)
		self.debugData.delete('1.0', END)
		self.runPollingThread = False

## 
#\mainpage ZWare Sample Client User Guide
#
#\section intro Introduction
#The ZWare Sample Client is an easy-to-use application which demonstrates a selection of the Z-Ware Web API to the user. The Client assists a Z-Wave supported device to communicate with a Z-Ware web server.
#\subsection prerequisites Prerequisites
#This guide describes how to setup and run the client on a PC.<br>
#\ref setup "Dependencies and Setup"
#\section function Functionality
#The ZWare Sample Client currently supports the following functionality:<br>1.Connect to either a ZWare local or portal server<br>2.Include a device securely/unsecurely to the network<br>3.Exclude a device from the network<br>4.Poll the network to get a list of nodes.<br>5.Poll the network to get the status of a binary switch (if any), binary sensor (if any) and multilevel sensor (if any) that is connected to the network and <br>6.Toggle a binary switch (if any) in the network to change it's current state using the application<br>7.Manage smart start devices in the zware network<br>
#\section details Details
#\ref connect "Connect to a network"<br>
#\ref poll_network "Polling the network"<br>
#\ref include_exclude "Including/Excluding a device"<br>
#\ref smartstart "Managing smart start devices in the network"<br>
#\ref binary_switch "Working with Binary Switches"<br>
#\ref binary_sensor "Working with Binary Sensors"<br>
#\ref multilevel_sensor "Working with Multilevel Sensors"<br>
#\defgroup setup Dependencies and Setup
#@{
#\section dependencies Dependencies
#1.Ensure that the PC has a network connection.<br>2.Python 3 should be installed on the PC. The recommended version is 3.5.2.<br>3.Install the python library <b>requests</b> by going to the command line and running \verbatim python -m pip install requests \endverbatim If the library is not available python will download and install it.
#\section setup Setup
#1.Ensure that the ZWare web server and the ZIP Gateway (Z-Wave over Internet Protocol Gateway) are installed on the Raspberry Pi board provided to the user.<br>2.Refer to the respective documentation of the ZWare web server and the ZIP Gateway in order to correctly install and configure them for use with the ZWare Sample Client.<br>3.The ZIP Gateway should be able to connect to the ZWare server.<br>4.Ensure that a Z-Wave supported device is available for using with the client.
#@}
#\defgroup connect Connect to a network
#\defgroup poll_network Polling the network
#\defgroup include_exclude Include and Exclude a device
#\defgroup smartstart Managing smart start devices in the network
#\defgroup binary_switch Working with Binary Switch
#\defgroup binary_sensor Working with Binary Sensor
#\defgroup multilevel_sensor Working with Multilevel Sensor

#Application Entry point
def main():
	zware_client_window = Tk()
	zware_client_window.title("Z-Ware Sample Client")
	zware = zwareWebApi()
	zwareClient = zwareClientClass(zware)
	zwareClient.main_window(zware_client_window)
	zware_client_window.mainloop()

main()
