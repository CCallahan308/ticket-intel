from fastapi import APIRouter, HTTPException
from typing import List
from src.api.schemas import (
    TicketRequest,
    RouteResponse,
    SummaryResponse,
    InsightsResponse,
    HealthResponse,
)

# We will create these models shortly
from src.models.router import load_router, route
from src.models.summarizer import summarize
from src.models.insights import insights

router = APIRouter()


# Global state for the models (in a real app, this might be managed differently, but keeping it simple for now)
class ModelState:
    pipe = None
    l2i = None
    i2l = None


state = ModelState()


@router.on_event("startup")
async def load_models():
    state.pipe, state.l2i, state.i2l = load_router()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        model_loaded=state.pipe is not None,
        categories=len(state.i2l) if state.i2l else 0,
    )


@router.post("/route", response_model=RouteResponse)
async def route_ticket(req: TicketRequest):
    if state.pipe is None:
        raise HTTPException(503, "Model not loaded")

    txt = f"{req.subject} {req.body}"
    try:
        cat, conf, probs = route(txt, state.pipe, state.i2l)
        return RouteResponse(category=cat, confidence=conf, probabilities=probs)
    except Exception as e:
        raise HTTPException(500, f"Routing failed: {str(e)}")


@router.post("/summarize", response_model=SummaryResponse)
async def summarize_ticket(req: TicketRequest):
    txt = f"{req.subject} {req.body}"
    try:
        summ, n = summarize(txt)
        return SummaryResponse(
            summary=summ,
            sentence_count=n,
            original_length=len(txt.split()),
            summary_length=len(summ.split()),
        )
    except Exception as e:
        raise HTTPException(500, f"Summarization failed: {str(e)}")


@router.post("/insights", response_model=InsightsResponse)
async def extract_insights(req: TicketRequest):
    txt = f"{req.subject} {req.body}"
    try:
        ents, kws, sent = insights(txt)
        return InsightsResponse(
            entities=ents, keywords=kws, sentiment=sent, entity_count=len(ents)
        )
    except Exception as e:
        raise HTTPException(500, f"Insight extraction failed: {str(e)}")


@router.post("/batch")
async def batch_process(tickets: List[TicketRequest]):
    if state.pipe is None:
        raise HTTPException(503, "Model not loaded")

    results = []
    for t in tickets:
        txt = f"{t.subject} {t.body}"
        cat, conf, probs = route(txt, state.pipe, state.i2l)
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
