from pydantic import BaseModel


class SearchResult(BaseModel):
    title: str
    link: str
