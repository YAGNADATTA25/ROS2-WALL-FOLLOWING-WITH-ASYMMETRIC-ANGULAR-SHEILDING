#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import numpy as np

class WallFollow(Node):
    def __init__(self):
        super().__init__("Wall_Follow")
        
        # Target 1.0 meter tracking gap configuration (Your original perfect bounds)
        self.min_distance_to_wall = 0.90
        self.max_distance_to_wall = 1.10
        
        # Front emergency threshold (Strictly for standalone static obstacles)
        self.obstacle_threshold = 0.50
        
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.listener_callback,
            10)
        
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info("🚀 ANGULAR SHIELDING ENGAGED - WALL IS NO LONGER AN OBSTACLE")
    
    def clean_ranges(self, ranges):
        """Filters out out-of-bounds readings and self-reflections."""
        clean = np.array(ranges)
        clean[np.isnan(clean) | np.isinf(clean) | (clean <= 0.32)] = 3.5
        return clean.tolist()

    def listener_callback(self, msg):
        self.twist_msg = Twist()
        
        ranges = self.clean_ranges(msg.ranges)
        num_readings = len(ranges)
        if num_readings == 0:
            return

        # =========================================================================
        # RE-ENGINEERED SENSORY WINDOWS WITH ANGULAR SHIELDING
        # =========================================================================
        
        # ZONE A: Front Obstacle Window shifted to the RIGHT (335 to 10 degrees)
        # This completely blinds the front-left quadrant from triggering obstacle warnings on the wall.
        idx_10 = int(num_readings * 10 / 360)
        idx_335 = int(num_readings * 335 / 360)
        front_wall_min_distance = min(min(ranges[0:idx_10]), min(ranges[idx_335:num_readings]))
        
        # ZONE B: Your exact perfect Left Flank Wall Follow Window (10 to 40 degrees)
        idx_wall_start = int(num_readings * 10 / 360)
        idx_wall_end = int(num_readings * 40 / 360)
        left_wall_min_distance = min(ranges[idx_wall_start:idx_wall_end])
            
        # =========================================================================
        # INDEPENDENT LIVE RADAR TEXT LOGIC
        # =========================================================================
        if front_wall_min_distance < self.obstacle_threshold:
            obstacle_log = f"⚠️ [TRUE OBSTACLE AHEAD AT {front_wall_min_distance:.2f}m!]"
        else:
            obstacle_log = "🟩 [FRONT PATH CLEAR]"

        # =========================================================================
        # DECISION ARBITRATION MATRIX
        # =========================================================================
        active_mode = "FORWARD"

        # 1. DEDICATED CRITICAL OBSTACLE AVOIDANCE LAYER
        if front_wall_min_distance < self.obstacle_threshold:
            self.twist_msg.linear.x = 0.02
            self.twist_msg.angular.z = -0.70  # Clean right pivot away from standalone blocking objects
            active_mode = "AVOIDING_OBSTACLE"
            
        # 2. SEPARATE LEFT WALL TRACKING ALGORITHM LAYER
        elif left_wall_min_distance > self.max_distance_to_wall:
            # Turn Left towards the wall if it drifts too far out
            self.twist_msg.linear.x = 0.12
            self.twist_msg.angular.z = 0.35
            active_mode = "AVOIDING_OBSTACLE"
            
        elif left_wall_min_distance < self.min_distance_to_wall:
            # Turn Right away from the wall if it edges too close
            self.twist_msg.linear.x = 0.12
            self.twist_msg.angular.z = -0.35
            active_mode = "ADJUSTING_RIGHT"
            
        else:
            # Maintain steady forward cruise speed matching your original logic bounds
            self.twist_msg.linear.x = 0.18
            self.twist_msg.angular.z = 0.0
            active_mode = "TRACKING_PERFECTLY"
                    
        # Ground unhandled non-planar dimensions
        self.twist_msg.linear.y = 0.0
        self.twist_msg.linear.z = 0.0
        self.twist_msg.angular.x = 0.0
        self.twist_msg.angular.y = 0.0
        
        self.publisher_.publish(self.twist_msg)

        # --- LIVE TERMINAL FEEDBACK CHANNEL ---
        print(f"{obstacle_log} | Left Wall Dist: {left_wall_min_distance:.2f}m | Steering Action: {active_mode}")

def main():
    rclpy.init()
    node = WallFollow()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
