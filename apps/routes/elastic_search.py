import logging
from types import NoneType

from fastapi import APIRouter, status, Depends
from fastapi.responses import UJSONResponse

from apps.services.elastic_search import search_post_worker, filling_worker
from config.es_connector import EsConnect

elastic_route = APIRouter(tags=['ElasticSearch'])

# connect to elastic
es = EsConnect()


@elastic_route.get("/search-post")
async def search_post_get(keywords: str):
    response = await search_post_worker(es, keywords)
    return response


@elastic_route.post("/filling", summary="Filling the Elastic with data from the database.")
async def filling():
    response = await filling_worker(es)
    return response
