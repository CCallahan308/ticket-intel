from pydantic import BaseModel
from typing import Dict, List


class TicketRequest(BaseModel):
    subject: str = ""
    body: str = ""


class RouteResponse(BaseModel):
    category: str
    confidence: float
    probabilities: Dict[str, float]


class SummaryResponse(BaseModel):
    summary: str
    sentence_count: int
    original_length: int
    summary_length: int


class InsightsResponse(BaseModel):
    entities: List[Dict[str, str]]
    keywords: List[str]
    sentiment: str
    entity_count: int


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    categories: int
