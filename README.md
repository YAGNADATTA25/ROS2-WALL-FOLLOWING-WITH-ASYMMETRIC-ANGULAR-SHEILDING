
### `ROS2-WALL-FOLLOWING-WITH-ASYMMETRIC-ANGULAR-SHEILDING`

```markdown
# ROS 2 Wall-Following Navigation: Asymmetric Angular Shielding & Reactive Control

![ROS 2 Humble](https://img.shields.io/badge/ROS_2-Humble-blue.svg)
![C++17](https://img.shields.io/badge/Language-C%2B%2B17-green.svg)
![Python 3.10](https://img.shields.io/badge/Language-Python_3.10-yellow.svg)
![Gazebo Simulator](https://img.shields.io/badge/Simulator-Gazebo_Classic-orange.svg)
![License](https://img.shields.io/badge/License-Apache_2.0-red.svg)

A high-performance ROS 2 reactive navigation architecture engineered for mobile robots navigating structured corridor and wall environments[cite: 1]. The system decouples raw 2D LiDAR range processing into asymmetric angular safety sectors, enabling smooth wall alignment, proactive cornering, and instantaneous emergency obstacle clearance without reliance on high-level navigation costmaps[cite: 1].

```

---

## 🏗 System Architecture & Closed-Loop Control Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     Target Platform / Gazebo Sim                        │
│             (TurtleBot3 Waffle Pi / Differential Drive Base)            │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ Topic: /scan (sensor_msgs/msg/LaserScan)
┌────────────────────────────────────▼────────────────────────────────────┐
│                    LiDAR Perception & Polar Processing                  │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ 2D LaserScan Range Filter (Inf/NaN Filtering + Outlier Rejection)│  │
│  │ Asymmetric Angular Ray Partitioning:                              │  │
│  │   ├─ Front Critical Zone (-15° to +15°)                           │  │
│  │   ├─ Front-Left / Front-Right Asymmetric Shield Sectors         │  │
│  │   └─ Lateral Wall Alignment Vector (90° Parallel Offset)          │  │
│  └─────────────────────────────────┬─────────────────────────────────┘  │
└────────────────────────────────────┼────────────────────────────────────┘
                                     │ Filtered Distance & Error Signals
┌────────────────────────────────────▼────────────────────────────────────┐
│               Asymmetric Reactive Safety & Controller Node              │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ Closed-Loop Distance Error Evaluator: \(e(t) = d_{\text{target}} - d_{\text{measured}}\) │
│  │ Dynamic Velocity Scaling & Turn Rate Saturation Engine            │  │
│  │ Asymmetric Shield Safety Override (Emergency Angular Pivot)      │  │
│  └─────────────────────────────────┬─────────────────────────────────┘  │
└────────────────────────────────────┼────────────────────────────────────┘
                                     │ Topic: /cmd_vel (geometry_msgs/msg/Twist)
┌────────────────────────────────────▼────────────────────────────────────┐
│                       Robot Hardware / Motor Actuators                  │
└─────────────────────────────────────────────────────────────────────────┘

```

---

## 🔑 Key Engineering & R&D Highlights

* **Asymmetric Angular Safety Shielding:** Evaluates non-symmetric LiDAR angular sectors (e.g., front-left vs. front-right clearance) to dynamically bias rotational maneuvers toward safe open space during sharp corridor corners and narrow transitions.


* **Low-Latency Perception Pipeline:** Filters raw `sensor_msgs/msg/LaserScan` arrays in real time, handling sensor noise, invalid readings (`inf`/`nan`), and ray-angle index mapping dynamically across varying LiDAR field-of-view (FOV) configurations.


* **Closed-Loop Wall Distance Regulation:** Implements a feedback controller that continuously calculates lateral cross-track distance errors and heading angles relative to parallel wall surfaces, driving cross-track error to zero.


* **Dynamic Velocity Scaling:** Automatically reduces linear speed $v_x$ as heading error or lateral deviation increases, preventing overshoot and mechanical instability during aggressive turn corrections.


* **Emergency Reactive Recovery Loop:** Intercepts standard wall-following commands to execute rapid in-place rotation or obstacle avoidance when objects enter the immediate front safety envelope.



---

## 📊 Technical Parameters & Control Matrix

| Control Parameter / Metric | Value | Description |
| --- | --- | --- |
| **ROS 2 Middleware** | Humble Hawksbill | Target LTS Framework |
| **Target Wall Distance ($d_{\text{target}}$)** | `0.5 m` (Configurable) | Desired lateral clearance offset |
| **Front Safety Envelope** | `0.4 m` Threshold | Immediate collision avoidance trigger |
| **Control Loop Frequency** | 20 Hz (50 ms cycle) | Low-latency reactive control loop |
| **Asymmetric Shield Angles** | Custom FOV Partitions | Angle-weighted sector ray filtering |
| **Execution Nodes** | `rclcpp` / `rclpy` | C++ / Python ROS 2 Node Architecture |

---

## 💻 Tech Stack & Interfaces

* **Middleware:** ROS 2 Humble Hawksbill
* **Programming Languages:** C++17, Python 3.10
* **ROS 2 Interface Types:** `sensor_msgs/msg/LaserScan`, `geometry_msgs/msg/Twist`, `nav_msgs/msg/Odometry`
* **Simulation Target:** Gazebo Classic 11 / TurtleBot3 Waffle Pi

---

## 🚀 Build & Execution Guide

### Prerequisites

Ensure ROS 2 Humble and Gazebo Classic are installed on Ubuntu 22.04 LTS.

```bash
# 1. Clone the repository into your ROS 2 workspace
cd ~/ros2_ws/src
git clone [https://github.com/YAGNADATTA25/ROS2-WALL-FOLLOWING-WITH-ASYMMETRIC-ANGULAR-SHEILDING.git](https://github.com/YAGNADATTA25/ROS2-WALL-FOLLOWING-WITH-ASYMMETRIC-ANGULAR-SHEILDING.git)

# 2. Install workspace dependencies
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y

# 3. Build and source workspace
colcon build --symlink-install --packages-select wall_following
source install/setup.bash

# 4. Launch Simulation Environment & Wall Follower Node
ros2 launch wall_following wall_following.launch.py

```

---

