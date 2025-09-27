"""
MCP (Model Context Protocol) module for Universal Scraper

This module provides a clean, modular MCP server implementation using OOP principles.
The MCP server exposes the Universal Scraper functionality as tools that can be used by AI models.
"""

from .server import UniversalScraperMCPServer
from .tools import ToolManager
from .validators import URLValidator
from .exceptions import MCPServerError, ValidationError

__all__ = [
    "UniversalScraperMCPServer",
    "ToolManager",
    "URLValidator",
    "MCPServerError",
    "ValidationError"
]
