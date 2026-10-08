from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime, timezone

orders = {} # dictionary to keep orders

class OrderItem(BaseModel):
    sku: str # stock keeping unit
    name: str
    quantity: int = Field(..., gt=0)
    unit_price_cents: int = Field(..., ge=0)

class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length = 1, max_length = 100)
    items: list[OrderItem] = Field(..., min_length=1)

app = FastAPI()

@app.post("/orders", status_code = 201)
def order_item(order: OrderRequest):
    total_cents = 0
    for item in order.items:
        item_total = item.unit_price_cents * item. quantity
        total_cents += item_total
    order_id = str(uuid4())
    status = "PENDING"
    created_at = datetime.now(timezone.utc)
    orders[order_id] = [order.customer_name, order.items, status, created_at, total_cents]
    return {"id": order_id, "status": status, "created_at": created_at, "total_cents": total_cents}

@app.get("/orders")
def all_orders():
    return orders
@app.get("/orders/{id}")
def order_status(id: str):
    try:
        return orders[id]
    except:
        raise HTTPException(
                status_code = 404,
                detail = "order not found"
        )

@app.get("/health")
def health():
    return {"status": "daves hot chicken"}
