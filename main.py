from fastapi import FastAPI
from app.api.routes import router
app=FastAPI(title="EGX Quant V1.2",version="1.2.0")
app.include_router(router)
@app.get("/health")
def health(): return {"status":"healthy","version":"1.2.0"}
