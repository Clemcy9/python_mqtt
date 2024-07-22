import paho.mqtt.client as mqtt
from paho import mqtt as mq
import ssl
def on_connect(client, userdata, flags, rc, *args):
    print("Connected with result code " + str(rc))
    # client.subscribe("test/#")
    client.subscribe('property/#')

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

def start_subscriber():
    client = mqtt.Client(client_id="", userdata=None, protocol=mqtt.MQTTv5)
    client.tls_set(tls_version=mq.client.ssl.PROTOCOL_TLS)
    client.username_pw_set("Property", "Mechatronic#1")  # Use your HiveMQ credentials
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("ae5dfdb2a7bf40c2a7537e3fe7dd57c6.s1.eu.hivemq.cloud", 8883)
    client.loop_forever()


def publish_message(topic, message):
    client = mqtt.Client(client_id="", userdata=None, protocol=mqtt.MQTTv5)
    client.tls_set(tls_version=ssl.PROTOCOL_TLS)
    client.username_pw_set("Property", "Mechatronic#1")  # Use your HiveMQ credentials
    client.connect("ae5dfdb2a7bf40c2a7537e3fe7dd57c6.s1.eu.hivemq.cloud", 8883)
    # Start the network loop
    client.loop_start()
    
    # Publish the message
    result = client.publish(topic, message, qos=1)
    
    # Wait for the publish to complete
    result.wait_for_publish()
    
    # Stop the network loop
    client.loop_stop()
    client.disconnect()


def publish_message1(topic, message):
    # Create MQTT client instance
    client = mqtt.Client(client_id="", userdata=None, protocol=mqtt.MQTTv311)
    
    # Configure TLS/SSL
    client.tls_set(tls_version=ssl.PROTOCOL_TLS)
    
    # Set username and password
    client.username_pw_set("Property", "Mechatronic#1")
    
    # Define the on_connect callback to handle connection success/failure
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully")
        else:
            print("Connection failed with code ", rc)

    # Assign the on_connect callback
    client.on_connect = on_connect
    
    # Define the on_publish callback to handle publish success/failure
    def on_publish(client, userdata, mid):
        print("Message published with mid: ", mid)
    
    # Assign the on_publish callback
    client.on_publish = on_publish
    
    # Connect to the broker
    client.connect("ae5dfdb2a7bf40c2a7537e3fe7dd57c6.s1.eu.hivemq.cloud", 8883)
    
    # Start the network loop
    client.loop_start()
    
    # Publish the message
    result = client.publish(topic, message, qos=1)
    
    # Wait for the publish to complete
    result.wait_for_publish()
    
    # Stop the network loop
    client.loop_stop()
    
    # Disconnect from the broker
    client.disconnect()

# Example usage
publish_message("your/topic", "Hello, HiveMQ!")
