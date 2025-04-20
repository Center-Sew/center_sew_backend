from pydantic import BaseModel, Field, field_validator
from bson import ObjectId

class BaseModelWithStrObjectId(BaseModel):
    id: str = Field(alias="_id")

    @field_validator("id", mode="before")
    @classmethod
    def convert_object_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    model_config = {
        "populate_by_name": True,
        "json_encoders": {
            ObjectId: str
        }
    }
