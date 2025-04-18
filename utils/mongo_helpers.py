def serialize_doc(doc: dict) -> dict:
    """
    Converte um documento MongoDB (_id como ObjectId) para um dicionário
    compatível com os modelos Pydantic (com id como string).
    """
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc