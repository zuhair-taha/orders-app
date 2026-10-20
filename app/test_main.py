from fastapi.testclient import TestClient

def helper_function_to_set_tmp_database(tmp_path):
    import os
    os.environ["ORDERS_DB"] = str(tmp_path/"test.db")
    from main import app
    return TestClient(app)

def test_order_item(tmp_path):
    request_body = {"customer_name": "test", "items": [{"sku": "strange", "name": "car", "quantity": 5, "unit_price_cents": 70}]}
    client = helper_function_to_set_tmp_database(tmp_path)
    response = client.post("/orders", json = request_body)
    response_json = response.json()
    assert response.status_code == 201
    assert response_json["status"] == "PENDING"
    assert response_json["total_cents"] == 70 * 5

