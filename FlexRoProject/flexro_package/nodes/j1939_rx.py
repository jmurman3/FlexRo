#!/usr/bin/env python2

import rospy
import flexro_package

if __name__ == '__main__':

    rospy.init_node("check_estop")
    j1939_rx = flexro_package.Receiver()
    rospy.spin()