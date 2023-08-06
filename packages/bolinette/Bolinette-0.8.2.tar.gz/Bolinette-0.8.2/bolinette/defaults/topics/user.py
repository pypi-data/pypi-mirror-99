from aiohttp import web as aio_web

from bolinette import web
from bolinette.decorators import topic


@topic('user')
class UserTopic(web.Topic):
    async def validate_subscription(self, socket: aio_web.WebSocketResponse, payload, current_user) -> bool:
        if current_user is None:
            await self.send_error(socket, f'user.{payload["channel"]}.require_auth')
            return False
        if not any([r for r in current_user.roles if r.name == payload['channel']]):
            await self.send_error(socket, f'user.{payload["channel"]}.forbidden')
            return False
        return True
