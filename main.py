"""
Ticket Intel - NLP feedback system for support tickets
Routes, summarizes, extracts insights.
"""

import logging
import os
import sys
from contextlib import asynccontextmanager

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app):
    from src.api.routes import init_models

    init_models()
    yield


def create_app():
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from src.api.routes import router

    app = FastAPI(
        title="Ticket Intel API",
        description="NLP system for support ticket routing, summarization, and insights",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=os.environ.get("CORS_ORIGINS", "http://localhost:8501").split(
            ","
        ),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

    return app


def run_api():
    """start api server"""
    import uvicorn

    app = create_app()
    logger.info("Ticket Intel API starting")
    logger.info("API:    http://localhost:8000")
    logger.info("Docs:   http://localhost:8000/docs")
    logger.info("Health: http://localhost:8000/health")
    uvicorn.run(app, host="0.0.0.0", port=8000)


def run_dashboard():
    """streamlit ui"""
    import subprocess
    from pathlib import Path

    pkg_dir = Path(__file__).parent
    dashboard_path = pkg_dir / "src" / "ui" / "dashboard.py"

    env = os.environ.copy()
    env["PYTHONPATH"] = str(pkg_dir)

    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", str(dashboard_path)], env=env
    )


def main():
    args = sys.argv[1:]

    if not args:
        run_api()
        return

    cmd = args[0]

    # Hand any remaining args to the sub-command's own argparse (e.g.
    # `main.py train --input tickets.csv`) by dropping the sub-command token.
    sys.argv = [sys.argv[0], *args[1:]]

    if cmd == "train":
        logger.info("Training router model...")
        from src.models.train_router import main as train_main

        train_main()
        logger.info("Done.")

    elif cmd == "evaluate":
        from src.models.evaluate import main as eval_main

        eval_main()

    elif cmd == "api":
        run_api()

    elif cmd == "ui":
        run_dashboard()

    elif cmd in ("--help", "-h"):
        print(
            """
Ticket Intel - NLP feedback system

Commands:
  api           Start FastAPI server (default)
  ui            Start Streamlit dashboard
  train         Train the TF-IDF + Naive Bayes routing model
  evaluate      Cross-validate the router and write metrics.json
        """
        )

    else:
        logger.error("Unknown command: %s (try --help)", cmd)
        sys.exit(1)


if __name__ == "__main__":
    main()
