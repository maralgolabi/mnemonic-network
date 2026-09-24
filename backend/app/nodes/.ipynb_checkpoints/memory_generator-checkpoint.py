import os
import uuid

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from app.models import MemoryFragment
from app.state import ArchiveState
from app.prompts.memory import MEMORY_PROMPT


load_dotenv()


model = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("GAPGPT_API_KEY"),
    base_url=os.getenv("GAPGPT_BASE_URL"),
    temperature=0.9,
)


structured_model = model.with_structured_output(MemoryFragment)


def generate_memory(state: ArchiveState):

    observation = state["observation"]

    memory_id = "M-" + uuid.uuid4().hex[:8].upper()

    prompt = f"""
Anonymous archive subject:

{observation.model_dump_json(indent=2)}

Create memory ID:

{memory_id}

Generate one fictional memory fragment inspired by this observation.

For this first version:

- The memory should concern only this anonymous person.
- Do not invent connections to other archive subjects yet.
- Do not identify the real photographed person.
- Do not invent a full biography.
- Prefer uncertainty, fragments, mundane objects, sensory details,
  incomplete recollection, and ambiguous chronology.

The memory must fit the required structured schema.
"""

    memory = structured_model.invoke(
        [
            {
                "role": "system",
                "content": MEMORY_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]
    )

    # We control these values ourselves
    memory.memory_id = memory_id
    memory.people = [observation.person_id]

    return {
        "generated_memory": memory
    }