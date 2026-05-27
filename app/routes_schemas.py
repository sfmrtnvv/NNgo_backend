from pydantic import BaseModel


class RouteResponseSchema(BaseModel):
    id: int
    name: str
    description: str
    estimated_time_minutes: int

    class Config:
        from_attributes = True


class RouteCreateSchema(BaseModel):
    name: str
    description: str
    estimated_time_minutes: int