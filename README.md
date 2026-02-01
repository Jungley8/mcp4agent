# MCP4Agent - 多功能MCP服务器

微信公众号管理工具，支持文章发布、草稿管理等功能。同时提供 Docker 容器监控功能。

## 项目结构

```
mcp4agent/
├── src/
│   ├── wechat_mcp/          # 微信公众号 MCP 包
│   │   ├── __init__.py
│   │   ├── server.py        # FastMCP 服务器和工具
│   │   ├── api.py           # 微信 API 封装
│   │   ├── config.py        # 配置管理
│   │   └── token_cache.py   # Token 缓存
│   ├── docker_status/       # Docker 监控 MCP 包
│   │   ├── __init__.py
│   │   └── server.py        # Docker 工具
│   ├── __init__.py          # 导出两个 MCP 应用
│   └── __main__.py          # 入口点
├── tests/
├── Dockerfile               # 优化构建（BuildKit 缓存）
├── docker-compose.yml
├── pyproject.toml           # 多包配置
└── README.md
```

## 功能特性

### 📝 微信公众号工具
- `create_draft` - 创建草稿
- `upload_image` - 上传图片
- `list_drafts` - 列出草稿
- `publish_draft` - 发布草稿（需要权限）

### 🐳 Docker 监控工具
- `list_containers` - 列出所有容器及状态
- `get_container_stats` - 查看容器资源使用（CPU/内存/网络）
- `get_container_logs` - 获取容器日志
- `restart_container` - 重启容器

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

### 运行微信公众号服务器

```bash
python -m mcp4agent --app wechat
```

### 运行 Docker 监控服务器

```bash
python -m mcp4agent --app docker
```

## Docker 监控使用

Docker 工具通过 Python `docker` 库连接 Docker 守护进程：

```python
# 列出所有运行中的容器
list_containers()

# 列出所有容器（包括已停止的）
list_containers(all_containers=True)

# 查看容器资源使用
get_container_stats("container_id_or_name")

# 获取容器日志
get_container_logs("container_id_or_name", lines=100)

# 重启容器
restart_container("container_id_or_name")
```

### 权限要求

使用 Docker 功能需要：
1. 运行 MCP 服务器的用户有权限访问 Docker socket
2. 通常需要将用户加入 docker 组：
   ```bash
   sudo usermod -aG docker $USER
   ```

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
DOCKER_BUILDKIT=1 docker build -t mcp4agent .
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
  --name mcp4agent \
  -p 8080:8080 \
  -e WECHAT_APP_ID=your_app_id \
  -e WECHAT_APP_SECRET=your_app_secret \
  -v $(pwd)/data:/app/.cache \
  mcp4agent
```

### 环境变量

| 变量 | 说明 | 必填 |
|------|------|------|
| `WECHAT_APP_ID` | 微信公众号AppID | 是 |
| `WECHAT_APP_SECRET` | 微信公众号AppSecret | 是 |
| `WECHAT_TOKEN_CACHE_DIR` | Token缓存目录 | 否 (默认: /app/.cache) |

### Docker in Docker 监控

要在容器内监控其他容器，需要挂载 Docker socket：

```bash
docker run -d \
  --name mcp4agent \
  -p 8080:8080 \
  -e WECHAT_APP_ID=your_app_id \
  -e WECHAT_APP_SECRET=your_app_secret \
  -v $(pwd)/data:/app/.cache \
  -v /var/run/docker.sock:/var/run/docker.sock \
  mcp4agent
```

⚠️ **注意**: 挂载 Docker socket 有安全风险，仅在可信环境中使用。

### 健康检查

服务运行在 8080 端口，MCP 客户端可连接进行健康检查。

## 更新日志

### v0.3.0
- 重构为多包架构 (mcp4agent)
- 分离 wechat_mcp 和 docker_status 为独立包
- 添加 BuildKit 缓存优化 Docker 构建
- 支持多平台构建

### v0.2.0
- 迁移到 FastMCP 框架
- 添加 Docker 容器监控功能
- 简化工具定义和使用
