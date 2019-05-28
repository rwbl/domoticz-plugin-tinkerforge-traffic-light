# Domoticz Home Automation - TrafficLight
# Set the color of a Tinkerforge RGB LED Bricklet to RED,YELLOW or GREEN via a Domoticz Selector Switch device.
# @author Robert W.B. Linn
# @version 1.1.0 (Build 20190528)
#
# NOTE:
# after every change run: sudo service domoticz.sh restart
# Check the Domoticz log: http://IP-ADDRESS:8080/#/Log 
#
# Domoticz Python Plugin Development Documentation:
# https://www.domoticz.com/wiki/Developing_a_Python_plugin
# https://www.tinkerforge.com/de/doc/Hardware/Bricklets/Air_Quality.html#air-quality-bricklet


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
            <li>Traffic Light State Selector - Set the traffic light color RED,YELLOW or GREEN Selector Switch</li>
            <li>Traffic Light Alert Indicator - Reflects the traffic light state</li>
            <li>Traffic Light Status - Shows lastest change or any error condition</li>
        </ul>
        <h3>Configuration</h3>
        Requires the Tinkerforge Master Brick WiFi Extention HTTP address and Port and the Tinkerforge RGB LED Bricklet UID.<br/>
        Use the Tinkerforge Brick Viewer to determine these parameter.
        <br/>
        <h4>Version</h4>
        20190528
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
        # Flag to check if connected to the master brick
        self.ipConnected = 0
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
            Domoticz.Device(Name="Status", Unit=3, TypeName="Text", Used=1).Create()
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
                Domoticz.Debug("IP Connection - OK")
            except:
                Domoticz.Debug("[ERROR] IP Connection failed")

            # Don't use device before ipcon is connected
            
            # Set Alert Indicator to Orange with ERROR text
            if self.ipConnected == 0:
                ## Alert device (2)
                ##   nvalue=LEVEL - (0=gray, 1=green, 2=yellow, 3=orange, 4=red)
                ##   svalue=TEXT
                Devices[2].Update( nValue=3, sValue="ERROR")
                Domoticz.Debug(Devices[2].Name + "-nValue=" + str(Devices[2].nValue) + ",sValue=" + Devices[2].sValue  )
                Devices[3].Update( nValue=0, sValue="[ERROR] Can not connect to Master Brick. Check settings, correct and restart Domoticz." )
                Domoticz.Log(Devices[3].sValue)
                return

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
            Domoticz.Log(Devices[3].sValue)
                
        except:
            # Error
            # Important to close the connection - if not, the plugin can not be disabled
            if self.ipConnected == 1:
                ipcon.disconnect()
            
            ## Set Alert Indicator to Level ORANGE with error flag and show text in text device
            Devices[2].Update( nValue=3, sValue="ERROR")
            Domoticz.Debug(Devices[2].Name + "-nValue=" + str(Devices[2].nValue) + ",sValue=" + Devices[2].sValue )
            
            Devices[3].Update( nValue=0, sValue="[ERROR] Check settings, correct and restart Domoticz." )
            Domoticz.Log(Devices[3].sValue)

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


