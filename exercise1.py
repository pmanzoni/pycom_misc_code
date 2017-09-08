from mqtt import MQTTClient
import time
import pycom

import ufun

wifi_ssid = "LOCAL_AP"
wifi_passwd = ''
broker_addr = "test.mosquitto.org"

def settimeout(duration):
   pass

def on_message(topic, msg):
    if msg == b'GREEN':
        ufun.set_led_to(ufun.GREEN)
    elif msg == b'RED':
        ufun.set_led_to(ufun.RED)
    elif msg == b'OFF':
        ufun.set_led_to(ufun.OFF)
    else:
        pycom.rgbled(ufun.YELLOW)

    print("topic is: "+str(topic))
    print("msg is: "+str(msg))

### if __name__ == "__main__":

ufun.connect_to_wifi(wifi_ssid, wifi_passwd)

client = MQTTClient("dev_id", broker_addr, 1883)
client.set_callback(on_message)

if not client.connect():
    print ("Connected to broker: "+broker_addr)
client.subscribe('lopy/lights')

print('Waiting messages...')
while 1:
    client.wait_msg()
