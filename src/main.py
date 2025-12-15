#!/usr/bin/env python3
# ==============================================================================
#                  Simple MCP Server - Demo Implementation
# ==============================================================================

"""A simple MCP server with practical utility tools.

This server demonstrates:
- Text manipulation tools
- Math operations
- Data formatting utilities
"""

from __future__ import annotations

import asyncio
import logging
import os

from dedalus_mcp import MCPServer, tool
from search import GoogleCustomSearch
from dotenv import load_dotenv
from typing import List
from models import SearchResult

load_dotenv()

# Suppress logs for clean output
for logger_name in ("mcp", "httpx", "uvicorn", "uvicorn.access", "uvicorn.error"):
    logging.getLogger(logger_name).setLevel(logging.CRITICAL)

server = MCPServer("simple-utility-server")
google = GoogleCustomSearch(api_key=os.getenv("GOOGLE_API_KEY"), search_engine_id=os.getenv("GOOGLE_SEARCH_ENGINE_ID"))

with server.binding():
    @tool(description="Find LinkedIn profiles by any keyword")
    def find_profiles(keyword: str) -> List[SearchResult]:
        search_results = google.search(keyword, substring="linkedin.com/in/")
        return search_results

    @tool(description="Find LinkedIn companies by any keyword")
    def find_companies(keyword: str) -> List[SearchResult]:
        search_results = google.search(keyword, substring="linkedin.com/company/")
        return search_results


async def main() -> None:
    """Start the MCP server on streamable-http transport."""
    print("🚀 Starting Simple Utility Server...")
    print("📡 Transport: streamable-http")
    print("🔧 Available tools: find_profiles, find_companies")
    print()
    await server.serve(transport="streamable-http", verbose=False, log_level="critical")


if __name__ == "__main__":
    asyncio.run(main())
