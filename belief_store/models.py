from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict
from datetime import datetime
from uuid import uuid4


from sqlmodel import Field, SQLModel, JSON, Column


# Models for each endpoint's response
class User(SQLModel, table=True):
    id: str = Field(primary_key=True)


class Belief(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    title: str = Field(default="")
    description: str = Field(default="")
    certainty: float = Field(default=0.0)
    tags: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
