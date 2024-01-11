from sqlmodel import Session, select
import models
import db

with Session(db.engine) as session:
    fake_beliefs = [
        models.Belief(
            id="1",
            title="The sky is blue",
            description="The color of the sky appears blue due to the scattering of sunlight by molecules in the atmosphere.",
            tags=["sky", "blue", "atmosphere", "scattering", "sunlight"],
            evidence=[
                "Scientific observations and experiments",
                "Personal experiences of seeing a blue sky",
            ],
            source="Science textbooks and articles",
            certainty=0.0,
            context="Typical daytime conditions on Earth",
            counterarguments=[
                "The sky can appear different colors under certain conditions, such as sunrise, sunset, or storms."
            ],
        ),
        models.Belief(
            id="2",
            title="The sky is red",
            description="The sky appears red during sunrise and sunset due to the longer wavelengths of light being scattered through the atmosphere.",
            tags=["sky", "red", "sunrise", "sunset", "atmosphere", "scattering"],
            evidence=["Personal experiences of seeing a red sky at sunrise or sunset"],
            source="Personal observations",
            certainty=0.0,
            context="Sunrise or sunset conditions",
            counterarguments=[
                "The sky is not always red, even at sunrise or sunset. It can appear other colors depending on atmospheric conditions."
            ],
        ),
        models.Belief(
            id="3",
            title="The sky is green",
            description="The sky can appear green under certain rare conditions, such as during severe thunderstorms or when light is refracted through ice crystals in the atmosphere.",
            tags=["sky", "green", "storm", "ice crystals", "refraction"],
            evidence=["Photographic evidence", "Eyewitness accounts"],
            source="News articles, scientific reports",
            certainty=0.0,
            context="Rare atmospheric phenomena",
            counterarguments=[
                "The sky is not typically green, and other explanations for green-colored skies may exist."
            ],
        ),
        models.Belief(
            id="4",
            title="The sky is a projection",
            description="The sky is not a physical object, but rather a projection created by our minds to make sense of the vastness of space.",
            tags=["sky", "projection", "mind", "space", "perception"],
            evidence=["Philosophical arguments", "Experiments in sensory deprivation"],
            source="Philosophical texts, psychological studies",
            certainty=0.0,
            context="Metaphysical discussions",
            counterarguments=[
                "The sky can be measured and observed using scientific instruments, suggesting it has a physical existence."
            ],
        ),
    ]

    for belief in fake_beliefs:
        session.add(belief)
    session.commit()
