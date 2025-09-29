#!/usr/bin/env python3
"""
Example low-level MCP server demonstrating structured output support.

This example shows how to use the low-level server API to return
structured data from tools, with automatic validation against output
schemas.
"""

import asyncio
from datetime import datetime
from typing import Any

import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

# Create low-level server instance
server = Server("structured-output-lowlevel-example")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """List available tools with their schemas."""
    return [
        types.Tool(
            name="add",
            description="Add two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
            outputSchema={
                "type": "object",
                "properties": {
                    "result": {"type": "number", "description": "Sum of a and b"},
                },
                "required": ["result"],
            },
        ),
        types.Tool(
            name="subtract",
            description="Subtract two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
            outputSchema={
                "type": "object",
                "properties": {
                    "result": {"type": "number", "description": "Difference of a and b"},
                },
                "required": ["result"],
            },
        ),
        types.Tool(
            name="multiply",
            description="Multiply two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
            outputSchema={
                "type": "object",
                "properties": {
                    "result": {"type": "number", "description": "Product of a and b"},
                },
                "required": ["result"],
            },
        ),
        types.Tool(
            name="divide",
            description="Divide two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "Dividend"},
                    "b": {"type": "number", "description": "Divisor"},
                },
                "required": ["a", "b"],
            },
            outputSchema={
                "type": "object",
                "properties": {
                    "result": {"type": "number", "description": "Quotient of a and b"},
                },
                "required": ["result"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> Any:
    """
    Handle tool call with structured output.
    """
    if name == "add":
        a = arguments["a"]
        b = arguments["b"]
        return {"result": a + b}
    elif name == "subtract":
        a = arguments["a"]
        b = arguments["b"]
        return {"result": a - b}
    elif name == "multiply":
        a = arguments["a"]
        b = arguments["b"]
        return {"result": a * b}
    elif name == "divide":
        a = arguments["a"]
        b = arguments["b"]
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return {"result": a / b}
    else:
        raise ValueError(f"Unknown tool: {name}")


async def run():
    """Run the low-level server using stdio transport."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="structured-output-lowlevel-example",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(run())