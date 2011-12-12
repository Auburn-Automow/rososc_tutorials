#!/usr/bin/env python
import roslib; roslib.load_manifest('rososc_tutorials')
import rospy

from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus, KeyValue
import random

class DummyDiagnostics(object):
    def __init__(self):
        self.publisher = rospy.Publisher("diagnostics",DiagnosticArray)

        self.values = []
        it = 0
        while it < 20:
            self.values.append(KeyValue("Key %i"%it,str(random.randint(0,50))))
            it += 1

    def update(self):
        msg = DiagnosticArray()
        msg.header.stamp = rospy.Time.now()
        msg.status = []
        it = 0
        while it < 20:
            status = DiagnosticStatus()
            status.level = random.randint(0,2)
            status.name = "Test %i"%it
            status.hardware_id = "Dummy Diagnostics"
            status.values = self.values
            it += 1
            msg.status.append(status)
        self.publisher.publish(msg)

if __name__ == "__main__":
    rospy.init_node('dummy_diag')
    node = DummyDiagnostics()
    
    while not rospy.is_shutdown():
        node.update()
        rospy.sleep(1.0)

