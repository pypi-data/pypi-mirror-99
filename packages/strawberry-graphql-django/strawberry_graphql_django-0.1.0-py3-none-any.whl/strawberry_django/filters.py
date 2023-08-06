from . import utils
import dataclasses
import strawberry
import typing
import django.core.exceptions

lookups = ('exact', 'iexact', 'contains', 'icontains', 'in',
        'gt', 'gte', 'lt', 'lte',
        'startswith', 'istartswith', 'endswith', 'iendswidth',
        'range', 'isnull', 'regex', 'iregex')

#LookupValueType = typing.Optional[typing.Any]
#LookupValueType = typing.Union[jstr, int, None]

def get_field_type(lookup, field_type):
    if lookup in ('in', 'range'):
        field_type = typing.List[field_type]
    elif lookup in ('regex', 'iregex'):
        field_type = str
    elif lookup in ('isnull'):
        field_type = bool
    return typing.Optional[field_type]

def gen_field_lookups(field_name, field_type):
    fields = [ (f'{field_name}__{lookup}', get_field_type(lookup, field_type)) for lookup in lookups ]
    return fields

def gen_filter_type(object_type):
    global cls
    model = object_type._django_model
    type_name = f'{model._meta.object_name}FilterType'
    fields = [
    #    ('OR', cls),
    #    ('OR', type_name),
    #    ('NOT', type_name),
    ]
    for field in dataclasses.fields(object_type):
        try:
            model_field = model._meta.get_field(field.name)
        except django.core.exceptions.FieldDoesNotExist:
            continue
        if model_field.is_relation:
            continue

        fields += gen_field_lookups(field.name, field.type)

    cls = dataclasses.make_dataclass(type_name, fields)
    #cls.__annotations__['OR'] = typing.Optional[typing.List[cls]]
    #cls.__annotations__['NOT'] = typing.Optional[typing.List[cls]]
    #cls.__annotations__['OR'] = typing.Optional['cls']
    cls = strawberry.input(cls)
    return cls



