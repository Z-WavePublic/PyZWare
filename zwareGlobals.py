BINARY_SWITCH_INTERFACE = 37
BINARY_SENSOR_INTERFACE = 48
MULTILEVEL_SENSOR_INTERFACE = 49
device_interface_list = [BINARY_SWITCH_INTERFACE,BINARY_SENSOR_INTERFACE,MULTILEVEL_SENSOR_INTERFACE]
device_dictionary_list = {}
for interface in device_interface_list:
	device_dictionary_list[interface] = {}
	device_dictionary_list[interface]['defaultState'] = -1
	device_dictionary_list[interface]['foundDevice'] = 0
	device_dictionary_list[interface]['tempFoundDevice'] = 0	
	device_dictionary_list[interface]['previouslyFoundDevice'] = 0
	device_dictionary_list[interface]['ifdDevice'] = 0
runPollingThread = True
debugData = None
binarySwitchButton = None
zwareSession = None
zwareUrl = ""
