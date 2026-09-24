from typing import TypedDict

from app.models import PersonObservation, MemoryFragment


class ArchiveState(TypedDict, total=False):
    person_id: str

    image_base64: str
    image_mime_type: str

    observation: PersonObservation

    related_memories: list[MemoryFragment]

    generated_memory: MemoryFragment