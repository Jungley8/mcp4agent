"""微信公众号MCP服务器入口 - FastMCP 2.x"""
import sys
from . import app, docker_app
from .config import config


def main():
    """主入口函数"""
    # 检查配置
    if not config.validate():
        print("⚠️  警告: WECHAT_APP_ID 或 WECHAT_APP_SECRET 未配置")
        print("请复制 .env.example 为 .env 并填入配置")
    
    # 启动FastMCP 2.x服务器 (Streamable HTTP)
    print("🚀 启动 wechat-mcp 服务器 (HTTP transport)...")
    app.run(transport="http", host="0.0.0.0", port=8080, path="/mcp")


if __name__ == "__main__":
    main()
