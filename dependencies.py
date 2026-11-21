from typing import Annotated, Literal
from pydantic import BaseModel, Field
from fastapi import Depends, Query, Path, HTTPException
from db import DB
from schemas import Attribute


class PaginationParams(BaseModel):
    limit: Annotated[int, Field(ge=1, le=100)] = 20
    offset: Annotated[int, Field(ge=0)] = 0

Pagination = Annotated[PaginationParams, Query()]

class SortParams(BaseModel):
    sort: Attribute | None = None

Sorting = Annotated[SortParams, Query()]