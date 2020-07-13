"""
Classes defined in this file are used with Mongodb ORM library mongoengine
For more information, Please refer to its website: http://mongoengine.org/
"""
from mongoengine import DynamicDocument
from mongoengine import StringField, IntField, ListField

class ThingDescription(DynamicDocument):
    """ORM class of Thing Description in the mongodb

    """
    thing_type = StringField(db_field='thing_type', max_length=20)
    thing_id = StringField(db_field='thing_id',
                           required=True, unique=True, max_length=160)
    publicity = IntField(db_field='publicity', default=0)

    meta = {
        'collection': 'td',
        'indexes': [
            "thing_type",
            [("properties.geo.coordinates", "2dsphere")]
        ]
    }

    def __str__(self):
        return f"type: {self.thing_type}\tthing_id: {self.thing_id}\tpublicity: {self.publicity}"


class DirectoryNameToURL(DynamicDocument):
    """ORM class that represents the mapping between directory name and corresponding URL

    """
    directory_name = StringField(db_field='loc')
    url = StringField(db_field='url')
    relationship = StringField(db_field='relationship')

    meta = {'collection': 'loc_to_url'}

    def __str__(self):
        return f"Directory Name : {self.directory_name} --- URL : {self.url}"


class TypeToChildrenNames(DynamicDocument):
    """Class Contains the list of child locaions that has a certain type of devices
    """
    thing_type = StringField(db_field='type')
    children_names = ListField(StringField(), db_field='childLocs')

    meta = {'collection': 'type_to_childLocs'}


class TargetToChildName(DynamicDocument):
    """ORM class that represents tha mapping `target_name` => `child_name`

    In order to reach the 'target_name, what should the next search node at the current node
    for example: "target_name": "level3" -> "child_name": "level2" means level3 node is behind level2 node in the hierarchy
    """
    target_name = StringField(db_field='targetLoc')
    child_name = StringField(db_field='childLoc')
    meta = {'collection': 'targetLoc_to_childLoc'}
