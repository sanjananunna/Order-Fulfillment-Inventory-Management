from fastapi import FastAPI
from app.routes.warehouses import router as warehouse_router
from app.routes.auth import router as auth_router
from app.routes.notifications import router as notification_router
from app.routes.audit_logs import router as audit_log_router
from app.routes.orders import router as order_router
app = FastAPI()

app.include_router(auth_router)
app.include_router(warehouse_router)
app.include_router(notification_router)
app.include_router(audit_log_router)
app.include_router(order_router)
@app.get("/")
def root():
    return {"message": "Order Fulfillment API is running"}