#!/usr/bin/env python2

import rospy
import flexro_package

if __name__ == '__main__':

    rospy.init_node("estop_process")
    node = flexro_package.EstopProcess()
    rospy.spin()