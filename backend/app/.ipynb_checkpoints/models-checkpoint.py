from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class MemorySource(str, Enum):
    DIRECT = "direct_memory"
    SECONDHAND = "secondhand_memory"
    RUMOR = "rumor"
    DREAM = "dream"
    PHOTOGRAPH = "photograph"
    UNCERTAIN = "uncertain"


class Reliability(str, Enum):
    CERTAIN = "certain"
    PROBABLE = "probable"
    UNCERTAIN = "uncertain"
    FRAGMENTARY = "fragmentary"
    LOST = "lost"


class PersonObservation(BaseModel):
    person_id: str

    # Only visible / environmental information.
    description: str

    visual_motifs: list[str] = Field(
        description="Objects, colors, gestures, environments or visual motifs."
    )

    possible_locations: list[str] = []

    atmosphere: list[str] = []


class MemoryFragment(BaseModel):
    memory_id: str

    text: str

    people: list[str]

    year: Optional[int] = None
    time_description: Optional[str] = None
    location: Optional[str] = None

    objects: list[str] = []
    emotions: list[str] = []

    source_type: MemorySource
    reliability: Reliability

    contradictions: list[str] = []