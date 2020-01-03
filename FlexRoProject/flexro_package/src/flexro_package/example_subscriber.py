import rospy
import std_msgs.msg


class ExampleSubscriber(object):

    def __init__(self):
        self._subscriber = rospy.Subscriber("/test_package/test_topic", std_msgs.msg.Float64MultiArray,
                                            callback=self._callback, queue_size=1)

    def _callback(self, msg):
        print msg.data
