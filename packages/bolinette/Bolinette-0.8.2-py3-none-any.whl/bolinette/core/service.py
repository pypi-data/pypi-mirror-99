from datetime import datetime
from typing import List, Dict, Any

from bolinette import blnt, core
from bolinette.blnt.objects import PaginationParams, OrderByParams
from bolinette.exceptions import EntityNotFoundError


class Service:
    __blnt__: 'ServiceMetadata' = None

    def __init__(self, context: 'blnt.BolinetteContext'):
        self.context = context

    def __repr__(self):
        return f'<Service {self.__blnt__.name}>'

    @property
    def repo(self) -> core.Repository:
        return self.context.repo(self.__blnt__.model_name)

    async def get(self, identifier, *, safe=False):
        entity = await self.repo.get(identifier)
        if entity is None and not safe:
            raise EntityNotFoundError(model=self.__blnt__.name, key='id', value=identifier)
        return entity

    async def get_by(self, key: str, value):
        return await self.repo.get_by(key, value)

    async def get_first_by(self, key: str, value, *, safe=False):
        entity = await self.repo.get_first_by(key, value)
        if entity is None and not safe:
            raise EntityNotFoundError(model=self.__blnt__.name, key=key, value=value)
        return entity

    async def get_all(self, *, pagination: PaginationParams = None, order_by: List[OrderByParams] = None):
        return await self.repo.get_all(pagination, order_by)

    async def create(self, values: Dict[str, Any]):
        return await self.repo.create(values)

    async def update(self, entity, values: Dict[str, Any]):
        return await self.repo.update(entity, values)

    async def patch(self, entity, values: Dict[str, Any]):
        return await self.repo.patch(entity, values)

    async def delete(self, entity):
        return await self.repo.delete(entity)


class SimpleService:
    __blnt__: 'ServiceMetadata' = None

    def __init__(self, context: 'blnt.BolinetteContext'):
        self.context = context

    def __repr__(self):
        return f'<Service {self.__blnt__.name}>'


class ServiceMetadata:
    def __init__(self, name: str, model_name: str):
        self.name = name
        self.model_name = model_name


class HistorizedService(Service):
    def __init__(self, context: 'blnt.BolinetteContext'):
        super().__init__(context)

    async def create(self, values, *, current_user=None):
        if current_user:
            now = datetime.utcnow()
            values['created_on'] = now
            values['created_by_id'] = current_user.id
            values['updated_on'] = now
            values['updated_by_id'] = current_user.id
        return await super().create(values)

    async def update(self, entity, values, *, current_user=None):
        if current_user:
            now = datetime.utcnow()
            values['created_on'] = entity.created_on
            values['created_by_id'] = entity.created_by_id
            values['updated_on'] = now
            values['updated_by_id'] = current_user.id
        return await super().update(entity, values)

    async def patch(self, entity, values, *, current_user=None):
        if current_user:
            now = datetime.utcnow()
            values['updated_on'] = now
            values['updated_by_id'] = current_user.id
        return await super().patch(entity, values)
