from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware 
 
from app.config import settings 
from app.api import health_router, meter_router
from app.models.telemetry import TelemetryReadingModel

# Initialize FastAPI instance
app = FastAPI(
    title=settings.APP_NAME,
    description="Backend service for AI Energy Monitoring and Analysis Assistant",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(health_router)
app.include_router(meter_router)


@app.get("/", summary="Root Endpoint")
def read_root():
    """Welcome endpoint providing service metadata."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
        "meter_current": "/api/meter/current",
        "meter_status": "/api/meter/status"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
