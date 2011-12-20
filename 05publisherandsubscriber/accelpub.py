#!/usr/bin/env python

import roslib; roslib.load_manifest('rososc_tutorials')
import rospy

from sensor_msgs.msg import Imu
from touchosc_msgs.msg import MultiFader


# Ring Buffer from: http://www.saltycrane.com/blog/2007/11/python-circular-buffer/
class RingBuffer:
    def __init__(self, size):
        self.data = [0.0 for i in xrange(size)]

    def append(self, x):
        self.data.pop(0)
        self.data.append(x)

    def get(self):
        return self.data

class PubSub(object):
    def __init__(self):
        rospy.init_node('pubsub')
        
        self.accel_sub = rospy.Subscriber('/touchosc/accel',Imu,self.imu_cb)
        self.fader_pub = rospy.Publisher('/touchosc/1/multifader',MultiFader)
        
        self.ringBuffer = RingBuffer(50)
        
    def imu_cb(self, msg):
        self.ringBuffer.append(float(msg.linear_acceleration.x)/5)
        newMsg = MultiFader()
        newMsg.values = self.ringBuffer.data
        self.fader_pub.publish(newMsg)
    
if __name__ == '__main__':
    try:
        a = PubSub()
        rospy.spin()
    except rospy.ROSInterruptException: pass
