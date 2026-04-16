# Dr Octopus - Build & Deploy

## Prerequisites

- Ubuntu 22.04
- ROS2 Humble (`sudo apt install ros-humble-desktop`)
- Joint State Publisher GUI (`sudo apt install ros-humble-joint-state-publisher-gui`)

## Build

```bash
cd dr_octopus_ws
source /opt/ros/humble/setup.bash
colcon build
```

## Launch

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch dr_octopus_description view.launch.py
```

RViz will open with dual arms and `joint_state_publisher_gui` providing 20 slider bars (9 revolute + 1 gripper per arm).

## Robot Description

**Dr Octopus** is a dual 9-DOF mechanical tentacle system based on OpenArmX kinematics, extended with an L-linkage (J3', J4') between J2 and J3.

### Kinematic Chain (per arm)

```
base_link → link0 → J1 → link1 → J2 → link2
  → J3' → link3_prime → J4' → link4_prime
  → J3 → link3 → J4 → link4
  → J5 → link5 → J6 → link6 → J7 → link7
  → hand → finger_joint1 (prismatic) → right_finger
         → finger_joint2 (prismatic, mimic) → left_finger
```

### Joint Naming Convention

| Joint | Type | Description |
|-------|------|-------------|
| `r_joint1` / `l_joint1` | revolute | Shoulder twist |
| `r_joint2` / `l_joint2` | revolute | Shoulder pitch |
| `r_joint3_prime` / `l_joint3_prime` | revolute | L-linkage twist |
| `r_joint4_prime` / `l_joint4_prime` | revolute | L-linkage elbow |
| `r_joint3` / `l_joint3` | revolute | Upper arm twist |
| `r_joint4` / `l_joint4` | revolute | Elbow |
| `r_joint5` / `l_joint5` | revolute | Forearm twist |
| `r_joint6` / `l_joint6` | revolute | Wrist pitch |
| `r_joint7` / `l_joint7` | revolute | Wrist roll |
| `r_finger_joint1` / `l_finger_joint1` | prismatic | Gripper |

### Directory Structure

```
dr_octopus_ws/
├── src/dr_octopus_description/   # ROS2 package
│   ├── urdf/dr_octopus.urdf      # Dual-arm URDF
│   ├── meshes/                   # DAE (visual) + STL (collision)
│   ├── launch/view.launch.py
│   └── rviz/view.rviz
├── urdf/dr_octopus_dual.urdf     # URDF source backup
└── .deprecated/                  # Legacy iteration artifacts
```
