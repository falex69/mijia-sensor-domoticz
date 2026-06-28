"""
<plugin key="Domoticz-Xiaomi-Mijia-Plugin" name="Xiaomi Mijia Bluetooth Plugin" author="FALEX69" version="2.0.0" wikilink="https://https://github.com/falex69/mijia-sensor-domoticz/Readme.md" externallink="https://https://github.com/falex69/mijia-sensor-domoticz/">
    <description>
        <h2>Mijia Bluetooth Temp/Hygro Plugin 2.1.0</h2><br/>
        <h3>Features</h3>
        <ul style="list-style-type:square">
            <li>Xiamo Mijia Temp/Hygro supported</li>
        </ul>
        <h3>Configuration</h3>
        <ul style="list-style-type:square">
            <li>Device Bluetooth MAC-Addresses: Unique MAC address of the sensor, comma separated.</li>
        </ul>
        <br/><br/>
    </description>
    <params>
        <param field="Mode6" label="MAC Addr, comma separated" width="200px" required="false"/>
    </params>
</plugin>
"""
import Domoticz
import json
import base64
import datetime
import os
# import domoticz_mijia

class BasePlugin:
  
    devicesId = []
    macAddresses = []

    domoticzIp = ""
    domoticzPort = ""
    domoticzUser = ""
    domoticzPasswd = ""
    Heartbeat = 0

    DEVICE_MIJIA = "MIJIA"

    def __init__(self):
        #self.var = 123
        return

    def onStart(self):
        Domoticz.Log("onStart called "+Parameters["Key"]) # Unique short name for the plugin, matches python filename.
        self.macAddresses = [item.strip() for item in Parameters["Mode6"].split(',')]
        Domoticz.Log(f"MacAddress List : {self.macAddresses}")
        
        # Create devices
        if len(Devices) == 0:
            Domoticz.Log("Create device")
            # Domoticz.Device(Name="MIJIA", Unit=1, TypeName="Temp+Hum", Used=0).Create()
            Domoticz.Log("Device created")
        else:
            Domoticz.Log(f"Device alreadey created : {len(Devices)}")
        
        #Set Heartbeat from 10s to 30s)
        #Domoticz.Heartbeat(30)

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Log("onHeartbeat called")
        self.Heartbeat = self.Heartbeat + 1
        if self.Heartbeat == 3:
            self.Heartbeat = 0
            # values = domoticz_mijia.read(self.macAddress)
            # if ((values['temp'] == None) or (values['hum'] == None) or (values['bat'])):
            #     Domoticz.Error("None value received, Device not updated")
            # else:
            #    Domoticz.Log(f"Device values {values}")
            #    Devices[1].Update(nValue=0,sValue=str(values['temp'] + ";" + values['hum'] + ";"+ values['comfort']),BatteryLevel=int(values['bat']))

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
