import logging
from fastapi import FastAPI
from routers import vehicles

logging.getLogger("uvicorn.error")

app = FastAPI(
    title="Test for BexUp", 
    openapi_url="/openapi.json"
)

app.include_router(vehicles.router, prefix='/api')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
