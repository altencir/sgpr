from fastapi import FastAPI
from app.controllers import producer_controller, farm_controller, culture_controller, dashboard_controller
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Rural Producer Management System",
    description="Sistema de gerenciamento de produtores rurais",
    version="1.0.0"
)

app.include_router(producer_controller.router)
app.include_router(farm_controller.router)
app.include_router(culture_controller.router)
app.include_router(dashboard_controller.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}