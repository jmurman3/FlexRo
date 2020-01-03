#!/usr/bin/env python2

import rospy
import flexro_package

if __name__ == '__main__':

    rospy.init_node("j1939_transmit")
    j1939_tx = flexro_package.Transmitter()
    rospy.spin()
