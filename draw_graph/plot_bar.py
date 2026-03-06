import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']  # 简体中文
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

# 创建数据
cell_types = ['CD4 + T细胞', 'CD8 + T细胞']
total_targets = [30, 45]
developed_targets = [17, 21]
developed_percent = [57, 46]
undeveloped_targets = [total - developed for total, developed in zip(total_targets, developed_targets)]

# 创建图表 - 调整宽度使柱子更窄
fig, ax = plt.subplots(figsize=(8, 8))

# 设置柱子位置和宽度 - 柱子间距减小
x = np.array([0, 1])  # 柱子中心位置
width = 0.4  # 柱子宽度
spacing = width  # 柱子间距等于柱子宽度

# 绘制柱状图
# 已研发靶点部分
ax.bar(x, developed_targets, width=width, 
       color='lightgray', edgecolor='none', linewidth=0)

# 未研发靶点部分
ax.bar(x, undeveloped_targets, width=width, bottom=developed_targets,
       color='white', edgecolor='none', linewidth=0)

# 为整个柱子添加黑框（已研发+未研发）
for i in range(len(x)):
    # 整个柱子的黑框
    rect = patches.Rectangle(
        (x[i] - width/2, 0),  # (x, y) 左下角坐标
        width,  # 宽度
        total_targets[i],  # 高度
        linewidth=1.5, 
        edgecolor='black', 
        facecolor='none'
    )
    ax.add_patch(rect)
    
    # 已研发部分标签
    ax.text(
        x[i], developed_targets[i]/2, 
        f"{developed_targets[i]} ({developed_percent[i]}%)", 
        ha='center', va='center', 
        color='black', fontsize=12, fontweight='bold'
    )
    
    # 总计标签（柱子顶部）
    ax.text(
        x[i], total_targets[i] + 1, 
        f"总计: {total_targets[i]}", 
        ha='center', va='bottom', 
        fontsize=12, fontweight='bold'
    )

# 设置x轴和y轴
ax.set_xlim(-0.6, 1.6)  # 扩大x轴范围以容纳柱子
ax.set_ylim(0, max(total_targets) * 1.25)  # y轴范围
ax.set_ylabel('靶点数量', fontsize=14)

# 隐藏x轴的默认刻度和标签
ax.set_xticks([])

# 在柱子下方添加类别标签
for i, cell_type in enumerate(cell_types):
    ax.text(
        x[i], -max(total_targets)*0.05, 
        cell_type, 
        ha='center', va='top', fontsize=12
    )

# 添加标题
ax.set_title('T细胞靶点研发情况分析 (2025)', fontsize=16, pad=20)

# 添加图例
from matplotlib.lines import Line2D
legend_elements = [
    patches.Patch(facecolor='lightgray', edgecolor='black', label='在研/上市靶点'),
    patches.Patch(facecolor='white', edgecolor='black', label='未研发靶点'),
]
ax.legend(handles=legend_elements, loc='upper right', frameon=True)

# 添加网格线
ax.grid(axis='y', alpha=0.3, linestyle='--')

# 调整布局并保存
plt.tight_layout()
plt.savefig('T细胞靶点研发情况.png', dpi=300, bbox_inches='tight')

print("图表已保存为 'T细胞靶点研发情况.png'")