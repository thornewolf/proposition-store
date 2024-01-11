from typing import Any, Iterable
from sqlmodel import Session
import models
import db
import functools


def convert_db_type(o: Any):
    match o:
        case list():
            return [convert_db_type(item) for item in o]
        case models.Market():
            return models.MarketDb.model_validate(o)
        case models.FullMarket():
            return models.FullMarketDb.model_validate(o)
        case other:
            print(f"Unknown type: {type(other)}, {other}")
            return None


def save_known_types(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        db_type = convert_db_type(result)
        with Session(db.engine) as session:
            match db_type:
                case list():
                    db_type = [item for item in db_type if item is not None]
                    session.add_all(db_type)
                case None:
                    pass
                case _:
                    session.add(db_type)
            session.commit()
        return result

    return wrapper
