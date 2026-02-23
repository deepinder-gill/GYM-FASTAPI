from pydantic import BaseModel
from typing import Optional, List

class WorkoutLog(BaseModel):
    note : Optional[str] = None
    exercises : List