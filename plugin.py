# Domoticz Home Automation - Tinkerforge Traffic Light
# Set the color of a Tinkerforge RGB LED Bricklet 2.0 to RED, YELLOW or GREEN via a Domoticz Selector Switch device.
# @author Robert W.B. Linn
# @version 1.2.0 (Build 20200216)
#
# NOTE:
# After every change restart Domoticz & check the Domoticz Log
# sudo systemctl restart domoticz.service OR sudo service domoticz.sh restart
# REFERENCES:
# Domoticz Python Plugin Development Documentation:
# https://www.domoticz.com/wiki/Developing_a_Python_plugin
# Tinkerforge RGB LED Bricklet 2.0 Documentation:
# Hardware:
# https://www.tinkerforge.com/en/doc/Hardware/Bricklets/RGB_LED_V2.html#rgb-led-v2-bricklet
# API Python Documentation:
# https://www.tinkerforge.com/en/doc/Software/Bricklets/RGBLEDV2_Bricklet_Python.html#rgb-led-v2-bricklet-python-api


"""
<plugin key="tftrafficlight" name="Tinkerforge Traffic Light" author="rwbL" version="1.2.0">
    <description>
        <h2>Tinkerforge Traffic Light</h2><br/>
        Set the color of a Tinkerforge RGB LED Bricklet 2.0 to RED, YELLOW or GREEN via Domoticz Selector Switch device.<br/>
        <br/>
        <h3>Features</h3>
        <ul style="list-style-type:square">
            <li>Traffic Light Color (R-G-B): RED=255-0-0; YELLOW=255-255-0; GREEN=0-255-0</li>
            <li>Traffic Light Brightness</li>
        </ul>
        <h3>Devices (Type;SubType;switchType)</h3>
        <ul style="list-style-type:square">
            <li>State Selector - Set the traffic light color RED, YELLOW or GREEN Selector Switch (Light/Switch;Selector Switch;Selector)</li>
            <li>Alert Indicator - Reflects the traffic light state (General;Alert)</li>
            <li>Status - Show the latest change or any error condition (General;Text)</li>
        </ul>
        <h3>Configuration</h3>
        <ul style="list-style-type:square">
            <li>Address: IP address of the host connected to. Default: 127.0.0.1 (localhost for USB connection else use Master Brick WiFi extension)</li>
            <li>Port: Port used by the host. Default: 4223</li>
            <li>UID: Unique identifier of RGB LED Bricklet 2.0. Obtain the UID via the Brick Viewer. Default: Jng</li>
        </ul>
        <br/>
    </description>
    <params>
        <param field="Address" label="Host" width="200px" required="true" default="127.0.0.1"/>
        <param field="Port" label="Port" width="75px" required="true" default="4223"/>
        <param field="Mode1" label="UID" width="75px" required="true" default="Jng"/>
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
# /home/pi/domoticz/plugins/tftrafficlight
from os import path
import sys
sys.path
sys.path.append('/usr/local/lib/python3.7/dist-packages')
                
import tinkerforge
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_rgb_led import BrickletRGBLED

# Units
## The first UNIT MUST start with 1
UNITSELECTOR = 1
UNITALERT = 2
UNITSTATUS = 3

# Set RGB LED brightness level 0(dark) - 255(brightest)
RGBBRIGHTNESSMIN = 0
RGBBRIGHTNESSMAX = 255

class BasePlugin:
    
    def __init__(self):
        # Flag to check if connected to the master brick
        self.ipConnected = 0
        return

    def onStart(self):
        Domoticz.Debug("onStart called")
        Domoticz.Debug("Debug Mode:" + Parameters["Mode6"])
        
        if Parameters["Mode6"] == "Debug":
            self.debug = True
            Domoticz.Debugging(1)
            dump_config_to_log()

        if (len(Devices) == 0):
            # Create new Domoticz devices for the Traffic Light Hardware and set the devices to used
            Domoticz.Debug("Creating new Devices")
            # Reference: https://www.domoticz.com/wiki/Developing_a_Python_plugin#Available_Device_Types
         
            # Set the options for the selector switch with style Buttons set ("0")
            Options = {"LevelActions": "|||",
                  "LevelNames": "Off|RED|YELLOW|GREEN",
                  "LevelOffHidden": "true",
                  "SelectorStyle": "0"}
            Domoticz.Device(Name="State Selector", Unit=UNITSELECTOR, TypeName="Selector Switch",  Options=Options, Used=1).Create()            
            Domoticz.Debug("Device created: "+Devices[UNITSELECTOR].Name)
            Domoticz.Device(Name="Alert Indicator", Unit=UNITALERT, TypeName="Alert", Used=1).Create()
            Domoticz.Debug("Device created: "+Devices[UNITALERT].Name)
            Domoticz.Device(Name="Status", Unit=UNITSTATUS, TypeName="Text", Used=1).Create()
            Domoticz.Debug("Device created: "+Devices[UNITSTATUS].Name)
            
        #  Set heartbeat to 10    
        Domoticz.Heartbeat(10) 

    def onStop(self):
        Domoticz.Debug("Plugin is stopping.")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Debug("onConnect called")
        
    def onMessage(self, Connection, Data):
        Domoticz.Debug("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Debug("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))
        # Flag to check if connected to the master brick
        self.ipConnected = 0
        try:
            # Create IP connection
            ipcon = IPConnection()
            
            # Create device objects using the UID as defined in the parameter Mode1
            # The string can contain multiple UIDs separated by comma (,). This enables to define more bricklets.
            brickletUIDParam = Parameters["Mode1"]
            # Split the parameter string into a list of UIDs
            brickletUIDList = brickletUIDParam.split(',')
            # Check the list length and create the device objects
            if len(brickletUIDList) == 1:
                # First bricklet
                lb = BrickletRGBLED(brickletUIDList[0], ipcon)

            # Connect to brickd using Host and Port
            try:
                ipcon.connect(Parameters["Address"], int(Parameters["Port"]))
                self.ipConnected = 1
                Domoticz.Debug("IP Connection: OK")
            except:
                Domoticz.Error("IP Connection: failed.")

            # Don't use device before ipcon is connected
            
            # Set Alert Indicator to Orange with ERROR text
            if self.ipConnected == 0:
                ## Alert device (2)
                ##   nvalue=LEVEL - (0=gray, 1=green, 2=yellow, 3=orange, 4=red)
                ##   svalue=TEXT
                Devices[UNITALERT].Update( nValue=3, sValue="ERROR")
                Domoticz.Debug(Devices[UNITALERT].Name + "-nValue=" + str(Devices[UNITALERT].nValue) + ",sValue=" + Devices[UNITALERT].sValue  )
                Devices[UNITSTATUS].Update( nValue=0, sValue="[ERROR] Can not connect to Master Brick. Check settings, correct and restart Domoticz." )
                Domoticz.Error(Devices[UNITSTATUS].sValue)
                return

            ## Get the selector switch value (1) triggered by the onCommand parameter Level
            ## Handle initial state being empty
            oldtrafficlightstate = 0
            if Devices[UNITSELECTOR].sValue != "":
                oldtrafficlightstate = int(Devices[UNITSELECTOR].sValue)
            Domoticz.Debug(Devices[UNITSELECTOR].Name + "-Traffic Light State Old=" + str(oldtrafficlightstate) )
            newtrafficlightstate = Level
            Domoticz.Debug(Devices[UNITSELECTOR].Name + "-Traffic Light State New=" + str(newtrafficlightstate) )
            Domoticz.Debug(Devices[UNITSELECTOR].Name + "-nValue=" + str(Devices[UNITSELECTOR].nValue) + ",sValue=" + Devices[UNITSELECTOR].sValue )

            # RGB LED
            ## Get the current RGB LED Color
            rgbvalue = lb.get_rgb_value()
            Domoticz.Debug(Devices[UNITSELECTOR].Name + "-RGB LED Colors R-G-B:" + str(rgbvalue.r) + "-" +  str(rgbvalue.g) + "-" + str(rgbvalue.b) )

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

            # Selector switch device (UNIT=1)
            Devices[UNITSELECTOR].Update( nValue=2, sValue=str(newtrafficlightstate) )
            Domoticz.Debug(Devices[UNITSELECTOR].Name + "-nValue=" + str(Devices[UNITSELECTOR].nValue) + ",sValue=" + Devices[UNITSELECTOR].sValue )
            
            ## Alert device (UNIT=2)
            ##   nvalue=LEVEL - (0=gray, 1=green, 2=yellow, 3=orange, 4=red)
            ##   svalue=TEXT
            Devices[UNITALERT].Update( nValue=trafficlightalert, sValue=trafficlightcolor )
            Domoticz.Debug(Devices[UNITALERT].Name + "-nValue=" + str(Devices[UNITALERT].nValue) + ",sValue=" + Devices[UNITALERT].sValue  )
            
            ## Text device (UNIT=3)
            Devices[UNITSTATUS].Update( nValue=0, sValue="Traffic Light changed from " + str(oldtrafficlightstate) + " to " + str(newtrafficlightstate) )
            Domoticz.Debug(Devices[UNITSTATUS].Name + "-nValue=" + str(Devices[UNITSTATUS].nValue) + ",sValue=" + Devices[UNITSTATUS].sValue  )
                  
            # Disconnect
            ipcon.disconnect()

            # Log Message
            Domoticz.Log(Devices[UNITSTATUS].sValue)
                
        except:
            # Error
            # Important to close the connection - if not, the plugin can not be disabled
            if self.ipConnected == 1:
                ipcon.disconnect()
            
            ## Set Alert Indicator to Level ORANGE with error flag and show text in text device
            Devices[UNITALERT].Update( nValue=3, sValue="ERROR")
            Domoticz.Debug(Devices[UNITALERT].Name + "-nValue=" + str(Devices[UNITALERT].nValue) + ",sValue=" + Devices[UNITALERT].sValue )
            
            Devices[UNITSTATUS].Update( nValue=0, sValue="[ERROR] Check settings, correct and restart Domoticz." )
            Domoticz.Error(Devices[UNITSTATUS].sValue)

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Debug("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Debug("onDisconnect called")

    def onHeartbeat(self):
        # On heart beat not used as the devices are updated via onCommand trigger from the Selector Switch
        Domoticz.Debug("onHeartbeat called")

                
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
def dump_config_to_log():
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
