import rospy
from j1939_ros_interface.msg import J1939
from std_msgs.msg import UInt8MultiArray


class EstopProcess(object):

    def __init__(self):

        self._j1939_sub = rospy.Subscriber("/j1939/flexro", J1939, callback=self._j1939_callback)
        self._publisher = rospy.Publisher("/flexro/estop/hydro", UInt8MultiArray, queue_size=1)
        self.estop_array = [0, 0, 0, 0, 0, 0, 0]

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

        print(self.estop_array)

        if 1 in self.estop_array:
            print('ESTOP ACTIVE')
        elif 2 in self.estop_array:
            print('Reset present')
        else:
            print('All clear')
