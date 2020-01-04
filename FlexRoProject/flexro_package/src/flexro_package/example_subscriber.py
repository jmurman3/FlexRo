import rospy
import random
from j1939_ros_interface.msg import J1939
from std_msgs.msg import UInt8MultiArray
from std_msgs.msg import String


class EstopProcess(object):

    def __init__(self):
        j1939_transmit_topic = rospy.get_param("~j1939_transmit_topic", default="/j1939/transmitter")
        self._j1939_sub = rospy.Subscriber("/j1939/flexro", J1939, callback=self._j1939_callback)
        self._reset_sub = rospy.Subscriber("/flexro/estop/reset", String, callback=self._reset_callback)
        self._publisher = rospy.Publisher("/flexro/estop/array", UInt8MultiArray, queue_size=1)
        self._publisher2 = rospy.Publisher("/flexro/estop/string", String, queue_size=1)
        self._j1939_pub = rospy.Publisher(j1939_transmit_topic, J1939, queue_size=1)
        self.estop_array = [0, 0, 0, 0, 0, 0, 0]
        self.reset_flag = 0

    def _j1939_callback(self, msg):
        data_bytes = bytearray(msg.data)
        sa_array = (0x2e, 0xd0, 0x1e, 0x80, 0x81, 0x82, 0x83)
        estop_send = UInt8MultiArray()
        index = 0

        for sa in sa_array:
            if sa == msg.source:
                self.estop_array[index] = data_bytes[1]
                estop_send.data = self.estop_array
                self._publisher.publish(estop_send)
            index += 1

        if 1 in self.estop_array and self.reset_flag == 0:
            estop_str = 'ESTOP ACTIVE'
            emstop_int = 0x01
        elif 1 in self.estop_array and self.reset_flag == 1:
            estop_str = 'RESET ACTIVE'
            emstop_int = 0x02
        else:
            estop_str = 'ALL CLEAR'
            self.reset_flag = 0
            emstop_int = 0x00

        self._publisher2.publish(estop_str)
        self.transmit_estop_j1939(emstop_int)

    def _reset_callback(self, msg):
        if msg.data == 'RESET':
            self.reset_flag = 1

    def transmit_estop_j1939(self, emstop_int):
        j1939_msg = J1939()
        j1939_msg.page = 0
        j1939_msg.pf = 0xFF
        j1939_msg.ps = 0x11
        rand_int = random.randint(0x0, 0xFF)

        j1939_msg.data = [rand_int, emstop_int, 0xFF]

        self._j1939_pub.publish(j1939_msg)