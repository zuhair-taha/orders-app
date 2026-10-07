from fastapi import FastAPI
from pydantic import BaseModel, Field

class OrderItem(BaseModel):
    sku: str # stock keeping unit
    name: str
    quantity: int = Field(..., gt=0)
    unit_price_cents: int = Field(..., ge=0)

class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length = 1, max_length = 100)
    items: list[OrderItem] = Field(..., min_length=1)

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "daves hot chicken"}
