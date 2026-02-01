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
    cover_image_path: str = None,
    thumb_media_id: str = None
) -> str:
    """
    创建微信公众号草稿
    
    Args:
        title: 文章标题
        content: 文章内容（HTML格式）
        cover_image_path: 封面图片路径（可选，本地路径）
        thumb_media_id: 封面media_id（可选，优先使用）
    
    Returns:
        操作结果消息
    """
    api = get_wechat_api()
    
    media_id = None
    # 优先使用传入的 thumb_media_id
    if thumb_media_id:
        media_id = thumb_media_id
    # 否则尝试上传本地图片
    elif cover_image_path and cover_image_path != "None":
        result = api.upload_image(cover_image_path)
        if result:
            media_id = result
    
    draft_result = api.create_draft(title, content, media_id)
    
    if draft_result:
        return f"✅ 草稿创建成功！media_id: {draft_result}"
    else:
        return "❌ 创建草稿失败"


@app.tool()
def upload_image(image_path: str = None, image_base64: str = None) -> str:
    """
    上传图片到微信公众号获取media_id
    
    Args:
        image_path: 图片文件路径（可选，与二选一）
        image_base64: Base64编码的图片数据（可选，与二选一）
    
    Returns:
        操作结果消息
    """
    api = get_wechat_api()
    
    import tempfile
    import base64
    import os
    
    temp_path = None
    try:
        # 如果传入 base64，先保存到临时文件
        if image_base64:
            # 检查是否是 data URL 格式
            if image_base64.startswith("data:"):
                image_base64 = image_base64.split(",", 1)[1]
            
            image_data = base64.b64decode(image_base64)
            
            # 创建临时文件
            fd, temp_path = tempfile.mkstemp(suffix=".jpg")
            with os.write(fd, image_data) as f:
                f.write(image_data)
            os.close(fd)
            image_path = temp_path
        
        if not image_path or image_path == "None":
            return "❌ 请提供 image_path 或 image_base64"
        
        result = api.upload_image(image_path)
        
        if result:
            return f"✅ 图片上传成功！media_id: {result}"
        else:
            return "❌ 图片上传失败"
            
    except Exception as e:
        return f"❌ 图片上传异常: {str(e)}"
    finally:
        # 清理临时文件
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass


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
