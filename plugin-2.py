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
import re
from mijia.mijia_poller import MijiaPoller, MI_HUMIDITY, MI_TEMPERATURE, MI_BATTERY

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
        self.macAddresses = self.parseMacList(Parameters["Mode6"])
        Domoticz.Log(f"MacAddress List : {self.macAddresses}")
        
        # Create devices
        unit = 1
        for mac in self.macAddresses:
            existing = self.findDevice(mac)
            if existing is not None:
                Domoticz.Log(f"{mac} already exists")
                continue
            while unit in Devices:
                unit += 1
            Domoticz.Device(
                Name=f"{mac}",
                Unit=unit,
                TypeName="Temp+Hum",
                Used=0,
                Description=mac
            ).Create()
            # Domoticz.Device(Name="MIJIA", Unit=1, TypeName="Temp+Hum", Used=0).Create()
            Domoticz.Log(f"Created device {mac}")
            unit += 1

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
        for unit in Devices:
            device = Devices[unit]
            # MAC address is stored in the device description
            mac = device.Description.strip()
            if mac == "":
                continue
            try:
                values = self.read(self.macAddress)
    
                if values['temp'] is None:
                    Domoticz.Log(f"No Temp value for {mac}")
                    continue
                if values['hum'] is None:
                    Domoticz.Log(f"No Humidity value for {mac}")
                    continue
                if values['comfort'] is None:
                    Domoticz.Log(f"No Comfort value for {mac}")
                    continue
                if values['bat'] is None:
                    Domoticz.Log(f"No Battery value for {mac}")
                    continue
    
                # Update the device
                device.Update(nValue=0,sValue=str(values['temp'] + ";" + values['hum'] + ";"+ values['comfort']),BatteryLevel=int(values['bat']))
                # DEBUG
                Domoticz.Log(f"Updated {device.Name} ({mac}) -> {values}")
    
            except Exception as e:
                Domoticz.Error(f"Error reading {mac} : {e}")

    def parseMacList(self, text):
        macs = []
        if not text:
            return macs
        parts = re.split(r'[\n,; ]+', text)
        for p in parts:
            p = p.strip().upper()
            if p == "":
                continue
            p = p.replace("-", ":")
            if re.match(r'^([0-9A-F]{2}:){5}[0-9A-F]{2}$', p):
                macs.append(p)
            else:
                Domoticz.Error("Invalid MAC: {}".format(p))
        return macs
        
    def findDevice(self, mac):
        for unit in Devices:
            if Devices[unit].Description.upper() == mac:
                return unit
        return None

    def read(self, address):
        values = {'address': address, 'temp': None, 'hum': None, 'bat': None, 'comfort':None, 'name': None, 'firmware_version': None}
    
        # Create Poller
        poller = MijiaPoller(address)
    
        # Poll device values
        values['firmware_version'] = poller.firmware_version()
        values['name'] = poller.name()
        values['temp'] = poller.parameter_value(MI_TEMPERATURE)
        values['hum'] = poller.parameter_value(MI_HUMIDITY)
        values['bat'] = poller.parameter_value(MI_BATTERY)
        values['comfort'] = "0"
        return values

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
