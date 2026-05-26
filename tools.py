import yfinance as yf
import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# from matplotlib.ticker import FuncFormatter

def moving_average_filter(data, window_size):
    return data.rolling(window=window_size, min_periods=1).mean()



def calculate_macd(df, short_window=12, long_window=26, signal_window=9):
    df['EMA12'] = df['Close'].ewm(span=short_window, adjust=False).mean()
    df['EMA26'] = df['Close'].ewm(span=long_window, adjust=False).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal'] = df['MACD'].ewm(span=signal_window, adjust=False).mean()
    df['MACD_Hist'] = df['MACD'] - df['Signal']
    return df

def calculate_rsi(df, window=14):
    delta = df['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df


def calculate_bollinger_bands(df, window=20, std_window=30, N=0):
    df['MiddleBand'] = df['Close'].rolling(window=window).mean() # 计算移动平均
    df['Std'] = df['Close'].rolling(window=std_window).std()  # 计算原始标准差
    df['Std'] = df['Std'].ewm(span=std_window).mean()  # 使用EMA平滑标准差
    df['SmoothedStd'] = df['Std']
    for i in range(N):
        df['SmoothedStd'] = moving_average_filter(df['SmoothedStd'], std_window)
        df['SmoothedStd'] = df['SmoothedStd'].ewm(span=std_window).mean()
    
    df['UpperBand'] = df['MiddleBand'] + 2 * df['SmoothedStd']
    df['LowerBand'] = df['MiddleBand'] - 2 * df['SmoothedStd']
    return df

def calculate_mfi(df, window=14):
    tp = (df['High'] + df['Low'] + df['Close']) / 3
    mf = tp * df['Volume']
    pmf = mf.where(df['Close'] > df['Close'].shift(1), 0)
    nmf = mf.where(df['Close'] < df['Close'].shift(1), 0)
    mfr = pmf.rolling(window=window).sum() / nmf.rolling(window=window).sum()
    df['MFI'] = 100 - (100 / (1 + mfr))
    return df

def identify_bull_and_bear_line(df, short_window, long_window):
    df['Bullish'] = (df[f'SMA{short_window}'] > df[f'SMA{long_window}']) & \
                            (df['Volume'] > df[f'VolumeSMA{volume_window}']) & \
                            (df['RSI'] > 50) & (df['MACD_Hist'] > 0) & \
                            (df['Close'] > df['MiddleBand']) & \
                            (df['MFI'] > 50)
                            
    df['Bearish'] = (df[f'SMA{short_window}'] < df[f'SMA{long_window}']) & \
                            (df['Volume'] < df[f'VolumeSMA{volume_window}']) & \
                            (df['RSI'] < 50) & (df['MACD_Hist'] < 0) & \
                            (df['Close'] < df['MiddleBand']) & \
                            (df['MFI'] < 50)
    return df