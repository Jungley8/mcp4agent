"""微信公众号 MCP 服务器入口"""
import asyncio
from .server import main

if __name__ == "__main__":
    asyncio.run(main())
