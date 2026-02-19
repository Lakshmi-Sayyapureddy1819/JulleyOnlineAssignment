from pydantic import BaseModel, Field
from typing import List, Optional

# Model for Chat Input
class ChatRequest(BaseModel):
    prompt: str

# Model for Chat Response
class ChatResponse(BaseModel):
    answer: str
    sources: List[str]

# Model for Drone Recommendation Input
class RecommendRequest(BaseModel):
    budget: float
    use: str = Field(..., alias="use_case") # Allow both but prefer 'use' to match frontend param if possible, or just use 'use'
    # Actually, frontend sends 'use'. Backend expect 'use'. Schema has 'use_case'. 
    # I'll just change it to 'use' to be simple.
    
class RecommendRequestSimple(BaseModel):
    budget: float
    use: str

# Model for Regulation Check Input
class ComplianceRequest(BaseModel):
    weight_kg: float
    zone: str
    altitude_ft: float
    purpose: str = "Recreational"
