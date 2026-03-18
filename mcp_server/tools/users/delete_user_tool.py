from typing import Any

from mcp_server.tools.users.base import BaseUserServiceTool


class DeleteUserTool(BaseUserServiceTool):

    @property
    def name(self) -> str:
        return "delete_users"

    @property
    def description(self) -> str:
        return "Delete a user from the system by user ID"

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "id": {
                    "type": "number",
                    "description": "The user ID to delete"
                }
            },
            "required": ["id"]
        }

    async def execute(self, arguments: dict[str, Any]) -> str:
        # 1. Get int `id` from arguments
        user_id = int(arguments.get("id"))
        # 2. Call user_client delete_user and return its results (it is async, don't forget to await)
        return await self._user_client.delete_user(user_id)