from fastapi import APIRouter
from app.models.patient import Query, Response
from app.logic import process_user_input

router = APIRouter(prefix="/assistant", tags=["assistant"])

@router.post("/query", response_model=Response)
async def query_assistant(payload: Query):
    response_text, patient_data = await process_user_input(payload.text)
    return Response(response=response_text, patient=patient_data)
