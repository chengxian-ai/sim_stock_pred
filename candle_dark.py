import warnings
warnings.filterwarnings("ignore")
import os
os.environ['MPLBACKEND'] = 'Agg'  # 确保无 GUI
import matplotlib
matplotlib.use('Agg')
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt
import pandas as pd
import argparse
# import os
import pdb
import random
import time
import requests

import matplotlib.patches as patches

from tools import moving_average_filter, calculate_bollinger_bands, calculate_macd, calculate_rsi, calculate_mfi

def custom_candlestick(ax, df, special_dates, g_color='red', s_color='green', bg_color='#d3d3d3', linewidth=1.0):
    # up&down -- solid&hollow
    # G&S -- color:[red&green]
    for i, row in df.iterrows():
        date = i.strftime('%Y-%m-%d')
        # print(date)
        fill = True if row['Open'] >= row['Close'] else False
        alpha = 1.0
        if date in special_dates:
            # color = g_color
            facecolor = g_color if fill else bg_color
            edgecolor = g_color
            linewidth = linewidth
        else:
            # color = s_color
            facecolor = s_color if fill else bg_color
            edgecolor = s_color
            linewidth = linewidth
            # continue
        # 绘制蜡烛
        date_index = df.index.get_loc(i)
        # print(f'i:{i}, date_index:{date_index}')
        h = abs(row['Close'] - row['Open'])
        h1 = row['High'] - max(row['Open'], row['Close'])
        h2 = min(row['Open'], row['Close']) - row['Low']
        delta = 0.01
        # rm
        rm_rect = patches.Rectangle(
            (date_index - 0.2 - delta, row['Low']),
            0.4 + 2 * delta, row['High']-row['Low'],
            facecolor=bg_color,
            edgecolor=bg_color,
            linewidth=linewidth,
            fill=True
        )
        ax.add_patch(rm_rect)

        rect = patches.Rectangle(
            (date_index - 0.2, min(row['Open'], row['Close'])),
            0.4, h,
            facecolor=facecolor,
            edgecolor=edgecolor,
            linewidth=linewidth,
            fill=fill,
            alpha=alpha
        )
        
        ax.add_patch(rect)
        
        rect1 = patches.Rectangle(
            (date_index - 0.025, max(row['Open'], row['Close'])),
            0.05, h1,
            facecolor=facecolor,
            edgecolor=edgecolor,
            linewidth=linewidth,
            fill=fill,
            alpha=alpha
        )
        ax.add_patch(rect1)

        rect2 = patches.Rectangle(
            (date_index - 0.025, row['Low']),
            0.05, h2,
            facecolor=facecolor,
            edgecolor=edgecolor,
            linewidth=linewidth,
            fill=fill,
            alpha=alpha
        )
        ax.add_patch(rect2)
        # 绘制蜡烛的上下影线
        ax.plot([date_index, date_index], [row['Low'], row['High']], color=facecolor, linewidth=linewidth)
        dx = 0.025
        ax.plot([date_index-dx, date_index+dx], [row['High'], row['High']], color=edgecolor, linewidth=linewidth)
        ax.plot([date_index-dx, date_index+dx], [row['Open'], row['Open']], color=edgecolor, linewidth=linewidth)
        ax.plot([date_index-dx, date_index+dx], [row['Close'], row['Close']], color=edgecolor, linewidth=linewidth)
        ax.plot([date_index-dx, date_index+dx], [row['Low'], row['Low']], color=edgecolor, linewidth=linewidth)
        # ax.plot([date_index, date_index], [row['Low'], row['High']], color='white', linewidth=0.8)
       

# 创建解析器
parser = argparse.ArgumentParser(description='input ticker symbol')

# 添加参数
parser.add_argument('--symbol', type=str, default='TSLA')
parser.add_argument('--period', type=str, default='1y')
parser.add_argument('--interval', type=str, default='1d')

# 解析参数
args = parser.parse_args()

symbol = args.symbol
period = args.period
interval = args.interval

