# server.py
from mcp.server.fastmcp import FastMCP

# ساخت سرور MCP با نام دلخواه
mcp = FastMCP("Diabetes Assistant")

# تعریف یک ابزار ساده برای جمع دو عدد
@mcp.tool()
def add(a: int, b: int) -> int:
    """جمع دو عدد"""
    return a + b

# تعریف یک منبع ساده با پارامتر
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """سلام شخصی‌سازی شده"""
    return f"سلام {name} عزیز! خوش اومدی."
