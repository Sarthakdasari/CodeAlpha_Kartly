async function draw() {
  const el = $("#cart");
  if (!USER) { el.innerHTML = '<p class="empty">Please <a href="/login">log in</a> to view your cart.</p>'; return; }
  const c = await get("/api/cart"); refreshCount();
  if (!c.items.length) { el.innerHTML = '<p class="empty">Your cart is empty.</p><a class="btn" href="/products">Continue Shopping</a>'; return; }
  el.innerHTML = c.items.map(i => `<div class="line"><img src="${esc(i.image_url)}" alt="" onerror="this.src=FALLBACK"><div class="grow"><b>${esc(i.name)}</b><br>${money(i.price)}</div>
  <div class="qty"><button class="btn ghost" data-q="${i.product_id}:${i.quantity - 1}" aria-label="Decrease">−</button><span>${i.quantity}</span><button class="btn ghost" data-q="${i.product_id}:${i.quantity + 1}" aria-label="Increase">+</button></div>
  <b>${money(i.subtotal)}</b><button class="btn ghost" data-rm="${i.product_id}">Remove</button></div>`).join("") +
  `<h2>Total: ${money(c.total)}</h2><a class="btn ghost" href="/products">Continue Shopping</a> <a class="btn big" href="/checkout">Proceed to Checkout</a>`;
}
window.pageInit = () => {
  draw().catch(e => toast(e.message, true));
  $("#cart").addEventListener("click", async e => {
    const q = e.target.closest("[data-q]"), r = e.target.closest("[data-rm]");
    try {
      if (q) { const [id, n] = q.dataset.q.split(":"); +n < 1 ? await del("/api/cart/items/" + id) : await put("/api/cart/items/" + id, { quantity: +n }); }
      else if (r && confirm("Remove this item?")) await del("/api/cart/items/" + r.dataset.rm); else return;
      draw();
    } catch (err) { toast(err.message, true); }
  });
};
