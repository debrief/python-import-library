from sqlalchemy import types
from sqlalchemy.types import Binary
from sqlalchemy.schema import Column
import uuid


class UUID(types.TypeDecorator):
    #impl = MSBinary
    impl = Binary
    def __init__(self):
        self.impl.length = 16
        types.TypeDecorator.__init__(self, length=self.impl.length)

    def process_bind_param(self, value, dialect=None):
        if value and isinstance(value, uuid.UUID):
            return value.bytes
        elif value and not isinstance(value, uuid.UUID):
            raise ValueError(f'value {value} is not a valid uuid.UUID')
        else:
            return None

    def process_result_value(self, value, dialect=None):
        if value:
            return uuid.UUID(bytes=value)
        else:
            return None

    def is_mutable(self):
        return False
#
#
# id_column_name = "id"
#
# def id_column():
#     import uuid
#     return Column(id_column_name,UUID(),primary_key=True,default=uuid.uuid4)
#
# #usage
# my_table = Table('test',metadata,id_column(),Column('parent_id',UUID(),ForeignKey(table_parent.c.id)))