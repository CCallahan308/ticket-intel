import logging

from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    TicketRequest,
    RouteResponse,
    SummaryResponse,
    InsightsResponse,
    HealthResponse,
)
from src.models.router import load_router, route
from src.models.summarizer import summarize
from src.models.insights import insights

logger = logging.getLogger(__name__)

router = APIRouter()


class ModelState:
    pipe = None
    l2i = None
    i2l = None


state = ModelState()


def init_models() -> None:
    """Load models into module-level state. Called from the app lifespan."""
    state.pipe, state.l2i, state.i2l = load_router()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        model_loaded=state.pipe is not None,
        categories=len(state.i2l) if state.i2l else 0,
    )


@router.post("/route", response_model=RouteResponse)
async def route_ticket(req: TicketRequest) -> RouteResponse:
    if state.pipe is None:
        raise HTTPException(503, "Model not loaded")

    txt = f"{req.subject} {req.body}"
    try:
        cat, conf, probs = route(txt, state.pipe, state.i2l)
    except Exception:
        logger.exception("Routing failed")
        raise HTTPException(500, "Routing failed")
    return RouteResponse(category=cat, confidence=conf, probabilities=probs)


@router.post("/summarize", response_model=SummaryResponse)
async def summarize_ticket(req: TicketRequest) -> SummaryResponse:
    txt = f"{req.subject} {req.body}"
    try:
        summ, n = summarize(txt)
    except Exception:
        logger.exception("Summarization failed")
        raise HTTPException(500, "Summarization failed")
    return SummaryResponse(
        summary=summ,
        sentence_count=n,
        original_length=len(txt.split()),
        summary_length=len(summ.split()),
    )


@router.post("/insights", response_model=InsightsResponse)
async def extract_insights(req: TicketRequest) -> InsightsResponse:
    txt = f"{req.subject} {req.body}"
    try:
        ents, kws, sent = insights(txt)
    except Exception:
        logger.exception("Insight extraction failed")
        raise HTTPException(500, "Insight extraction failed")
    return InsightsResponse(
        entities=ents, keywords=kws, sentiment=sent, entity_count=len(ents)
    )


@router.post("/batch")
async def batch_process(tickets: list[TicketRequest]) -> dict:
    if state.pipe is None:
        raise HTTPException(503, "Model not loaded")

    results = []
    for t in tickets:
        txt = f"{t.subject} {t.body}"
        cat, conf, _ = route(txt, state.pipe, state.i2l)
        summ, _ = summarize(txt)
        ents, kws, sent = insights(txt)
        results.append(
            {
                "category": cat,
                "confidence": conf,
                "summary": summ[:200],
                "sentiment": sent,
                "keywords": kws[:5],
            }
        )
    return {"results": results, "count": len(results)}
