window.pageInit = async () => {
  const id = new URLSearchParams(location.search).get("id");
  try {
    const p = (await get("/api/products/" + encodeURIComponent(id))).product;
    $("#detail").innerHTML = `<div class="two"><img class="big-img" src="${esc(p.image_url)}" alt="${esc(p.name)}" onerror="this.onerror=null;this.src=FALLBACK"><div><small>${esc(p.category)}</small><h1>${esc(p.name)}</h1><p>${esc(p.description)}</p><h2>${money(p.price)}</h2><p>${p.stock ? p.stock + " in stock" : "Out of stock"}</p>
    <label>Quantity<input id="qty" type="number" min="1" max="${p.stock}" value="1"></label><button class="btn big" id="add" ${p.stock ? "" : "disabled"}>Add to Cart</button></div></div>`;
    $("#add").onclick = () => addToCart(p.id, Math.max(1, parseInt($("#qty").value) || 1));
    showGrid($("#related"), (await get("/api/products?category=" + encodeURIComponent(p.category))).products.filter(x => x.id !== p.id).slice(0, 4));
  } catch (e) { $("#detail").innerHTML = `<p class="error">${esc(e.message)}</p>`; }
};
