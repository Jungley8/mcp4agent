"""微信公众号MCP服务器"""
import asyncio
import sys
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .config import config
from .api import get_wechat_api


def create_tools() -> list[Tool]:
    """创建工具列表"""
    return [
        Tool(
            name="create_draft",
            description="创建微信公众号草稿",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "文章标题"
                    },
                    "content": {
                        "type": "string", 
                        "description": "文章内容（HTML格式）"
                    },
                    "cover_image_path": {
                        "type": "string",
                        "description": "封面图片路径（可选）"
                    }
                },
                "required": ["title", "content"]
            }
        ),
        Tool(
            name="upload_image",
            description="上传图片到微信公众号获取media_id",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "图片文件路径"
                    }
                },
                "required": ["image_path"]
            }
        ),
        Tool(
            name="list_drafts",
            description="列出所有草稿",
            inputSchema={
                "type": "object",
                "properties": {
                    "offset": {
                        "type": "integer",
                        "description": "分页偏移",
                        "default": 0
                    },
                    "count": {
                        "type": "integer",
                        "description": "每页数量",
                        "default": 20
                    }
                }
            }
        ),
        Tool(
            name="publish_draft",
            description="发布草稿（需要相应权限）",
            inputSchema={
                "type": "object",
                "properties": {
                    "media_id": {
                        "type": "string",
                        "description": "草稿media_id"
                    }
                },
                "required": ["media_id"]
            }
        ),
    ]


async def main():
    """主函数"""
    app = Server("wechat-mcp")
    api = get_wechat_api()
    
    @app.list_tools()
    async def list_tools() -> list[Tool]:
        return create_tools()
    
    @app.call_tool()
    async def call_tool(name: str, arguments: Any) -> list[TextContent]:
        try:
            if name == "create_draft":
                title = arguments["title"]
                content = arguments["content"]
                cover_path = arguments.get("cover_image_path")
                
                thumb_media_id = None
                if cover_path and api.upload_image(cover_path):
                    thumb_media_id = api.upload_image(cover_path)
                
                result = api.create_draft(title, content, thumb_media_id)
                
                if result:
                    return [TextContent(
                        type="text",
                        text=f"✅ 草稿创建成功！media_id: {result}"
                    )]
                else:
                    return [TextContent(
                        type="text",
                        text="❌ 创建草稿失败"
                    )]
            
            elif name == "upload_image":
                image_path = arguments["image_path"]
                result = api.upload_image(image_path)
                
                if result:
                    return [TextContent(
                        type="text",
                        text=f"✅ 图片上传成功！media_id: {result}"
                    )]
                else:
                    return [TextContent(
                        type="text",
                        text="❌ 图片上传失败"
                    )]
            
            elif name == "list_drafts":
                offset = arguments.get("offset", 0)
                count = arguments.get("count", 20)
                
                drafts = api.list_drafts(offset, count)
                
                if drafts:
                    text = "📋 草稿列表：\n\n"
                    for i, draft in enumerate(drafts, 1):
                        text += f"{i}. {draft['title']}\n"
                        text += f"   media_id: {draft['media_id']}\n\n"
                    return [TextContent(type="text", text=text)]
                else:
                    return [TextContent(type="text", text="📋 暂无草稿")]
            
            elif name == "publish_draft":
                media_id = arguments["media_id"]
                result = api.publish_draft(media_id)
                
                if result:
                    return [TextContent(
                        type="text",
                        text="✅ 发布成功！"
                    )]
                else:
                    return [TextContent(
                        type="text",
                        text="❌ 发布失败，可能权限不足"
                    )]
            
            else:
                return [TextContent(
                    type="text",
                    text=f"❌ 未知工具: {name}"
                )]
        
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 执行出错: {str(e)}"
            )]
    
    # 检查配置
    if not config.validate():
        print("⚠️  警告: WECHAT_APP_ID 或 WECHAT_APP_SECRET 未配置")
        print("请复制 .env.example 为 .env 并填入配置")
    
    # 启动服务器
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
