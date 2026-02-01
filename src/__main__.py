"""MCP4Agent - Multi-package MCP server entry point"""
import sys

# Import both apps
from wechat_mcp import app as wechat_app
from docker_status import docker_app

if __name__ == "__main__":
    # For testing, run wechat app by default
    # Users can choose which app to run
    import argparse
    
    parser = argparse.ArgumentParser(description="MCP4Agent Server")
    parser.add_argument("--app", choices=["wechat", "docker"], default="wechat",
                        help="Which MCP app to run (default: wechat)")
    parser.add_argument("--port", type=int, default=8080, help="Port to listen on")
    
    args = parser.parse_args()
    
    if args.app == "wechat":
        print("Starting WeChat MCP Server...")
        wechat_app.run(port=args.port)
    else:
        print("Starting Docker Status MCP Server...")
        docker_app.run(port=args.port)
