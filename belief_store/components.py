import models
import nicegui.ui as ui


def belief_card(belief: models.Belief):
    with ui.card():
        # ui.label(belief.id)
        ui.label(belief.title).tailwind("text-2xl", "font-bold")
        ui.label(belief.description)
        ui.label(f'Tags: {", ".join(belief.tags)}').tailwind("text-sm", "font-light")
        n = ui.number("Certainty", value=belief.certainty)
        n.disable()
        with ui.row():
            ui.link("View", f"/beliefs/{belief.id}")
            ui.link("Edit", f"/beliefs/{belief.id}/edit")


class Layout:
    # allow use of context manager for this class
    def __enter__(self):
        with ui.header():
            ui.link("Belief Store", "/").tailwind("text-2xl", "font-bold", "text-white")

    def __exit__(self, exc_type, exc_value, traceback):
        ui.footer()
