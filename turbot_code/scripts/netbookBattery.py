# Monitor the netbook's battery level

import roslib
import rospy
from smart_battery_msgs.msg import SmartBatteryStatus #for netbook battery

class netbook_battery():

    def __init__(self):
        rospy.init_node("netbook_battery")      

        #monitor netbook's battery status.  Everytime anything changes call the call back function self.NetbookPowerEventCallback and pass the data regarding the current battery status
        rospy.Subscriber("/laptop_charge/",SmartBatteryStatus,self.NetbookPowerEventCallback)

        #rospy.spin() tells the program to not exit until you press ctrl + c.  If this wasn't there... it'd subscribe to /laptop_charge/ then immediatly exit (therefore stop "listening" to the thread).
        rospy.spin();


    def NetbookPowerEventCallback(self,data):
        print("Percent: " + str(data.percentage)) 
        print("Charge: " + str(data.charge))
        if(int(data.charge_state) == 1):
            print("Currently charging")
        else:
            print("Not charging")
        print("-----")
        #Tip: try print(data) for a complete list of information available in the /laptop_charge/ thread

if __name__ == '__main__':
    try:
        netbook_battery()
    except rospy.ROSInterruptException:
        rospy.loginfo("exception")
