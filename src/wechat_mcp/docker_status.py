"""Docker容器监控工具 - FastMCP 2.x"""
import docker
from docker.errors import DockerException, NotFound
from typing import Optional, Dict, Any, List
from fastmcp import FastMCP

# 创建Docker监控的FastMCP实例
docker_app = FastMCP("docker-mcp")


def get_client() -> docker.DockerClient:
    """获取Docker客户端"""
    return docker.from_env()


@docker_app.tool()
def list_containers(all_containers: bool = False) -> str:
    """
    列出所有Docker容器及其状态
    
    Args:
        all_containers: 是否显示所有容器（包括已停止的），默认只显示运行中的
    
    Returns:
        容器列表信息
    """
    try:
        client = get_client()
        containers = client.containers.list(all=all_containers)
        
        if not containers:
            return "📦 暂无容器"
        
        result = "🐳 Docker容器列表：\n\n"
        result += f"{'ID':<15} {'名称':<25} {'镜像':<30} {'状态':<15} {'端口'}\n"
        result += "-" * 100 + "\n"
        
        for c in containers:
            short_id = c.short_id[:12]
            name = c.name[:24]
            image = c.image.tags[0] if c.image.tags else c.image.short_id[:28]
            status = c.status
            ports = ", ".join(p for p in c.ports) if c.ports else "-"
            
            result += f"{short_id:<15} {name:<25} {image:<30} {status:<15} {ports}\n"
        
        return result
        
    except DockerException as e:
        return f"❌ Docker连接失败: {str(e)}"


@docker_app.tool()
def get_container_stats(container_id: str) -> str:
    """
    获取容器的CPU、内存、网络使用情况
    
    Args:
        container_id: 容器ID或名称
    
    Returns:
        容器资源使用统计
    """
    try:
        client = get_client()
        container = client.containers.get(container_id)
        
        stats = container.stats(stream=False)
        
        # 计算CPU使用率
        cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - \
                    stats["precpu_stats"]["cpu_usage"]["total_usage"]
        system_delta = stats["cpu_stats"]["system_cpu_usage"] - \
                       stats["precpu_stats"]["system_cpu_usage"]
        cpu_count = stats["cpu_stats"].get("online_cpus", 1)
        
        if system_delta > 0 and cpu_delta > 0:
            cpu_percent = (cpu_delta / system_delta) * cpu_count * 100.0
        else:
            cpu_percent = 0.0
        
        # 计算内存使用率
        memory_usage = stats["memory_stats"]["usage"]
        memory_limit = stats["memory_stats"]["limit"]
        memory_percent = (memory_usage / memory_limit) * 100.0
        
        # 格式化输出
        result = f"📊 容器 {container.short_id} ({container.name}) 资源统计：\n\n"
        result += f"🖥️  CPU使用率: {cpu_percent:.2f}%\n"
        result += f"💾 内存使用: {memory_usage / 1024 / 1024:.2f} MB / {memory_limit / 1024 / 1024:.2f} MB ({memory_percent:.2f}%)\n"
        
        # 网络IO
        networks = stats.get("networks", {})
        if networks:
            rx_bytes = sum(n["rx_bytes"] for n in networks.values())
            tx_bytes = sum(n["tx_bytes"] for n in networks.values())
            result += f"🌐 网络: 接收 {rx_bytes / 1024:.2f} KB, 发送 {tx_bytes / 1024:.2f} KB\n"
        
        return result
        
    except NotFound:
        return f"❌ 容器未找到: {container_id}"
    except DockerException as e:
        return f"❌ Docker错误: {str(e)}"


@docker_app.tool()
def get_container_logs(container_id: str, lines: int = 50, tail: bool = False) -> str:
    """
    获取容器的日志输出
    
    Args:
        container_id: 容器ID或名称
        lines: 日志行数，默认50
        tail: 是否从尾部开始查看，默认False（从头部）
    
    Returns:
        容器日志
    """
    try:
        client = get_client()
        container = client.containers.get(container_id)
        
        logs = container.logs(
            stream=False,
            tail="all" if tail else lines,
            timestamps=False
        )
        
        # 解码日志
        if isinstance(logs, bytes):
            logs = logs.decode("utf-8", errors="replace")
        
        # 截取指定行数
        log_lines = logs.split("\n")
        if not tail and len(log_lines) > lines:
            log_lines = log_lines[-lines:]
        
        result = f"📋 容器 {container.name} 日志（最近{lines}行）：\n\n"
        result += "\n".join(log_lines)
        
        return result
        
    except NotFound:
        return f"❌ 容器未找到: {container_id}"
    except DockerException as e:
        return f"❌ Docker错误: {str(e)}"


@docker_app.tool()
def restart_container(container_id: str) -> str:
    """
    重启Docker容器
    
    Args:
        container_id: 容器ID或名称
    
    Returns:
        操作结果消息
    """
    try:
        client = get_client()
        container = client.containers.get(container_id)
        
        container.restart(timeout=10)
        
        return f"✅ 容器 {container.short_id} ({container.name}) 已重启"
        
    except NotFound:
        return f"❌ 容器未找到: {container_id}"
    except DockerException as e:
        return f"❌ Docker错误: {str(e)}"
