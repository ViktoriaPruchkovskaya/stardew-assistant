from .mcp_client import MCPClient


class IOCContainer:
    def __init__(self, mcp_client_service: MCPClient):
        self.mcp_client_service = mcp_client_service
