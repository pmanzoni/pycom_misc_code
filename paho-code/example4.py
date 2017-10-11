import paho.mqtt.client as mqtt 
import time

mqttc=mqtt.Client()
mqttc.connect("localhost", 1883, 60)

mqttc.loop_start()
while True:
    mqttc.publish("pietro/test","Hello")
    time.sleep(10)# sleep for 10 seconds before next call

mqttc.loop_stop()
