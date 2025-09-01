from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import (
    school_router, student_router, invoice_router, 
    payment_router, account_statement_router
)
from app.infrastructure.config.settings import settings

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Sistema de gestión académica y facturación para colegios",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(school_router, prefix="/api/v1")
app.include_router(student_router, prefix="/api/v1")
app.include_router(invoice_router, prefix="/api/v1")
app.include_router(payment_router, prefix="/api/v1")
app.include_router(account_statement_router, prefix="/api/v1")

# Endpoint de salud
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.VERSION}

# Endpoint raíz
@app.get("/")
async def root():
    return {
        "message": "Mattilda API - Sistema de Gestión Académica",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=settings.DEBUG
    )