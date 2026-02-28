"""
Ticket Intel - NLP feedback system for support tickets
Routes, summarizes, extracts insights.
"""
import sys


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
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
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
    print("\n" + "=" * 50)
    print("Ticket Intel API")
    print("=" * 50)
    print(f"API:     http://localhost:8000")
    print(f"Docs:    http://localhost:8000/docs")
    print(f"Health:  http://localhost:8000/health")
    print("=" * 50 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)


def run_dashboard():
    """streamlit ui"""
    import subprocess
    import sys
    import os
    from pathlib import Path

    pkg_dir = Path(__file__).parent
    dashboard_path = pkg_dir / "src" / "ui" / "dashboard.py"

    env = os.environ.copy()
    env["PYTHONPATH"] = str(pkg_dir)
    
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(dashboard_path)], env=env)


def main():
    args = sys.argv[1:]

    if not args:
        run_api()
        return

    cmd = args[0]

    if cmd == "train":
        print("Training router model...")
        from src.models.train_router import train_router

        train_router()
        print("Done!")

    elif cmd == "train_bert":
        print("Training BERT router model...")
        from src.models.train_bert_router import train_bert_router

        train_bert_router()
        print("Done!")

    elif cmd == "api":
        run_api()

    elif cmd == "ui":
        run_dashboard()

    elif cmd == "--help" or cmd == "-h":
        print(
            """
Ticket Intel - NLP feedback system

Commands:
  api           Start FastAPI server (default)
  ui            Start Streamlit dashboard
  train         Train the local TF-IDF routing model
  train_bert    Fine-tune the DistilBERT routing model
        """
        )


if __name__ == "__main__":
    main()
