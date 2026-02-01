"""Token缓存模块 - 使用diskcache实现本地缓存"""
import os
import time
from pathlib import Path
import diskcache as dc
from typing import Optional

from .config import config


class TokenCache:
    """Access Token缓存管理"""
    
    def __init__(self):
        self._cache_dir = Path(config.token_cache_dir)
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._cache = dc.Cache(self._cache_dir, expire=7000)  # 微信token有效期2小时，缓存1小时50分
    
    def get_access_token(self, app_id: str, app_secret: str) -> Optional[str]:
        """
        获取access_token，优先从缓存读取
        
        Args:
            app_id: 微信公众号AppID
            app_secret: 微信公众号AppSecret
            
        Returns:
            access_token字符串，失败返回None
        """
        cache_key = f"access_token_{app_id}"
        
        # 检查缓存
        cached = self._cache.get(cache_key)
        if cached:
            token, expire_at = cached
            if time.time() < expire_at:
                return token
        
        # 请求新token
        import requests
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": app_id,
            "secret": app_secret
        }
        
        try:
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()
            
            if "access_token" in data:
                token = data["access_token"]
                expires_in = data.get("expires_in", 7200)
                expire_at = time.time() + expires_in - 200  # 提前200秒刷新
                
                # 写入缓存
                self._cache.set(cache_key, (token, expire_at))
                return token
            else:
                print(f"获取token失败: {data}")
                return None
                
        except Exception as e:
            print(f"请求token异常: {e}")
            return None
    
    def clear_cache(self, app_id: str = None):
        """清除缓存"""
        if app_id:
            cache_key = f"access_token_{app_id}"
            self._cache.delete(cache_key)
        else:
            self._cache.clear()
    
    def close(self):
        """关闭缓存"""
        self._cache.close()


# 全局缓存实例
_token_cache: Optional[TokenCache] = None


def get_token_cache() -> TokenCache:
    """获取全局TokenCache实例"""
    global _token_cache
    if _token_cache is None:
        _token_cache = TokenCache()
    return _token_cache
