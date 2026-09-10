"""Versioned public API router."""

from fastapi import APIRouter

from app.api.v1.routers import analysis, auth, cases, preprocess, system

api_router = APIRouter()
api_router.include_router(system.router, tags=["system"])
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(cases.router, prefix="/cases", tags=["cases"])
api_router.include_router(analysis.router, prefix="/cases", tags=["analysis"])
api_router.include_router(preprocess.router, tags=["preprocessing"])
