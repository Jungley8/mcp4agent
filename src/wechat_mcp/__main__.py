"""微信公众号MCP服务器入口"""
import sys
from . import app, docker_app
from .config import config


def main():
    """主入口函数"""
    # 检查配置
    if not config.validate():
        print("⚠️  警告: WECHAT_APP_ID 或 WECHAT_APP_SECRET 未配置")
        print("请复制 .env.example 为 .env 并填入配置")
    
    # 启动FastMCP服务器（wechat工具）
    print("🚀 启动 wechat-mcp 服务器...")
    app.run()


if __name__ == "__main__":
    main()
