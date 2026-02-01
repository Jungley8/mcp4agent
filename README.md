# 微信公众号 MCP Server

微信公众号管理工具，支持文章发布、草稿管理等功能。

## 安装

```bash
pip install -e .
```

## 配置

复制 `.env.example` 为 `.env`，填入你的配置：

```bash
cp .env.example .env
```

### 环境变量

| 变量 | 说明 |
|------|------|
| `WECHAT_APP_ID` | 微信公众号AppID |
| `WECHAT_APP_SECRET` | 微信公众号AppSecret |
| `WECHAT_TOKEN_CACHE_DIR` | Token缓存目录 (默认: ~/.cache/wechat-mcp) |

## 使用

启动MCP服务器：

```bash
python -m wechat_mcp
```

## 可用工具

- `create_draft` - 创建草稿
- `upload_image` - 上传图片
- `list_drafts` - 列出草稿
- `publish_draft` - 发布草稿（需要权限）

## Token缓存

使用 `diskcache` 实现本地缓存，避免频繁请求access_token。

```python
from wechat_mcp.token_cache import TokenCache

cache = TokenCache()
token = cache.get_access_token(app_id, app_secret)
```

## Docker 部署

### 构建镜像

```bash
docker build -t wechat-mcp .
```

### 使用 Docker Compose（推荐）

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 填入你的配置
nano .env

# 启动服务
docker-compose up -d
```

### 使用 Docker Run

```bash
docker run -d \
  --name wechat-mcp \
  -p 8080:8080 \
  -e WECHAT_APP_ID=your_app_id \
  -e WECHAT_APP_SECRET=your_app_secret \
  -v $(pwd)/data:/app/.cache \
  wechat-mcp
```

### 环境变量

| 变量 | 说明 | 必填 |
|------|------|------|
| `WECHAT_APP_ID` | 微信公众号AppID | 是 |
| `WECHAT_APP_SECRET` | 微信公众号AppSecret | 是 |
| `WECHAT_TOKEN_CACHE_DIR` | Token缓存目录 | 否 (默认: /app/.cache) |

### 健康检查

服务运行在 8080 端口，MCP 客户端可连接进行健康检查。
