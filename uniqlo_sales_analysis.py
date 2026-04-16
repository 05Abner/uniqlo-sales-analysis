import pandas as pd
import sqlite3

df = pd.read_excel("优衣库销售数据.xlsx", engine='openpyxl')
print(df.head())
print("数据形状（行，列）：", df.shape) # 数据大小
print("\n所有字段:")
print(df.columns.tolist()) # 列名
print("\n数据信息：")
print(df.info()) # 数据类型和缺失值
print("\n前十行：")
print(df.head(10))
print("\n每列缺失值数量：") # 缺失值
print(df.isnull().sum())
print("\n重复行数：", df.duplicated().sum()) #重复数据
print()

# 数据清洗
print("数据清洗开始：")
# 1. 删除重复行
df = df.drop_duplicates()
# 2. 删除含缺失值的行
df = df.dropna()
print("清洗后数据形状（行，列）：", df.shape)  # 显示清洗后有多少行多少列
print("清洗后缺失值总数：", df.isnull().sum().sum())  # 确认缺失值全清掉
print("清洗后重复行数：", df.duplicated().sum())  # 确认重复行全删
# 提取月份
df["订单日期"] = pd.to_datetime(df["订单日期"], errors='coerce')
df["月份"] = df["订单日期"].dt.month
#创建数据库连接，将清洗后的数据存入SQLite
conn = sqlite3.connect("uniqlo_sales.db")
df.to_sql("sales_data", conn, if_exists="replace", index=False)
# 用SQL查询数据
df = pd.read_sql("SELECT * FROM sales_data", conn)
df.to_excel("优衣库_清洗后数据.xlsx", index=False, engine="openpyxl")
print("数据清洗结束")
print()
# 基础统计分析
print("基础统计分析")
# 1. 整体业绩：总销售、总利润、总订单
print("【整体业绩】")
print("总销售金额：", round(df["销售金额"].sum(), 2))
print("总利润：", round(df["利润"].sum(), 2))
print("总订单数：", df["订单数量"].sum())
print("总客户数：", df["客户数量"].sum())

# 2. 各城市销售排行
print("\n【城市销售排行】")
city_sale = df.groupby("门店所在城市")["销售金额"].sum().sort_values(ascending=False)
print(city_sale)

# 3. 渠道对比（线上 / 线下）
print("\n【渠道销售对比】")
channel_sale = df.groupby("渠道")["销售金额"].sum()
print(channel_sale)

# 4. 产品类别销量
print("\n【产品类别销售】")
cate_sale = df.groupby("产品类别")["销售金额"].sum().sort_values(ascending=False)
print(cate_sale)

# 5. 性别群体消费
print("\n【性别群体消费】")
gender_sale = df.groupby("性别群体")["销售金额"].sum()
print(gender_sale)

# 6. 年龄群体消费
print("\n【年龄群体消费】")
age_sale = df.groupby("年龄群体")["销售金额"].sum()
print(age_sale)
print()
print("时间维度分析")
# 时间维度分析（按星期/日期统计）
# 按星期统计销售额
print("【星期销售排行】")
week_sale = df.groupby("星期")["销售金额"].sum().sort_values(ascending=False)
print(week_sale)
# 按月份统计销售额
print("\n【月度销售趋势】")
month_sale = df.groupby("月份")["销售金额"].sum()
print(month_sale)
print()
#数据可视化
import matplotlib.pyplot as plt
# 设置中文显示
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
#1. 城市销售柱状图
plt.figure(figsize=(8, 4))
city_sale.plot(kind="bar", color="skyblue")
plt.title("各城市销售额排行")
plt.ylabel("销售金额")
plt.tight_layout()
plt.savefig("各城市销售额排行.png", dpi=300, bbox_inches='tight')
plt.show()
# 2. 产品类别销售柱状图
plt.figure(figsize=(10, 4))
cate_sale.plot(kind="bar", color="orange")
plt.title("产品类别销售额排行")
plt.ylabel("销售金额")
plt.tight_layout()
plt.savefig("产品类别销售额排行.png", dpi=300, bbox_inches='tight')
plt.show()
# 3. 月度销售趋势图
plt.figure(figsize=(8, 4))
month_sale.plot(kind="line", marker="o", color="green")
plt.title("月度销售趋势")
plt.ylabel("销售金额")
plt.tight_layout()
plt.savefig("月度销售趋势.png", dpi=300, bbox_inches='tight')
plt.show()
# 4. 性别群体销售柱状图
plt.figure(figsize=(6, 4))
gender_sale.plot(kind="bar", color="pink")
plt.title("性别群体销售额对比")
plt.ylabel("销售金额")
plt.tight_layout()
plt.savefig("性别群体销售额对比.png", dpi=300, bbox_inches='tight')
plt.show()
# 5. 年龄群体销售柱状图
plt.figure(figsize=(10, 4))
age_sale.plot(kind="bar", color="purple")
plt.title("年龄群体销售额排行")
plt.ylabel("销售金额")
plt.tight_layout()
plt.savefig("年龄群体销售额排行.png", dpi=300, bbox_inches='tight')
plt.show()
print()
# 优衣库销售数据分析

