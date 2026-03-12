# dMCP Weather Server

基于 [Dedalus MCP](https://github.com/dedalus-labs/dedalus-mcp-python) 规范构建的中国天气查询服务器。

## 特性

- 🌤️ 实时天气查询（温度、天气状况、风向、风速、湿度、AQI）
- 🔌 符合 dMCP 规范，支持 Streamable HTTP 传输
- 🚀 轻量级，137KB（比 FastMCP 小 60 倍）
- 🔒 无全局状态，支持多服务器实例

## 安装

```bash
pip install -r requirements.txt
```

## 快速开始

### 启动服务器

```bash
python weather_server.py
```

服务器将在 `http://127.0.0.1:8000/mcp` 运行。

### 使用客户端连接

```python
import asyncio
from dedalus_mcp.client import MCPClient

async def main():
    client = await MCPClient.connect("http://127.0.0.1:8000/mcp")
    
    # 列出可用工具
    tools = await client.list_tools()
    print("可用工具:", tools)
    
    # 查询北京天气（城市代码：101010100）
    result = await client.call_tool("get_weather_by_city_code", {"city_code": 101010100})
    print(result)
    
    await client.close()

asyncio.run(main())
```

## 城市代码

中国城市天气代码（部分）：

| 城市 | 代码 |
|------|------|
| 北京 | 101010100 |
| 上海 | 101020100 |
| 广州 | 101280101 |
| 深圳 | 101280601 |
| 杭州 | 101210101 |
| 成都 | 101270101 |

更多城市代码可在 [中国天气网](http://www.weather.com.cn/) 查询。

## API

### get_weather_by_city_code

根据城市代码获取天气信息。

**参数：**
- `city_code` (int): 城市代码

**返回：**
- 格式化的天气信息字符串

## 测试

```bash
python test_weather.py
```

## 与 Dedalus SDK 集成

```python
from dedalus_labs import AsyncDedalus, DedalusRunner

async def main():
    client = AsyncDedalus()
    runner = DedalusRunner(client)
    
    result = await runner.run(
        input="查询北京的天气",
        model="openai/gpt-5-nano",
        mcp_servers=["local/weather-server"]  # 指向本地服务器
    )
    print(result.final_output)

asyncio.run(main())
```

## 技术栈

- [dedalus_mcp](https://github.com/dedalus-labs/dedalus-mcp-python) - Dedalus MCP Python SDK
- [requests](https://requests.readthedocs.io/) - HTTP 请求
- 天气数据来源：[中国天气网](http://www.weather.com.cn/)

## 许可证

MIT License