# check
assert (period in ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']), 'period is out of range !'
assert (interval in ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']), 'interval is out of range !'

# 要获取价格的股票代码
# symbol = 'TSLA'
# symbol = 'MSFT'
# symbol = 'INTC'
# symbol = 'NVDA'
# symbol = 'DPST'
# symbol = 'SOFI'

# session
# 让系统走你的 MONOPROXY（端口8119）
os.environ["ALL_PROXY"] = "socks5://127.0.0.1:8119"
os.environ["HTTP_PROXY"] = "socks5://127.0.0.1:8119"
os.environ["HTTPS_PROXY"] = "socks5://127.0.0.1:8119"

# time
time.sleep(random.uniform(2, 4))

# 使用yfinance获取股票数据
ticker_data = yf.Ticker(symbol)
# pdb.set_trace()
df = yf.download(
    symbol,
    period=period,
    interval=interval,
    progress=False
)

company_name = ticker_data.info.get("longName", "xyz")
# # print(f'company_name:{company_name}')
market_cap = ticker_data.info.get("marketCap", 0.00)/1e8
print(f'symbol:{symbol}, company_name:{company_name}, market_cap:{market_cap:.2f}')
# 获取股票历史数据
# df = ticker_data.history(start='2020-01-01', end='2024-07-30',interval=interval)
# import pdb; pdb.set_trace()
# df = ticker_data.history(period=period, interval=interval)
assert len(df) > 0, 'ticker symbol may be wrong!'
# df = ticker_data.history(period='2y', interval='1d')
# df = ticker_data.history(period='1y', interval='60m')

# start_date = '2023-01-01'
# end_date = '2024-12-31'
# df = yf.download(symbol, start=start_date, end=end_date)

# 计算均线
df['MA5'] = df['Close'].rolling(window=5).mean()
df['MA10'] = df['Close'].rolling(window=10).mean()
df['MA20'] = df['Close'].rolling(window=20).mean()
df['MA30'] = df['Close'].rolling(window=30).mean()
df['MA35'] = df['Close'].rolling(window=35).mean()
df['MA60'] = df['Close'].rolling(window=60).mean()
df['MA75'] = df['Close'].rolling(window=75).mean()
df['MA90'] = df['Close'].rolling(window=90).mean()
df['MA120'] = df['Close'].rolling(window=120).mean()

# 设置蜡烛图颜色
# 创建市场颜色对象
mc = mpf.make_marketcolors(up='r', down='g', edge='inherit', wick='inherit', volume='inherit',alpha=0.5)

# 设置颜色透明度
rc = {'axes.labelcolor': '#c4c4c4',  # 标签颜色
      'text.color': '#c4c4c4',       # 文本颜色
      'patch.edgecolor': 'w',        # 边缘颜色
      'patch.linewidth': 0.1,        # 边缘宽度
      'patch.facecolor': 'blue',     # 补丁颜色
      'axes.labelsize': 'large',     # 标签尺寸
      'axes.titlesize': 'medium',    # 标题尺寸
      'axes.facecolor': 'dark',
      'grid.color': 'r',             # 网格颜色
      'grid.linestyle': '-.',        # 网格线条风格
      'grid.linewidth': 1.5          # 网格线条宽度
      }

# 创建样式对象
s = mpf.make_mpf_style(marketcolors=mc, rc=rc)

s2 = mpf.make_mpf_style(
    base_mpf_style='nightclouds',
    marketcolors=mc,
    rc={
        'axes.facecolor': '#1e1e1e',  # 深灰色背景
        'figure.facecolor': '#1e1e1e',
        'grid.color': 'lightgray',  # 更深的灰色网格线
        'grid.linestyle': '-',        # 网格线条风格
        'text.color': '#e0e0e0',  # 浅灰色文本
        'axes.labelcolor': '#e0e0e0',
        'xtick.color': '#e0e0e0',
        'ytick.color': '#e0e0e0',
    }
)

# # 计算MACD、RSI、布林带和MFI
df = calculate_macd(df)
df = calculate_rsi(df)
df = calculate_bollinger_bands(df, window=20, std_window=5)
#df = calculate_bollinger_bands(df, window=20, std_window=30)
df = calculate_mfi(df)

# print(f'std:{df["SmoothedStd"].values}, std_mean:{df["SmoothedStd"].mean()}')
# compare
alpha = 0.5
beta = 0.5
std_mean = df['SmoothedStd'].mean()

# short term
lower_bound = df['MA20'] - alpha * std_mean
upper_bound = df['MA20'] + alpha * std_mean

# long term
lower_bound2 = df['MA75'] - beta * std_mean
upper_bound2 = df['MA75'] + beta * std_mean


# 删除包含NaN值的行
# df.dropna(inplace=True)

# 创建均线的添加图
colors = ['red' if val >= 0 else 'green' for val in df['MACD_Hist']] # macd hist color
apds = [
    # ma
    mpf.make_addplot(df['MA5'], color='red', linestyle='solid', width=1, label='MA5'),
    # mpf.make_addplot(df['MA10'], color='green', linestyle='solid', width=1, label='MA10'),
    # mpf.make_addplot(df['MA20'], color='blue', linestyle='solid', width=1, label='MA20'),
    # mpf.make_addplot(df['MA30'], color='red', linestyle='solid', width=1, label='MA30'),
    # mpf.make_addplot(df['MA35'], color='blue', linestyle='solid', width=1, label='MA35'),
    # mpf.make_addplot(df['MA60'], color='purple', linestyle='solid', width=1, label='MA60'),
    # mpf.make_addplot(df['MA75'], color='orange', linestyle='solid', width=1, label='MA75'),
    # mpf.make_addplot(df['MA90'], color='orange', linestyle='solid', width=1, label='MA90'),
    # bound
    # mpf.make_addplot(df['MiddleBand'], color='blue', linestyle='solid', width=2, label='lower_bound'),
    mpf.make_addplot(lower_bound, color='cyan', linestyle='solid', width=1, label='lower_bound', alpha=0.5),
    mpf.make_addplot(upper_bound, color='cyan', linestyle='solid', width=1, label='upper_bound', alpha=0.5),
    mpf.make_addplot(lower_bound2, color='orange', linestyle='solid', width=1, label='lower_bound2', alpha=0.5),
    mpf.make_addplot(upper_bound2, color='orange', linestyle='solid', width=1, label='upper_bound2', alpha=0.5),

    # macd
    mpf.make_addplot(df['MACD'], panel=2, color='cyan', secondary_y=True, label='MACD'),
    mpf.make_addplot(df['Signal'], panel=2, color='orange', secondary_y=True, label='Signal'),
    mpf.make_addplot(df['MACD_Hist'], panel=2, type='bar', color=colors, secondary_y=True, label='MACD_Hist')
    
]
# 绘制蜡烛图
# mav=(5, 20, 35, 75, 90)
# mav=(21, 35, 77, 91)
# mpf.plot(df, type='candle', mav=(21, 35, 77, 91), volume=True, show_nontrading=False,
# pdb.set_trace()
# 【关键】把多层列名变成单层，让 mplfinance 识别
df = df.droplevel('Ticker', axis=1)
fig, axlist = mpf.plot(df, type='candle', volume=True, show_nontrading=False,
        #  style=s,  # 应用样式
         style=s2,  # 应用样式
         title=f'{company_name},{market_cap:.2f},{symbol}-{period}-{interval}',  # 标题
         ylabel='Price',  # y轴标签
         ylabel_lower='Volume',  # 低部y轴标签
         figsize=(48, 32), # 设置图像大小
         addplot=apds,
         returnfig=True,
         )

# print(f'axlist:{len(axlist)}')
ax = axlist[0]

# rm
for axi in axlist:
    axi.grid(False)
    
# # 移除垂直网格线，保留水平网格线
# axi.yaxis.grid(True)  # 保留水平网格线
# axi.xaxis.grid(False)  # 移除垂直网格线

# # 设置主要刻度线
# ax.tick_params(axis='x', colors='white', which='major', direction='out', length=10, width=2)
# ax.tick_params(axis='y', colors='white', which='major', direction='out', length=10, width=2)

# # 设置次要刻度线
# ax.tick_params(axis='x', colors='white', which='minor', direction='out', length=5, width=1)
# ax.tick_params(axis='y', colors='white', which='minor', direction='out', length=5, width=1)

# 移除上下引线
for line in ax.get_lines():
    if line.get_label() == 'Candle':
        line.set_visible(False)
        import sys; sys.exit()

# 绘制梯子
# for i in range(len(df)):
#     if pd.notna(df['MA5'].iloc[i]) and pd.notna(df['MA10'].iloc[i]):
#         ax.plot([i, i], 
#                 [df['MA5'].iloc[i], df['MA10'].iloc[i]], 
#                 color='gray', linestyle='-', linewidth=2)

# for i in range(len(df)):
#     if pd.notna(df['MA20'].iloc[i]) and pd.notna(df['MA35'].iloc[i]):
#         ax.plot([i, i], 
#                 # [top, bottom], 
#                 [df['MA20'].iloc[i], df['MA35'].iloc[i]],
#                 color='cyan', linestyle='-', linewidth=2)

# for i in range(len(df)):
#     if pd.notna(df['MA75'].iloc[i]) and pd.notna(df['MA90'].iloc[i]):
#         ax.plot([i, i], 
#                 [df['MA75'].iloc[i], df['MA90'].iloc[i]], 
#                 color='orange', linestyle='-', linewidth=2)

# 绘制梯子
# lower_bound = df['MiddleBand'] - df['SmoothedStd']
# upper_bound = df['MiddleBand'] + df['SmoothedStd']
# ax.plot(lower_bound.index, lower_bound, label='lower_bound', color='blue')
# ax.plot(upper_bound.index, upper_bound, label='upper_bound', color='blue')

# for i in range(len(lower_bound)):
#     if pd.notna(lower_bound.iloc[i]):
#         ax.plot(i, lower_bound.iloc[i], color='blue', linestyle='-', linewidth=2)

# for i in range(len(lower_bound)):
#     if pd.notna(upper_bound.iloc[i]):
#         ax.plot(i, upper_bound.iloc[i], color='blue', linestyle='-', linewidth=2)

# 绘制梯子
for i in range(len(lower_bound)):
    if pd.notna(lower_bound.iloc[i]) and pd.notna(upper_bound.iloc[i]) and pd.notna(df['Close'].iloc[i]):
        if not (lower_bound.iloc[i] <= df['Close'].iloc[i] <= upper_bound.iloc[i]):
            ax.plot([i, i], [lower_bound.iloc[i], upper_bound.iloc[i]], color='cyan', linestyle='-', linewidth=2, alpha=1.0) # 0.5

for i in range(len(lower_bound2)):
    if pd.notna(lower_bound2.iloc[i]) and pd.notna(upper_bound2.iloc[i]) and pd.notna(df['Close'].iloc[i]):
        if not (lower_bound2.iloc[i] <= df['Close'].iloc[i] <= upper_bound2.iloc[i]):
            ax.plot([i, i], [lower_bound2.iloc[i], upper_bound2.iloc[i]], color='orange', linestyle='-', linewidth=2, alpha=1.0) # 0.5


# current price
current_price = df['Close'].iloc[-1]
# print(f'current_price:{current_price}')
ax.axhline(y=current_price, color='red', linestyle='--', linewidth=1, label='Real-Time Price')

# if interval in ['1d']:
#     # text  
#     special_date = df.index[-1].strftime("%Y-%m-%d")
#     special_date2 = df.index[-20].strftime("%Y-%m-%d")
#     special_text = 'S'
#     special_text2 = 'G'

#     # 找到特定日期的索引和位置
#     date_index = df.index.get_loc(special_date)
#     date_index2 = df.index.get_loc(special_date2)
#     high_price = df.loc[special_date, 'High']
#     low_price = df.loc[special_date, 'Low']
#     high_price2 = df.loc[special_date2, 'High']
#     low_price2 = df.loc[special_date2, 'Low']

#     # print(f'date_index:{date_index}')
#     # print(f'high_price:{high_price}')
#     # print(f'df.index:{df.index[date_index]}')
#     # 在特定日期上方添加文字
#     ax.text(date_index, high_price + 0.4 * (high_price - low_price), special_text, color='green', fontsize=15, ha='center', fontweight='bold')
#     ax.text(date_index2, low_price2 - 0.8 * (high_price2 - low_price2), special_text2, color='red', fontsize=15, ha='center', fontweight='bold')

# 使用自定义函数绘制特定日期的蜡烛
# special_dates3 = [['2023-05-24', '2023-07-02'], ['2023-09-24', '2023-10-30'], ['2024-03-24', '2024-05-02'], ['2024-01-24', '2024-07-02']]
# print(special_dates3)
# special_dates3 = []
# gs_file_root = f'./GS/{symbol}'
# if os.path.exists(gs_file_root):
#     with open(gs_file_root, 'r') as g:
#         lines = g.readlines()
#         special_dates3 = list(map(lambda x: x.strip().split(' '), lines))
#         special_dates3 = [e for e in special_dates3 if len(e) == 2]
#         # print(special_dates3)

# special_date_list = []
# for i, row in df.iterrows():
#     for dt in special_dates3:
#         # if len(dt) != 2:
#         #     continue
#         assert len(dt) == 2, 'len must be 2!'
#         ymd = i.strftime('%Y-%m-%d')
#         if dt[0] <= ymd <= dt[1] :
#             special_date_list.append(ymd)
# print(special_date_list)
# custom_candlestick(ax, df, special_date_list,bg_color='#1e1e1e')
# custom_candlestick(ax, df, special_date_list,bg_color='black')

# 显示
# plt.show()

# 保存
latest_date = df.index[-1].strftime("%Y-%m-%d")
save_dir = f"/Users/chengxian/Desktop/buy_sell_images/{latest_date}/{period}-{interval}"  # 你想保存的路径+文件名
if not os.path.exists(save_dir):
    os.makedirs(save_dir, exist_ok=True)  # 自动创建文件夹
save_path = os.path.join(save_dir, f'{symbol}.png')
if not os.path.exists(save_path):
    plt.savefig(
        save_path,
        dpi=300,          # 高清
        bbox_inches='tight',  # 裁剪白边
        pad_inches=0      # 去留白
    )
plt.close(fig)  # 关闭画布，不占内存