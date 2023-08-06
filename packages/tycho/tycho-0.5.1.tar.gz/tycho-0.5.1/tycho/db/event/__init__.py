import asyncio
import pymongo
import queue as q
import random

from pymongo.errors import DuplicateKeyError
from aiohttp.web import HTTPNotFound

from ..utils import async_generator
from ...models.eventnode import EventNode
from ...models.event import Event as ModelEvent
from .deserialize import deserialize_db_event
from .serialize import serialize_to_db_event


MAX_RECURSIVE_DEPTH = 100
MAX_WAIT_TIME_SECONDS = 0.5


class Event:
    """
    Tycho stores events in a MongoDB database, with indices against tags, time created, and update time.

    The cardinality of the keys is not a concern, as regardless of the key value, the
    index will include the raw value. To ensure that the keys and values themselves are
    not too large (which would impact record size), there is a 100 character limit.

    Queries that span both a key:value with a larger number of records, and a long time
    frame, will result in a scanning query, as MongoDB cannot build a compound index
    that includes both the tags and the update time. As such it is best to restrict time
    ranges to as short of a range as possible, and filter to a specific tag.
    """

    _collection = "event"

    indexes = [
        {"unique": False, "keys": [("tags", pymongo.ASCENDING)]},
        {"unique": False, "keys": [("time", pymongo.ASCENDING)]},
        {"unique": False, "keys": [("update_time", pymongo.ASCENDING)]},
    ]

    def __init__(self, collection):
        self.collection = collection

    async def save(self, data: ModelEvent):
        new_db_format = serialize_to_db_event(data)
        result = await self.collection.insert_one(new_db_format)
        return result

    async def find_one(self) -> ModelEvent:
        result = await self.collection.find_one()
        return deserialize_db_event(result)

    async def find_by_id(self, id) -> ModelEvent:
        document = None
        cursor = self.collection.find({"_id": id})
        while await cursor.fetch_next:
            document = cursor.next_object()
        if document is None:
            raise HTTPNotFound(text="cannot find event {0}".format(id))
        return deserialize_db_event(document)

    async def update_by_id(self, id, update_doc: ModelEvent, insert: bool = False):
        new_data = serialize_to_db_event(update_doc)

        retries = 1
        while retries >= 0:
            try:
                result = await self.collection.find_one_and_replace(
                    {"_id": id}, new_data, upsert=insert
                )
                return result
            except DuplicateKeyError:
                await asyncio.sleep(random.uniform(0.0, MAX_WAIT_TIME_SECONDS))
                retries -= 1
                if retries < 0:
                    raise

    async def find_by_parent_id(self, id):
        cursor = self.collection.find({"tags": {"$in": ["parent_id:{0}".format(id)]}})
        return async_generator(cursor, deserialize_db_event)

    async def find(
        self, tags=None, frm=None, to=None, use_update_time=False, count=100, page=1
    ):
        if count < 0:
            raise ValueError("Count must be greater than or equal to zero.")

        if page < 1:
            raise ValueError("Page count must be greater than or equal to one.")

        time_field = "update_time" if use_update_time else "time"

        query = {}
        if tags is not None:
            query["tags"] = {"$all": tags}

        # optimize common use case
        # https://docs.mongodb.com/manual/core/multikey-index-bounds/
        if frm and to and not use_update_time:
            query[time_field] = {"$elemMatch": {"$gte": frm, "$lt": to,}}
        else:
            if frm is not None:
                query[time_field] = {"$gte": frm}
            if to is not None:
                if query.get(time_field) is None:
                    query[time_field] = {"$lt": to}
                else:
                    query[time_field]["$lt"] = to

        cursor = (
            self.collection.find(query)
            .sort([(time_field, -1)])
            .skip((page - 1) * count)
            .limit(count)
        )
        return async_generator(cursor, deserialize_db_event)

    async def get_tree(self, id):
        root_event = await self.find_by_id(id)
        root_event_node = EventNode(event=root_event)
        queue = q.Queue()
        queue.put(root_event_node)
        while not queue.empty():
            event_node = queue.get()
            children = await self.find_by_parent_id(event_node.event.id)
            async for child in children:
                child_node = EventNode(event=child)
                if child_node not in event_node.children:
                    event_node.children.append(child_node)
                queue.put(child_node)
        return root_event_node

    async def trace(self, event_id):
        """ return back the root-level parent id of the event """
        result = []

        currId = event_id
        curr_depth = 0
        while currId and curr_depth < MAX_RECURSIVE_DEPTH:
            try:
                doc = await self.find_by_id(currId)
                result.append(doc)
                currId = doc.parent_id
                curr_depth += 1
            except HTTPNotFound:
                currId = None
        return result

    async def delete_by_id(self, id) -> bool:
        """ deletes event with provided id and returns True otherwise False"""
        result_map = {0: False, 1: True, None: False}
        result = await self.collection.delete_one({"_id": id})
        return result_map[result.deleted_count]
