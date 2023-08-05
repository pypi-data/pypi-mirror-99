import jsonpickle
import time
import importlib


class HivePubSub:
    def subscribe(self, topic, cls, callback):
        '''
        Subscribe to a topic, with a callback expecting instances of type cls
        :param topic:
        :param cls:
        :param callback:
        :return:
        '''
        pass

    def publish(self, topic, obj):
        '''
        Subscribe to a topic, with a callback expecting instances of type cls
        :param topic:
        :param cls:
        :param callback:
        :return:
        '''
        pass

    def spin(self):
        '''
        Hand control to the pubsub and process incoming messages
        :return:
        '''
        while True:
            self.spin_once()

    def spin_once(self):
        '''
        Process the next message
        :return:
        '''
        time.sleep(0.001)


def json_encoder(cls, obj):
    return jsonpickle.encode(obj, unpicklable=False).encode("utf-8")


def json_decoder(cls, msg_bytes):
    d = jsonpickle.decode(msg_bytes.decode("utf-8"))
    if type(d) == cls:
        return d

    obj = cls()
    for k, v in d.items():
        setattr(obj, k, v)
    return obj


class HiveBytePubSub(HivePubSub):
    '''
    A specific Hive PubSub where all topics take bytes objects, and in-process
    encoders are used to convert the objects to and from byte streams.

    subscribe and publish call the encoders and then the subscribe_raw and publish_raw methods
    respectively. the *_raw methods always send and recieve bytes, and should be implemented
    in the subclasses

    Mqtt and Redis both use this as their base
    '''

    def __init__(self,
                 encoder=json_encoder,
                 decoder=json_decoder
                 ):
        self.encoder = encoder
        self.decoder = decoder

    def subscribe(self, topic, cls, callback):
        self.subscribe_raw(
            topic,
            lambda obj: callback(self.decoder(cls, obj))
        )

    def publish(self, topic, obj):
        self.publish_raw(topic, self.encoder(type(obj), obj))

    def subscribe_raw(self, topic, callback):
        """
        Subscribe to the bytes received on a topic

        :param topic: topic name
        :param callback: callback function to execute - cb(bytes)
        :return: None
        """
        pass

    def publish_raw(self, topic, message):
        """
        Publish raw bytes to a topic
        :param topic: topic to subscribe
        :param message: message bytes to publish
        :return:
        """
        pass


class Publisher:
    '''
    Convenience class to collect a pubsub instance and a topic for easy repeat publishing
    '''

    def __init__(
            self,
            pubsub,
            topic,
    ):
        self.pubsub = pubsub
        self.topic = topic

    def publish(self, obj):
        self.pubsub.publish(self.topic, obj)


class HiveWorker:
    pubsub_cls = HivePubSub

    def __init__(self, *args, **kwargs):
        self.pubsub = HiveWorker.pubsub_cls(*args, **kwargs)

    def spin(self):
        try:
            self.pubsub.spin()
        except KeyboardInterrupt:
            pass

    def publisher(self, topic):
        return Publisher(self.pubsub, topic)

    def subscribe(self, topic, cls, callback):
        return self.pubsub.subscribe(topic, cls, callback)

    @staticmethod
    def load_from_config(filename="hive.json"):
        with open(filename) as f:
            json = f.read()
        options = jsonpickle.decode(json)

        module_name, _, class_name = options["pubsub"].rpartition('.')
        module = importlib.import_module(module_name)
        cls = getattr(module, class_name)
        HiveWorker.pubsub_cls = cls
        return HiveWorker(**options["init"])
