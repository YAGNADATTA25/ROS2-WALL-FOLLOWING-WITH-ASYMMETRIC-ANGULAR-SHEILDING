# ROS 2 Left-Flank Wall Follower with Angular Shielding

An autonomous navigation package developed in **ROS 2 Humble** for a TurtleBot3 mobile robot. The system utilizes real-time 360° LiDAR data to map sensory windows, execute robust left-wall tracking, and dodge standalone obstacles using a unique asymmetric angular shielding technique.

## 🚀 Key Engineering Highlights
* **Asymmetric Angular Shielding:** Bypasses the classic wall-following failure mode where a tracked wall bleeds into the front obstacle zone. By shifting the front window to $[335^\circ, 10^\circ]$, the robot completely blinds its front-left quadrant to the wall while remaining 100% reactive to dynamic threats ahead.
* **Deterministic Decision Arbitration:** Replaces unstable controller loops with a high-frequency, tiered state machine that prioritizes safety deceleration over tracking maneuvers.
* **Telemetry Monitoring Layer:** Pipes live operational modes directly to the console (`[TRUE OBSTACLE AHEAD]`, `[TRACKING_PERFECTLY]`) for real-time tracking performance auditing.

---

## 📊 System Architecture & Sensory Windows

The system splits incoming `sensor_msgs/msg/LaserScan` arrays into two decoupled, high-precision observation sectors:

```text
               [0° / 360°] Front
                   |
     [335°] .------|------. [10°]
           /       |       \
          /  ZONE A: FRONT  \
         /   OBSTACLE ZONE   \
        |                     |
 [40°]  |                     |
   \    |                     |
    \   |                     |
  ZONE B:                     |
  LEFT WALL                   |
  TRACKING                    |
        |                     |
        |                     |
                   |
                 [180°]

𝔐 Decision Arbitration LogicData Sanitization: Out-of-bounds metrics, infinite metrics, and robot frame self-reflections ($d \le 0.32\text{m}$) are flattened to $3.5\text{m}$ to prevent erroneous state jumps.Zone A evaluation (Obstacle Override):$$d_{\text{front}} = \min\left(\text{ranges}[0^\circ \to 10^\circ], \text{ranges}[335^\circ \to 360^\circ]\right)$$If $d_{\text{front}} < 0.50\text{m} \implies$ State: AVOIDING_OBSTACLE ($v_x = 0.02\text{m/s}, \omega_z = -0.70\text{rad/s}$).Zone B evaluation (Wall Tracking):$$d_{\text{left}} = \min\left(\text{ranges}[10^\circ \to 40^\circ]\right)$$If $d_{\text{left}} > 1.10\text{m} \implies$ State: AVOIDING_OBSTACLE (Drifting away; correct left).If $d_{\text{left}} < 0.90\text{m} \implies$ State: ADJUSTING_RIGHT (Too close; bank right).Else $\implies$ State: TRACKING_PERFECTLY ($v_x = 0.18\text{m/s}, \omega_z = 0.0\text{rad/s}$).
