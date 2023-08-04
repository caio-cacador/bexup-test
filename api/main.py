from fastapi import FastAPI
from api.routers import cars


app = FastAPI(
    title="Test for BexUp", 
    openapi_url="/openapi.json"
)

app.include_router(cars.router, prefix='/api')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
