
## 功能特性

### 技术指标计算 (`tools.py`)
- **移动平均滤波** (`moving_average_filter`)
- **MACD 指标** (`calculate_macd`) - EMA12、EMA26、MACD线、信号线、柱状图
- **RSI 指标** (`calculate_rsi`) - 相对强弱指数
- **布林带** (`calculate_bollinger_bands`) - 中轨、上轨、下轨
- **MFI 指标** (`calculate_mfi`) - 资金流量指数
- **多指标综合判断** (`identify_bull_and_bear_line`) - 牛市/熊市信号识别

## 快速开始

### 1. 环境配置

确保已安装所需依赖库：
- `yfinance` - Yahoo财经数据获取
- `pandas` - 数据处理

```bash
# 使用 Conda 环境（推荐）
conda env create -f stock_pred_env
conda activate stock_pred_env

# 或使用 pip 安装
pip install yfinance pandas
```

### 2. 运行方式

```bash
# 方式一：批量运行（推荐）
bash batch_run.sh

# 方式二：单独运行 Python 脚本
python candle_dark.py
```

## 使用说明

### 添加股票代码
在 `batch_run.sh` 文件中添加您感兴趣的股票代码：
```bash
# 示例：添加股票代码
STOCKS="AAPL GOOGL MSFT TSLA"
```

### 修改保存路径
在 `.py` 文件中修改结果保存路径：
```python
# 示例：设置保存路径
save_path = "/your/path/to/save/results/"
```

## 注意事项

1. **VPN 端口适配**：如果使用 VPN 软件，请确保网络端口适配，避免数据获取失败。
2. **数据来源**：数据来自 Yahoo Finance，需要稳定的网络连接。
3. **文件路径**：运行前请确保保存路径存在且有写入权限。

## 依赖库

| 库名 | 用途 |
|------|------|
| yfinance | Yahoo财经数据获取 |
| pandas | 数据处理与分析 |