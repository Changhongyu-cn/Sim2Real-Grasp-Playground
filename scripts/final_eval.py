import sys
import os

# 获取当前脚本所在的目录（scripts/）
script_dir = os.path.dirname(os.path.abspath(__file__))
# 项目根目录是 scripts/ 的上一级
project_root = os.path.dirname(script_dir)

# 把项目根目录加入模块搜索路径
sys.path.insert(0, project_root)

from ur5_env import UR5RobotiqEnv
from stable_baselines3 import SAC
import numpy as np

# 用绝对路径加载模型
model_path = os.path.join(project_root, 'models', 'ur_robot_sac_14000_steps')
model = SAC.load(model_path)

success = 0
n = 100

for ep in range(n):
    env = UR5RobotiqEnv()
    obs, _ = env.reset()
    done = False
    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
    if reward > 0:
        success += 1
    env.close()

print(f"📊 正式评估结果 (n={n}): {success/n*100:.1f}%")