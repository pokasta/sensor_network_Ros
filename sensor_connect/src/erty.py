import rospy

from sensor_msgs.msg import Joy


def callback(msg):
  
  data1 = msg.axes[1]
  data2 = msg.axes[2]
  print(data1)
  
 





def joy_teleop():
  rospy.init_node('joy_teleop')
  # Get parameters from the server
  global speed_factor
  
  # Susbscribe to the topic that contains the ps3 keys
  rospy.Subscriber('/joy', Joy, callback)   
  # Keeps python from exiting until this node is stopped
  rospy.spin()
 
if __name__ == '__main__':
  joy_teleop()