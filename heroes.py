from db import DB
from fastapi import Query, HTTPException, APIRouter, Path
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from dependencies import Pagination, Sorting
from schemas import Attribute, Heroes, HeroesPost, HeroesUpdate, HeroesStats
from typing import Annotated
from models import HeroesORM

router = APIRouter(prefix="/heroes", tags=["heroes"])


@router.get("")
def get_all(db: DB, page: Pagination, sort: Sorting) -> list[Heroes]:
    get_heroes = select(HeroesORM)
    if sort.sort is not None:
        get_heroes = get_heroes.where(HeroesORM.attribute == sort.sort)
    get_heroes = get_heroes.order_by(HeroesORM.id.asc())
    get_heroes = get_heroes.limit(page.limit).offset(page.offset)
    return db.scalars(get_heroes).all()


@router.get("/stats")
def get_stats(db: DB) -> list[HeroesStats]:
    att_heroes = (select(HeroesORM.attribute, func.count(HeroesORM.id).label('hero_count'), 
                func.round(func.avg(HeroesORM.difficulty), 2).label('avg_difficulty'))
                .group_by(HeroesORM.attribute).order_by(func.avg(HeroesORM.difficulty).desc()))
    response = db.execute(att_heroes).all()
    return [row._asdict() for row in response]
        

@router.get("/{hero_id}")
def get_hero_by_id(db: DB, hero_id: Annotated[int, Path(ge=1)]) -> Heroes:
    hero = db.get(HeroesORM, hero_id)
    if hero is None:
        raise HTTPException(404)
    return hero


@router.post("", status_code=201)
def post_hero(db: DB, data: HeroesPost) -> Heroes:
    new_hero = HeroesORM(**data.model_dump())
    try:
        db.add(new_hero)
        db.commit()
        db.refresh(new_hero)
        return new_hero
    except IntegrityError:
        db.rollback()
        raise HTTPException(409)


@router.patch("/{hero_id}")
def edit_hero(db: DB, data: HeroesUpdate, hero_id: Annotated[int, Path(ge=1)]) -> Heroes:
    hero_to_edit = db.get(HeroesORM, hero_id)
    updated = data.model_dump(exclude_unset=True, exclude_none=True)
    if hero_to_edit is None:
        raise HTTPException(404)
    if not updated:
        raise HTTPException(400)
    for key, value in updated.items():
        setattr(hero_to_edit, key, value)
    db.commit()
    db.refresh(hero_to_edit)
    return hero_to_edit
    
    


@router.delete("/{hero_id}", status_code=204)
def delete_hero(db: DB, hero_id: Annotated[int, Path(ge=1)]) -> None:
    hero_to_delete = db.get(HeroesORM, hero_id)
    if hero_to_delete is None:
        raise HTTPException(404)
    db.delete(hero_to_delete)
    db.commit()
    return 
    

    
