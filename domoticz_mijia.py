import urllib.request
import base64
import time
from mijia.mijia_poller import MijiaPoller, \
    MI_HUMIDITY, MI_TEMPERATURE, MI_BATTERY

# Settings for the domoticz server

# Forum see: http://domoticz.com/forum/viewtopic.php?f=56&t=13306&hilit=mi+flora&start=20#p105255

"""
domoticzserver   = "127.0.0.1:8000"
domoticzusername = ""
domoticzpassword = ""
"""

# So id devices use: sudo hcitool lescan

# Sensor IDs

# Create virtual sensors in dummy hardware
# type temperature & humidity

"""
base64string = base64.encodestring(('%s:%s' % (domoticzusername, domoticzpassword)).encode()).decode().replace('\n', '')

def domoticzrequest (url):
  print(url)
  request = urllib.request.Request(url)
  request.add_header("Authorization", "Basic %s" % base64string)
  response = urllib.request.urlopen(request)
  return response.read()
"""

# New read function, input the macaddress, output a dict with {temp, hum, bat, comfort} values.
def read(address, debug=False):
	values = {'address': address, 'temp': None, 'hum': None, 'bat': None, 'comfort':None, 'name': None, 'firmware_version': None}

	# Create Poller
	poller = MijiaPoller(address)

	# Poll device values
	values['firmware_version'] = poller.firmware_version()
	values['name'] = poller.name()
	values['temp'] = poller.parameter_value(MI_TEMPERATURE)
	values['hum'] = poller.parameter_value(MI_HUMIDITY)
	values['bat'] = poller.parameter_value(MI_BATTERY)

	# Evaluate comfort
	values['comfort'] = "0"
    if float(values['hum']) < 40:
        values['comfort'] = "2"
    elif float(values['hum']) <= 70:
        values['comfort'] = "1"
    elif float(values['hum']) > 70:
        values['comfort'] = "3"

	if debug:
		print(f"Mi Sensor: {values['address']}")
	    print(f"Firmware: {values['firmware_version']}")
	    print(f"Name: {values['name']}")
	    print(f"Temperature: {values['temp']}°C")
	    print(f"Humidity: {values['hum']}%")
	    print(f"Battery: {values['bat']}%")
		print(f"Comfort: {values['comfort']}%")

	return values

def update(address,idx_temp):

    poller = MijiaPoller(address)


    loop = 0
    try:
        temp = poller.parameter_value(MI_TEMPERATURE)
    except:
        temp = "Not set"
    
    while loop < 2 and temp == "Not set":
        print("Error reading value retry after 5 seconds...\n")
        time.sleep(5)
        poller = MijiaPoller(address)
        loop += 1
        try:
            temp = poller.parameter_value(MI_TEMPERATURE)
        except:
            temp = "Not set"
    
    if temp == "Not set":
        print("Error reading value\n")
        return
    
    global domoticzserver

    print("Mi Sensor: " + address)
    print("Firmware: {}".format(poller.firmware_version()))
    print("Name: {}".format(poller.name()))
    print("Temperature: {}°C".format(poller.parameter_value(MI_TEMPERATURE)))
    print("Humidity: {}%".format(poller.parameter_value(MI_HUMIDITY)))
    print("Battery: {}%".format(poller.parameter_value(MI_BATTERY)))

    val_bat  = "{}".format(poller.parameter_value(MI_BATTERY))
    
    # Update temp
    #val_temp = "{}".format(poller.parameter_value(MI_TEMPERATURE))
    #domoticzrequest("http://" + domoticzserver + "/json.htm?type=command&param=udevice&idx=" + idx_temp + "&nvalue=0&svalue=" + val_temp + "&battery=" + val_bat)

    # Update humidity
    #val_hum = "{}".format(poller.parameter_value(MI_HUMIDITY))
    #domoticzrequest("http://" + domoticzserver + "/json.htm?type=command&param=udevice&idx=" + idx_hum + "&svalue=" + val_hum + "&battery=" + val_bat)

	#/json.htm?type=command&param=udevice&idx=IDX&nvalue=0&svalue=TEMP;HUM;HUM_STAT
    val_temp = "{}".format(poller.parameter_value(MI_TEMPERATURE))
    val_hum = "{}".format(poller.parameter_value(MI_HUMIDITY))
    
    val_comfort = "0"
    if float(val_hum) < 40:
        val_comfort = "2"
    elif float(val_hum) <= 70:
        val_comfort = "1"
    elif float(val_hum) > 70:
        val_comfort = "3"
    
    domoticzrequest("http://" + domoticzserver + "/json.htm?type=command&param=udevice&idx=" + idx_temp + "&nvalue=0&svalue=" + val_temp + ";" + val_hum + ";"+ val_comfort + "&battery=" + val_bat)
	

print("\n1: updating")
# manual testing via direct shell launch `# python domoticz_mijia.py`
# update("4C:65:A8:D0:4C:98","752")
# update("4C:65:A8:D0:26:D2","753")
# update("4C:65:A8:D0:57:2A","754")
read("4C:65:A8:D0:4C:98", debug=True)




