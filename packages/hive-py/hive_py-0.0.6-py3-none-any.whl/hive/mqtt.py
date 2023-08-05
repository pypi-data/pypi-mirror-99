import paho.mqtt.client as mqtt
from hive.core import HiveBytePubSub, json_encoder, json_decoder


class HiveMqtt(HiveBytePubSub):

    def __init__(self,
                 # Connection options
                 host="localhost",
                 port=1883,
                 keepalive=60,
                 bind_address="",
                 bind_port=0,
                 clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY,
                 properties=None,

                 # client options
                 client_id="",
                 clean_session=None,
                 userdata=None,
                 protocol=mqtt.MQTTv311,
                 transport="tcp",

                 # encoder options
                 encoder=json_encoder,
                 decoder=json_decoder
                 ):
        super().__init__(encoder, decoder)
        self.client = mqtt.Client(client_id, clean_session, userdata, protocol, transport)
        self.client.connect(host, port, keepalive, bind_address, bind_port, clean_start, properties)
        self.client.on_message = self.on_message()  # we use this to close over self so we can access the subscription list
        self.subscriptions = {}

    def on_message(self):
        def client_on_message(client, userdata, message):
            for cb in self.subscriptions[message.topic]:
                cb(message.payload)

        return client_on_message

    def subscribe_raw(self, topic, callback):
        self.client.subscribe(topic)
        subscriptions = self.subscriptions.get(topic, [])
        subscriptions.append(callback)
        self.subscriptions[topic] = subscriptions

    def publish_raw(self, topic, message):
        self.client.publish(topic, message)

    def spin(self):
        self.client.loop_forever()
