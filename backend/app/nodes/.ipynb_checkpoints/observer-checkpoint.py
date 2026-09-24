import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from app.models import PersonObservation
from app.state import ArchiveState
from app.prompts.observer import OBSERVER_PROMPT

load_dotenv()

model = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("GAPGPT_API_KEY"),
    base_url=os.getenv("GAPGPT_BASE_URL"),
    temperature=0.2,
)

structured_model = model.with_structured_output(PersonObservation)


def observe_person(state: ArchiveState):
    person_id = state["person_id"]
    image_base64 = state["image_base64"]
    mime_type = state["image_mime_type"]

    message = [
        {
            "role": "system",
            "content": OBSERVER_PROMPT,
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"""
This photograph belongs to anonymous archive subject {person_id}.

Describe only observable visual motifs.
""",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{image_base64}"
                    },
                },
            ],
        },
    ]

    observation = structured_model.invoke(message)
    observation.person_id = person_id

    return {
        "observation": observation
    }