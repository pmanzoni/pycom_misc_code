import paho.mqtt.client as mqtt
import json

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    themsg = json.loads(str(msg.payload))
    print "Sensor "+str(themsg['Sensor'])+" got value ",
    print str(themsg['Value'])+" "+themsg['C_F'],
    print " at time "+str(themsg['Time'])

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.subscribe("pietro/test")

client.loop_forever()

