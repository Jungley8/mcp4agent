"""微信公众号MCP服务器 - 支持Docker容器监控"""
__version__ = "0.2.0"

# 微信相关
from .server import app, create_draft, upload_image, list_drafts, publish_draft
from .api import WeChatAPI, get_wechat_api
from .config import Config, config
from .token_cache import TokenCache, get_token_cache

# Docker相关
from .docker_status import (
    list_containers,
    get_container_stats,
    get_container_logs,
    restart_container,
    docker_app,
)

__all__ = [
    # 版本
    "__version__",
    # FastMCP应用
    "app",
    "docker_app",
    # 微信工具
    "create_draft",
    "upload_image",
    "list_drafts",
    "publish_draft",
    # API
    "WeChatAPI",
    "get_wechat_api",
    # 配置
    "Config",
    "config",
    # 缓存
    "TokenCache",
    "get_token_cache",
    # Docker工具
    "list_containers",
    "get_container_stats",
    "get_container_logs",
    "restart_container",
]
