from typing import Optional

from pydantic import BaseModel, Field


class DBConfig(BaseModel):
    db_type: str
    host: str = "localhost"
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = Field(default=None, repr=False)  # keep password out of repr/logs
    database: str

    class Config:
        # prevents accidental leakage of secrets when the model is printed/logged
        str_strip_whitespace = True