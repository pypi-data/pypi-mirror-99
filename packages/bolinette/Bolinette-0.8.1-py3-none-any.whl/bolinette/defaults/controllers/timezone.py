from bolinette import web
from bolinette.decorators import controller, get
from bolinette.defaults.services import TimezoneService


@controller('tz', '/tz')
class TimezoneController(web.Controller):
    @property
    def tz_service(self) -> TimezoneService:
        return self.context.service('tz')

    @get('')
    async def all_timezones(self):
        """
        Gets all available IANA timezones
        """
        return self.response.ok(data=await self.tz_service.get_all())
