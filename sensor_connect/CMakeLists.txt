cmake_minimum_required(VERSION 2.8.3)
project(sensor_connect)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  actionlib_msgs
  message_generation
)


## Generate messages in the 'msg' folder
 add_message_files(
   FILES
   sensor.msg 
)


## Generate added messages and services with any dependencies listed here
 generate_messages(
   DEPENDENCIES
   std_msgs
)



catkin_package(
  INCLUDE_DIRS include
  CATKIN_DEPENDS roscpp rospy std_msgs message_runtime
  DEPENDS system_lib
)

