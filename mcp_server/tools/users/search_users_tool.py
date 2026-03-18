from typing import Any

from mcp_server.tools.users.base import BaseUserServiceTool


class SearchUsersTool(BaseUserServiceTool):

    @property
    def name(self) -> str:
        return "search_users"

    @property
    def description(self) -> str:
        return "Search for users by name, surname, email, or gender"

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "User's name to search for"
                },
                "surname": {
                    "type": "string",
                    "description": "User's surname to search for"
                },
                "email": {
                    "type": "string",
                    "description": "User's email to search for"
                },
                "gender": {
                    "type": "string",
                    "description": "User's gender to search for"
                }
            },
            "required": []
        }

    async def execute(self, arguments: dict[str, Any]) -> str:
        # Call user_client search_users (with `**arguments`) and return its results (it is async, don't forget to await)
        return await self._user_client.search_users(**arguments)