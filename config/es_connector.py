from elasticsearch import AsyncElasticsearch
from sqlalchemy import desc
from sqlalchemy.orm import Session

from apps import models
from config.db import get_db
from config.settings import settings


class EsConnect:
    def __init__(self) -> None:
        self.es_client = None
        self.connect()  # noqa

    def connect(self):
        es = AsyncElasticsearch(settings.ELASTICSEARCH_CONNECT)
        self.es_client = es

    async def search_document(self, index="posts", query="Hello world !"):
        try:
            response = await self.es_client.search(
                index=index,
                body={
                    "query": {
                        "multi_match": {
                            "query": query
                        }
                    }
                }
            )
            return [i['_source'] for i in response['hits']['hits']]
        except Exception as e:
            print(e)

    async def populate_es(self):
        db: Session = next(get_db())
        posts = db.query(models.Post).order_by(desc(models.Post.created_at)).all()
        for post in posts:
            e1 = {
                'id': post.id,
                'title': post.title,
                'description': post.description
            }

            await self.es_client.index(index='posts', id=post.id, document=e1)
