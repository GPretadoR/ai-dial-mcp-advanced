from typing import Any

from mcp_server.models.user_info import UserUpdate
from mcp_server.tools.users.base import BaseUserServiceTool


class UpdateUserTool(BaseUserServiceTool):

    @property
    def name(self) -> str:
        return "update_user"

    @property
    def description(self) -> str:
        return "Update an existing user's information by user ID"

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "id": {
                    "type": "number",
                    "description": "User ID that should be updated"
                },
                "new_info": UserUpdate.model_json_schema()
            },
            "required": ["id"]
        }

    async def execute(self, arguments: dict[str, Any]) -> str:
        # 1. Get user `id` from `arguments`
        user_id = arguments.get("id")
        # 2. Get `new_info` from `arguments` and create `UserUpdate` via pydentic `UserUpdate.model_validate`
        new_info = UserUpdate.model_validate(arguments.get("new_info", {}))
        # 3. Call user_client update_user and return its results (it is async, don't forget to await)
        return await self._user_client.update_user(user_id, new_info)

