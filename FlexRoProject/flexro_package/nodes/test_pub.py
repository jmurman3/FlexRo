#!/usr/bin/env python2

import rospy
import test_package

if __name__ == '__main__':

    rospy.init_node("test_node")
    node = test_package.ExamplePublisher()
    subscriber = test_package.ExampleSubscriber()
    node.run()