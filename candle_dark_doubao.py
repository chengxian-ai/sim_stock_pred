import warnings
warnings.filterwarnings("ignore")

import os
import random
import time
import matplotlib
matplotlib.use('Agg')
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt
import pandas as pd
import argparse

from tools import calculate_bollinger_bands, calculate_macd, calculate_rsi, calculate_mfi

# 配置类
class Config:
    VPN_PORT = 8119
    FIG_SIZE = (48, 32)
    DPI = 300
    ALPHA = 0.5
    BETA = 0.5
    
    # 颜色配置
    COLORS = {
        'bg': '#1e1e1e',
        'text': '#e0e0e0',
        'grid': 'lightgray',
        'upper_bound': 'cyan',
        'lower_bound': 'orange',
        'current_price': 'red',
        'ma5': 'red',
        'macd': 'cyan',
        'signal': 'orange'
    }

def setup_proxy():
    """设置VPN代理"""
    os.environ["ALL_PROXY"] = f"socks5://127.0.0.1:{Config.VPN_PORT}"
    os.environ["HTTP_PROXY"] = f"socks5://127.0.0.1:{Config.VPN_PORT}"
    os.environ["HTTPS_PROXY"] = f"socks5://127.0.0.1:{Config.VPN_PORT}"

def fetch_stock_data(symbol, period, interval):
    """
    获取股票数据
    
    参数:
        symbol: 股票代码
        period: 数据周期 (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
        interval: 数据间隔 (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
    
    返回:
        df: 股票数据DataFrame
        company_name: 公司名称
        market_cap: 市值（亿）
    """
    # 参数校验
    valid_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    valid_intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
    
    if period not in valid_periods:
        raise ValueError(f"Invalid period. Must be one of: {valid_periods}")
    if interval not in valid_intervals:
        raise ValueError(f"Invalid interval. Must be one of: {valid_intervals}")
    
    # 设置代理并获取数据
    setup_proxy()
    time.sleep(random.uniform(2, 4))
    
    ticker_data = yf.Ticker(symbol)
    df = yf.download(symbol, period=period, interval=interval, progress=False)
    
    if df.empty:
        raise ValueError(f"No data found for symbol: {symbol}")
    
    company_name = ticker_data.info.get("longName", symbol)
    market_cap = ticker_data.info.get("marketCap", 0.0) / 1e8
    
    print(f"Fetched data: {symbol}, {company_name}, market_cap: {market_cap:.2f}亿")
    return df, company_name, market_cap

def calculate_indicators(df):
    """
    计算技术指标
    
    参数:
        df: 股票数据DataFrame
    
    返回:
        df: 添加了技术指标的DataFrame
    """
    # 计算均线
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA75'] = df['Close'].rolling(window=75).mean()
    
    # 计算技术指标
    df = calculate_macd(df)
    df = calculate_rsi(df)
    df = calculate_bollinger_bands(df, window=20, std_window=5)
    df = calculate_mfi(df)
    
    return df

