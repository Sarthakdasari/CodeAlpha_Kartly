# Kartly

Flask + SQLite + vanilla JS store with sessions, CSRF protection, cart, COD checkout and order history.

## Run (Windows PowerShell)
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env   # then set SECRET_KEY in your shell: $env:SECRET_KEY="long-random"
python app.py
```
Open http://127.0.0.1:5000. The DB (`instance/ecommerce.db`) is created and seeded automatically (no duplicates on restart).

## Tests
```
python -m pytest -q
```
Tests use a temporary database.

## API
Products: GET /api/products?q=&category=&sort=, /api/products/<id>, /api/categories. Auth: POST /api/register, /api/login, /api/logout, GET /api/me. Cart: GET/DELETE /api/cart, POST/PUT/DELETE /api/cart/items/<id>. Orders: POST/GET /api/orders, GET /api/orders/<id>.
All POST/PUT/DELETE calls need header `X-CSRF-Token` from GET /api/csrf (same session cookie).

## Limitations
COD simulation only, no rate limiting, no email verification. Set FLASK_ENV=production and SECRET_KEY when deploying behind HTTPS.

## GitHub
```
git init; git add .; git commit -m "Initial commit"; git remote add origin <url>; git push -u origin main
```
