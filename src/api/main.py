"""
Main FastAPI application setup.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from src.api.users import router as users_router
from src.api.tasks import router as tasks_router
from src.settings import Setup

# Initialize FastAPI app
app = FastAPI(
    title="Task Manager API",
    description="A RESTful API for managing users and tasks",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users_router)
app.include_router(tasks_router)


@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup."""
    try:
        MONGO_URI, DB_NAME = Setup()
        print(f"✓ Database connection initialized")
        print(f"✓ MongoDB URI: {MONGO_URI}")
        print(f"✓ Database Name: {DB_NAME}")
    except Exception as e:
        print(f"⚠ Warning: Database connection failed: {e}")
        print("⚠ Running in mock mode")


@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Task Manager API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "users": "/users",
            "tasks": "/tasks"
        }
    }


@app.get("/health", response_model=dict)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "Task Manager API is running"
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_code": "INTERNAL_ERROR"
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
