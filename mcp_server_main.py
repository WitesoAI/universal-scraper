#!/usr/bin/env python3
"""
Standalone MCP Server for Universal Scraper

Entry point for running the Universal Scraper as an MCP server.

Usage:
    python mcp_server_main.py
"""

import asyncio
import sys
import logging
from universal_scraper.core.mcp.server import create_and_run_server

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("universal-scraper-mcp")


def main_entry():
    """Main entry point for the MCP server console script"""
    try:
        logger.info("Starting Universal Scraper MCP Server")
        asyncio.run(create_and_run_server())
    except KeyboardInterrupt:
        logger.info("MCP Server stopped by user")
        print("\nMCP Server stopped by user", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        logger.error(f"MCP Server error: {e}", exc_info=True)
        print(f"MCP Server error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main_entry()