from fastapi import FastAPI

from src.config.logging import configure_logging, LogLevels
from src.controller.classifier_controller import router

configure_logging(LogLevels.info)

app = FastAPI()

app.include_router(router, prefix="/audio")
