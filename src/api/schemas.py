from pydantic import BaseModel, Field


class TicketRequest(BaseModel):
    subject: str = Field(default="", min_length=0)
    body: str = Field(default="", description="Ticket body text")


class RouteResponse(BaseModel):
    category: str
    confidence: float
    probabilities: dict[str, float]


class SummaryResponse(BaseModel):
    summary: str
    sentence_count: int
    original_length: int
    summary_length: int


class InsightsResponse(BaseModel):
    entities: list[dict[str, str]]
    keywords: list[str]
    sentiment: str
    entity_count: int


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    categories: int
