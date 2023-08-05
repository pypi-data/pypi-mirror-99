from hive.core import HivePubSub
import rospy


class HiveRos(HivePubSub):

    def __init__(self, name):
        rospy.init_node(name, anonymous=True)
        self.publishers = {}

    def subscribe(self, topic, cls, callback):
        rospy.Subscriber(topic, cls, callback)

    def publish(self, topic, obj):
        publisher = self.publishers.get(topic, None)
        if publisher is None:
            publisher = rospy.Publisher(topic, type(obj), queue_size=1)
            self.publishers[topic] = publisher
        publisher.publish(obj)

    def spin(self):
        rospy.spin()

    def spin_once(self):
        pass
