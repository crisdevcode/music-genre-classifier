from fastapi import UploadFile, File


class AudioRequest:
    def __init__(self, audio: UploadFile = File(...)):
        self.audio = audio
        