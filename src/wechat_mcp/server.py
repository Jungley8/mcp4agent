"""微信公众号MCP服务器 - FastMCP版本"""
from fastmcp import FastMCP
from typing import Any

from .config import config
from .api import get_wechat_api

app = FastMCP("wechat-mcp")


@app.tool()
def create_draft(
    title: str,
    content: str,
    cover_image_path: str = None
) -> str:
    """
    创建微信公众号草稿
    
    Args:
        title: 文章标题
        content: 文章内容（HTML格式）
        cover_image_path: 封面图片路径（可选）
    
    Returns:
        操作结果消息
    """
    api = get_wechat_api()
    
    thumb_media_id = None
    if cover_image_path:
        result = api.upload_image(cover_image_path)
        if result:
            thumb_media_id = result
    
    draft_result = api.create_draft(title, content, thumb_media_id)
    
    if draft_result:
        return f"✅ 草稿创建成功！media_id: {draft_result}"
    else:
        return "❌ 创建草稿失败"


@app.tool()
def upload_image(image_path: str) -> str:
    """
    上传图片到微信公众号获取media_id
    
    Args:
        image_path: 图片文件路径
    
    Returns:
        操作结果消息
    """
    api = get_wechat_api()
    result = api.upload_image(image_path)
    
    if result:
        return f"✅ 图片上传成功！media_id: {result}"
    else:
        return "❌ 图片上传失败"


@app.tool()
def list_drafts(offset: int = 0, count: int = 20) -> str:
    """
    列出所有草稿
    
    Args:
        offset: 分页偏移，默认0
        count: 每页数量，默认20
    
    Returns:
        草稿列表
    """
    api = get_wechat_api()
    drafts = api.list_drafts(offset, count)
    
    if drafts:
        text = "📋 草稿列表：\n\n"
        for i, draft in enumerate(drafts, 1):
            text += f"{i}. {draft['title']}\n"
            text += f"   media_id: {draft['media_id']}\n\n"
        return text
    else:
        return "📋 暂无草稿"


@app.tool()
def publish_draft(media_id: str) -> str:
    """
    发布草稿（需要相应权限）
    
    Args:
        media_id: 草稿media_id
    
    Returns:
        操作结果消息
    """
    api = get_wechat_api()
    result = api.publish_draft(media_id)
    
    if result:
        return "✅ 发布成功！"
    else:
        return "❌ 发布失败，可能权限不足"
