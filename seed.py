PRODUCTS = [
 ("Wireless Noise-Cancelling Headphones","Over-ear Bluetooth headphones with active noise cancellation and 30-hour battery life.",1599,"Electronics",25,1),
 ("Smart Fitness Watch","AMOLED display, heart-rate tracking, GPS and 7-day battery.",1299,"Electronics",40,1),
 ("Portable Bluetooth Speaker","Waterproof speaker with deep bass and 12-hour playtime.",999,"Electronics",60,0),
 ("Mechanical Keyboard","Compact hot-swappable keyboard with tactile switches and RGB backlight.",1999,"Electronics",30,0),
 ("Classic Denim Jacket","Midweight cotton denim jacket with a relaxed modern fit.",799,"Fashion",35,1),
 ("Everyday Running Shoes","Lightweight breathable sneakers with cushioned soles.",1249,"Fashion",50,0),
 ("Organic Cotton T-Shirt","Soft, breathable crew-neck tee in a timeless cut.",499,"Fashion",120,0),
 ("Ceramic Table Lamp","Minimal ceramic base with a warm linen shade.",1199,"Home and Living",20,1),
 ("Stoneware Dinner Set","16-piece matte stoneware set for four.",2199,"Home and Living",15,0),
 ("Linen Throw Blanket","Textured, breathable linen blanket for sofa or bed.",999,"Home and Living",45,0),
 ("Leather Bifold Wallet","Full-grain leather wallet with RFID-blocking lining.",699,"Accessories",70,1),
 ("Canvas Backpack","Water-resistant 22L backpack with padded laptop sleeve.",1349,"Accessories",3,0),
 ("Polarized Sunglasses","UV400 polarized lenses in a lightweight frame.",899,"Accessories",55,0),
]
import os, re
COL = {"Electronics": ("#818cf8", "#4338ca"), "Fashion": ("#fb7185", "#be123c"), "Home and Living": ("#2dd4bf", "#0f766e"), "Accessories": ("#fbbf24", "#b45309")}
def _keys():
    return "".join(f'<rect x="{150+c*44}" y="{150+r*52}" width="36" height="40" rx="8" fill="#fff"/>' for r in range(4) for c in range(8)) + '<rect x="190" y="358" width="220" height="30" rx="8" fill="#fff"/>'
SHAPES = [
 '<path d="M170 250 A130 130 0 0 1 430 250" fill="none" stroke="#fff" stroke-width="22" stroke-linecap="round"/><rect x="150" y="235" width="55" height="105" rx="26" fill="#fff"/><rect x="395" y="235" width="55" height="105" rx="26" fill="#fff"/>',
 '<rect x="265" y="60" width="70" height="330" rx="20" fill="#fff" opacity=".6"/><rect x="215" y="130" width="170" height="190" rx="42" fill="#fff"/><rect x="232" y="147" width="136" height="156" rx="30" fill="DK"/><circle cx="300" cy="225" r="38" fill="none" stroke="#fff" stroke-width="8"/>',
 '<rect x="195" y="100" width="210" height="250" rx="40" fill="#fff"/><circle cx="300" cy="190" r="48" fill="DK"/><circle cx="300" cy="190" r="18" fill="#fff"/><circle cx="300" cy="290" r="26" fill="DK"/>',
 '<rect x="120" y="120" width="360" height="290" rx="30" fill="#fff" opacity=".35"/>' + _keys(),
 '<path d="M230 100 L170 135 L130 280 L180 295 L195 220 L195 350 L405 350 L405 220 L420 295 L470 280 L430 135 L370 100 L300 160 Z" fill="#fff"/><path d="M300 160 L300 350" stroke="DK" stroke-width="6"/>',
 '<path d="M110 270 Q140 150 230 190 L260 215 Q330 235 440 250 Q495 262 495 305 L495 325 L110 325 Z" fill="#fff"/><rect x="110" y="322" width="385" height="28" rx="14" fill="DK"/><path d="M240 215 L270 250 M270 225 L300 258" stroke="DK" stroke-width="6" stroke-linecap="round"/>',
 '<path d="M215 100 L120 155 L158 230 L200 208 L200 355 L400 355 L400 208 L442 230 L480 155 L385 100 Q300 170 215 100Z" fill="#fff"/>',
 '<path d="M225 80 L375 80 L415 215 L185 215 Z" fill="#fff"/><rect x="291" y="215" width="18" height="100" fill="#fff"/><ellipse cx="300" cy="335" rx="75" ry="20" fill="#fff"/>',
 '<circle cx="300" cy="215" r="135" fill="#fff"/><circle cx="300" cy="215" r="95" fill="none" stroke="DK" stroke-width="6"/><circle cx="300" cy="215" r="52" fill="DK" opacity=".3"/>',
 '<rect x="115" y="120" width="370" height="220" rx="16" fill="#fff"/><rect x="115" y="185" width="370" height="24" fill="DK" opacity=".35"/><rect x="115" y="245" width="370" height="24" fill="DK" opacity=".35"/>',
 '<rect x="145" y="130" width="310" height="200" rx="28" fill="#fff"/><rect x="145" y="130" width="310" height="62" rx="28" fill="DK" opacity=".3"/><rect x="380" y="215" width="95" height="58" rx="18" fill="DK"/><circle cx="412" cy="244" r="9" fill="#fff"/>',
 '<rect x="190" y="105" width="220" height="260" rx="72" fill="#fff"/><rect x="225" y="240" width="150" height="95" rx="22" fill="DK" opacity=".3"/><path d="M250 108 Q300 40 350 108" fill="none" stroke="#fff" stroke-width="16"/><rect x="255" y="200" width="90" height="9" rx="4" fill="DK"/>',
 '<circle cx="222" cy="225" r="78" fill="#fff"/><circle cx="378" cy="225" r="78" fill="#fff"/><circle cx="222" cy="225" r="60" fill="DK"/><circle cx="378" cy="225" r="60" fill="DK"/><rect x="288" y="205" width="24" height="14" rx="7" fill="#fff"/><path d="M144 220 L100 190 M456 220 L500 190" stroke="#fff" stroke-width="12" stroke-linecap="round"/>',
]
def slug(n): return re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")
IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "images")
def img(i):
    n = slug(PRODUCTS[i][0])
    return f"/static/images/{n}." + ("jpg" if os.path.exists(os.path.join(IMG_DIR, n + ".jpg")) else "svg")
def write_images():
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "images")
    os.makedirs(d, exist_ok=True)
    for i, p in enumerate(PRODUCTS):
        light, dark = COL[p[3]]
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 450"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{light}"/><stop offset="1" stop-color="{dark}"/></linearGradient></defs>'
               f'<rect width="600" height="450" fill="url(#g)"/>' + SHAPES[i].replace("DK", dark) + "</svg>")
        if not os.path.exists(os.path.join(d, slug(p[0]) + ".jpg")):
            with open(os.path.join(d, slug(p[0]) + ".svg"), "w", encoding="utf-8") as f: f.write(svg)
def seed(db):
    write_images()
    if db.execute("SELECT COUNT(*) FROM products").fetchone()[0]:
        for i, p in enumerate(PRODUCTS): db.execute("UPDATE products SET image_url=?, price=? WHERE name=?", (img(i), p[2], p[0]))
        return
    for i, (n, d, p, c, s, f) in enumerate(PRODUCTS):
        db.execute("INSERT INTO products(name,description,price,image_url,category,stock,featured) VALUES(?,?,?,?,?,?,?)", (n, d, p, img(i), c, s, f))
