"""配置管理模块"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """公众号配置"""
    
    @property
    def app_id(self) -> str:
        return os.getenv("WECHAT_APP_ID", "")
    
    @property
    def app_secret(self) -> str:
        return os.getenv("WECHAT_APP_SECRET", "")
    
    @property
    def token_cache_dir(self) -> str:
        return os.path.expanduser(os.getenv("WECHAT_TOKEN_CACHE_DIR", "~/.cache/wechat-mcp"))
    
    def validate(self) -> bool:
        """验证配置是否完整"""
        return bool(self.app_id and self.app_secret)


config = Config()
