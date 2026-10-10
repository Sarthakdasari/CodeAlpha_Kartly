window.pageInit = async () => {
  if (!USER) { location.href = "/login"; return; }
  const c = await get("/api/cart");
  if (!c.items.length) { $("#summary").innerHTML = '<p class="empty">Your cart is empty.</p><a class="btn" href="/products">Shop</a>'; $("#place").disabled = true; }
  else $("#summary").innerHTML = "<h2>Order summary</h2>" + c.items.map(i => `<p>${esc(i.name)} × ${i.quantity} <b>${money(i.subtotal)}</b></p>`).join("") + `<h3>Total: ${money(c.total)}</h3><small>Payment: Cash on Delivery</small>`;
  $("#coform").onsubmit = async ev => {
    ev.preventDefault(); const d = Object.fromEntries(new FormData(ev.target)), m = $("#msg"), b = $("#place");
    if (!d.customer_name.trim() || !/^[0-9+\-\s]{7,15}$/.test(d.phone) || d.shipping_address.trim().length < 10) return m.textContent = "Enter your name, a valid phone number and full address.";
    b.disabled = true; m.textContent = "";
    try {
      const o = (await post("/api/orders", d)).order; refreshCount();
      $("main").innerHTML = `<section class="card auth"><h1>Order confirmed</h1><p>Order #${o.id} for ${money(o.total_amount)} will be delivered to you. Pay on delivery.</p><a class="btn big" href="/orders">View orders</a></section>`;
    } catch (e) { m.textContent = e.message; b.disabled = false; }
  };
};
