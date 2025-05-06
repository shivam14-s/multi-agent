from pydantic import BaseModel, Field

class responseFormat(BaseModel):
        r : str = Field(..., description="The response you want to give")
        n : str = Field(..., description="next_agent token")