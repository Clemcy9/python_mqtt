import requests
from requests.auth import HTTPBasicAuth
from rest_framework import serializers
import paho.mqtt.client as mqtt
from paho import mqtt as mq
import ssl
from .models import Notification, Reminder, RentDemand

MESSENGER_URL = 'http://127.0.0.2:8000/api/upload/'
# Define the user credentials
username = "07066186691"
password = "08020366909"

class PayloadSerializer(serializers.ModelSerializer):
    sender = serializers.CharField() #returns str of foreign key field insted of id
    class Meta:
        model = Notification
        fields = '__all__'

# via api model
def send_via_api(payload, username=username, password=password):
    try:
        # Convert queryset to list of dictionaries
        data = PayloadSerializer(payload,many=True)

        # Send POST request with basic authentication and form-encoded data
        response = requests.post(MESSENGER_URL, auth=HTTPBasicAuth(username, password), json=data.data)
        
        if response.status_code == 200 or 201:
            print('[send] Sent successfully')
            # Assuming payload is a queryset of objects with a 'status_flag' field
            for obj in payload:
                obj.status_flag = 'sent'
                obj.save()
        else:
            print(f'[send] Failed to send (status code: {response.status_code})')
            # Assuming payload is a queryset of objects with a 'status_flag' field
            for obj in payload:
                obj.status_flag = 'failed'
                obj.save()

        return response.json()  # Return JSON response from the server
    except requests.exceptions.RequestException as e:
        print(f'[send] Exception occurred: {str(e)}')
        return None


class MqttSender:
    def __init__(self, broker_url = 'ae5dfdb2a7bf40c2a7537e3fe7dd57c6.s1.eu.hivemq.cloud', port = 8883, username ='Property', password ='Mechatronic#1'):
        self.client = mqtt.Client(client_id="", userdata=None, protocol=mqtt.MQTTv5)
        self.client.tls_set(tls_version=ssl.PROTOCOL_TLS)
        self.client.username_pw_set(username,password)    
        self.broker_url = broker_url
        self.port = port
        # self.client.connect('ae5dfdb2a7bf40c2a7537e3fe7dd57c6.s1.eu.hivemq.cloud',1883,60)
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
    
    def on_connect(self, client, userdata, flags, rc, *args):
        if rc == 0:
            print("Connected successfully")
        else:
            print("Connection failed with code ", rc)

    def on_publish(self, client, userdata, mid):
        print("Message published with mid: ", mid)
        return 'successful'


    def send_via_mqtt(self,payload, topic='property'):
        self.client.connect(self.broker_url,self.port)
        self.client.loop_start()
        # Publish the message
        self.result = self.client.publish(topic=topic, payload=payload, qos=1)
        
        # Wait for the publish to complete
        self.result.wait_for_publish()
        
        # Stop the network loop
        self.client.loop_stop()
        self.client.disconnect()
