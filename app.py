import re, secrets
from functools import wraps
from flask import Flask, jsonify, request, session, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
import database
from database import get_db
EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE = re.compile(r"^[0-9+\-\s]{7,15}$")
def err(msg, code): return jsonify(error=msg), code
def qty_of(v):
    return v if isinstance(v, int) and not isinstance(v, bool) and 1 <= v <= 99 else None
def create_app(cfg=None):
    app = Flask(__name__); app.config.from_object(Config)
    if cfg: app.config.update(cfg)
    database.init_app(app)

    @app.before_request
    def csrf_guard():
        if request.method in ("POST", "PUT", "DELETE") and request.path.startswith("/api/"):
            tok = session.get("csrf")
            if not tok or not secrets.compare_digest(tok, request.headers.get("X-CSRF-Token", "")):
                return err("Invalid or missing CSRF token", 403)
    def login_required(f):
        @wraps(f)
        def w(*a, **k):
            if "user_id" not in session: return err("Authentication required", 401)
            return f(*a, **k)
        return w
    @app.get("/api/csrf")
    def csrf():
        session.setdefault("csrf", secrets.token_hex(16)); return jsonify(csrf=session["csrf"])

    # pages
    for path, tpl in {"/": "index", "/products": "products", "/product": "product", "/cart": "cart", "/register": "register",
                      "/login": "login", "/checkout": "checkout", "/orders": "orders", "/account": "account"}.items():
        app.add_url_rule(path, "page_" + tpl, (lambda t: lambda: render_template(t + ".html"))(tpl))
    @app.errorhandler(404)
    def nf(_):
        if request.path.startswith("/api/"): return err("Not found", 404)
        return render_template("404.html"), 404
    @app.errorhandler(500)
    def ise(_): return err("Internal server error", 500)

    # products
    @app.get("/api/products")
    def products():
        q, cat, sort = request.args.get("q", "").strip(), request.args.get("category", ""), request.args.get("sort", "")
        sql, args = "SELECT * FROM products WHERE 1=1", []
        if q: sql += " AND name LIKE ?"; args.append(f"%{q}%")
        if cat: sql += " AND category=?"; args.append(cat)
        if request.args.get("featured") == "1": sql += " AND featured=1"
        sql += " ORDER BY " + {"price_asc": "price ASC", "price_desc": "price DESC", "name": "name ASC", "popular": "stock ASC"}.get(sort, "id ASC")
        return jsonify(products=[dict(r) for r in get_db().execute(sql, args)])
    @app.get("/api/products/<int:pid>")
    def product(pid):
        r = get_db().execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
        return jsonify(product=dict(r)) if r else err("Product not found", 404)
    @app.get("/api/categories")
    def categories():
        return jsonify(categories=[r[0] for r in get_db().execute("SELECT DISTINCT category FROM products ORDER BY category")])

    # auth
    @app.post("/api/register")
    def register():
        d = request.get_json(silent=True) or {}
        name, email, pw = (str(d.get(k) or "").strip() for k in ("name", "email", "password"))
        if not name or not EMAIL.match(email): return err("Valid name and email are required", 400)
        if len(pw) < 8 or not re.search(r"[A-Za-z]", pw) or not re.search(r"\d", pw):
            return err("Password must be 8+ characters with letters and numbers", 400)
        db = get_db()
        if db.execute("SELECT 1 FROM users WHERE email=?", (email.lower(),)).fetchone(): return err("Email already registered", 409)
        cur = db.execute("INSERT INTO users(name,email,password_hash) VALUES(?,?,?)", (name, email.lower(), generate_password_hash(pw)))
        session["user_id"] = cur.lastrowid
        return jsonify(user={"id": cur.lastrowid, "name": name, "email": email.lower()}), 201
    @app.post("/api/login")
    def login():
        d = request.get_json(silent=True) or {}
        u = get_db().execute("SELECT * FROM users WHERE email=?", (str(d.get("email") or "").strip().lower(),)).fetchone()
        if not u or not check_password_hash(u["password_hash"], str(d.get("password") or "")): return err("Incorrect email or password", 401)
        session["user_id"] = u["id"]
        return jsonify(user={"id": u["id"], "name": u["name"], "email": u["email"]})
    @app.post("/api/logout")
    def logout():
        session.pop("user_id", None); return jsonify(ok=True)
    @app.get("/api/me")
    def me():
        session.setdefault("csrf", secrets.token_hex(16))
        u = get_db().execute("SELECT id,name,email,created_at FROM users WHERE id=?", (session.get("user_id"),)).fetchone()
        return jsonify(user=dict(u) if u else None, csrf=session["csrf"])

    # cart
    def cart_payload(uid):
        rows = get_db().execute("SELECT p.id product_id,p.name,p.price,p.image_url,p.stock,c.quantity FROM cart_items c JOIN products p ON p.id=c.product_id WHERE c.user_id=? ORDER BY c.id", (uid,)).fetchall()
        items = [dict(r, subtotal=r["price"] * r["quantity"]) for r in rows]
        return {"items": items, "total": sum(i["subtotal"] for i in items), "count": sum(i["quantity"] for i in items)}
    @app.get("/api/cart")
    @login_required
    def cart(): return jsonify(cart_payload(session["user_id"]))
    def check_product(pid, q):
        p = get_db().execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
        if not p: return None, err("Product not found", 404)
        if q > p["stock"]: return None, err(f"Only {p['stock']} in stock", 409)
        return p, None
    @app.post("/api/cart/items/<int:pid>")
    @login_required
    def cart_add(pid):
        q = qty_of((request.get_json(silent=True) or {}).get("quantity", 1))
        if q is None: return err("Quantity must be an integer from 1 to 99", 400)
        db, uid = get_db(), session["user_id"]
        cur = db.execute("SELECT quantity FROM cart_items WHERE user_id=? AND product_id=?", (uid, pid)).fetchone()
        new = q + (cur["quantity"] if cur else 0)
        p, e = check_product(pid, new)
        if e: return e
        db.execute("INSERT INTO cart_items(user_id,product_id,quantity) VALUES(?,?,?) ON CONFLICT(user_id,product_id) DO UPDATE SET quantity=?", (uid, pid, new, new))
        return jsonify(cart_payload(uid)), 201
    @app.put("/api/cart/items/<int:pid>")
    @login_required
    def cart_set(pid):
        q = qty_of((request.get_json(silent=True) or {}).get("quantity"))
        if q is None: return err("Quantity must be an integer from 1 to 99", 400)
        p, e = check_product(pid, q)
        if e: return e
        cur = get_db().execute("UPDATE cart_items SET quantity=? WHERE user_id=? AND product_id=?", (q, session["user_id"], pid))
        if not cur.rowcount: return err("Item not in cart", 404)
        return jsonify(cart_payload(session["user_id"]))
    @app.delete("/api/cart/items/<int:pid>")
    @login_required
    def cart_del(pid):
        get_db().execute("DELETE FROM cart_items WHERE user_id=? AND product_id=?", (session["user_id"], pid))
        return jsonify(cart_payload(session["user_id"]))
    @app.delete("/api/cart")
    @login_required
    def cart_clear():
        get_db().execute("DELETE FROM cart_items WHERE user_id=?", (session["user_id"],))
        return jsonify(cart_payload(session["user_id"]))

    # orders
    def order_dict(o):
        items = get_db().execute("SELECT product_id,product_name,unit_price,quantity,subtotal FROM order_items WHERE order_id=?", (o["id"],)).fetchall()
        return dict(o, items=[dict(i) for i in items])
    @app.post("/api/orders")
    @login_required
    def place_order():
        d = request.get_json(silent=True) or {}
        name, phone, addr = (str(d.get(k) or "").strip() for k in ("customer_name", "phone", "shipping_address"))
        if not name or not PHONE.match(phone) or len(addr) < 10: return err("Name, valid phone and full shipping address are required", 400)
        db, uid = get_db(), session["user_id"]
        db.execute("BEGIN IMMEDIATE")
        try:
            rows = db.execute("SELECT c.quantity,p.id,p.name,p.price,p.stock FROM cart_items c JOIN products p ON p.id=c.product_id WHERE c.user_id=?", (uid,)).fetchall()
            if not rows: db.execute("ROLLBACK"); return err("Your cart is empty", 400)
            for r in rows:
                if r["quantity"] > r["stock"]: db.execute("ROLLBACK"); return err(f"Insufficient stock for {r['name']}", 409)
            total = sum(r["price"] * r["quantity"] for r in rows)
            oid = db.execute("INSERT INTO orders(user_id,total_amount,customer_name,phone,shipping_address) VALUES(?,?,?,?,?)", (uid, total, name, phone, addr)).lastrowid
            for r in rows:
                if not db.execute("UPDATE products SET stock=stock-? WHERE id=? AND stock>=?", (r["quantity"], r["id"], r["quantity"])).rowcount: raise ValueError("stock")
                db.execute("INSERT INTO order_items(order_id,product_id,product_name,unit_price,quantity,subtotal) VALUES(?,?,?,?,?,?)", (oid, r["id"], r["name"], r["price"], r["quantity"], r["price"] * r["quantity"]))
            db.execute("DELETE FROM cart_items WHERE user_id=?", (uid,))
            db.execute("COMMIT")
        except Exception:
            if db.in_transaction: db.execute("ROLLBACK")
            return err("Could not place order", 409)
        return jsonify(order=order_dict(db.execute("SELECT * FROM orders WHERE id=?", (oid,)).fetchone())), 201
    @app.get("/api/orders")
    @login_required
    def orders():
        rs = get_db().execute("SELECT * FROM orders WHERE user_id=? ORDER BY id DESC", (session["user_id"],)).fetchall()
        return jsonify(orders=[order_dict(o) for o in rs])
    @app.get("/api/orders/<int:oid>")
    @login_required
    def order(oid):
        o = get_db().execute("SELECT * FROM orders WHERE id=? AND user_id=?", (oid, session["user_id"])).fetchone()
        return jsonify(order=order_dict(o)) if o else err("Order not found", 404)
    return app

app = create_app()
if __name__ == "__main__":
    app.run(debug=False, port=5000)
