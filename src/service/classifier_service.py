import os

from fastapi import UploadFile
from src.dto.audio_response import AudioResponse
from transformers import AutoModelForAudioClassification, AutoFeatureExtractor, pipeline
import tempfile
import shutil

class ClassifierService:
    def __init__(self):
        # Load model and feature extractor from 'artifacts' folder
        self.model = AutoModelForAudioClassification.from_pretrained("artifacts")
        self.feature_extractor = AutoFeatureExtractor.from_pretrained("artifacts")
        self.pipe = pipeline(
            "audio-classification",
            model=self.model,
            feature_extractor=self.feature_extractor
        )

    def classify_audio(self, audio: UploadFile) -> AudioResponse:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            shutil.copyfileobj(audio.file, tmp)
            tmp_path = tmp.name

        try:
            preds = self.pipe(tmp_path)
        finally:
            os.unlink(tmp_path)

        outputs = {p["label"]: p["score"] for p in preds}
        max_label = max(outputs, key=outputs.get)
        max_score = outputs[max_label]

        return AudioResponse(genre=max_label, 
                             confidence=max_score)
