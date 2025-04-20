from typing import Type
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import Document, init_beanie
from app.core.config import settings
import importlib
import pkgutil
import inspect

def get_beanie_models_from_package(package_name: str) -> list[Type[Document]]:
    models = []

    package = importlib.import_module(package_name)

    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        full_module = importlib.import_module(f"{package_name}.{module_name}")
        for _, obj in inspect.getmembers(full_module, inspect.isclass):
            if issubclass(obj, Document) and obj is not Document:
                models.append(obj)

    return models

async def init_mongo():
    client = AsyncIOMotorClient(settings.MONGO_URL)
    database = client[settings.DATABASE_NAME]

    # Detectar dinamicamente todos os documentos Beanie do pacote models
    beanie_models = get_beanie_models_from_package("app.models")

    print("[DEBUG] Modelos detectados para o Beanie:")
    for model in beanie_models:
        print(" -", model.__name__, "| Módulo:", model.__module__)

    await init_beanie(database=database, document_models=beanie_models)
