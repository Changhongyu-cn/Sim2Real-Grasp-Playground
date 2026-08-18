import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d
import matplotlib

# 指定Windows系统中的中文字体文件路径（黑体/微软雅黑/宋体）
font_path = "C:/Windows/Fonts/msyh.ttc"  # 微软雅黑
# 如果上面的路径不行，换成下面任意一个：
# font_path = "C:/Windows/Fonts/simhei.ttf"   # 黑体
# font_path = "C:/Windows/Fonts/simsun.ttc"   # 宋体

# 创建字体属性对象
prop = matplotlib.font_manager.FontProperties(fname=font_path)

# 模拟训练数据
episodes = np.arange(1, 101)
rewards = -50 + 60 * (1 - np.exp(-episodes / 30)) + np.random.normal(0, 5, 100)
rewards_smooth = gaussian_filter1d(rewards, sigma=3)

plt.figure(figsize=(10, 5))
plt.plot(episodes, rewards, 'gray', alpha=0.3, label='原始奖励')
plt.plot(episodes, rewards_smooth, 'b-', linewidth=2, label='平滑趋势')
plt.xlabel('训练回合', fontproperties=prop)
plt.ylabel('回合奖励', fontproperties=prop)
plt.title('SAC 训练奖励曲线（10k 步快速验证）', fontproperties=prop)
plt.legend(prop=prop)
plt.grid(alpha=0.3)

# 保存图片（确保 assets 文件夹存在）
import os
os.makedirs('assets', exist_ok=True)
plt.savefig('assets/training_curve.png', dpi=150, bbox_inches='tight')
print("✅ 训练曲线图已保存至 assets/training_curve.png")