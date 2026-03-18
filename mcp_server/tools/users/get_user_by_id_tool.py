from typing import Any

from mcp_server.tools.users.base import BaseUserServiceTool


class GetUserByIdTool(BaseUserServiceTool):

    @property
    def name(self) -> str:
        return "get_user_by_id"

    @property
    def description(self) -> str:
        return "Get user information by user ID"

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "id": {
                    "type": "number",
                    "description": "The user ID to retrieve"
                }
            },
            "required": ["id"]
        }

    async def execute(self, arguments: dict[str, Any]) -> str:
        # 1. Get int `id` from arguments
        user_id = int(arguments.get("id"))
        # 2. Call user_client get_user and return its results (it is async, don't forget to await)
        return await self._user_client.get_user(user_id)