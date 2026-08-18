 
### ROS2 策略推理节点示例

通过 ROS2 话题通信（`/robot_obs` 订阅观测，`/robot_action` 发布动作）将强化学习策略接入机器人控制流。

**运行方式**（需已安装 ROS2）：
```bash
# 先编译工作空间（略）
ros2 run your_package policy_node.py