"""MCP4Agent - Multi-package MCP server"""
__version__ = "0.3.0"

# WeChat MCP
from wechat_mcp import (
    app as wechat_app,
    create_draft,
    upload_image,
    list_drafts,
    publish_draft,
    WeChatAPI,
    get_wechat_api,
    Config,
    config,
    TokenCache,
    get_token_cache,
)

# Docker Status MCP
from docker_status import (
    docker_app,
    list_containers,
    get_container_stats,
    get_container_logs,
    restart_container,
)

__all__ = [
    "__version__",
    # WeChat
    "wechat_app",
    "create_draft",
    "upload_image",
    "list_drafts",
    "publish_draft",
    "WeChatAPI",
    "get_wechat_api",
    "Config",
    "config",
    "TokenCache",
    "get_token_cache",
    # Docker
    "docker_app",
    "list_containers",
    "get_container_stats",
    "get_container_logs",
    "restart_container",
]
