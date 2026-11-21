from sqlalchemy import String, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from typing import Literal
from db import Base, engine 


class HeroesORM(Base):
    __tablename__ = "heroes"
    __table_args__ = (
    CheckConstraint("difficulty BETWEEN 1 AND 3", name="difficulty_range"),
    CheckConstraint("attribute IN ('strength', 'agility', 'intelligence', 'universal')", name="attribute_values"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    attribute: Mapped[str] = mapped_column(String(150), default="universal", nullable=False) 
    difficulty: Mapped[int] = mapped_column(nullable=False)



