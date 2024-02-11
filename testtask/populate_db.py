import logging
from itertools import count
from pathlib import Path
from typing import Iterable

import weaviate as wv
import weaviate.classes as wvc

from testtask.weavate import get_weaviate_client, WikiCollectionField

logger = logging.getLogger(__name__)


def create_wiki_collection(client: wv.WeaviateClient) -> None:
    client.collections.create(
        name=WikiCollectionField.COLLECTION_NAME,
        description='Collection of Wikipedia articles',
        vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_transformers(
            vectorize_collection_name=False,
        ),
        properties=[
            wvc.config.Property(
                name=WikiCollectionField.PAGE,
                data_type=wvc.config.DataType.TEXT,
            ),
            wvc.config.Property(
                name=WikiCollectionField.CHUNK_INDEX,
                data_type=wvc.config.DataType.INT,
            ),
            wvc.config.Property(
                name=WikiCollectionField.CHUNK_CONTENT,
                description="Content that will be vectorized",
                data_type=wvc.config.DataType.TEXT,
                skip_vectorization=False,
                vectorize_property_name=False,
            ),
        ],
    )


def get_wiki_files(folder: Path) -> Iterable[Path]:
    for file in folder.iterdir():
        if file.is_file():
            yield file


def create_wiki_objects(
    client: wv.WeaviateClient,
    chunk_size: int,
    chunk_overlap: int,
) -> None:
    """Create Weaviate objects for Wikipedia articles.

    Chunk the articles into chunks of `chunk_size` words with `chunk_overlap` characters overlap.
    """
    wiki_collection = client.collections.get(WikiCollectionField.COLLECTION_NAME)

    for file in get_wiki_files(Path('wiki_texts')):
        logger.info(f'Processing {file}')
        with file.open() as f:
            page = f.read()

            for chunk_index in count(0):
                if chunk_index % 100 == 0:
                    logger.info(f'Processing chunk {chunk_index}')

                if chunk_index == 0:
                    chunk_start = 0
                else:
                    chunk_start = chunk_index * (chunk_size - chunk_overlap)

                chunk_end = chunk_start + chunk_size
                chunk = page[chunk_start:chunk_end]

                if not chunk:
                    break

                wiki_collection.data.insert({
                    WikiCollectionField.PAGE: file.stem,
                    WikiCollectionField.CHUNK_INDEX: chunk_index,
                    WikiCollectionField.CHUNK_CONTENT: chunk,
                })


def main() -> None:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.getLogger('httpx').setLevel(logging.WARNING)

    logger.info('Populating Weaviate database')
    with get_weaviate_client() as client:
        if client.collections.exists(WikiCollectionField.COLLECTION_NAME):
            logger.info('Collection already exists')
            return

        create_wiki_collection(client)

        logger.info('Creating Wiki objects')
        create_wiki_objects(client, chunk_size=400, chunk_overlap=200)

        logger.info('Done')


if __name__ == '__main__':
    main()
