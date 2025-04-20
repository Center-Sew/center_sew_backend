from typing import Any, Dict, Union
from bson import ObjectId

def serialize_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converte um documento MongoDB para um dicionário compatível com Pydantic,
    substituindo o campo _id por uma string 'id' ou mantendo '_id' com string.

    Exemplo:
    { "_id": ObjectId(...) } -> { "_id": "abc123..." }
    """
    return {
        **doc,
        "_id": str(doc["_id"]) if "_id" in doc and isinstance(doc["_id"], ObjectId) else doc.get("_id")
    }

def serialize_docs(docs: list[Dict[str, Any]]) -> list[Dict[str, Any]]:
    return [serialize_doc(doc) for doc in docs]


def serialize_doc_id(doc: Dict[str, Any]) -> Dict[str, Any]:
    new_doc = dict(doc)
    new_doc["id"] = str(new_doc.pop("_id"))
    return new_doc
