from fastapi import APIRouter, Depends, status

from src.dto.audio_request import AudioRequest
from src.dto.audio_response import AudioResponse
from src.service.classifier_service import ClassifierService


router = APIRouter()


@router.post(
    "/classify",
    response_model=AudioResponse,
    status_code=status.HTTP_200_OK,
    summary="Classify music genre",
    tags=["Audio Classification"]
)
def classify(dto: AudioRequest = Depends()) -> AudioResponse:
    response = ClassifierService().classify_audio(dto.audio)
    return response
