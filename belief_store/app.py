import dotenv

dotenv.load_dotenv()

from typing import Optional

import db
import models
import nicegui.ui as ui
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlmodel import Session, select
from components import belief_card, Layout

db.create_db_and_tables()
import belief_store.fake_data as fake_data  # fake data side effect


def _jaccard(s1, s2):
    return len(s1.intersection(s2)) / len(s1.union(s2))


def related_beliefs(belief: models.Belief):
    with Session(db.engine) as session:
        beliefs = session.exec(select(models.Belief)).all()
    bag1 = set(belief.title.split(" ") + belief.tags + belief.description.split(" "))
    for other in beliefs:
        bag2 = set(other.title.split(" ") + other.tags + other.description.split(" "))
        if _jaccard(bag1, bag2) > 0.3:
            yield other


@ui.page("/")
def index():
    with Layout():
        with Session(db.engine) as session:
            beliefs = session.exec(
                select(models.Belief).where(models.Belief.title != "")
            ).all()

        with ui.grid(columns=3):
            with ui.card():
                ui.link("New Belief", "/beliefs/new")
            for belief in beliefs:
                belief_card(belief=belief)


@ui.page("/beliefs/new")
def belief_new():
    def create_belief():
        with Session(db.engine) as session:
            belief = models.Belief()
            session.add(belief)
            session.commit()
            session.refresh(belief)
            id_ = belief.id
        return id_

    bid = create_belief()
    return RedirectResponse(f"/beliefs/{bid}/edit")


@ui.page("/beliefs/{belief_id}")
def belief_detail(belief_id: str):
    with Layout():
        with Session(db.engine) as session:
            belief = session.exec(
                select(models.Belief).where(models.Belief.id == belief_id)
            ).first()
        belief_card(belief=belief)
        with ui.card():
            ui.label("related beliefs").tailwind("text-2xl", "font-bold")
            for other in related_beliefs(belief):
                with ui.row():
                    ui.link(
                        other.title + f" - {other.description[:10]}",
                        f"/beliefs/{other.id}",
                    )
                    ui.button("Add as dependant")


def update_model(cls, id_: str, data: dict):
    with Session(db.engine) as session:
        db_model = session.exec(select(cls).where(cls.id == id_)).first()
        for key, value in data.items():
            setattr(db_model, key, value)
        session.commit()


def update_for_field(cls, id_, field: str, value):
    update_model(cls, id_, {field: value})


def input_for_field(cls, id_, field: str, value: str):
    on_change_fn = lambda x: update_for_field(cls, id_, field, x.value)
    match field:
        case str(a):
            ui.textarea(field, value=value, on_change=on_change_fn).tailwind("w-64")
        case float():
            ui.number(field, value=value, on_change=on_change_fn)
        case list():
            ui.textarea(field, value=", ".join(value), on_change=on_change_fn)
        case dict():
            ui.textarea(field, value=", ".join(value), on_change=on_change_fn)
        case int():
            ui.number(field, value=value, on_change=on_change_fn)


def edit_form_from_model(model: BaseModel, include: Optional[list] = None):
    if include is None:
        include = model.model_fields
    with ui.card():
        for field in include:
            value = getattr(model, field)
            input_for_field(model.__class__, model.id, field, value)


@ui.page("/beliefs/{belief_id}/edit")
def belief_edit(belief_id: str):
    with Layout():
        with ui.card():
            with Session(db.engine) as session:
                belief = session.exec(
                    select(models.Belief).where(models.Belief.id == belief_id)
                ).first()

            edit_form_from_model(
                belief, include=["title", "description", "tags", "certainty"]
            )
            ui.link("Back", f"/beliefs/{belief_id}")


ui.run()
