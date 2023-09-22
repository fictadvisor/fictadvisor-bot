from pydantic import BaseModel, ConfigDict


class Base(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