def generate_plot(df, symbol, company_name, market_cap, period, interval, save_root):
    """
    生成蜡烛图并保存
    
    参数:
        df: 股票数据DataFrame
        symbol: 股票代码
        company_name: 公司名称
        market_cap: 市值
        period: 数据周期
        interval: 数据间隔
        save_root: 保存根目录
    """
    # 计算上下边界
    std_mean = df['SmoothedStd'].mean()
    lower_bound = df['MA20'] - Config.ALPHA * std_mean
    upper_bound = df['MA20'] + Config.ALPHA * std_mean
    lower_bound2 = df['MA75'] - Config.BETA * std_mean
    upper_bound2 = df['MA75'] + Config.BETA * std_mean
    
    # MACD柱状图颜色
    colors = ['red' if val >= 0 else 'green' for val in df['MACD_Hist']]
    
    # 创建添加图
    apds = [
        mpf.make_addplot(df['MA5'], color=Config.COLORS['ma5'], linestyle='solid', width=1, label='MA5'),
        mpf.make_addplot(lower_bound, color=Config.COLORS['upper_bound'], linestyle='solid', width=1, alpha=0.5),
        mpf.make_addplot(upper_bound, color=Config.COLORS['upper_bound'], linestyle='solid', width=1, alpha=0.5),
        mpf.make_addplot(lower_bound2, color=Config.COLORS['lower_bound'], linestyle='solid', width=1, alpha=0.5),
        mpf.make_addplot(upper_bound2, color=Config.COLORS['lower_bound'], linestyle='solid', width=1, alpha=0.5),
        mpf.make_addplot(df['MACD'], panel=2, color=Config.COLORS['macd'], secondary_y=True, label='MACD'),
        mpf.make_addplot(df['Signal'], panel=2, color=Config.COLORS['signal'], secondary_y=True, label='Signal'),
        mpf.make_addplot(df['MACD_Hist'], panel=2, type='bar', color=colors, secondary_y=True, label='MACD_Hist')
    ]
    
    # 创建样式
    mc = mpf.make_marketcolors(up='r', down='g', edge='inherit', wick='inherit', volume='inherit', alpha=0.5)
    s = mpf.make_mpf_style(
        base_mpf_style='nightclouds',
        marketcolors=mc,
        rc={
            'axes.facecolor': Config.COLORS['bg'],
            'figure.facecolor': Config.COLORS['bg'],
            'grid.color': Config.COLORS['grid'],
            'grid.linestyle': '-',
            'text.color': Config.COLORS['text'],
            'axes.labelcolor': Config.COLORS['text'],
            'xtick.color': Config.COLORS['text'],
            'ytick.color': Config.COLORS['text'],
        }
    )
    
    # 处理多层列名（兼容旧版 pandas）
    if isinstance(df.columns, pd.MultiIndex):
        if 'Ticker' in df.columns.names:
            df = df.droplevel('Ticker', axis=1)
        elif len(df.columns.names) > 1:
            # 如果没有明确的 'Ticker' 名称，尝试移除第一层
            df = df.droplevel(0, axis=1)
    
    # 绘制蜡烛图
    fig, axlist = mpf.plot(
        df,
        type='candle',
        volume=True,
        show_nontrading=False,
        style=s,
        title=f'{company_name} ({market_cap:.2f}亿) - {symbol} [{period}-{interval}]',
        ylabel='Price',
        ylabel_lower='Volume',
        figsize=Config.FIG_SIZE,
        addplot=apds,
        returnfig=True
    )
    
    # 移除网格
    for axi in axlist:
        axi.grid(False)
    
    ax = axlist[0]
    
    # 绘制梯子（价格突破边界时）
    for i in range(len(lower_bound)):
        if pd.notna(lower_bound.iloc[i]) and pd.notna(upper_bound.iloc[i]) and pd.notna(df['Close'].iloc[i]):
            if not (lower_bound.iloc[i] <= df['Close'].iloc[i] <= upper_bound.iloc[i]):
                ax.plot([i, i], [lower_bound.iloc[i], upper_bound.iloc[i]], 
                        color=Config.COLORS['upper_bound'], linestyle='-', linewidth=2, alpha=1.0)
    
    for i in range(len(lower_bound2)):
        if pd.notna(lower_bound2.iloc[i]) and pd.notna(upper_bound2.iloc[i]) and pd.notna(df['Close'].iloc[i]):
            if not (lower_bound2.iloc[i] <= df['Close'].iloc[i] <= upper_bound2.iloc[i]):
                ax.plot([i, i], [lower_bound2.iloc[i], upper_bound2.iloc[i]], 
                        color=Config.COLORS['lower_bound'], linestyle='-', linewidth=2, alpha=1.0)
    
    # 绘制当前价格线
    current_price = df['Close'].iloc[-1]
    ax.axhline(y=current_price, color=Config.COLORS['current_price'], linestyle='--', linewidth=1, label='Current Price')
    
    # 保存图片
    latest_date = df.index[-1].strftime("%Y-%m-%d")
    save_dir = os.path.join(save_root, latest_date, f"{period}-{interval}")
    os.makedirs(save_dir, exist_ok=True)
    
    save_path = os.path.join(save_dir, f'{symbol}.png')
    plt.savefig(
        save_path,
        dpi=Config.DPI,
        bbox_inches='tight',
        pad_inches=0
    )
    plt.close(fig)
    
    print(f"Chart saved to: {save_path}")
    return save_path

def main(symbol='TSLA', period='1y', interval='1d', save_root='/Users/chengxian/Desktop/buy_sell_images'):
    """
    主函数：获取股票数据、计算指标、生成图表
    
    参数:
        symbol: 股票代码，默认为 'TSLA'
        period: 数据周期，默认为 '1y'
        interval: 数据间隔，默认为 '1d'
        save_root: 保存根目录，默认为 '/Users/chengxian/Desktop/buy_sell_images'
    
    返回:
        save_path: 保存的文件路径
    """
    try:
        df, company_name, market_cap = fetch_stock_data(symbol, period, interval)
        df = calculate_indicators(df)
        save_path = generate_plot(df, symbol, company_name, market_cap, period, interval, save_root)
        return save_path
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Stock Candle Chart Generator')
    parser.add_argument('--symbol', type=str, default='TSLA', help='Stock ticker symbol')
    parser.add_argument('--period', type=str, default='1y', help='Data period')
    parser.add_argument('--interval', type=str, default='1d', help='Data interval')
    parser.add_argument('--save_root', type=str, default='/Users/chengxian/Desktop/buy_sell_images', 
                        help='Root directory to save images')
    
    args = parser.parse_args()
    main(args.symbol, args.period, args.interval, args.save_root)