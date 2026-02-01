"""MCP4Agent - Multi-package MCP server entry point"""
import sys
import argparse
from multiprocessing import Process

# Import both apps
from wechat_mcp import app as wechat_app
from docker_status import docker_app


def run_wechat(port: int = 8080):
    """启动微信 MCP 服务"""
    print(f"🚀 启动 WeChat MCP Server (端口: {port})...")
    wechat_app.run(transport="http", host="0.0.0.0", port=port, path="/mcp")


def run_docker(port: int = 8081):
    """启动 Docker 监控服务"""
    print(f"🐳 启动 Docker Status MCP Server (端口: {port})...")
    docker_app.run(transport="http", host="0.0.0.0", port=port, path="/mcp")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MCP4Agent Server")
    parser.add_argument("--app", choices=["wechat", "docker", "all"], default="all",
                        help="Which MCP app to run (default: all)")
    parser.add_argument("--wechat-port", type=int, default=8080, 
                        help="Port for WeChat MCP (default: 8080)")
    parser.add_argument("--docker-port", type=int, default=8081,
                        help="Port for Docker Status MCP (default: 8081)")
    
    args = parser.parse_args()
    
    if args.app == "all":
        print("🚀🚀 启动全部 MCP 服务...")
        p_wechat = Process(target=run_wechat, args=(args.wechat_port,))
        p_docker = Process(target=run_docker, args=(args.docker_port,))
        
        p_wechat.start()
        p_docker.start()
        
        print(f"✅ WeChat MCP: http://0.0.0.0:{args.wechat_port}/mcp")
        print(f"✅ Docker MCP: http://0.0.0.0:{args.docker_port}/mcp")
        print("\n按 Ctrl+C 停止所有服务")
        
        try:
            p_wechat.join()
            p_docker.join()
        except KeyboardInterrupt:
            print("\n🛑 正在停止服务...")
            p_wechat.terminate()
            p_docker.terminate()
    
    elif args.app == "wechat":
        run_wechat(args.wechat_port)
    
    else:  # docker
        run_docker(args.docker_port)
