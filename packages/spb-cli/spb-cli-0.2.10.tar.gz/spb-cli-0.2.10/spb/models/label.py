import json
from spb.orm.type_base import Type
from spb.orm.json_type import JsonObject
from spb.orm import Model
from spb.orm import AttributeModel
from spb.orm import ListAttribute
from spb.orm.type import String, ID, Number, Object, List


class Stats(ListAttribute):
    def __init__(self, *args, **kwargs):
        self.name = kwargs['name'] if 'name' in kwargs else None
        self.count = kwargs['count'] if 'count' in kwargs else None

class Tags(ListAttribute):
    def __init__(self, *args, **kwargs):
        self.name = kwargs['name'] if 'name' in kwargs else None

class Label(Model):
    MODEL_UUID = '16be2af8-958b-11ea-bb37-0242ac130002'
    RESOURCE_NAME = 'labels'

    # id
    id = ID(property_name='id', immutable=True, filterable=True)
    project_id = ID(property_name='projectId', filterable=True)
    tags = Object(property_name='tags', express=Tags, filterable=True)

    # basic info
    status = String(property_name='status', immutable=True, filterable=True)
    stats = Object(property_name='stats', immutable=True, express=Stats)

    # For assets
    data_id = ID(property_name='dataId', immutable=True)
    dataset = String(property_name='dataset', immutable=True, filterable=True)
    data_key = String(property_name='dataKey', immutable=True, filterable=True)
    data_url = String(property_name='dataUrl', immutable=True)

    # label datas
    result = JsonObject(property_name='result')

    def toJson(self):
        return json.dumps({
            'id': self.id,
            'project_id': self.project_id,
            'status': self.status,
            'stats': [stat.get_datas(stat) for stat in self.stats] if self.stats is not None else None,
            'tags': [tag.get_datas(tag) for tag in self.tags] if self.tags is not None else None,
            'data_id': self.data_id,
            'dataset': self.dataset,
            'data_key': self.data_key,
            'result': self.result
        }, indent=4)

