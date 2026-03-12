from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class InvestigationCreate(BaseModel):
    title: str
    description: Optional[str] = None
    target_identifier: str

class InvestigationResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    target_identifier: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class EvidenceResponse(BaseModel):
    id: str
    source: str
    data: str
    hash_sha256: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ToolRequest(BaseModel):
    query: str
    options: Optional[dict] = {}

class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[dict] = None
