import rospy
from j1939_ros_interface.msg import J1939, J1939Filter
from j1939_ros_interface.srv import Filter, FilterRequest, FilterResponse
from std_msgs.msg import UInt8MultiArray


class Transmitter(object):

    def __init__(self):
        j1939_transmit_topic = rospy.get_param("~j1939_transmit_topic", default="/j1939/transmitter")
        self._j1939_pub = rospy.Publisher(j1939_transmit_topic, J1939, queue_size=1)
        self._j1939_sub = rospy.Subscriber("/flexro/estop/hydro", UInt8MultiArray, callback=self._callback, queue_size=1)

    def _callback(self, msg):
        j1939_msg = J1939()
        j1939_msg.page = 0
        j1939_msg.pf = 0xFF
        j1939_msg.ps = 0x11
        j1939_msg.source = 0x27

        if msg.data == [0]:
            j1939_msg.data = [69, 0x1, 0xFF]
        else:
            j1939_msg.data = [69, 0x0, 0xFF]

        self._j1939_pub.publish(j1939_msg)


class Receiver(object):

    def __init__(self):

        rospy.wait_for_service("j1939_filter", timeout=5)

        self._add_j1939_filter = rospy.ServiceProxy("j1939_filter", Filter)

        j1939_filter = J1939Filter()
        j1939_filter.page = [0, 0]
        j1939_filter.pf = [0xff, 0xff]
        j1939_filter.ps = [0x12, 0x17]
        j1939_filter.source = [0x2e, 0x80]

        filter_request = FilterRequest()
        filter_request.filters = [j1939_filter]
        filter_request.topic = "/j1939/flexro/hydro"

        self._add_j1939_filter(filter_request)
        self._j1939_sub = rospy.Subscriber("/j1939/flexro/hydro", J1939, callback=self._j1939_callback)
        self._publisher = rospy.Publisher("/flexro/estop/hydro", UInt8MultiArray, queue_size=1)

    def _j1939_callback(self, msg):
        data_bytes = bytearray(msg.data)

        array = UInt8MultiArray()
        array.data = [0, 1]

        if data_bytes[1] == 0:
            self._publisher.publish(array)
        else:
            self._publisher.publish(array)
