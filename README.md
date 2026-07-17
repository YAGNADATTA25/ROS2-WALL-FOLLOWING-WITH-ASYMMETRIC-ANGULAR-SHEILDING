# ROS 2 Wall Following Package (`wall_following_project`)

A high-speed autonomous navigation package implemented within the ROS 2 Humble framework. This package utilizes a custom-engineered asymmetric LiDAR angular filtering model paired with a proportional feedback steering loop to achieve stable corridor traversal and wall-hugging for a differential drive mobile robot without grazing sharp corners or sidewall irregularities.

---

## Technical Approach & Control Architecture

The reactive control logic executes continuously across two main subsystems to calculate stable velocity commands:

*   **Asymmetric Angular Shielding:** Instead of processing a heavy symmetric 360^\circ laser rangefinder array, the parser slices the incoming `sensor_msgs/msg/LaserScan` topic into isolated tracking sectors. An aggressive filtering window isolates the front-to-sidewall profile . Sidelining environmental noise prevents false steering reactions caused by open spaces or sharp wall cutouts.
*   **Proportional Steering Controller:** The node derives the immediate lateral error distance ($e_{\text{dist}}$) between the geometric center of the robot and the targeted wall contour line.
*    streering adjustments are regulated dynamically through an optimized proportional feedback loop designed to mitigate high-frequency chassis oscillations.

---

## Repository Directory Structure

```text
wall_following_project/
├── CMakeLists.txt             # Colcon compilation properties
├── package.xml                # ROS 2 rclcpp, sensor_msgs, and geometry_msgs dependencies
├── README.md                  # System technical documentation
├── config/
│   └── wall_follower_params.yaml  # Tuned Kp steering gains and distance safety margins
├── launch/
│   └── wall_follow.launch.py  # Launches the tracker node and syncs runtime parameters
└── src/
    └── wall_follower_node.cpp # High-rate LaserScan parsing and steering command logic

Installation & Build Setup

Ensure your local system operates with ROS 2 Humble and your workspace environment is correctly configured. Clone this package directory straight into your src folder, resolve its dependencies via rosdep, and compile:
Bash

cd ~/turtlebot3_ws
rosdep update
rosdep install --from-paths src --ignore-src -r -y --rosdistro humble

colcon build --packages-select wall_following_project
source install/setup.bash

Execution Guidelines
1. Launch the Environment Simulation

Set your platform model environment variable and launch the tracking setup pipeline to spin up the Gazebo maze/corridor scene:
Bash

export TURTLEBOT3_MODEL=waffle_pi
ros2 launch wall_following_project wall_follow.launch.py

2. Trigger the Wall Follower Control Loop

In a secondary terminal window, activate the compiled C++ controller node to instantly begin high-frequency wall tracking and automated guidance:
Bash

source ~/turtlebot3_ws/install/setup.bash
ros2 run wall_following_project wall_follower_node
