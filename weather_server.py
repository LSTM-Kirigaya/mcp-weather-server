"""
dMCP Weather Server - 基于 Dedalus MCP 规范的天气查询服务器

使用中国天气网 API 提供实时天气查询服务。
"""

import os
import sys
import requests
import json
from typing import NamedTuple, Optional
from dedalus_mcp import MCPServer, tool


class CityWeather(NamedTuple):
    """城市天气数据结构"""
    city_name_en: str
    city_name_cn: str
    city_code: str
    temp: str
    wd: str
    ws: str
    sd: str
    aqi: str
    weather: str


def get_city_weather_by_city_code(city_code: str) -> Optional[CityWeather]:
    """
    根据城市代码获取天气信息
    
    Args:
        city_code: 中国天气网城市代码，如北京为 "101010100"
    
    Returns:
        CityWeather 对象或 None（获取失败时）
    """
    if not city_code:
        return None
    
    try:
        # 构造请求URL
        url = f"http://d1.weather.com.cn/sk_2d/{city_code}.html"
        
        # 设置请求头
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.0.0",
            "Host": "d1.weather.com.cn",
            "Referer": "http://www.weather.com.cn/"
        }
        
        # 发送HTTP请求
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 解析JSON数据前先处理编码问题
        content = response.text.encode('latin1').decode('unicode_escape')
        json_start = content.find("{")
        json_str = content[json_start:]
        
        weather_data = json.loads(json_str)
        
        # 构造返回对象
        return CityWeather(
            city_name_en=weather_data.get("nameen", ""),
            city_name_cn=weather_data.get("cityname", "").encode('latin1').decode('utf-8'),
            city_code=weather_data.get("city", ""),
            temp=weather_data.get("temp", ""),
            wd=weather_data.get("wd", "").encode('latin1').decode('utf-8'),
            ws=weather_data.get("ws", "").encode('latin1').decode('utf-8'),
            sd=weather_data.get("sd", ""),
            aqi=weather_data.get("aqi", ""),
            weather=weather_data.get("weather", "").encode('latin1').decode('utf-8')
        )
        
    except Exception as e:
        print(f"获取天气信息失败: {str(e)}", file=sys.stderr)
        return None


@tool(description="根据城市代码获取指定城市的实时天气信息，包括温度、天气状况、风向、风速、湿度和空气质量指数")
def get_weather_by_city_code(city_code: int) -> str:
    """
    根据城市代码获取天气信息
    
    Args:
        city_code: 城市代码（整数），如北京 101010100、上海 101020100
    
    Returns:
        格式化的天气信息字符串
    """
    city_weather = get_city_weather_by_city_code(str(city_code))
    if city_weather is None:
        return f"错误：无法获取城市代码 {city_code} 的天气信息，请检查城市代码是否正确。"
    
    return (
        f"城市：{city_weather.city_name_cn} ({city_weather.city_name_en})\n"
        f"温度：{city_weather.temp}°C\n"
        f"天气：{city_weather.weather}\n"
        f"风向：{city_weather.wd}\n"
        f"风速：{city_weather.ws}\n"
        f"湿度：{city_weather.sd}\n"
        f"空气质量指数(AQI)：{city_weather.aqi}"
    )


# 创建 MCP 服务器
server = MCPServer("weather-server")

# 收集/注册工具
server.collect(get_weather_by_city_code)


async def main():
    """主函数 - 启动 Streamable HTTP 服务器"""
    # 从环境变量获取配置，使用默认值
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))
    
    print(f"启动 dMCP 天气服务器...", file=sys.stderr)
    print(f"服务器配置: host={host}, port={port}, path=/mcp", file=sys.stderr)
    print(f"服务器将在 http://{host}:{port}/mcp 运行", file=sys.stderr)
    
    # 使用 serve_streamable_http 启动服务器
    # 这会保持服务器运行并监听 HTTP/SSE 请求
    await server.serve_streamable_http(
        host=host,
        port=port,
        path="/mcp",
        log_level="info"
    )


if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n服务器已停止", file=sys.stderr)
    except Exception as e:
        print(f"服务器错误: {e}", file=sys.stderr)
        sys.exit(1)
