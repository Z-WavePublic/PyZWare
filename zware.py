#Copyright 2014-2018 Silicon Laboratories Inc.
#The licensor of this software is Silicon Laboratories Inc.  Your use of this software is governed by the terms of  Silicon Labs Z-Wave Development Kit License Agreement.  A copy of the license is available at www.silabs.com.  

import requests
import xml.etree.ElementTree as ET
import sys

class zwareWebApi:
	zwareSession = None
	zwareUrl = ""

	""" web api wrapper """
	def zw_api(self,uri, parm=''):
		try:
			r = self.zwareSession.post(self.zwareUrl + uri, data=parm, verify=False)
		except:
			assert False, print(sys.exc_info()[0])
		assert r.status_code == 200, r.status_code
		try:
			x = ET.fromstring(r.text)
		except:
			return r.text
		e = x.find('./error')
		assert e == None, e.text
		return x

	""" Network operations """
	def zw_net_wait(self):
		while int(self.zw_api('zwnet_get_operation').find('./zwnet/operation').get('curr_op')):
			pass

	def zw_net_comp(self,op):
		while op != int(self.zw_api('zwnet_get_operation').find('./zwnet/operation').get('prev_op')):
			pass

	def zw_net_op_sts(self,op):
		while op != int(self.zw_api('zwnet_get_operation').find('./zwnet/operation').get('op_sts')):
			pass

	def zw_net_get_grant_keys(self):
		grant_key = self.zw_api('zwnet_add_s2_get_req_keys').find('./zwnet/security').get('req_key')
		return grant_key

	def zw_net_add_s2_get_dsk(self):
		dsk = self.zw_api('zwnet_add_s2_get_dsk').find('./zwnet/security').get('dsk')
		return dsk

	def zw_net_set_grant_keys(self,grant_key):
		return self.zw_api('zwnet_add_s2_set_grant_keys','granted_keys='+grant_key)

	def zw_net_provisioning_list_add(self,dsk,bootMode,grantKeys,interval,deviceName,deviceLocation,applicationVersion,subVersion,vendor,productId,productType,status,genericClass,specificClass,installerIcon,uuidFormat,uuid):
		provisioningListString = 'dsk='+dsk
		if deviceName != "":
			provisioningListString = provisioningListString + '&name='+deviceName
		if deviceLocation != "":
			provisioningListString = provisioningListString + '&loc='+deviceLocation
		if genericClass != "":
			provisioningListString = provisioningListString + '&ptype_generic='+genericClass
		if specificClass != "":
			provisioningListString = provisioningListString + '&ptype_specific='+specificClass
		if installerIcon != "":
			provisioningListString = provisioningListString + '&ptype_icon='+installerIcon
		if vendor != "":
			provisioningListString = provisioningListString + '&pid_manufacturer_id='+vendor
		if productType != "":
			provisioningListString = provisioningListString + '&pid_product_type='+productType
		if productId != "":
			provisioningListString = provisioningListString + '&pid_product_id='+productId
		if applicationVersion != "":
			provisioningListString = provisioningListString + '&pid_app_version='+applicationVersion
		if subVersion != "":
			provisioningListString = provisioningListString + '&pid_app_sub_version='+subVersion
		if interval != "":
			provisioningListString = provisioningListString + '&interval='+interval
		if uuidFormat != "":
			provisioningListString = provisioningListString + '&uuid_format='+uuidFormat
		if uuid != "":
			provisioningListString = provisioningListString + '&uuid_data='+uuid
		if status != "":
			provisioningListString = provisioningListString + '&pl_status='+status
		if grantKeys != "":
			provisioningListString = provisioningListString + '&grant_keys='+grantKeys
		if bootMode != "":
			provisioningListString = provisioningListString + '&boot_mode='+bootMode
		return self.zw_api('zwnet_provisioning_list_add',provisioningListString)

	def zw_net_provisioning_list_list_get(self):
		devices_info = self.zw_api('zwnet_provisioning_list_list_get').findall('./zwnet/pl_list/pl_device_info')
		return devices_info
		
	def zw_net_provisioning_list_remove(self,dsk):
		result = self.zw_api('zwnet_provisioning_list_remove','dsk='+dsk)
		return result

	def zw_net_provisioning_list_remove_all(self):
		result = self.zw_api('zwnet_provisioning_list_remove_all')
		return result

	def zw_net_set_dsk(self,dsk):
		return self.zw_api('zwnet_add_s2_accept','accept=1&value='+dsk)

	def zw_init(self,url='https://127.0.0.1/', user='test_user', pswd='test_password'):
		self.zwareSession = requests.session()
		self.zwareUrl = url
		self.zwareSession.headers.update({'Content-Type':'application/x-www-form-urlencoded'}) # apache requires this
		self.zw_api('register/login.php', 'usrname='+ user + '&passwd=' + pswd) 
		self.zwareUrl += 'cgi/zcgi/networks//'
		return self.zw_api('zw_version')

	def zw_add_remove(self,cmd):
		return self.zw_api('zwnet_add','cmd='+str(cmd))

	def zw_abort(self):
		return self.zw_api('zwnet_abort','')

	""" Interfaces """

	def zwif_api(self,dev, ifd, cmd=1, arg=''):
		return self.zw_api('zwif_' + dev, 'cmd=' + str(cmd) + '&ifd=' + str(ifd) + arg)

	def zwif_api_ret(self,dev, ifd, cmd=1, arg=''):
		r = self.zwif_api(dev, ifd, cmd, arg)
		if cmd == 2 or cmd == 3:
			return r.find('./zwif/' + dev)
		return r

	def zwif_basic_api(self,ifd, cmd=1, arg=''):
		return self.zwif_api_ret('basic', ifd, cmd, arg)

	def zwif_switch_api(self,ifd, cmd=1, arg=''):
		return self.zwif_api_ret('switch', ifd, cmd, arg)

	def zwif_level_api(self,ifd, cmd=1, arg=''):
		return self.zwif_api_ret('level', ifd, cmd, arg)

	def zwif_doorlock_api(self,ifd, cmd=1, arg=''):
		r = self.zwif_api('dlck', ifd, cmd, arg)
		if cmd == 2 or cmd == 3:
			return r.find('./zwif/dlck_op')
		elif cmd == 5 or cmd == 6:
			return r.find('./zwif/dlck_cfg')
		return r

	def zwif_usercode_api(self,ifd, cmd=1, arg=''):
		r = self.zwif_api('usrcod', ifd, cmd, arg)
		if cmd == 1 or cmd == 2:
			return r.find('./zwif/usrcod')
		elif cmd == 4:
			return r.find('./zwif/usrcod_sup')
		return r

	def zwif_thermo_list_api(self,dev, ifd, cmd=1, arg=''):
		r = self.zwif_api_ret('thrmo_' + dev, ifd, cmd, arg)
		if cmd == 5 or cmd == 6:
			return r.find('./zwif/thrmo_' + dev + '_sup')
		return r

	def zwif_thermo_mode_api(self,ifd, cmd=1, arg=''):
		return self.zwif_thermo_list_api('md', ifd, cmd, arg)

	def zwif_thermo_state_api(self,ifd, cmd=1, arg=''):
		return self.zwif_api_ret('thrmo_op_sta', ifd, cmd, arg)

	def zwif_thermo_setpoint_api(self,ifd, cmd=1, arg=''):
		return self.zwif_thermo_list_api('setp', ifd, cmd, arg)

	def zwif_thermo_fan_mode_api(self,ifd, cmd=1, arg=''):
		return self.zwif_thermo_list_api('fan_md', ifd, cmd, arg)

	def zwif_thermo_fan_state_api(self,ifd, cmd=1, arg=''):
		return self.zwif_api_ret('thrmo_fan_sta', ifd, cmd, arg)

	def zwif_meter_api(self,ifd, cmd=1, arg=''):
		return self.zwif_api_ret('meter', ifd, cmd, arg)

	def zwif_bsensor_api(self,ifd, cmd=1, arg=''):
		return self.zwif_api_ret('bsensor', ifd, cmd, arg)

	def zwif_sensor_api(self,ifd, cmd=1, arg=''):
		return self.zwif_api_ret('sensor', ifd, cmd, arg)

	def zwif_battery_api(self,ifd, cmd=1, arg=''):
		return self.zwif_api_ret('battery', ifd, cmd, arg)

	def zwif_av_api(self,ifd, cmd=1, arg=''):
		r = self.zwif_api('av', ifd, cmd, arg)
		if cmd == 2 or cmd == 3:
			return r.find('./zwif/av_caps')
		return r
