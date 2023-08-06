from bergen.extenders.pod import PodExtender
from bergen.types.model import ArnheimModelManager
from bergen.extenders.user import UserExtender
from bergen.queries.delayed.node import CREATE_NODE_MUTATION, NODE_FILTER_QUERY, NODE_QUERY, UPDATE_OR_CREATE_NODE
from bergen.queries.delayed.pod import POD_QUERY
from bergen.extenders.node import NodeExtender
from bergen.schema import Node as SchemaNode
from bergen.schema import Pod as SchemaPod
from bergen.schema import User as SchemaUser
from bergen.schema import *
try:
	# python 3.8
	from typing import ForwardRef, Type
except ImportError:
	# ForwardRef is private in python 3.6 and 3.7
	from typing import _ForwardRef as ForwardRef, Type

Node = ForwardRef('Node')

class NodeManager(ArnheimModelManager[Node]):
    pass


class Node(NodeExtender, SchemaNode):
    __slots__ = ("_loop", "_force_sync", "_postman", "_ui")

    objects = NodeManager()

    class Meta:
        overwrite_default = True
        identifier = "node"
        filter = NODE_FILTER_QUERY
        get = NODE_QUERY
        update_or_create = UPDATE_OR_CREATE_NODE



class Pod(PodExtender, SchemaPod):
    __slots__ = ("_loop", "_force_sync", "_postman")

    objects = NodeManager()

    class Meta:
        overwrite_default = True
        identifier = "pod"
        get = POD_QUERY


class User(UserExtender, SchemaUser):

    class Meta:
        overwrite_default = True
        identifier = "user"
