from fastapi import FastAPI

from .routes.materials import router as materials_router
from .routes.sales_orders import router as sales_orders_router
from .routes.customers import router as customers_router
from .routes.tickets import router as tickets_router
from .routes.invoices import router as invoices_router

app = FastAPI(
    title="JouleOps NorthWind API",
    description="FastAPI action layer for JouleOps NorthWind",
    version="1.0.0",
)


app.include_router(materials_router)
app.include_router(sales_orders_router)
app.include_router(customers_router)
app.include_router(tickets_router)
app.include_router(invoices_router)


@app.get("/")
def root():
    return {
        "message": "JouleOps NorthWind API is running"
    }