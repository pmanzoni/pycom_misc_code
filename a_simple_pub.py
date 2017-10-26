from mqtt import MQTTClient
import time
import pycom

import ufun

wifi_ssid = "raspiWLAN"
wifi_passwd = ''
broker_addr = "test.mosquitto.org"
MYDEVID = "PMdev"

def settimeout(duration):
   pass

def get_data_from_sensor(sensor_id="RAND"):
    if sensor_id == "RAND":
        return ufun.random_in_range()

### if __name__ == "__main__":

ufun.connect_to_wifi(wifi_ssid, wifi_passwd)

client = MQTTClient(MYDEVID, broker_addr, 1883)

if not client.connect():
    print ("Connected to broker: "+broker_addr)

print('Sending messages...')
while True:
    # creating the data
    the_data = get_data_from_sensor()
    # publishing the data
    client.publish(MYDEVID+'/value', str(the_data))
    time.sleep(1)
