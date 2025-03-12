# LAB 3\* - Localization through particle filter

## Introduction

Welcome to LAB 3 of the mobile robotics course! Here, you will make your stack more elaborate through adding a robust localization with particle filter. By the end of this lab, participants will be able to:
- Have a good understanding of the particle filter.
- Integrate the particle filter localization with the point controller from LAB 2.
- Make an interactive interface to work with your navigational stack. 


#### The summary of what you should learn is as following:

1. You will learn how to search effieciently when you have a large space. 
2. You will learn how to do resampling when you have better distributions for your states.
3. You will learn how to leverage ros visualization tool (Rviz) to make an interactive interface with.


### NOTES for pre-lab activities
Given the limited time in the lab, it is highly recommended to go through this manual and start (or complete) your implementation before the lab date, by working on your personal setup (VMWare, remote desktop, lent laptop), and using simulation for testing when needed to verify that your codes are working before coming into the lab. For simulation, refer to [tbt3Simulation.md](https://github.com/ME597c/ME597c-Students/blob/main/tbt3Simulation.md) in the `main` branch.

During the 3 hours in the lab, you want to utilize this time to test your code, work with the actual robot, get feedback from the TAs, and acquire the in-lab marks (check `rubrics.md` in the same branch).

While in-lab, you are required to use the Desktop PCs and **NOT** your personal setup (VMWare, remote desktop, lent laptop). So, make sure that you have your modified files, either online or on a USB, with you to try it out in-lab. 

#### For Simulation
As now, there is no path planning included in the whole stack to avoid obstacles, so you are suggested to use a much simpler map for simulation. You can use the `room` map for the simulation, which corresponding to
```
ros2 launch turtlebot3_gazebo turtlebot3_dqn_stage1.launch.py
```

You are also welcome to use some other map, or even add obstacles by yourself in gazebo, just remember to use the same map for SLAM and the particle filter.

### Pre-lab deliverable (5 marks)
A first version of the completed code is to be submitted **24 hours before the group's lab section** (e.g. groups on the Thursday section must submit by Wednesday at 5:30 PM), along with a list of doubts/questions to be solved during the in-person lab section (optional, if needed). The in-person lab is not meant for implementation but for testing and getting help from the TAs. 

Failure to submit will result in a penalty of 5 marks on the lab report. The code does not have to be fully correct, but it should be (at least almost) complete and meaningful with appropriate comments.


## Part 1 - connecting to the robot (no marks)
Open the [connectToUWtb4s.md](https://github.com/ME597c/ME597c-Students/blob/main/connectToUWtb4s.md) markdown file in the main branch, and follow along. Read and follow each step carefully.

## Part 2 - Robot teleop (no marks)

In this part, you will learn to play with the robot; you will get to undock it from the charger and then move it around by keyboard.  
When you want to dock it again, It should be able to find it only when it is in less than ~0.5 meter around it. Note, that it doesn't
necessarily goes to the dock that it was undocked from, it will just find the next available dock.

The undock command goes through a [action server](https://docs.ros.org/en/humble/Tutorials/Intermediate/Writing-an-Action-Server-Client/Cpp.html).

```
ros2 action send_goal /undock irobot_create_msgs/action/Undock {}
```
You robot should undock.
If not, revisit *Part 1* - Connect to robot via VPN, and make sure the VPN terminal is still running and that you can still see the robot's topics. If you suspect the vpn isn't working, make sure you terminate it, and then run again.

Next run the teleop command to be able to move the robot manually around.

```
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

See the prompt for help on the keys. 

To dock the robot, use:

```
ros2 action send_goal /dock irobot_create_msgs/action/Dock {}
```

### NOTE: when you open a new terminal, you need to source again and set the domain ID, or you will not see the topics:

- Source the .bashrc file: `source ~/robohub/turtlebot4/configs/.bashrc`
- Declare ros2 domain: `export ROS_DOMAIN_ID=X` (X being the number of your robot)

### Odometry reset
For this lab, you may want to reset the odometry so that when you start your path, the odometry starts from the (0, 0, 0) state.
Use this command to reset the odometry on the physical TurtleBot4 (in **simulation**, by simply **restarting** the simulation, you can reset the odometry):

```
ros2 service call /reset_pose irobot_create_msgs/srv/ResetPose {}

```

## Part 3 - Map aquisition (10 marks)

We are planning to have two maps for the in-lab part, you will scan one of them and save it as `room` map. Remember to use the same map for the particle filter.

Undock the robot, put the robot in the closest entrance marked for you, **try your best to align the robot with the marker**, and reset the odometry, and then acquire the map as you did in LAB-1 and save it as room for use in the planning.

```
# terminal 1: reset the odometry pose
ros2 service call /reset_pose irobot_create_msgs/srv/ResetPose {}
# terminal 2: run the SLAM
ros2 launch turtlebot4_navigation slam.launch.py
# terminal 3: view the results in RViz
ros2 launch turtlebot4_viz view_robot.launch.py
# terminal 4: move around the robot
ros2 run teleop_twist_keyboard teleop_twist_keyboard
# terminal 5: save the map
ros2 run nav2_map_server map_saver_cli -f room
``` 

**Note: if you face "Failed to spin map subscription" error, just rerun the `ros2 run nav2_map_server map_saver_cli -f room`**.

When the map is **acquired and saved**, make sure you **take out the robot from the map** and **leave room for the other groups**.

#### In-lab marking: Show the map to a TA to score the marks associated to this part.

## Part 4 - Localize your robot with Particle Filter (20 marks)
Start by first fixing your particle filter, so you can run the standalone ```particleFilter.py``` to localize your robot. 
To fix your particle filter, you will need to:
- Complete the motion model for each particle; follow the comments in ```particle.py```;
- See through impelementing a search algorithm for the map occupancy grids and each particle weight calculation in ```particle.py``` and ```mapUtilities.py```; You will need to explain two functions to a TA in the lab.
- Complete the initialization and resampling for the particle filter algorithm; follow the comments in ```particleFilter.py```.

In the lab, you will need to run the particle filter standalone to see the particles converging to the robot pose.
- Place the robot in the map where you run the SLAM and reset the odometry.
- Run the following commands:
  ```
  # terminal 1
  python3 particleFilter.py
  # terminal 2
  rviz2 -d for_pf.rviz
  # terminal 3
  ros2 run teleop_twist_keyboard teleop_twist_keyboard
  ``` 
- When the Rviz window opened throw a good guess by using ```2D pose estimate``` button in the top toolbar.
- If the particles converged, try to moving the robot around with the ```ros2 run teleop_twist_keyboard teleop_twist_keyboard```.

#### In-lab marking: You need to explain how to compute the likelihood in `mapUtilities.py -> make_likelihood_field` to a TA (5 marks).
#### In-lab marking: You need to explain how to compute the weight for each particle in `particle.py -> calculateParticleWeight` to a TA (5 marks).
#### In-lab marking: Show the particle filter to a TA to score the marks associated to this part. You need to show the particle filter pose estimation in Rviz while robot is moving around via keyboard. (10 marks)


## Part 5 - Integration to the stack (10 marks)
Now you need to run the point controller developed in LAB #2 with particle filter in the loop:
- Integrate the particle filter into your localization model, ```localization.py```;
- Design the proper flow; follow the comments in ```decisions.py```;
- Test your navigation stack with particle filter in the loop as following,
  - Place the robot in the map where you run the SLAM, **try your best to align the robot with the marker**, and reset the odometry.
  - Run the following commands:
  ```
  # terminal 1
  python3 particleFilter.py
  # terminal 2
  rviz2 -d for_pf.rviz
  # terminal 3
  python3 decisions.py
  ``` 
  - When the Rviz window opened throw a good guess by using ```2D pose estimate``` button in the top toolbar.
  - When the particles converged, choose your goal using ```2D Goal Pose``` button in the top toolbar.
- Remember to **save the robotPose.csv file for the report**.
#### In-lab marking: You need to show the particle filter pose estimation in Rviz and the robot moving to the goal via the point controller. (10 marks)
**IMPORTANT!! Before you leave, DELETE all of your codes, files, etc.**

## Part 6 - Experiments for the report
### Part 6.1 - Comparison between the particle filter and the rawSensor method
In addition to the robotPose.csv saved in the Part 5, you should try to **place the robot with some deviation from the marker** and then **reset the odometry** and run the particle filter.
```
# terminal 1
python3 particleFilter.py
# terminal 2
rviz2 -d for_pf.rviz
# terminal 3
python3 decisions.py
``` 

- Remember to **save the robotPose.csv file for the report**.

### Part 6.2 - Performance comparison by changing the laser scan deviation
In addtion to the robotPose.csv saved in the Part 5, you should try to **change the laser scan deviation (laser_sig)** in the particleFilter.py `self.mapUtilities = mapManipulator(mapFilename, laser_sig=0.1)` and then **reset the odometry** and run the particle filter.

**Try your best to align the robot with the marker** and then **reset the odometry** and run the particle filter.

- Remember to **save the robotPose.csv file for the report**.


## Conclusions - Written report (25 marks)
You can do this part in the lab (time allowing) or at home. Make sure you have the proper data saved.

Please prepare a written report containing in the front page:
- Names (Family Name, First Name) of all group members;
- Student ID of all group members;
- Station number and robot number.

In a maximum of 3 pages (excluding the front page), report a comparison between the particle filter and the rawSensor (odom) method:

* Section 1 - the plots of the logged positions (x, y) from the particle filter versus the odometry for Part5, Part6.1, and Part6.2 (ploting x in axis and y in y axis).
* Section 2 - the plots of the logged positions (theta) from the particle filter versus the odometry for Part5, Part6.1, and Part6.2 (ploting time in axis and theta in y axis).
* Section 3 - discussion between the particle filter and the rawSensor method in the light of the plots.
* Section 4 - discussion for the performance comparison by changing the laser scan deviation.

**NOTE: Make sure plots have title, label name for axis, legends, different shapes/colors for each data, and grids.**

## Submission

Submit the report and the code on Dropbox (LEARN) in the corresponding folder. Only one submission per group is needed:
- **Report**: one single pdf;
- **Code**: make sure to have commented your code! Submit one single zip file with everything (including the csv files obtained from the data log).


Good luck!
