# Domoticz Tinkerforge Plugin - TrafficLight
20190526 by Robert W.B. Linn (rwblinn@outlook.de)

# Objectives
* To set the color of a Tinkerforge RGB Bricklet to red, yellow or green using a Domoticz Selector Switch Device.
* To learn how to write generic Python [plugin(s)](https://www.domoticz.com/wiki/Developing_a_Python_plugin) for the Domoticz Home Automation System.
* To learn how to interact7 with [Tinkerforge](http://www.tinkerforge.com) Building Blocks.
* To use this sample plugin as a template for other Domoticz plugins interacting with Tinkerforge Building Blocks.

## Solution
A Domoticz Python plugin "Traffic Light" with a Tinkerforge RGB LED Bricklet.
The Tinkerforge RGB LED Bricklet is connected to a Tinkerforge Master Brick with WiFi extension.

## Hardware Parts
* Raspberry Pi 3B+
* Tinkerforge Master Brick 1.1 [ref](https://www.tinkerforge.com/en/doc/Hardware/Bricks/Master_Brick.html#master-brick)
* Tinkerforge WIFI Master Extention 2.0 [ref](https://www.tinkerforge.com/en/doc/Hardware/Master_Extensions/WIFI_V2_Extension.html)
* Tinkerforge RGB LED Bricklet [ref](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/RGB_LED.html)

## Software
Versions for developing & using this plugin.
* Raspberry Pi Raspian Linux 4.19.42-v7+ #1219
* Domoticz Home Automation System V4.1nnnn (BETA)
* Tinkerforge Python Binding v2.1.22
* Python 3.5.3
* Thonny 3.1.2 (Python IDE)

## Setup Tinkerforge and Domoticz
For details setting up Tinkerforge and Domoticz read the documentation **SETUP.md**.
Below steps are how to in a nutshell.

## Tinkerforge Python API bindings
sudo pip3 install tinkerforge
Check if Tinkerforge Python API bindings are installed in folder: /usr/local/lib/python3.5/dist-packages

## Tinkerforge Master Brick and Bricklets
Ensure the Master Brick and Bricklets are running with the latest firmware.
See **SETUP.md**.

## Traffic Light Prototype
Build the prototype by connecting the Tinkerforge building blocks (see hardware).
Connect the Master Brick to a device running the Brick Deamon and Viewer.
Summary steps to setup the Tinkerforge building blocks using the Tinkerforge Brick Viewer.
* Update the devices firmware
* Set the WiFi master extension fixed IP address in client mode
* Obtain the UID's of the Tinkerforge bricklets as required by the Python plugin

After setting up the Tinkerforge building blocks, reset the master brick and check if the master brick can be reached via WLAN:
ping tf-wifi-ext-ip-address

## Domoticz Plugin Folder and File
mkdir /home/pi/domoticz/plugins/trafficlight
As a starter, take the template from [here](https://github.com/domoticz/domoticz/blob/master/plugins/examples/BaseTemplate.py).
Save as plugin.py in the folder /home/pi/domoticz/plugins/trafficlight

## Python Plugin Path to Tinkerforge API Bindings
In the Python Plugin code (**plugin.py**) amend the import path to enable using the Tinkerforge API Bindings:
	from os import path
	import sys
	sys.path
	sys.path.append('/usr/lib/python3/dist-packages')

## Development Setup
Development PC:
* Thonny to develop the Python Plugin
* A shared drive Z: is defined pointing to /home/pi/domoticz
* Browser Tab Domoticz Web UI > Setup > Log
* Browser Tab Domoticz Web UI > Setup > Hardware
* Browser Tab Domoticz Web UI > Setup > Devices
* WinSCP session connected to the Domoticz server
* Putty session connected to the Domoticz server

The Browser tabs required to add the new hardware with its device and monitor if the plugin code is running without errors.

## Development Iteration
The development process step used are:
1. Thonny develop z:\plugins\trafficlight\plugin.py
2. Make changes and save plugin.py
3. Restart Domoticz from Terminal: sudo service domoticz.sh restart
4. Wait a moment and refresh the Browser Tab Domoticz Web UI > Log
5. Check the log and fix as required

!IMPORTANT!
In the Domoticz Web UI > Setup > Settings,  enable accepting new hardware.
This is required to add the new hardware with its device and monitor if the plugin code is running without errors.

## Domoticz Web UI's
Open windows Domoticz Setup > Hardware, Domoticz Setup > Log, Domoticz Setup > Devices
This is required to add the new hardware with its device and monitor if the plugin code is running without errors.

## Create the plugin
The plugin has a mandatory filename plugin.py located in the newly created plugin folder
For Python development Thonny, running on a Windows 10 device, is used.

See APPENDIX Domoticz Python Plugin Code (well documented).

Domoticz Devices created and set as used.
	Domoticz.Device(Name="State Selector", Unit=1, TypeName="Selector Switch",  Options=Options, Used=1).Create()            
	Domoticz.Device(Name="Alert Indicator", Unit=2, TypeName="Alert", Used=1).Create()
	Domoticz.Device(Name="Change Info", Unit=3, TypeName="Text", Used=1).Create()

The devices are manually added to the Domoticz Dashboard.

Handling the state change of the Traffic Light Selector Switch is done by the **onCommand** function.
This function updates the state of the Domoticz Devices: State Selector (idx=13), Alert Indicator (idx=14), Change Info (idx=15).

Pseudo Code
* FIRST TIME: onStart to create the Domoticz Devices
* NEXT TIMES: onCommand to handle state changes
	* Domoticz make IP connection to the Tinkerforge Master Brick
	* Get the Level of the Domoticz Device "State Selector" (Selector Switch)
	* Update the Tinkerforge Bricklet RGB LED with the new color depending Level
	* Update the Domoticz Devices "Alert Indicator" and "State Info"
	* Domoticz to disconnect from the Tinkerforge Master Brick

**Note**
onHeartbeat is not used as not polling for the state of a Tinkerforge Bricklet and update Domoticz Device(s) accordingly.

## Restart Domoticz
Restart Domoticz to find the plugin:
sudo systemctl restart domoticz.service

**Note**
When making changes to the Python plugin code, ensure to restart Domoticz and refresh any of the Domoticz Web UI's.

## Domoticz Add Hardware Traffic Light
**IMPORTANT**
Prior adding, set in the Domoticz Settings the option to allow new hardware.
If this option is not enabled, no new soilmoisture device is created.
Check in the Domoticz log as error message Python script at the line where the new device is used
(i.e. Domoticz.Debug("Device created: "+Devices[1].Name))

In Domoticz Web UI, select tab Setup > Hardware and add the new hardware Traffic Light.
The initial check interval is set at 60 seconds. This is a good value for testing, but for finalversion set tohigher value like once per hour (3600 seconds).

## Add Hardware - Check the Domoticz Log
After adding,ensure to check the Domoticz Log (Domoticz Web UI, select tab Setup > Log)
Example:
```
2019-05-27 09:43:31.992 Status: (Traffic Light) Started. 
2019-05-27 09:43:32.550 (Traffic Light) Debug logging mask set to: PYTHON PLUGIN QUEUE IMAGE DEVICE CONNECTION MESSAGE ALL 
2019-05-27 09:43:32.550 (Traffic Light) 'DomoticzHash':'fccd39bb' 
2019-05-27 09:43:32.550 (Traffic Light) 'HardwareID':'7' 
2019-05-27 09:43:32.550 (Traffic Light) 'Database':'/home/pi/domoticz/domoticz.db' 
2019-05-27 09:43:32.550 (Traffic Light) 'Version':'1.0.0' 
2019-05-27 09:43:32.550 (Traffic Light) 'HomeFolder':'/home/pi/domoticz/plugins/TrafficLight/' 
2019-05-27 09:43:32.550 (Traffic Light) 'DomoticzVersion':'4.10826' 
2019-05-27 09:43:32.550 (Traffic Light) 'Name':'Traffic Light' 
2019-05-27 09:43:32.550 (Traffic Light) 'Mode6':'Debug' 
2019-05-27 09:43:32.550 (Traffic Light) 'DomoticzBuildTime':'2019-05-24 10:04:40' 
2019-05-27 09:43:32.550 (Traffic Light) 'Mode4':'100' 
2019-05-27 09:43:32.550 (Traffic Light) 'StartupFolder':'/home/pi/domoticz/' 
2019-05-27 09:43:32.550 (Traffic Light) 'Port':'4223' 
2019-05-27 09:43:32.550 (Traffic Light) 'Key':'TrafficLight' 
2019-05-27 09:43:32.550 (Traffic Light) 'Language':'en' 
2019-05-27 09:43:32.550 (Traffic Light) 'Address':'192.168.N.NNN' 
2019-05-27 09:43:32.550 (Traffic Light) 'Author':'rwbL' 
2019-05-27 09:43:32.550 (Traffic Light) 'UserDataFolder':'/home/pi/domoticz/' 
2019-05-27 09:43:32.550 (Traffic Light) 'Mode1':'zMF' 
2019-05-27 09:43:32.550 (Traffic Light) Device count: 0 
2019-05-27 09:43:32.550 (Traffic Light) Creating new Devices 
2019-05-27 09:43:32.551 (Traffic Light) Creating device 'State Selector'. 
2019-05-27 09:43:32.552 (Traffic Light) Device created: Traffic Light - State Selector 
2019-05-27 09:43:32.552 (Traffic Light) Creating device 'Alert Indicator'. 
2019-05-27 09:43:32.553 (Traffic Light) Device created: Traffic Light - Alert Indicator 
2019-05-27 09:43:32.553 (Traffic Light) Creating device 'Change Info'. 
2019-05-27 09:43:32.554 (Traffic Light) Device created: Traffic Light - Change Info 
2019-05-27 09:43:32.554 (Traffic Light) Pushing 'PollIntervalDirective' on to queue 
2019-05-27 09:43:32.554 (Traffic Light) Processing 'PollIntervalDirective' message 
2019-05-27 09:43:32.554 (Traffic Light) Heartbeat interval set to: 60. 
2019-05-27 09:43:32.547 Status: (Traffic Light) Entering work loop. 
2019-05-27 09:43:32.548 Status: (Traffic Light) Initialized version 1.0.0, author 'rwbL' 
```
## Domoticz Log Entry State Change Off to RED
Handling the state changes are managed by the function onCommand.
```
2019-05-27 09:51:50.997 Status: User: Admin initiated a switch command (13/Traffic Light - State Selector/Set Level) 
2019-05-27 09:51:51.002 (Traffic Light) Processing 'onCommandCallback' message 
2019-05-27 09:51:51.002 (Traffic Light) Calling message handler 'onCommand'. 
2019-05-27 09:51:51.003 (Traffic Light) onCommand called for Unit 1: Parameter 'Set Level', Level: 10 
2019-05-27 09:51:51.012 (Traffic Light) IP Connection - OK 
2019-05-27 09:51:51.012 (Traffic Light) Traffic Light - State Selector-Traffic Light State New=10 
2019-05-27 09:51:51.012 (Traffic Light) Traffic Light - State Selector-nValue=0,sValue= 
2019-05-27 09:51:51.017 (Traffic Light) Traffic Light - State Selector-RGB LED Colors R-G-B:0-100-0 
2019-05-27 09:51:51.018 (Traffic Light) RGB LED Brightness updated:100 
2019-05-27 09:51:51.018 (Traffic Light - State Selector) Updating device from 0:'' to have values 2:'10'. 
2019-05-27 09:51:51.030 (Traffic Light) Traffic Light - State Selector-nValue=2,sValue=10 
2019-05-27 09:51:51.030 (Traffic Light - Alert Indicator) Updating device from 0:'No Alert!' to have values 4:'RED'. 
2019-05-27 09:51:51.038 (Traffic Light) Traffic Light - Alert Indicator-nValue=4,sValue=RED 
2019-05-27 09:51:51.038 (Traffic Light - Change Info) Updating device from 0:'' to have values 0:'Traffic Light changed from 0 to 10'. 
2019-05-27 09:51:51.045 (Traffic Light) Traffic Light - Change Info-nValue=0,sValue=Traffic Light changed from 0 to 10 
2019-05-27 09:51:51.148 (Traffic Light) TrafficLight Update: OK 
```

## ToDo
Exception handling for communicating with the Master Brick & WiFi extension.

## Version
20190527

## APPENDIX Tinkerforge - Master Brick and Bricklets
Ensure the Master Brick and Bricklets are running with the latest firmware.
To update the Tinkerforge [Brick Viewer](https://www.tinkerforge.com/en/doc/Software/Brickv.html#brickv) is required.
For Tinkerforge development purposes installed the Brick Viewer and the required Brick Daemon on a Linux PC (called the piDevBook as running [Raspberry Pi Desktop](https://www.raspberrypi.org/downloads/raspberry-pi-desktop/).
Steps to update the Master Brick and Bricklets:
1. Connect the Master Brick to the piDevBook using USB mini cable
2. Start Brick  Viewer (ensure latest version, used v2.4.4)
3. Connect localhost:4223
4. Check if Master brickand Bricklets found
5. Select Update and check version differences
6. Update Master Brick
a. Button Erase - press and hold (DO NOT RELEASE)!
b. Button Reset - press and release
c. Button Erase - release!
The Master Brick Blue LED is turned off indicating boot mode.
7. The Brick Viewer shows only the Brick Tab
8. Refresh serial port= Serial Port: /dev/ttyACMo, Fiirmware: Master (2.4.10)
9. Flash
10. Master Brick reboots > Blue LED turns on and the Brick Viewer shows tabs Brick and Bricklets

## APPENDIX Tinkerforge - Python API bindings
The Tinkerforge Python API bindings are required, installed using pip3.
Pip3 installs the bindings in a common dist-packages folder, which is on the Raspberry Pi Domoticz Server, folder:
/usr/lib/python3/dist-packages

Running pip3:
sudo pip3 install tinkerforge
Log Output:
Collecting tinkerforge
Installing collected packages: tinkerforge
Successfully installed tinkerforge-2.1.22

The Tinkerforge Python API bindings are installed in folder:
/usr/local/lib/python3.5/dist-packages

Check the content results in two folders, from which the folder tinkerforge is required
ls /usr/local/lib/python3.5/dist-packages
tinkerforge tinkerforge-2.1.22.dist-info

**IMPORTANT**
Depending setup of the Python distributed packages, following steps are required.
Check the folder /usr/local/lib/python3.5/dist-packages if there are more distributed packages.
If thats the case, then leave the next steps out.

Copy the content of the folder /usr/local/lib/python3.5/dist-packages/tinkerforge to folder /usr/lib/python3/dist-packages/tinkerforge,
because all the Python distributed packages are located in folder /usr/lib/python3/dist-packages/:
sudo cp -r /usr/local/lib/python3.5/dist-packages/tinkerforge /usr/lib/python3/dist-packages

Check the content of the dist-packages folder tinkerforge:
ls /usr/lib/python3/dist-packages/tinkerforge
brick_dc.py bricklet_led_strip.py brick_hat.py bricklet_led_strip_v2.py ...

Remove the dist-packages folders:
sudo rm -r /usr/local/lib/python3.5/dist-packages/tinkerforge
sudo rm -r /usr/local/lib/python3.5/dist-packages/tinkerforge-2.1.22.dist-info
ls /usr/local/lib/python3.5/dist-packages

## APPENDIX Domoticz - Python Plugin Code
	"""
	<plugin key="TrafficLight" name="Traffic Light" author="rwbL" version="1.0.0">
		<description>
			<h2>Traffic Light</h2><br/>
			Set the color of a Tinkerforge RGB LED Bricklet to RED,YELLOW or GREEN via Domoticz Selector Switch device.
			<h3>Features</h3>
			<ul style="list-style-type:square">
				<li>Traffic Light Color (R-G-B): RED=255-0-0; YELLOW=255-255-0; GREEN=0-255-0</li>
				<li>Traffic Light Brightness</li>
			</ul>
			<h3>Traffic Light Devices</h3>
			<ul style="list-style-type:square">
				<li>Set Traffic Light Color via Selector Switch with options RED, YELLOW or GREEN</li>
				<li>Display Traffic Light Alert Indicator</li>
				<li>Display Traffic Light Change Info</li>
			</ul>
			<h3>Configuration</h3>
			Requires the HTTP address and Port of the Master Brick WiFi Extention and the UID of the Tinkerforge RGB LED Bricklet.
		</description>
		<params>
			<param field="Address" label="Host" width="200px" required="true" default="192.168.N.NNN"/>
			<param field="Port" label="Port" width="75px" required="true" default="4223"/>
			<param field="Mode1" label="UID" width="75px" required="true" default="zMF"/>
			<param field="Mode4" label="Brightness" width="75px" required="true" default="100"/>
			<param field="Mode6" label="Debug" width="75px">
				<options>
					<option label="True" value="Debug" default="true"/>
					<option label="False" value="Normal"/>
				</options>
			</param>
		</params>
	</plugin>
	""" 

	## Imports
	import Domoticz
	import urllib
	import urllib.request

	# Amend the import path to enable using the Tinkerforge libraries
	# Alternate (ensure to update in case newer Python API bindings):
	# create folder tinkerforge and copy the binding content, i.e.
	# /home/pi/domoticz/plugins/trafficlight/tinkerforge
	from os import path
	import sys
	sys.path
	sys.path.append('/usr/local/lib/python3.5/dist-packages')
					
	import tinkerforge
	from tinkerforge.ip_connection import IPConnection
	from tinkerforge.bricklet_rgb_led import BrickletRGBLED

	# Set RGB LED brightness level 0(dark) - 255(brightest)
	RGBBRIGHTNESSMIN = 0
	RGBBRIGHTNESSMAX = 255

	class BasePlugin:
		
		def __init__(self):
			return

		def onStart(self):
			Domoticz.Debug("onStart called")
			Domoticz.Debug("Debug Mode:" + Parameters["Mode6"])
			
			if Parameters["Mode6"] == "Debug":
				self.debug = True
				Domoticz.Debugging(1)
				DumpConfigToLog()

			if (len(Devices) == 0):
				# Create new devices for the Traffic Light Hardware
				Domoticz.Debug("Creating new Devices")
				# Reference: https://www.domoticz.com/wiki/Developing_a_Python_plugin#Available_Device_Types
			 
				# Set the options for the selector switch with style Buttons set ("0")
				Options = {"LevelActions": "|||",
					  "LevelNames": "Off|RED|YELLOW|GREEN",
					  "LevelOffHidden": "true",
					  "SelectorStyle": "0"}
				Domoticz.Device(Name="State Selector", Unit=1, TypeName="Selector Switch",  Options=Options, Used=1).Create()            
				Domoticz.Debug("Device created: "+Devices[1].Name)
				Domoticz.Device(Name="Alert Indicator", Unit=2, TypeName="Alert", Used=1).Create()
				Domoticz.Debug("Device created: "+Devices[2].Name)
				Domoticz.Device(Name="Change Info", Unit=3, TypeName="Text", Used=1).Create()
				Domoticz.Debug("Device created: "+Devices[3].Name)
				
			#  Set heartbeat to 60    
			Domoticz.Heartbeat(60) 

		def onStop(self):
			Domoticz.Debug("Plugin is stopping.")

		def onConnect(self, Connection, Status, Description):
			Domoticz.Debug("onConnect called")
			
		def onMessage(self, Connection, Data):
			Domoticz.Debug("onMessage called")

		def onCommand(self, Unit, Command, Level, Hue):
			Domoticz.Debug("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))
			try:
				# Create IP connection
				ipcon = IPConnection()
				
				# Create device objects using the UID  as defined in the parameters
				lb = BrickletRGBLED(Parameters["Mode1"], ipcon)

				# Connect to brickd using Host and Port
				ipconnected = 0
				try:
					ipcon.connect(Parameters["Address"], int(Parameters["Port"]))
					ipconnected = 1
					Domoticz.Debug("IP Connection - OK")
				except:
					Domoticz.Debug("[ERROR] IP Connection failed")

				# Don't use device before ipcon is connected

				## Get the selector switch value (1) triggered by the onCommand parameter Level
				## Handle initial state being empty
				oldtrafficlightstate = 0
				if Devices[1].sValue != "":
					oldtrafficlightstate = int(Devices[1].sValue)
				Domoticz.Debug(Devices[1].Name + "-Traffic Light State Old=" + str(oldtrafficlightstate) )
				newtrafficlightstate = Level
				Domoticz.Debug(Devices[1].Name + "-Traffic Light State New=" + str(newtrafficlightstate) )
				Domoticz.Debug(Devices[1].Name + "-nValue=" + str(Devices[1].nValue) + ",sValue=" + Devices[1].sValue )

				# RGB LED
				## Get the current RGB LED Color
				rgbvalue = lb.get_rgb_value()
				Domoticz.Debug(Devices[1].Name + "-RGB LED Colors R-G-B:" + str(rgbvalue.r) + "-" +  str(rgbvalue.g) + "-" + str(rgbvalue.b) )

				## Set the brightness using the value of the parameter Mode4
				lbbrightness = int(Parameters["Mode4"])
				if lbbrightness < RGBBRIGHTNESSMIN:
					lbbrightness = RGBBRIGHTNESSMIN
				if lbbrightness > RGBBRIGHTNESSMAX:
					lbbrightness = RGBBRIGHTNESSMIN
				Domoticz.Debug("RGB LED Brightness updated:" + str(lbbrightness) )
					   
				## Set the Tinkerforge RGB LED Bricklet Color via API function
				## Update the Domoticz devices (check the Domoticz Web-UI Widget)
				trafficlightcolor = "UNKNOWN"
				trafficlightalert  = 0
				if newtrafficlightstate == 10:
					lb.set_rgb_value(lbbrightness, 0, 0)
					trafficlightcolor = "RED"
					trafficlightalert = 4

				if newtrafficlightstate == 20:
					lb.set_rgb_value(lbbrightness, lbbrightness, 0)
					trafficlightcolor = "YELLOW"
					trafficlightalert = 2
						
				if newtrafficlightstate == 30:
					lb.set_rgb_value(0, lbbrightness, 0)
					trafficlightcolor = "GREEN"
					trafficlightalert = 1

				# Selector switch device (1)
				Devices[1].Update( nValue=2, sValue=str(newtrafficlightstate) )
				Domoticz.Debug(Devices[1].Name + "-nValue=" + str(Devices[1].nValue) + ",sValue=" + Devices[1].sValue  )
				
				## Alert device (2)
				##   nvalue=LEVEL - (0=gray, 1=green, 2=yellow, 3=orange, 4=red)
				##   svalue=TEXT
				Devices[2].Update( nValue=trafficlightalert, sValue=trafficlightcolor )
				Domoticz.Debug(Devices[2].Name + "-nValue=" + str(Devices[2].nValue) + ",sValue=" + Devices[2].sValue  )
				
				## Text device (3)
				Devices[3].Update( nValue=0, sValue="Traffic Light changed from " + str(oldtrafficlightstate) + " to " + str(newtrafficlightstate) )
				Domoticz.Debug(Devices[3].Name + "-nValue=" + str(Devices[3].nValue) + ",sValue=" + Devices[3].sValue  )
					  
				# Disconnect
				ipcon.disconnect()

				# Log Message
				Domoticz.Log("TrafficLight Update: OK")
					
			except:
				# Error
				# Important to close the connection - if not, the plugin can notbe disabled
				if ipconnected == 1:
					ipcon.disconnect()
					# Devices[1].Name
					Domoticz.Log("[ERROR] Check settings, correct and restart Domoticz")

		def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
			Domoticz.Debug("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

		def onDisconnect(self, Connection):
			Domoticz.Debug("onDisconnect called")

		def onHeartbeat(self):
			Domoticz.Log("onHeartbeat called")

					
	global _plugin
	_plugin = BasePlugin()

	def onStart():
		global _plugin
		_plugin.onStart()

	def onStop():
		global _plugin
		_plugin.onStop()

	def onConnect(Connection, Status, Description):
		global _plugin
		_plugin.onConnect(Connection, Status, Description)

	def onMessage(Connection, Data):
		global _plugin
		_plugin.onMessage(Connection, Data)

	def onCommand(Unit, Command, Level, Hue):
		global _plugin
		_plugin.onCommand(Unit, Command, Level, Hue)

	def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
		global _plugin
		_plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

	def onDisconnect(Connection):
		global _plugin
		_plugin.onDisconnect(Connection)

	def onHeartbeat():
		global _plugin
		_plugin.onHeartbeat()

	# Generic helper functions
	def DumpConfigToLog():
		for x in Parameters:
			if Parameters[x] != "":
				Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
		Domoticz.Debug("Device count: " + str(len(Devices)))
		for x in Devices:
			Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
			Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
			Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
			Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
			Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
			Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
		return

##  APPENDIX Samba Shared Drive
Steps to create and connect to a Samba shared drive on the Raspberry Pi Domoticz Server.
Login as user "Pi" on the Raspberry Pi Domoticz Server.
(Linux dodev 4.19.42-v7+ #1219 SMP Tue May 14 21:20:58 BST 2019 armv7l)

### Update & Upgrade
sudo apt-get update && sudo apt-get upgrade

## Install Samba
sudo apt-get install samba samba-common-bin

### Edit smb.conf
sudo nano /etc/samba/smb.conf
Add:
[DoDevDomoticz]
Comment = Raspberry Pi Domoticz Development Folder
Path = /home/pi/domoticz
Browseable = yes
Writeable = Yes
only guest = no
create mask = 0777
directory mask = 0777
Public = yes
Guest ok = yes

### Make Domoticz Folder Executable
sudo chmod 777 /home/pi/domoticz

### Restart Samba
sudo /etc/init.d/samba restart
[ ok ] Restarting nmbd (via systemctl): nmbd.service.
[ ok ] Restarting smbd (via systemctl): smbd.service.

## Windows Shared Drive
Connect to \\ip-raspi-server\DoDevDomoticz
