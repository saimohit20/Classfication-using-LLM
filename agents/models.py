# from pydantic import BaseModel, Field
# from typing import List

# class DetectionResponse(BaseModel):
#     class_: List[str] = Field(..., alias="class")

#     class Config:
#         populate_by_name = True

from pydantic import BaseModel, Field
from typing import List

class DetectionResponse(BaseModel):
   
    label_ids: List[int] = Field(..., alias="labelId")

    class Config:
        populate_by_name = True

