 
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import torch
import numpy as np

class PolicyNode(Node):
    def __init__(self):
        super().__init__('ur5_policy_node')
        # 订阅观测话题（仿真/真机发来的状态）
        self.subscription = self.create_subscription(
            Float32MultiArray,
            '/robot_obs',
            self.obs_callback,
            10)
        # 发布动作话题
        self.publisher = self.create_publisher(
            Float32MultiArray,
            '/robot_action',
            10)

        self.get_logger().info('ROS2 Policy Node 已启动，等待观测数据...')
        self.model = None
        try:
            # 加载模型（注意：路径相对于启动位置，可能需要调整）
            self.model = torch.jit.load("../ur5_policy_traced.pt")
            self.model.eval()
            self.get_logger().info('✅ 模型加载成功！')
        except Exception as e:
            self.get_logger().error(f'模型加载失败: {e}')

    def obs_callback(self, msg):
        if self.model is None:
            return
        # 转换观测并推理
        obs = torch.tensor(np.array(msg.data)).float().unsqueeze(0)
        with torch.no_grad():
            action_tensor = self.model(obs)
        # 发布动作
        action_msg = Float32MultiArray()
        action_msg.data = action_tensor.squeeze().tolist()
        self.publisher.publish(action_msg)
        self.get_logger().info('✅ 已发布动作指令')

def main(args=None):
    rclpy.init(args=args)
    node = PolicyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()