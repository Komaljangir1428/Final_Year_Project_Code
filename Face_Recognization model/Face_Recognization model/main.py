"""Face Recognition API - Main FastAPI application."""

from contextlib import asynccontextmanager

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from database import connect_to_db, close_db_connection, get_db
from models import HealthResponse
from routers import persons, attendance


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    await connect_to_db()
    # Preload face model so first register/recognize is faster (avoids timeout)
    import asyncio
    from services.face_service import _get_face_lib
    try:
        await asyncio.get_event_loop().run_in_executor(None, _get_face_lib)
        print("Face model loaded")
    except Exception as e:
        print(f"Face model preload skipped: {e}")
    yield
    await close_db_connection()


app = FastAPI(
    title="Face Recognition API",
    description="REST API for face registration and recognition using MongoDB",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(persons.router)
app.include_router(attendance.router)

# Static files and UI
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/", tags=["root"])
async def root():
    """Serve attendance UI."""
    index_path = static_dir / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {
        "message": "Face Recognition Attendance API",
        "docs": "/docs",
        "ui": "Static files not found. Run from project root.",
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check - verify API and MongoDB connectivity."""
    try:
        db = get_db()
        await db.command("ping")
        mongodb_connected = True
    except Exception:
        mongodb_connected = False
    
    return HealthResponse(
        status="healthy" if mongodb_connected else "degraded",
        mongodb_connected=mongodb_connected,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