print("优衣库基础销售数据分析")
print("整体概况：总销售额 322,105.03 元，总利润 147,242.03 元，毛利率约 45.7%")

print("城市结构：深圳一家独大，贡献 53.7% 销售额(17.3万)，为杭州2.8倍、西安5.7倍，区域极度不均衡")
print("品类结构：T恤垄断 41.6% 销售额(13.4万)，为绝对核心；配件排名第3，销售额 47,141.18 元(14.6%)，具备高连带潜力")
print("用户结构：女性占比 71.2%，消费力为男性2.5倍；30-34岁客群最强(25.3%)，25-39岁合计占70.8%")
print("时间规律：8月单月贡献63%销售额，呈年度爆发；周五占周销22.1%，周三仅1.6%，周内差异极其显著")
print("渠道结构：100%线下销售，渠道单一，线上存在拓展空间")
# 基于 Excel 交叉透视表的深度洞察
print("\n基于 Excel交叉透视表的分析")
# 产品类别 × 城市（销售金额）
print("1. 产品类别 × 城市交叉分析：")
print("• 深圳全品类销售额均为四城最高，T恤 65,842.47 元占深圳总业绩38%，为核心驱动力；")
print("• 深圳配件占本市销售额15.8%，为四城最高，组合销售潜力最优；")
print("• 杭州、重庆品类结构均衡，但整体规模仅为深圳1/3左右；")
print("• 西安全品类均偏弱，无强势品类，区域整体购买力不足。")
# 2. 性别 × 年龄（客户数量）—— 完全精准修正！
print("2. 性别 × 年龄交叉分析：")
print("• 女性客户占70.8%，核心集中在 20–39 岁全年龄段；")
print("• 女性峰值在 30–34 岁(683人)，其次35–39岁(440人)、25–29岁(435人)，是绝对消费主力；")
print("• 男性客户占29.2%，主力均匀分布在20–34岁，各年龄段人数接近；")
print("• 整体客群以中青年为主，20–39岁是品牌最核心人群。")
# 3. 月份 × 产品类别（销售金额）
print("3. 月份 × 产品类别交叉分析：")
print("• 8 月爆发完全依靠 T恤(90888.46)+配件(23210.6)+当季新品(32936.06)；")
print("• 淡季(1-3月、11月)全品类同步下滑，无稳定防御品类；")
# 综合业务建议
print("\n综合业务建议")
print("1. 深圳为核心仓：优先保 T恤 库存，主推「T恤+配件」组合，放大搭配优势；")
print("2. 杭州、重庆维持均衡运营，重点提升配件连带率；")
print("3. 女性核心聚焦 30–39 岁，同时覆盖25–29、20–24岁全年龄段；")
print("4. 8月旺季提前备货 T恤、配件、当季新品；")
print("5. 西安以爆款T恤引流，搭配小件配件提升客单价。")

