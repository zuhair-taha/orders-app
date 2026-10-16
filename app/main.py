from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime, timezone
import sqlite3
import os

connection = sqlite3.connect(os.environ.get("ORDERS_DB", "orders.db"), check_same_thread = False) # creates db if not exist, alos check_same_thread is set to False because uvicorn uses a differnet thread
cursor = connection.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("""CREATE TABLE IF NOT EXISTS orders (
    id TEXT PRIMARY KEY,
    customer_name TEXT,
    status TEXT,
    total_cents INT,
    created_at TEXT);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY,
    order_id TEXT,
    sku TEXT,
    name TEXT,
    quantity INT,
    unit_price_cents INT,
    FOREIGN KEY (ORDER_ID) references orders(id));""")

connection.commit()

orders = {} # dict to process orders before inserting into database

def insert_into_database(order_id) -> int:
    current_order = orders[order_id]
    try:
        with connection:
            cursor.execute("""INSERT INTO orders VALUES(
                ?, ?, ?, ?, ?);""", [order_id, current_order[0], current_order[2], current_order[4], str(current_order[3])])
            for item in current_order[1]:
                cursor.execute("""INSERT INTO order_items(order_id, sku, name, quantity, unit_price_cents) VALUES(
                    ?, ?, ?, ?, ?);""", [order_id, item.sku, item.name, item.quantity, item.unit_price_cents])
        del orders[order_id]
        return 0
    except Exception:
        return 1
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
        item_total = item.unit_price_cents * item.quantity
        total_cents += item_total
    order_id = str(uuid4())
    status = "PENDING"
    created_at = datetime.now(timezone.utc)
    orders[order_id] = [order.customer_name, order.items, status, created_at, total_cents]
    success_status = insert_into_database(order_id)
    if success_status == 1:
        return {"database_transaction_status": "failed"}
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
