import rospy
from std_msgs.msg import Float64MultiArray


class ExamplePublisher(object):

    def __init__(self):
        self._publisher = rospy.Publisher("/test_package/test_topic", Float64MultiArray, queue_size=1)

    def run(self):
        rate = rospy.Rate(10)
        message = Float64MultiArray()
        count = 1

        while not rospy.is_shutdown():
            rate.sleep()

            count += 1

            imu_array = [6, 7, 10, 19, 2, 3]

            message.data = imu_array

            self._publisher.publish(message)
