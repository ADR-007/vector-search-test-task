import os
from enum import StrEnum

import weaviate as wv


def get_weaviate_client() -> wv.WeaviateClient:
    return wv.connect_to_local(
        host=os.getenv('WEAVIATE_HOST', 'localhost'),
    )


class WikiCollectionField(StrEnum):
    COLLECTION_NAME = 'Wiki'

    PAGE = 'page'
    CHUNK_INDEX = 'chunk_index'
    CHUNK_CONTENT = 'chunk_content'
