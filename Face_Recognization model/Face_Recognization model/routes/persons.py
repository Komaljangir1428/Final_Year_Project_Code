"""Person and face recognition API endpoints."""

from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from typing import Optional
import json

from models import PersonResponse, RecognitionResult
import services.person_service as person_svc

router = APIRouter(prefix="/api", tags=["persons"])


@router.post("/register", response_model=PersonResponse)
async def register_person(
    name: str = Form(...),
    image: UploadFile = File(...),
    metadata: Optional[str] = Form(None),
):
    """
    Register a new person with their face.
    Upload an image containing a clear face. The face will be encoded and stored.
    """
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(400, "File must be an image (jpeg, png, etc.)")
    
    image_bytes = await image.read()
    
    meta = {}
    if metadata:
        try:
            meta = json.loads(metadata)
        except json.JSONDecodeError:
            raise HTTPException(400, "metadata must be valid JSON")
    
    try:
        person = await person_svc.register_person(name, image_bytes, meta)
    except ValueError as e:
        raise HTTPException(400, str(e))
    
    return PersonResponse(
        id=str(person["_id"]),
        name=person["name"],
        metadata=person.get("metadata", {}),
        face_count=person["face_count"],
        created_at=person["created_at"],
        updated_at=person["updated_at"],
    )


@router.post("/persons/{person_id}/add-face", response_model=PersonResponse)
async def add_face(person_id: str, image: UploadFile = File(...)):
    """
    Add another face image to an existing person for better recognition accuracy.
    """
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(400, "File must be an image")
    
    image_bytes = await image.read()
    
    try:
        person = await person_svc.add_face_to_person(person_id, image_bytes)
    except ValueError as e:
        raise HTTPException(404 if "not found" in str(e).lower() else 400, str(e))
    
    return PersonResponse(
        id=person["id"],
        name=person["name"],
        metadata=person.get("metadata", {}),
        face_count=person["face_count"],
        created_at=person["created_at"],
        updated_at=person["updated_at"],
    )


@router.post("/recognize", response_model=RecognitionResult)
async def recognize_face(image: UploadFile = File(...)):
    """
    Recognize a face from an uploaded image.
    Returns the matched person if found, otherwise indicates no match.
    """
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(400, "File must be an image")
    
    image_bytes = await image.read()
    result = await person_svc.recognize_face(image_bytes)
    
    return RecognitionResult(**result)


@router.get("/persons", response_model=list)
async def list_persons():
    """List all registered persons."""
    persons = await person_svc.get_all_persons()
    return persons


@router.get("/persons/{person_id}", response_model=PersonResponse)
async def get_person(person_id: str):
    """Get a specific person by ID."""
    person = await person_svc.get_person_by_id(person_id)
    if not person:
        raise HTTPException(404, "Person not found")
    
    return PersonResponse(
        id=person["id"],
        name=person["name"],
        metadata=person.get("metadata", {}),
        face_count=person["face_count"],
        created_at=person["created_at"],
        updated_at=person["updated_at"],
    )


@router.delete("/persons/{person_id}")
async def delete_person(person_id: str):
    """Delete a person from the database."""
    deleted = await person_svc.delete_person(person_id)
    if not deleted:
        raise HTTPException(404, "Person not found")
    return {"message": "Person deleted successfully"}
