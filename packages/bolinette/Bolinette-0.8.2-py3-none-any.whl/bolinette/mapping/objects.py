from abc import ABC
from typing import Union

from bolinette import core, mapping, types


class MappingObject(ABC):
    def __init__(self, *, key=None, name=None, default=None, required=False,
                 nullable=True, function=False, formatting=False):
        self.key = key
        self.name = name
        self.default = default
        self.required = required
        self.nullable = nullable
        self.function = function
        self.formatting = formatting
        if not self.name and self.key:
            self.name = self.key


class Field(MappingObject):
    def __init__(self, field_type, *, key=None, name=None, default=None, required=False,
                 nullable=True, function=None, formatting=None):
        super().__init__(key=key, name=name, default=default, required=required,
                         nullable=nullable, function=function, formatting=formatting)
        self.type = field_type

    def __repr__(self):
        return f'<MappingField {self.key}:{self.type} -> {self.name}>'


class Column(Field):
    def __init__(self, column: 'core.models.Column', *, name=None, default=None, required=False,
                 function=None, formatting=None):
        super().__init__(column.type, key=column.name, name=name, default=default, required=required,
                         nullable=column.nullable, function=function, formatting=formatting)


class List(MappingObject):
    def __init__(self, element: Union['types.db.DataType', 'mapping.Definition'], *,
                 key=None, name=None, default=None, required=False, function=None, formatting=None):
        super().__init__(key=key, name=name, default=default, required=required,
                         function=function, formatting=formatting)
        self.element = element

    def __repr__(self):
        return f'<MappingList {self.name}:[{repr(self.element)}]>'


class Definition(MappingObject):
    def __init__(self, model_name, model_key='default', *, key=None, name=None, default=None,
                 required=False, function=None, formatting=None):
        super().__init__(key=key, name=name, default=default, required=required,
                         function=function, formatting=formatting)
        self.fields = []
        self.model_name = model_name
        self.model_key = model_key

    def __repr__(self):
        return f'<MappingModel {self.model_name}.{self.model_key}>'


class Reference(Definition):
    def __init__(self, relationship: 'core.models.Relationship', model_key='default', *, name=None, default=None,
                 required=False, function=None, formatting=None):
        super().__init__(relationship.target_model_name, model_key, key=relationship.name, name=name, default=default,
                         required=required, function=function, formatting=formatting)
        self.foreign_key = relationship.foreign_key.name
        self.reference_model = relationship.foreign_key.reference.target_model_name
        self.reference_key = relationship.foreign_key.reference.target_column_name
