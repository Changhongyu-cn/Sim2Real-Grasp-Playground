import gymnasium as gym
from stable_baselines3 import SAC
from stable_baselines3.common.callbacks import CheckpointCallback
import torch
import numpy as np
from ur5_env import  UR5RobotiqEnv

# 1. 创建环境（这里需要换成你真正的 UR5 环境类名）
# 注意：你需要在 main_rl.py 中搜索 “gym.make(” 并查看具体环境名
# 例如：env = gym.make("UR5GraspEnv-v0")
# 如果找不到，请把你 main_rl.py 中创建环境的代码行告诉我
env = UR5RobotiqEnv()  # ← 请替换为你的真实环境名称

# 2. 定义模型（使用 MLP 策略）
model = SAC("MlpPolicy", env, verbose=1)

# 3. 设置 checkpoint 回调（每 1000 步保存一次）
checkpoint_callback = CheckpointCallback(save_freq=1000, save_path="./models", name_prefix="ur_robot_sac")

# 4. 开始训练（总步数可以先设少一点用于测试，比如 10000）
model.learn(total_timesteps=10000, callback=checkpoint_callback)

# 5. 保存最终模型
model.save("ur_robot_sac_final")

# 6. 导出 TorchScript 模型（供 C++ 调用）
obs_dim = env.observation_space.shape[0]
dummy_input = torch.randn(1, obs_dim)
model.policy.eval()
traced_policy = torch.jit.trace(lambda x: model.policy(x).mode, dummy_input)
traced_policy.save("ur5_policy_traced.pt")
print("✅ TorchScript 模型已导出为 ur5_policy_traced.pt")

# 7. 关闭环境
env.close()