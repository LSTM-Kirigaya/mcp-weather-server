"""测试天气查询功能"""

import asyncio
import sys
sys.path.insert(0, '/Users/kirigaya/code/dedalus-tutorial/mcp-weather-server')

from weather_server import get_city_weather_by_city_code, get_weather_by_city_code, server


def test_weather_api():
    """测试天气 API 调用"""
    print("=== 测试获取北京天气 ===")
    beijing_code = "101010100"
    result = get_city_weather_by_city_code(beijing_code)
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
        return False
    
    print("\n=== 测试 MCP 工具函数 ===")
    tool_result = get_weather_by_city_code(101010100)
    print(f"工具返回:\n{tool_result}")
    
    return True


def test_server_tools():
    """测试服务器工具注册"""
    print("\n=== 测试服务器工具列表 ===")
    # 检查工具是否已注册
    tool_names = server.tool_names
    print(f"已注册工具数量: {len(tool_names)}")
    for name in tool_names:
        print(f"  - {name}")
    return len(tool_names) > 0


async def main():
    print("开始测试 dMCP 天气服务器...\n")
    
    success = True
    
    # 测试天气 API
    if not test_weather_api():
        success = False
    
    # 测试服务器工具
    if not test_server_tools():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("✅ 所有测试通过!")
    else:
        print("❌ 部分测试失败")
    print("=" * 50)
    
    return success


if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)
