import logging
from types import NoneType
from fastapi import status, Depends

from fastapi.responses import UJSONResponse

log = logging.getLogger("uvicorn")


async def search_post_worker(es, keywords):
    response = await es.search_document(index="posts", query=keywords)
    if type(response) == NoneType or len(response) == 0:
        return UJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content="No information was found for the word you entered !"
        )
    return response


async def filling_worker(es):
    log.info("Initialize filling Elastic from DB...")
    await es.populate_es()
    log.info("Finish filling Elastic")
    return UJSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Successfully initialize !"}
    )
