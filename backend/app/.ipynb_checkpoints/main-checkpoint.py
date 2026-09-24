import base64
import uuid

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException

from app.graph import memory_graph


load_dotenv()


app = FastAPI(
    title="Memory Network",
    description="A fictional generative memory archive.",
)


@app.get("/")
def root():
    return {
        "project": "Memory Network",
        "status": "alive",
    }


@app.post("/archive/person")
async def create_archive_person(
    image: UploadFile = File(...)
):

    if not image.content_type:
        raise HTTPException(
            status_code=400,
            detail="Unknown image format."
        )

    if not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Uploaded file must be an image."
        )

    raw_image = await image.read()

    image_base64 = base64.b64encode(
        raw_image
    ).decode("utf-8")

    person_id = "P-" + uuid.uuid4().hex[:6].upper()

    result = memory_graph.invoke(
        {
            "person_id": person_id,
            "image_base64": image_base64,
            "image_mime_type": image.content_type,
            "related_memories": [],
        }
    )

    return {
        "person_id": person_id,
        "observation": result["observation"],
        "memory": result["generated_memory"],
    }