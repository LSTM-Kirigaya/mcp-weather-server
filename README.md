# MCP Weather Server

一个基于 MCP (Model Context Protocol) 的天气查询服务器，支持通过城市代码获取中国城市的天气信息。

## 功能

- 通过城市代码查询天气信息
- 返回温度、风向、风速、湿度、空气质量指数等信息
- 支持 MCP 协议，可作为工具被 AI 助手调用

## 安装

```bash
pip install -r requirements.txt
```

## 使用

### 直接运行

```bash
python weather_server.py
```

### 作为 MCP 工具使用

在支持 MCP 的客户端中配置：

```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["/path/to/weather_server.py"]
    }
  }
}
```

## 城市代码

中国城市天气代码可在 [中国天气网](http://www.weather.com.cn/) 查询。例如：
- 北京: `101010100`
- 上海: `101020100`
- 广州: `101280101`
- 深圳: `101280601`

## API

### get_weather_by_city_code

根据城市代码获取天气信息。

**参数:**
- `city_code` (int): 城市代码

**返回:**
- 城市天气信息的字符串表示

## 数据来源

天气数据来源于 [中国天气网](http://www.weather.com.cn/)。
