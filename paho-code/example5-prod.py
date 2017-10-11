import paho.mqtt.client as mqtt 
import time
import random
import json

mqttc=mqtt.Client()
mqttc.connect("localhost", 1883, 60)

mqttc.loop_start()

while True:
    # Getting the data
    the_time = time.strftime("%H:%M:%S")
    the_value = random.randint(1,100)
    the_msg={'Sensor': 1, 'C_F': 'C', 'Value': the_value, 'Time': the_time}
    the_msg_str = json.dumps(the_msg)

    print the_msg_str

    mqttc.publish("pietro/test",the_msg_str)
    time.sleep(5)# sleep for 5 seconds before next call

mqttc.loop_stop()


