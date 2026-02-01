"""微信公众号API模块"""
import requests
from typing import Optional, Dict, Any
from pathlib import Path

from .token_cache import get_token_cache
from .config import config


class WeChatAPI:
    """微信公众号API封装"""
    
    def __init__(self, app_id: str = None, app_secret: str = None):
        self.app_id = app_id or config.app_id
        self.app_secret = app_secret or config.app_secret
        self._token_cache = get_token_cache()
    
    def _get_token(self) -> Optional[str]:
        """获取access_token"""
        return self._token_cache.get_access_token(self.app_id, self.app_secret)
    
    def _request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """发起请求"""
        resp = requests.request(method, url, **kwargs)
        return resp.json()
    
    # ============ 素材管理 ============
    
    def upload_image(self, image_path: str) -> Optional[str]:
        """
        上传图片获取永久素材media_id
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            media_id，失败返回None
        """
        token = self._get_token()
        if not token:
            return None
        
        url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
        
        try:
            with open(image_path, "rb") as f:
                resp = requests.post(url, files={"media": f}, timeout=30)
                data = resp.json()
                
                if "media_id" in data:
                    return data["media_id"]
                else:
                    print(f"上传图片失败: {data}")
                    return None
        except Exception as e:
            print(f"上传图片异常: {e}")
            return None
    
    def upload_temp_image(self, image_path: str) -> Optional[str]:
        """上传临时素材"""
        token = self._get_token()
        if not token:
            return None
        
        url = f"https://api.weixin.qq.com/cgi-bin/media/upload?access_token={token}&type=image"
        
        try:
            with open(image_path, "rb") as f:
                resp = requests.post(url, files={"media": f}, timeout=30)
                data = resp.json()
                
                if "media_id" in data:
                    return data["media_id"]
                else:
                    print(f"上传临时素材失败: {data}")
                    return None
        except Exception as e:
            print(f"上传临时素材异常: {e}")
            return None
    
    # ============ 草稿管理 ============
    
    def create_draft(
        self,
        title: str,
        content: str,
        thumb_media_id: str = None,
        show_cover_pic: int = 0
    ) -> Optional[str]:
        """
        创建草稿
        
        Args:
            title: 标题
            content: 内容 (HTML格式)
            thumb_media_id: 封面media_id
            show_cover_pic: 是否显示封面 (0/1)
            
        Returns:
            media_id，失败返回None
        """
        token = self._get_token()
        if not token:
            return None
        
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
        
        article = {
            "title": title,
            "content": content,
            "show_cover_pic": show_cover_pic,
            "need_open_comment": 1,
            "only_fans_can_comment": 0
        }
        
        if thumb_media_id:
            article["thumb_media_id"] = thumb_media_id
        
        try:
            resp = requests.post(url, json={"articles": [article]}, timeout=30)
            data = resp.json()
            
            if "media_id" in data:
                return data["media_id"]
            else:
                print(f"创建草稿失败: {data}")
                return None
        except Exception as e:
            print(f"创建草稿异常: {e}")
            return None
    
    def list_drafts(self, offset: int = 0, count: int = 20) -> list:
        """列出草稿"""
        token = self._get_token()
        if not token:
            return []
        
        url = f"https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token={token}"
        
        try:
            resp = requests.post(url, json={"offset": offset, "count": count}, timeout=30)
            data = resp.json()
            
            if "item" in data:
                return [
                    {
                        "media_id": item.get("media_id"),
                        "title": item.get("content", {}).get("news_item", [{}])[0].get("title", ""),
                        "update_time": item.get("update_time", 0)
                    }
                    for item in data["item"]
                ]
            return []
        except Exception as e:
            print(f"获取草稿列表异常: {e}")
            return []
    
    def delete_draft(self, media_id: str) -> bool:
        """删除草稿"""
        token = self._get_token()
        if not token:
            return False
        
        url = f"https://api.weixin.qq.com/cgi-bin/draft/delete?access_token={token}"
        
        try:
            resp = requests.post(url, json={"media_id": media_id}, timeout=30)
            data = resp.json()
            return data.get("errcode", -1) == 0
        except Exception as e:
            print(f"删除草稿异常: {e}")
            return False
    
    # ============ 发布管理 ============
    
    def publish_draft(self, media_id: str) -> bool:
        """
        发布草稿
        
        Args:
            media_id: 草稿media_id
            
        Returns:
            是否成功
        """
        token = self._get_token()
        if not token:
            return False
        
        url = f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={token}"
        
        try:
            resp = requests.post(url, json={"media_id": media_id}, timeout=30)
            data = resp.json()
            
            if data.get("errcode", -1) == 0:
                return True
            else:
                print(f"发布失败: {data}")
                return False
        except Exception as e:
            print(f"发布异常: {e}")
            return False


# 全局API实例
_api_instance: Optional[WeChatAPI] = None


def get_wechat_api() -> WeChatAPI:
    """获取全局WeChatAPI实例"""
    global _api_instance
    if _api_instance is None:
        _api_instance = WeChatAPI()
    return _api_instance
