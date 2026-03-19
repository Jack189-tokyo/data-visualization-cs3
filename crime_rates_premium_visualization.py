import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec

# 设置高质量样式
plt.rcParams['font.family'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['figure.facecolor'] = 'white'

# 读取数据
df = pd.read_csv('./crimeRatesByState2005.csv')
df_states = df[df['state'] != 'United States'].copy()

# 犯罪类型
crime_types = ['murder', 'forcible_rape', 'robbery', 'aggravated_assault', 
               'burglary', 'larceny_theft', 'motor_vehicle_theft']

crime_names = ['谋杀', '强奸', '抢劫', '严重攻击', '入室盗窃', '盗窃', '车辆盗窃']

# 高质量配色方案
colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E', '#BC4749', '#F4A261']

# 计算布局
num_states = len(df_states)
cols = 8  # 8列布局
rows = (num_states + cols - 1) // cols

# 创建大图 - 调整间距，增大饼图
fig = plt.figure(figsize=(32, 18))
gs = GridSpec(rows, cols, figure=fig, 
              hspace=0.15, wspace=0.02,  # 增加垂直间距
              top=0.92, bottom=0.12, left=0.005, right=0.995)  # 扩大边距

# 主标题
fig.suptitle('2005年美国各州犯罪率分布', 
            fontsize=20, fontweight='bold', y=0.96, 
            color='#2C3E50')

# 为每个州创建饼图
for idx, (index, row) in enumerate(df_states.iterrows()):
    row_idx = idx // cols  # 从第0行开始
    col_idx = idx % cols
    
    ax = fig.add_subplot(gs[row_idx, col_idx])
    
    # 获取犯罪率数据
    crime_rates = row[crime_types].values
    total_crime_rate = np.sum(crime_rates)
    
    # 创建饼图 - 增大饼图，移除百分比
    wedges, texts = ax.pie(crime_rates, 
                          colors=colors,
                          autopct=None,  # 移除百分比
                          startangle=90,
                          radius=1.3)  # 增大饼图半径
    
    # 在饼图中央添加州名 - 用圆润矩形框住
    bbox_props = dict(boxstyle="round,pad=0.3", facecolor='white', 
                     edgecolor='#2C3E50', linewidth=1.5, alpha=0.9)
    ax.text(0, 0, f'{row["state"]}', 
            ha='center', va='center', 
            fontsize=11, fontweight='bold', color='#2C3E50',
            bbox=bbox_props)

# 创建图例元素
legend_elements = []
for i, (crime_name, color) in enumerate(zip(crime_names, colors)):
    legend_elements.append(plt.Rectangle((0, 0), 1, 1, fc=color, label=crime_name))

# 添加图例到底部 - 一行横向排列
fig.legend(handles=legend_elements, 
          loc='lower center', 
          bbox_to_anchor=(0.5, 0.02), 
          ncol=len(crime_names), 
          fontsize=13, 
          title='犯罪类型',
          title_fontsize=14,
          frameon=True,
          edgecolor='#333333',
          facecolor='#F8F8F8',
          columnspacing=1.8,
          handletextpad=0.8,
          borderpad=0.8)

# 保存图片
plt.savefig('crime_rates_by_state_2005_premium.png', 
            dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none',
            pad_inches=0.5)

plt.show()

print(f"已生成 {num_states} 个州的高质量犯罪率饼图")
print("图片已保存为 'crime_rates_by_state_2005_premium.png'")

# 生成详细统计报告
print("\n" + "="*60)
print("2005年美国各州犯罪率统计报告")
print("="*60)

for i, crime_type in enumerate(crime_types):
    data = df_states[crime_type]
    mean_rate = data.mean()
    median_rate = data.median()
    max_state = df_states.loc[data.idxmax(), 'state']
    max_rate = data.max()
    min_state = df_states.loc[data.idxmin(), 'state']
    min_rate = data.min()
    
    print(f"\n{crime_names[i]}:")
    print(f"  平均值: {mean_rate:.2f}")
    print(f"  中位数: {median_rate:.2f}")
    print(f"  最高: {max_state} ({max_rate:.2f})")
    print(f"  最低: {min_state} ({min_rate:.2f})")

print(f"\n总体统计:")
print(f"  平均总犯罪率: {df_states[crime_types].sum(axis=1).mean():.1f}")
print(f"  最高总犯罪率: {df_states.loc[df_states[crime_types].sum(axis=1).idxmax(), 'state']} ({df_states[crime_types].sum(axis=1).max():.1f})")
print(f"  最低总犯罪率: {df_states.loc[df_states[crime_types].sum(axis=1).idxmin(), 'state']} ({df_states[crime_types].sum(axis=1).min():.1f})")
