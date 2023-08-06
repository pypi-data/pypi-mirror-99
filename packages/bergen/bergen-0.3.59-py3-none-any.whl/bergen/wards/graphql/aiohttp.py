from abc import ABC
from bergen.wards.graphql.base import BaseGraphQLWard, GraphQLException

from gql.gql import gql
from bergen.wards.base import BaseWard
from bergen.query import GQL, TypedGQL
from gql.transport.aiohttp import AIOHTTPTransport
import logging
from gql.transport.aiohttp import log as aiohttp_logger
from gql.transport.requests import RequestsHTTPTransport


aiohttp_logger.setLevel(logging.WARNING)
import asyncio
from gql import Client, gql
import requests

class AIOHttpGraphQLWard(BaseGraphQLWard):
    can_subscribe = False

    def __init__(self, port, host, protocol, token, loop=None) -> None:
        super().__init__(port=port, host=host, protocol=protocol, token=token, loop=loop)

    async def configure(self):
        self.transport = AIOHTTPTransport(url=self._graphql_endpoint, headers=self._headers)
        await self.transport.connect()


    async def run_async(self, the_query: TypedGQL, variables: dict = {}, **kwargs):
        query_node = gql(the_query.query)

        response = await self.transport.execute(query_node, variable_values=variables)
        if response.errors:
            raise GraphQLException(str(response.errors))
        return the_query.extract(response.data)

    async def disconnect(self):
        await self.transport.close()