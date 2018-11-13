#!/usr/bin/env python 
# Monitor the kobuki's button status

import roslib
import rospy
from kobuki_msgs.msg import ButtonEvent
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from math import pow, sqrt

class kobuki_button():

    def __init__(self):
        rospy.init_node("kobuki_button")    

        # Goal state return values
        self.goal_states = ['PENDING', 'ACTIVE', 'PREEMPTED', 
                       'SUCCEEDED', 'ABORTED', 'REJECTED',
                       'PREEMPTING', 'RECALLING', 'RECALLED',
                       'LOST']      

        #monitor kobuki's button events
        rospy.Subscriber("/mobile_base/events/button",ButtonEvent,self.ButtonEventCallback)
        
        # Publisher to manually control the robot (e.g. to stop it, queue_size=5)
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=5)
        
        # Subscribe to the move_base action server
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        
        rospy.loginfo("Waiting for move_base action server...")
        
        # Wait 60 seconds for the action server to become available
        self.move_base.wait_for_server(rospy.Duration(60))
        
        rospy.loginfo("Connected to move base server")  

        self.locations = dict()
        
        self.locations['A'] = Pose(Point(-1.79, -1.23, 0.000), Quaternion(0.000, 0.000, 0.223, 0.975))
        self.locations['B'] = Pose(Point(-1.31, -0.131, 0.000), Quaternion(0.000, 0.000, -0.670, 0.743))
        self.locations['C'] = Pose(Point(-2.62, -0.286, 0.000), Quaternion(0.000, 0.000, 0.733, 0.680))
    
        self.goal = MoveBaseGoal()
        
        #rospy.spin() tells the program to not exit until you press ctrl + c.  If this wasn't there... it'd subscribe and then immediatly exit (therefore stop "listening" to the thread).
        rospy.spin();

    def go(self, location):
        # Set up the next goal location
        
        self.goal.target_pose.pose = self.locations[location]
        self.goal.target_pose.header.frame_id = 'map'
        self.goal.target_pose.header.stamp = rospy.Time.now()
        
        # Let the user know where the robot is going next
        rospy.loginfo("Going to: " + str(location))
        
        # Start the robot toward the next location
        self.move_base.send_goal(self.goal)
        
        # Allow 5 minutes to get there
        finished_within_time = self.move_base.wait_for_result(rospy.Duration(300)) 
        
        # Check for success or failure
        if not finished_within_time:
            self.move_base.cancel_goal()
            rospy.loginfo("Timed out achieving goal")
        else:
            state = self.move_base.get_state()
            if state == GoalStatus.SUCCEEDED:
                rospy.loginfo("Goal succeeded!")
                rospy.loginfo("State:" + str(state))
            else:
              rospy.loginfo("Goal failed with error code: " + str(self.goal_states[state]))

    
    def ButtonEventCallback(self,data):
        if ( data.state == ButtonEvent.RELEASED ) :
            ButtonState = "released"
        else:
            ButtonState = "pressed"  
        if ( data.button == ButtonEvent.Button0 ) :
            button = "A"
        elif ( data.button == ButtonEvent.Button1 ) :
            button = "B"
        else:
            button = "C"
            rospy.loginfo("Button %s was %s."%(button, ButtonState))

        self.go(button)
    

if __name__ == '__main__':
    try:
        kobuki_button()
    except rospy.ROSInterruptException:
        rospy.loginfo("exception")
