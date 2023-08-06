
from aiodataloader import DataLoader
from igloo.models.utils import wrapWith


class FloatSeriesVariableLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{floatSeriesVariable(id:"%s"){%s}}' % (self._id, fields), keys=["floatSeriesVariable"])

        # if fetching object the key will be the first part of the field
        # e.g. when fetching thing{id} the result is in the thing key
        resolvedValues = [res[key.split("{")[0]] for key in keys]

        return resolvedValues


class FloatSeriesVariable:
    def __init__(self, client, id):
        self.client = client
        self._id = id
        self.loader = FloatSeriesVariableLoader(client, id)

    @property
    def id(self):
        return self._id

    @property
    def last_node(self):
        if self.client.asyncio:
            res = self.loader.load("lastNode{id}")
        else:
            res = self.client.query('{floatSeriesVariable(id:"%s"){lastNode{id}}}' % self._id, keys=[
                "floatSeriesVariable", "lastNode"])

        def wrapper(res):
            from .float_series_node import FloatSeriesNode
            return FloatSeriesNode(self.client, res["id"])

        return wrapWith(res, wrapper)

    @property
    def nodes(self):
        from .float_series_node import FloatSeriesNodeList
        return FloatSeriesNodeList(self.client, self._id)

    @property
    def name(self):
        if self.client.asyncio:
            return self.loader.load("name")
        else:
            return self.client.query('{floatSeriesVariable(id:"%s"){name}}' % self._id, keys=[
                "floatSeriesVariable", "name"])

    @name.setter
    def name(self, newName):
        self.client.mutation(
            'mutation{updateFloatSeriesVariable(id:"%s", name:"%s"){id}}' % (self._id, newName), asyncio=False)

    @property
    def developer_only(self):
        if self.client.asyncio:
            return self.loader.load("developerOnly")
        else:
            return self.client.query('{floatSeriesVariable(id:"%s"){developerOnly}}' % self._id, keys=[
                "floatSeriesVariable", "developerOnly"])

    @developer_only.setter
    def developer_only(self, newValue):
        self.client.mutation(
            'mutation{updateFloatSeriesVariable(id:"%s", developerOnly:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def hidden(self):
        if self.client.asyncio:
            return self.loader.load("hidden")
        else:
            return self.client.query('{floatSeriesVariable(id:"%s"){hidden}}' % self._id, keys=[
                "floatSeriesVariable", "hidden"])

    @hidden.setter
    def hidden(self, newValue):
        self.client.mutation(
            'mutation{updateFloatSeriesVariable(id:"%s", hidden:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def index(self):
        if self.client.asyncio:
            return self.loader.load("index")
        else:
            return self.client.query('{floatSeriesVariable(id:"%s"){index}}' % self._id, keys=[
                "floatSeriesVariable", "index"])

    @index.setter
    def index(self, newValue):
        self.client.mutation(
            'mutation{updateFloatSeriesVariable(id:"%s", index:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def shown_nodes(self):
        if self.client.asyncio:
            return self.loader.load("index")
        else:
            return self.client.query('{floatSeriesVariable(id:"%s"){shownNodes}}' % self._id, keys=[
                "floatSeriesVariable", "shownNodes"])

    @shown_nodes.setter
    def shown_nodes(self, newValue):
        self.client.mutation(
            'mutation{updateFloatSeriesVariable(id:"%s", shownNodes:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def stored_nodes(self):
        if self.client.asyncio:
            return self.loader.load("index")
        else:
            return self.client.query('{floatSeriesVariable(id:"%s"){storedNodes}}' % self._id, keys=[
                "floatSeriesVariable", "storedNodes"])

    @stored_nodes.setter
    def stored_nodes(self, newValue):
        self.client.mutation(
            'mutation{updateFloatSeriesVariable(id:"%s", storedNodes:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def my_role(self):
        if self.client.asyncio:
            return self.loader.load("myRole")
        else:
            return self.client.query('{floatSeriesVariable(id:"%s"){myRole}}' % self._id, keys=[
                "floatSeriesVariable", "myRole"])

    @property
    def createdAt(self):
        if self.client.asyncio:
            return self.loader.load("createdAt")
        else:
            return self.client.query('{floatSeriesVariable(id:"%s"){createdAt}}' % self._id, keys=[
                "floatSeriesVariable", "createdAt"])

    @property
    def updatedAt(self):
        if self.client.asyncio:
            return self.loader.load("updatedAt")
        else:
            return self.client.query('{floatSeriesVariable(id:"%s"){updatedAt}}' % self._id, keys=[
                "floatSeriesVariable", "updatedAt"])

    async def _async_load_thing(self):
        id = await self.loader.load("thing{id}")["id"]
        from .thing import Thing
        return Thing(self.client, id)

    @property
    def thing(self):
        if self.client.asyncio:
            return self._async_load_thing()
        else:
            id = self.client.query('{floatSeriesVariable(id:"%s"){thing{id}}}' % self._id, keys=[
                "floatSeriesVariable", "thing", "id"])

            from .thing import Thing
            return Thing(self.client, id)

    @property
    def unit_of_measurement(self):
        if self.client.asyncio:
            return self.loader.load("unitOfMeasurement")
        else:
            return self.client.query('{floatSeriesVariable(id:"%s"){unitOfMeasurement}}' % self._id, keys=[
                "floatSeriesVariable", "unitOfMeasurement"])

    @unit_of_measurement.setter
    def unit_of_measurement(self, newValue):
        self.client.mutation(
            'mutation{updateFloatSeriesVariable(id:"%s", unitOfMeasurement:"%s"){id}}' % (self._id, newValue), asyncio=False)

    @property
    def precision(self):
        if self.client.asyncio:
            return self.loader.load("precision")
        else:
            return self.client.query('{floatSeriesVariable(id:"%s"){precision}}' % self._id, keys=[
                "floatSeriesVariable", "precision"])

    @precision.setter
    def precision(self, newValue):
        self.client.mutation(
            'mutation{updateFloatSeriesVariable(id:"%s", precision:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def min(self):
        if self.client.asyncio:
            return self.loader.load("min")
        else:
            return self.client.query('{floatSeriesVariable(id:"%s"){min}}' % self._id, keys=[
                "floatSeriesVariable", "min"])

    @min.setter
    def min(self, newValue):
        self.client.mutation(
            'mutation{updateFloatSeriesVariable(id:"%s", min:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def max(self):
        if self.client.asyncio:
            return self.loader.load("max")
        else:
            return self.client.query('{floatSeriesVariable(id:"%s"){max}}' % self._id, keys=[
                "floatSeriesVariable", "max"])

    @max.setter
    def max(self, newValue):
        self.client.mutation(
            'mutation{updateFloatSeriesVariable(id:"%s", max:%s){id}}' % (self._id, newValue), asyncio=False)
