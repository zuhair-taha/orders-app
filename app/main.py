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
    table = cursor.execute("""SELECT orders.id, orders.customer_name, order_items.sku, order_items.name, order_items.quantity, order_items.unit_price_cents, orders.status, orders.created_at, orders.total_cents FROM orders
            INNER JOIN order_items
            ON orders.id = order_items.order_id;""")
    return_orders_json = {}
    i = 1
    for row in table:
        if
        return_orders_json[f"row {i}"] = {"order_id": row[0], "customer_name": row[1], "item_sku": row[2], "item_name": row[3], "item_quantity": row[4], "item_unit_price_cents": row[5], "item_total_cents": row[5] * row[4], "order_status": row[6], "order_created_at": row[7], "order_total_cents": row[8]}
        i += 1
    return return_orders_json

@app.get("/orders/{id}")
def order_status(id: str):
    try:
        table = cursor.execute("""SELECT orders.id, orders.customer_name, order_items.sku, order_items.name, order_items.quantity, order_items.unit_price_cents, orders.status, orders.created_at, orders.total_cents FROM orders
        INNER JOIN order_items
        ON orders.id = order_items.order_id
        WHERE orders.id = ?;""", [id])
        return_order_json = {}
        i = 1
        for row in table:
            return_order_json[f"item {i}"] = {"order_id": row[0], "customer_name": row[1], "item_sku": row[2], "item_name": row[3], "item_quantity": row[4], "item_unit_price_cents": row[5], "item_total_cents": row[5] * row[4], "order_status": row[6], "order_created_at": row[7], "order_total_cents": row[8]}
            i += 1
        if not return_order_json:
            raise Exception()
        return return_order_json
    except Exception:
            raise HTTPException(status_code = 404, detail = "oops! order_id not found")

@app.get("/health")
def health():
    return {"craving": "daves hot chicken"}
