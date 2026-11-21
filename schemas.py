from typing import Literal, Annotated 
from pydantic import Field
from pydantic import BaseModel, ConfigDict


Attribute = Literal["universal", "agility", "strength", "intelligence"]


class HeroesBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Annotated[str, Field(min_length=2, max_length=150)]
    attribute: Attribute = "universal"
    difficulty: Annotated[int, Field(ge=1, le=3)]

class HeroesUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: Annotated[str, Field(min_length=2, max_length=150)] | None = None
    attribute: Attribute | None = None
    difficulty: Annotated[int , Field(ge=1, le=3)] | None = None

class HeroesPost(HeroesBase):
    pass

class Heroes(HeroesBase):
    id: Annotated[int, Field(ge=1)]

class HeroesStats(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    attribute: Attribute
    hero_count: Annotated[int, Field(ge=1, le=50)]
    avg_difficulty: Annotated[float, Field(ge=1, le=3)]




