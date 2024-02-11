from typing import Annotated, Any

import uvicorn
import weaviate.classes as wvc
from fastapi import FastAPI, Query
from starlette.responses import RedirectResponse

from testtask.weavate import get_weaviate_client, WikiCollectionField

app = FastAPI()


@app.get("/", include_in_schema=False)
def read_root() -> Any:
    return RedirectResponse(url="/docs")


@app.get("/query")
def query(
    q: Annotated[
        str,
        Query(description="The query to search for")
    ],
    filters: Annotated[
        list[str] | None,
        Query(description="Phrases that must be present in the result (can be many)"),
    ] = None,
    limit: Annotated[
        int,
        Query(gt=0, le=100, description="Maximum number of results to return"),
    ] = 10,
    offset: Annotated[
        int,
        Query(ge=0, description="Offset from the start of the results"),
    ] = 0,
) -> list[str]:
    with get_weaviate_client() as client:
        wiki_collection = client.collections.get(WikiCollectionField.COLLECTION_NAME)
        query_filters = None
        if filters:
            query_filters = wvc.query.Filter.by_property(WikiCollectionField.CHUNK_CONTENT).contains_all(filters)

        response = wiki_collection.query.near_text(
            query=q,
            distance=0.8,
            filters=query_filters,
            offset=offset,
            limit=limit,
        )
    return [obj.properties[WikiCollectionField.CHUNK_CONTENT] for obj in response.objects]


if __name__ == '__main__':
    uvicorn.run(app)
