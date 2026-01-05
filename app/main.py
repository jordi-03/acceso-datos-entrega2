from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import customers, rentals

app = FastAPI(title="Sakila API", version="1.0.0")

# CORS (para que Swagger "Try it out" funcione sin problemas)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customers.router, prefix="/api/v1")
app.include_router(rentals.router, prefix="/api/v1")


@app.get("/health", tags=["default"])
def health():
    return {"status": "ok"}
