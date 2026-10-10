import pytest
from app import create_app
@pytest.fixture
def c(tmp_path):
    return create_app({"DATABASE": str(tmp_path / "t.db"), "TESTING": True}).test_client()
def call(c, m, url, **kw):
    tok = c.get("/api/csrf").json["csrf"]
    return getattr(c, m)(url, headers={"X-CSRF-Token": tok}, **kw)
def signup(c, email="a@x.com"):
    return call(c, "post", "/api/register", json={"name": "A", "email": email, "password": "secret123"})
ADDR = {"customer_name": "A", "phone": "9999999999", "shipping_address": "12 Long Street, Hyderabad"}
def test_pages_and_products(c):
    assert c.get("/").status_code == 200 and c.get("/nope").status_code == 404
    assert len(c.get("/api/products").json["products"]) >= 12
    assert c.get("/api/products/1").json["product"]["id"] == 1 and c.get("/api/products/999").status_code == 404
    assert c.get("/api/products?q=lamp").json["products"]
def test_auth(c):
    assert signup(c).status_code == 201 and signup(c).status_code == 409
    call(c, "post", "/api/logout"); assert c.get("/api/me").json["user"] is None
    assert call(c, "post", "/api/login", json={"email": "a@x.com", "password": "bad"}).status_code == 401
    r = call(c, "post", "/api/login", json={"email": "a@x.com", "password": "secret123"})
    assert r.status_code == 200 and "password_hash" not in r.text
    assert c.post("/api/logout").status_code == 403
def test_cart_and_orders(c):
    assert c.get("/api/cart").status_code == 401
    signup(c)
    assert call(c, "post", "/api/orders", json=ADDR).status_code == 400
    assert call(c, "post", "/api/cart/items/1", json={"quantity": 2}).status_code == 201
    assert call(c, "put", "/api/cart/items/1", json={"quantity": 3}).json["count"] == 3
    assert call(c, "put", "/api/cart/items/1", json={"quantity": -1}).status_code == 400
    assert call(c, "post", "/api/cart/items/12", json={"quantity": 5}).status_code == 409
    call(c, "delete", "/api/cart/items/1"); assert c.get("/api/cart").json["count"] == 0
    call(c, "post", "/api/cart/items/1", json={"quantity": 2})
    o = call(c, "post", "/api/orders", json=ADDR)
    assert o.status_code == 201 and o.json["order"]["total_amount"] == 3198
    assert c.get("/api/products/1").json["product"]["stock"] == 23 and c.get("/api/cart").json["count"] == 0
    oid = o.json["order"]["id"]
    call(c, "post", "/api/logout"); signup(c, "b@x.com")
    assert c.get(f"/api/orders/{oid}").status_code == 404 and c.get("/api/orders").json["orders"] == []
