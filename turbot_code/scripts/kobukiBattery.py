# Monitor the kobuki's battery level

import roslib
import rospy
from kobuki_msgs.msg import SensorState

class kobuki_battery():

    kobuki_base_max_charge = 160

    def __init__(self):
        rospy.init_node("kobuki_battery")       

        #monitor Kobuki's power and charging status.  If an event occurs (low battery, charging, not charging etc) call function SensorPowerEventCallback
            rospy.Subscriber("/mobile_base/sensors/core",SensorState,self.SensorPowerEventCallback)

        #rospy.spin() tells the program to not exit until you press ctrl + c.  If this wasn't there... it'd subscribe and then immediatly exit (therefore stop "listening" to the thread).
        rospy.spin();


    def SensorPowerEventCallback(self,data):
        rospy.loginfo("Kobuki's battery is now: " + str(round(float(data.battery) / float(self.kobuki_base_max_charge) * 100)) + "%")
        if(int(data.charger) == 0) :
            rospy.loginfo("Not charging at docking station")
        else:
            rospy.loginfo("Charging at docking station")
    

if __name__ == '__main__':
    try:
        kobuki_battery()
    except rospy.ROSInterruptException:
        rospy.loginfo("exception")
