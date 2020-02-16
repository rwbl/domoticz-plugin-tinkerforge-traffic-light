# domoticz-plugin-tinkerforge-trafficLight
Domoticz plugin to explore how to interact with Tinkerforge Building Blocks.

# Objectives
* To set the color of a Tinkerforge RGB Bricklet to red, yellow or green using a Domoticz Selector Switch Device.
* To learn how to write generic Python [plugin(s)](https://www.domoticz.com/wiki/Developing_a_Python_plugin) for the Domoticz Home Automation System.
* To learn how to interact with [Tinkerforge](http://www.tinkerforge.com) Building Blocks.
* To use this sample plugin as a template for other Domoticz plugins interacting with Tinkerforge Building Blocks.

_Abbreviations_: GUI=Domoticz Web UI.

## Solution
A Domoticz Python plugin "Tinkerforge Traffic Light" with a Tinkerforge RGB LED Bricklet.
The Tinkerforge RGB LED Bricklet is connected to a Tinkerforge Master Brick.
The Master Brick has been tested with direct USB connection to the Raspberry Pi and with the Master Brick WiFi extension.

The traffic light color is set using a Domoticz device Selector Switch with 3 buttons RED, YELLOW and GREEN.
Selecting a color, will 
* set the RGB LED bricklet color
* update the Alert device to the level associated with the color (1=green, 2=yellow, 4=red)
* set the text of the Text device (used to indicate changes), i.e. "Traffic Light changed from 10 to 30" which means color has changed from RED to GREEN - see below devices information)

If a color is changed, the plugin makes an IP connection, updates the Tinkerforge RGB LED bricklet and Domoticz devices, disconnects from IP.
There is no ongoing IP connection after the bricklet starts (either during Domoticz start or if the plugin gets updated or added first time).
For other Domoticz Plugins using Tinkerforge building block an ongoing connection is established where bricklet callbacks are used, i.e. IO-4 or LCD 20x4 bricklet etc..

### Domoticz Devices
The Domoticz devices (Type;SubType;switchType) created are:
* State Selector - Set the traffic light color RED, YELLOW or GREEN Selector Switch (Light/Switch;Selector Switch;Selector) with settings Hide Off Level; Selector Level 10 = RED, 20 = YELLOW, 30 = GREEN.
* Alert Indicator - Reflects the traffic light state (General;Alert)
* Status - Show the latest change or any error condition (General;Text)

After adding the hardware and changing the color, the Domoticz devices lists the 3 devices (Idx,Hardware,Unit,Name,Type,SubType,Data):
99,TrafficLight,000E0003,3,TrafficLight - Status,General,Text,Traffic Light changed from 10 to 30
98,TrafficLight,000E0002,2,TrafficLight - Alert Indicator,General,Alert,GREEN
97,TrafficLight,000E0001,1,TrafficLight - State Selector,Light/Switch,Selector Switch,Set Level: 30 %

### Plugin Configuration
* Address: IP address of the host connected to. Default: 127.0.0.1 (localhost for USB connection else use Master Brick WiFi extension)
* Port: Port used by the host. Default: 4223
* UID: Unique identifier of RGB LED Bricklet 2.0. Obtain the UID via the Brick Viewer. Default: Jng

## Hardware Parts
* Raspberry Pi 3B+
* Tinkerforge Master Brick 2.1 FW 2.4.10 [(Info)](https://www.tinkerforge.com/en/doc/Hardware/Bricks/Master_Brick.html#master-brick)
* Tinkerforge WIFI Master Extension 2.0 [(Info)](https://www.tinkerforge.com/en/doc/Hardware/Master_Extensions/WIFI_V2_Extension.html)
* Tinkerforge RGB LED Bricklet 2.0 FW 2.0.1 [(Info)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/RGB_LED_V2.html#)

## Software
* Raspberry Pi Raspian Debian Linux Buster 4.19.93-v7+ #1290
* Domoticz Home Automation System 4.11696 (BETA)
* Tinkerforge Python API-Binding 2.1.24 [(Info)](https://www.tinkerforge.com/en/doc/Software/Bricklets/RGBLEDV2_Bricklet_Python.html#rgb-led-v2-bricklet-python-api)
* Python 3.7.3, GCC 8.2.0
* The versions for developing this plugin are subject to change.

## Setup Tinkerforge and Domoticz

## Tinkerforge Python API bindings
```
sudo pip3 install tinkerforge
```
Check if the Tinkerforge Python API bindings are installed in folder: /usr/local/lib/python3.5/dist-packages
**Note**
Check the version of "python3" in the folder path. This could also be python 3.7 or other.

## Tinkerforge Master Brick and Bricklets
Ensure the Master Brick and Bricklets are running with the latest firmware.
See **APPENDIX Tinkerforge - Master Brick and Bricklets**.

## Traffic Light Prototype
Build the prototype by connecting the Tinkerforge building blocks (see hardware).
Connect the Master Brick to a device running the Brick Deamon and Viewer.
Summary steps to setup the Tinkerforge building blocks using the Tinkerforge Brick Viewer.
* Update the devices firmware
* Set the WiFi master extension fixed IP address in client mode
* Obtain the UID's of the Tinkerforge bricklets as required by the Python plugin

After setting up the Tinkerforge building blocks, reset the master brick and check if the master brick can be reached via WLAN:
```
ping tf-wifi-ext-ip-address
```

For USB connection, use IP address: 127.0.0.1

## Domoticz Plugin Folder and File
```
mkdir /home/pi/domoticz/plugins/tftrafficlight
```
As a starter, take the template from [here](https://github.com/domoticz/domoticz/blob/master/plugins/examples/BaseTemplate.py).
Save as **plugin.py** in the folder /home/pi/domoticz/plugins/tftrafficlight

## Python Plugin Path to Tinkerforge API Bindings
In the Python Plugin code (**plugin.py**) amend the import path to enable using the Tinkerforge API Bindings:
```
from os import path
import sys
sys.path
sys.path.append('/usr/local/lib/python3.7/dist-packages')
```

## Development Setup
Development PC:
* Thonny to develop the Python Plugin
* A shared drive Z: is defined pointing to /home/pi/domoticz
* GUI > Setup > Log
* GUI > Setup > Hardware
* GUI > Setup > Devices
* WinSCP session connected to the Domoticz server
* Putty session connected to the Domoticz server

The GUI's are required to add the new hardware with its device and monitor if the plugin code is running without errors.

## Development Iteration
The development process step used are:
1. Thonny develop z:\plugins\trafficlight\plugin.py
2. Make changes and save plugin.py
3. Restart Domoticz from Terminal: sudo service domoticz.sh restart
4. Wait a moment and refresh GUI > Log
5. Check the log and fix as required

**!IMPORTANT!**
In the GUI Setup > Settings, enable accepting new hardware.
This is required to add the new hardware with its device and monitor if the plugin code is running without errors.

## Domoticz Web UI's
Open GUI Setup > Hardware, GUI Setup > Log, GUI Setup > Devices
This is required to add the new hardware with its device and monitor if the plugin code is running without errors.

## Create the plugin
The plugin has a mandatory filename **plugin.py** located in the created plugin folder **/home/pi/domoticz/plugins/tftrafficlight**
For Python development Thonny, running on a Windows 10 device, is used.

See APPENDIX Domoticz Python Plugin Code (well documented).

Domoticz Devices created and set as used.
```
Domoticz.Device(Name="State Selector", Unit=1, TypeName="Selector Switch",  Options=Options, Used=1).Create()            
Domoticz.Device(Name="Alert Indicator", Unit=2, TypeName="Alert", Used=1).Create()
Domoticz.Device(Name="Status", Unit=3, TypeName="Text", Used=1).Create()
```

The devices are manually added to the Domoticz Dashboard.

Handling the state change of the Traffic Light Selector Switch is done by the **onCommand** function.
This function updates the state of the Domoticz Devices: State Selector (idx=13), Alert Indicator (idx=14), Status (idx=15).

**Pseudo Code**
* FIRST TIME: _onStart_ to create the Domoticz Devices
* NEXT TIME(S): _onCommand_ to handle state changes
	* Domoticz make IP connection to the Tinkerforge Master Brick
	* Get the Level of the Domoticz Device "State Selector" (Selector Switch)
	* Update the Tinkerforge Bricklet RGB LED with the new color depending Level
	* Update the Domoticz Devices "Alert Indicator" and "Status"
	* Domoticz to disconnect from the Tinkerforge Master Brick

**Note**
Function _onHeartbeat_ is not used as not polling for the state of a Tinkerforge Bricklet and update Domoticz Device(s) accordingly.

## Restart Domoticz
Restart Domoticz to find the plugin:
```
sudo systemctl restart domoticz.service
```
**Note**
When making changes to the Python plugin code, ensure to restart Domoticz and refresh any of the Domoticz Web UI's.

## Domoticz Add Hardware Traffic Light
**IMPORTANT**
Prior adding, set GUI Setup > Settings > Hardware, the option to allow new hardware.
If this option is not enabled, no new soilmoisture device is created.
Check the Domoticz Log as error message Python script at the line where the new device is used
(i.e. Domoticz.Debug("Device created: "+Devices[1].Name))

## Add Hardware - Check the Domoticz Log
After adding,ensure to check the Domoticz Log.
Example:
```
2020-02-16 09:58:24.964 Status: (TrafficLight) Started. 
2020-02-16 09:58:25.407 (TrafficLight) Debug logging mask set to: PYTHON PLUGIN QUEUE IMAGE DEVICE CONNECTION MESSAGE ALL 
2020-02-16 09:58:25.407 (TrafficLight) 'HardwareID':'14' 
2020-02-16 09:58:25.407 (TrafficLight) 'HomeFolder':'/home/pi/domoticz/plugins/tftrafficlight/' 
2020-02-16 09:58:25.407 (TrafficLight) 'StartupFolder':'/home/pi/domoticz/' 
2020-02-16 09:58:25.407 (TrafficLight) 'UserDataFolder':'/home/pi/domoticz/' 
2020-02-16 09:58:25.407 (TrafficLight) 'Database':'/home/pi/domoticz/domoticz.db' 
2020-02-16 09:58:25.407 (TrafficLight) 'Language':'en' 
2020-02-16 09:58:25.407 (TrafficLight) 'Version':'1.2.0' 
2020-02-16 09:58:25.407 (TrafficLight) 'Author':'rwbL' 
2020-02-16 09:58:25.407 (TrafficLight) 'Name':'TrafficLight' 
2020-02-16 09:58:25.407 (TrafficLight) 'Address':'127.0.0.1' 
2020-02-16 09:58:25.407 (TrafficLight) 'Port':'4223' 
2020-02-16 09:58:25.407 (TrafficLight) 'Key':'tftrafficlight' 
2020-02-16 09:58:25.407 (TrafficLight) 'Mode1':'Jng' 
2020-02-16 09:58:25.407 (TrafficLight) 'Mode4':'100' 
2020-02-16 09:58:25.407 (TrafficLight) 'Mode6':'Debug' 
2020-02-16 09:58:25.407 (TrafficLight) 'DomoticzVersion':'4.11696' 
2020-02-16 09:58:25.407 (TrafficLight) 'DomoticzHash':'5a4048f3e' 
2020-02-16 09:58:25.407 (TrafficLight) 'DomoticzBuildTime':'2020-02-16 09:26:35' 
2020-02-16 09:58:25.407 (TrafficLight) Device count: 0 
2020-02-16 09:58:25.407 (TrafficLight) Creating new Devices 
2020-02-16 09:58:25.407 (TrafficLight) Creating device 'State Selector'. 
2020-02-16 09:58:25.411 (TrafficLight) Device created: TrafficLight - State Selector 
2020-02-16 09:58:25.411 (TrafficLight) Creating device 'Alert Indicator'. 
2020-02-16 09:58:25.413 (TrafficLight) Device created: TrafficLight - Alert Indicator 
2020-02-16 09:58:25.413 (TrafficLight) Creating device 'Status'. 
2020-02-16 09:58:25.415 (TrafficLight) Device created: TrafficLight - Status 
2020-02-16 09:58:25.415 (TrafficLight) Pushing 'PollIntervalDirective' on to queue 
2020-02-16 09:58:25.416 (TrafficLight) Processing 'PollIntervalDirective' message 
2020-02-16 09:58:25.416 (TrafficLight) Heartbeat interval set to: 10. 
2020-02-16 09:58:25.404 Status: (TrafficLight) Entering work loop. 
2020-02-16 09:58:25.404 Status: (TrafficLight) Initialized version 1.2.0, author 'rwbL' 
```
## Domoticz Log Entry State Change Off to RED
Handling the state changes are managed by the function onCommand.
```
020-02-16 10:01:24.538 (TrafficLight) Processing 'onCommandCallback' message 
2020-02-16 10:01:24.538 (TrafficLight) Calling message handler 'onCommand'. 
2020-02-16 10:01:24.538 (TrafficLight) onCommand called for Unit 1: Parameter 'Set Level', Level: 10 
2020-02-16 10:01:24.547 (TrafficLight) IP Connection: OK 
2020-02-16 10:01:24.547 (TrafficLight) TrafficLight - State Selector-Traffic Light State Old=0 
2020-02-16 10:01:24.547 (TrafficLight) TrafficLight - State Selector-Traffic Light State New=10 
2020-02-16 10:01:24.547 (TrafficLight) TrafficLight - State Selector-nValue=0,sValue= 
2020-02-16 10:01:24.550 (TrafficLight) TrafficLight - State Selector-RGB LED Colors R-G-B:0-255-0 
2020-02-16 10:01:24.550 (TrafficLight) RGB LED Brightness updated:100 
2020-02-16 10:01:24.551 (TrafficLight - State Selector) Updating device from 0:'' to have values 2:'10'. 
2020-02-16 10:01:24.580 (TrafficLight) TrafficLight - State Selector-nValue=2,sValue=10 
2020-02-16 10:01:24.580 (TrafficLight - Alert Indicator) Updating device from 0:'No Alert!' to have values 4:'RED'. 
2020-02-16 10:01:24.603 (TrafficLight) TrafficLight - Alert Indicator-nValue=4,sValue=RED 
2020-02-16 10:01:24.604 (TrafficLight - Status) Updating device from 0:'' to have values 0:'Traffic Light changed from 0 to 10'. 
2020-02-16 10:01:24.619 (TrafficLight) TrafficLight - Status-nValue=0,sValue=Traffic Light changed from 0 to 10 
2020-02-16 10:01:24.720 (TrafficLight) Traffic Light changed from 0 to 10 
2020-02-16 10:01:24.512 Status: User: Admin initiated a switch command (97/TrafficLight - State Selector/Set Level) 
```

## APPENDIX HTTP API Tests
Via HTTP API requests, the solution can be tested as well.

#### Set Color to GREEN = level 30
The URL submitted using browser with HTTP response and Domoticz log.
```
http://domoticz-ip-address:8080/json.htm?type=command&param=switchlight&idx=97&switchcmd=Set%20Level&level=30
```

HTTP Response (JSON format):
```
{"status" : "OK","title" : "SwitchLight"}
```

Domoticz Log:
```
2020-02-16 10:44:22.485 (TrafficLight) Pushing 'onCommandCallback' on to queue 
2020-02-16 10:44:22.493 (TrafficLight) Processing 'onCommandCallback' message 
2020-02-16 10:44:22.493 (TrafficLight) Calling message handler 'onCommand'. 
2020-02-16 10:44:22.493 (TrafficLight) onCommand called for Unit 1: Parameter 'Set Level', Level: 30 
2020-02-16 10:44:22.505 (TrafficLight) IP Connection: OK 
2020-02-16 10:44:22.505 (TrafficLight) TrafficLight - State Selector-Traffic Light State Old=20 
2020-02-16 10:44:22.505 (TrafficLight) TrafficLight - State Selector-Traffic Light State New=30 
2020-02-16 10:44:22.505 (TrafficLight) TrafficLight - State Selector-nValue=2,sValue=20 
2020-02-16 10:44:22.509 (TrafficLight) TrafficLight - State Selector-RGB LED Colors R-G-B:100-100-0 
2020-02-16 10:44:22.509 (TrafficLight) RGB LED Brightness updated:100 
2020-02-16 10:44:22.510 (TrafficLight - State Selector) Updating device from 2:'20' to have values 2:'30'. 
2020-02-16 10:44:22.544 (TrafficLight) TrafficLight - State Selector-nValue=2,sValue=30 
2020-02-16 10:44:22.544 (TrafficLight - Alert Indicator) Updating device from 2:'YELLOW' to have values 1:'GREEN'. 
2020-02-16 10:44:22.564 (TrafficLight) TrafficLight - Alert Indicator-nValue=1,sValue=GREEN 
2020-02-16 10:44:22.565 (TrafficLight - Status) Updating device from 0:'Traffic Light changed from 30 to 20' to have values 0:'Traffic Light changed from 20 to 30'. 
2020-02-16 10:44:22.584 (TrafficLight) TrafficLight - Status-nValue=0,sValue=Traffic Light changed from 20 to 30 
2020-02-16 10:44:22.687 (TrafficLight) Traffic Light changed from 20 to 30 
2020-02-16 10:44:22.484 Status: User: Admin initiated a switch command (97/TrafficLight - State Selector/Set Level) 
```

## APPENDIX dzVents Lua Automation Script Example - Raspberry Pi CPU Temperature Monitor

### Lua Script
```
-- dzVents Automation Script: tftrafficlight_rpi_monitor
-- Use a RGBLED to indicate the CPU temperature depending level and set to R or Y or G.
-- 20200216 by rwbL

-- Idx devices.
IDXRPICPUTEMP = 2
IDXSTATESELECTOR  = 97

-- Define the state selector switch levels according the switch selector settings
LEVELRED = 10
LEVELYELLOW = 20
LEVELGREEN = 30

-- Define the cpu temp thresholds in C
THRED = 43
THGREEN = 42

return {
	on = {
		timer = {
			'every minute',
	   },
    },
	execute = function(domoticz, timer)
		domoticz.log('Timer event triggered by ' .. timer.trigger, domoticz.LOG_INFO)
    	-- Get the cputemp and log
    	local cputemp = tonumber(domoticz.devices(IDXRPICPUTEMP).sValue)
		domoticz.log(string.format('CPU Temperature: %.f', cputemp), domoticz.LOG_INFO)

        -- Device CPU Temperature set RGBLED color
        local newlevel = 0
        if (cputemp >= THRED) then newlevel = LEVELRED end
        if (cputemp >= THGREEN and cputemp < THRED) then newlevel = LEVELYELLOW end
        if (cputemp < THGREEN) then newlevel = LEVELGREEN end

        local oldlevel = domoticz.devices(IDXSTATESELECTOR).level
		domoticz.log(string.format('Level Old / New: %d/%d', oldlevel,newlevel), domoticz.LOG_INFO)
        if (newlevel ~= oldlevel) then domoticz.devices(IDXSTATESELECTOR).setLevel(newlevel) end
        -- Clear the device log
        domoticz.openURL('http://localhost:8080/json.htm?type=command&param=clearlightlog&idx=' .. IDXSTATESELECTOR)

    end
}
```

### Domoticz Log
```
*** Debug and State Change
2020-02-16 11:12:57.044 (TrafficLight) onHeartbeat called 
2020-02-16 11:13:00.311 (TrafficLight) Pushing 'onCommandCallback' on to queue 
2020-02-16 11:13:00.350 (TrafficLight) Processing 'onCommandCallback' message 
2020-02-16 11:13:00.350 (TrafficLight) Calling message handler 'onCommand'. 
2020-02-16 11:13:00.350 (TrafficLight) onCommand called for Unit 1: Parameter 'Set Level', Level: 20 
2020-02-16 11:13:00.353 (TrafficLight) IP Connection: OK 
2020-02-16 11:13:00.354 (TrafficLight) TrafficLight - State Selector-Traffic Light State Old=30 
2020-02-16 11:13:00.354 (TrafficLight) TrafficLight - State Selector-Traffic Light State New=20 
2020-02-16 11:13:00.354 (TrafficLight) TrafficLight - State Selector-nValue=2,sValue=30 
2020-02-16 11:13:00.356 (TrafficLight) TrafficLight - State Selector-RGB LED Colors R-G-B:0-100-0 
2020-02-16 11:13:00.356 (TrafficLight) RGB LED Brightness updated:100 
2020-02-16 11:13:00.356 (TrafficLight - State Selector) Updating device from 2:'30' to have values 2:'20'. 
2020-02-16 11:13:00.373 (TrafficLight) TrafficLight - State Selector-nValue=2,sValue=20 
2020-02-16 11:13:00.373 (TrafficLight - Alert Indicator) Updating device from 1:'GREEN' to have values 2:'YELLOW'. 
2020-02-16 11:13:00.388 (TrafficLight) TrafficLight - Alert Indicator-nValue=2,sValue=YELLOW 
2020-02-16 11:13:00.388 (TrafficLight - Status) Updating device from 0:'Traffic Light changed from 30 to 30' to have values 0:'Traffic Light changed from 30 to 20'. 
2020-02-16 11:13:00.403 (TrafficLight) TrafficLight - Status-nValue=0,sValue=Traffic Light changed from 30 to 20 
2020-02-16 11:13:00.291 Status: dzVents: Info: ------ Start internal script: tftrafficlight_rpi_monitor:, trigger: "every minute" 
2020-02-16 11:13:00.291 Status: dzVents: Info: Timer event triggered by every minute 
2020-02-16 11:13:00.307 Status: dzVents: Info: CPU Temperature: 43 
2020-02-16 11:13:00.309 Status: dzVents: Info: Level Old / New: 30/20 
2020-02-16 11:13:00.309 Status: dzVents: Info: ------ Finished tftrafficlight_rpi_monitor 
2020-02-16 11:13:00.310 Status: EventSystem: Script event triggered: /home/pi/domoticz/dzVents/runtime/dzVents.lua 
*** NO Debug and no change in color
2020-02-16 11:15:00.321 Status: dzVents: Info: ------ Start internal script: tftrafficlight_rpi_monitor:, trigger: "every minute" 
2020-02-16 11:15:00.321 Status: dzVents: Info: Timer event triggered by every minute 
2020-02-16 11:15:00.340 Status: dzVents: Info: CPU Temperature: 44 
2020-02-16 11:15:00.341 Status: dzVents: Info: Level Old / New: 10/10 
2020-02-16 11:15:00.341 Status: dzVents: Info: ------ Finished tftrafficlight_rpi_monitor 
2020-02-16 11:15:00.341 Status: EventSystem: Script event triggered: /home/pi/domoticz/dzVents/runtime/dzVents.lua
***NO Debug and color changed to YELLOW
2020-02-16 11:16:00.533 (TrafficLight) Traffic Light changed from 10 to 20 
2020-02-16 11:16:00.332 Status: dzVents: Info: ------ Start internal script: tftrafficlight_rpi_monitor:, trigger: "every minute" 
2020-02-16 11:16:00.332 Status: dzVents: Info: Timer event triggered by every minute 
2020-02-16 11:16:00.350 Status: dzVents: Info: CPU Temperature: 43 
2020-02-16 11:16:00.351 Status: dzVents: Info: Level Old / New: 10/20 
2020-02-16 11:16:00.352 Status: dzVents: Info: ------ Finished tftrafficlight_rpi_monitor 
2020-02-16 11:16:00.353 Status: EventSystem: Script event triggered: /home/pi/domoticz/dzVents/runtime/dzVents.lua
```

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
```
/usr/lib/python3/dist-packages
```

Running pip3:
```
sudo pip3 install tinkerforge
```
Log Output:
```
Collecting tinkerforge
Installing collected packages: tinkerforge
Successfully installed tinkerforge-2.1.22
```

The Tinkerforge Python API bindings are installed in folder:
```
/usr/local/lib/python3.5/dist-packages
```

Check the content results in two folders, from which the folder tinkerforge is required
```
ls /usr/local/lib/python3.5/dist-packages
tinkerforge tinkerforge-2.1.22.dist-info
```

**IMPORTANT**
Depending setup of the Python distributed packages, following steps are required.
Check the folder /usr/local/lib/python3.5/dist-packages if there are more distributed packages.
If thats the case, then leave the next steps out.

Copy the content of the folder /usr/local/lib/python3.5/dist-packages/tinkerforge to folder /usr/lib/python3/dist-packages/tinkerforge,
because all the Python distributed packages are located in folder /usr/lib/python3/dist-packages/:
```
sudo cp -r /usr/local/lib/python3.5/dist-packages/tinkerforge /usr/lib/python3/dist-packages
```

Check the content of the dist-packages folder tinkerforge:
```
ls /usr/lib/python3/dist-packages/tinkerforge
brick_dc.py bricklet_led_strip.py brick_hat.py bricklet_led_strip_v2.py ...
```

Remove the dist-packages folders:
```
sudo rm -r /usr/local/lib/python3.5/dist-packages/tinkerforge
sudo rm -r /usr/local/lib/python3.5/dist-packages/tinkerforge-2.1.22.dist-info
ls /usr/local/lib/python3.5/dist-packages
```

## APPENDIX Domoticz - Python Plugin Code
See file **plugin.py**.

## APPENDIX Domoticz - MQTT Message
Example of an MQTT message issued by the Traffic Light Selector Switch.
Analyzing MQTT messages helps to understand the properties and values of a device.
```
{
"Battery" : 255,
"LevelActions" : "|||",   "LevelNames" : "Off|RED|YELLOW|GREEN",   "LevelOffHidden" : "true",   
"RSSI" : 12,   "SelectorStyle" : "0",   "description" : "",   "dtype" : "Light/Switch",   "id" : "00050001",   
"idx" : 13,   "name" : "Traffic Light - State Selector", 
"nvalue" : 2,   "stype" : "Selector Switch",   "svalue1" : "30",   "switchType" : "Selector",  "unit" : 1
}
```

##  APPENDIX Samba Shared Drive
Steps to create and connect to a Samba shared drive on the Raspberry Pi Domoticz Server.
Login as user "Pi" on the Raspberry Pi Domoticz Server.
(Linux dodev 4.19.42-v7+ #1219 SMP Tue May 14 21:20:58 BST 2019 armv7l)

### Update & Upgrade
```
sudo apt-get update && sudo apt-get upgrade
```

### Install Samba
```
sudo apt-get install samba samba-common-bin
```

#### Edit smb.conf
```
sudo nano /etc/samba/smb.conf
```
Add:
```
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
```

#### Make Domoticz Folder Executable
```
sudo chmod 777 /home/pi/domoticz
```

#### Restart Samba
```
sudo /etc/init.d/samba restart
```
```
[ ok ] Restarting nmbd (via systemctl): nmbd.service.
[ ok ] Restarting smbd (via systemctl): smbd.service.
```

### Windows Shared Drive
Connect to \\ip-raspi-server\DoDevDomoticz

