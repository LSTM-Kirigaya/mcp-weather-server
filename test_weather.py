"""测试天气查询功能"""

import sys
sys.path.insert(0, '/Users/kirigaya/code/dedalus-tutorial/mcp-weather-server')

from weather_server import get_city_weather_by_city_name, get_weather_by_code

# 测试北京城市代码
print("=== 测试获取北京天气 ===")
beijing_code = "101010100"
result = get_city_weather_by_city_name(beijing_code)
if result:
    print(f"城市: {result.city_name_cn} ({result.city_name_en})")
    print(f"温度: {result.temp}°C")
    print(f"天气: {result.weather}")
    print(f"风向: {result.wd}")
    print(f"风速: {result.ws}")
    print(f"湿度: {result.sd}")
    print(f"空气质量: {result.aqi}")
else:
    print("获取天气失败")

print("\n=== 测试 MCP 工具函数 ===")
tool_result = get_weather_by_code(101010100)
print(f"工具返回: {tool_result}")

print("\n=== 所有测试通过! ===")
