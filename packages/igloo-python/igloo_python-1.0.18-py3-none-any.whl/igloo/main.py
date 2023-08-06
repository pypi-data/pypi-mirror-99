import requests
import asyncio
import pathlib
import websockets
import json
from igloo.mutations import MutationRoot
from igloo.subscriptions import SubscriptionRoot
from igloo.utils import get_from_dict, _Undefined, UNDEFINED, undefined
from aiohttp import ClientSession
from .query import QueryRoot
import asyncio

host = "v1.igloo.ooo"
url = "https://{}/graphql".format(host)


class GraphQLException(Exception):
    pass


def exponential_backoff():
    yield 1
    yield 5

    while True:
        yield 20


class Client:
    def __init__(self, token, asynchronous=False):
        self.token = token
        self.session = ClientSession()
        self.asyncio = asynchronous

    def set_token(self, newToken):
        self.token = newToken

    def __del__(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__close__())

    async def __close__(self):
        await self.session.close()

    @property
    def query_root(self):
        return QueryRoot(self)

    @property
    def mutation_root(self):
        return MutationRoot(self)

    @property
    def subscription_root(self):
        return SubscriptionRoot(self)

    async def __async_query(self, query, variables=None, keys=[]):
        payload = {"query": query}
        if variables != None:
            payload["variables"] = variables

        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + self.token
        }

        async with self.session.post(url, data=json.dumps(payload), headers=headers) as response:
            parsedRes = await response.json()

        if "errors" in parsedRes.keys():
            raise GraphQLException(parsedRes["errors"][0]["message"])

        return get_from_dict(parsedRes, ["data", *keys])

    def __sync_query(self, query, variables=None, keys=[]):
        payload = {"query": query}
        if variables != None:
            payload["variables"] = variables

        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + self.token
        }

        response = requests.request(
            "POST", url, data=json.dumps(payload), headers=headers)

        parsedRes = json.loads(response.text)
        if "errors" in parsedRes.keys():
            raise GraphQLException(parsedRes["errors"][0]["message"])

        return get_from_dict(parsedRes, ["data", *keys])

    def query(self, query, variables=None, keys=[], asyncio=None):
        if asyncio == False or (asyncio is None and not self.asyncio):
            return self.__sync_query(query, variables=variables, keys=keys)
        else:
            return self.__async_query(query, variables=variables, keys=keys)

    mutation = query

    async def _subscribe(self, query):
        async with websockets.connect(
                'wss://{}/subscriptions'.format(host), ssl=True, subprotocols=["graphql-ws"]) as websocket:
            await websocket.send('{"type":"connection_init","payload":{"Authorization":"Bearer %s"}}' % (self.token))

            res = await websocket.recv()
            if json.loads(res)["type"] != "connection_ack":
                raise Exception("failed to connect")

            # TODO: escape better the query
            listen_query_message = '{"id":"1","type":"start","payload":{"query":"%s","variables":null}}' % (
                query.replace('"', '\\"').replace('\n', '\\n')
            )
            await websocket.send(listen_query_message)
            while True:
                response = await websocket.recv()
                parsedResponse = json.loads(response)
                if parsedResponse["type"] == "data":
                    if "errors" in parsedResponse["payload"].keys():
                        raise GraphQLException(
                            parsedResponse["payload"]["errors"][0]["message"])
                    else:
                        yield parsedResponse["payload"]["data"]

    async def subscribe(self, query, autoreconnect=True):
        for backoff in exponential_backoff():
            try:
                async for res in self._subscribe(query):
                    yield res
            except GraphQLException:
                raise
            except Exception:
                if not autoreconnect:
                    raise
                await asyncio.sleep(backoff)
