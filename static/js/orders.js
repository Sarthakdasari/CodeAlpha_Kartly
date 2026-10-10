window.pageInit = async () => {
  if (!USER) { location.href = "/login"; return; }
  try {
    const os = (await get("/api/orders")).orders;
    $("#orders").innerHTML = os.length ? os.map(o => `<div class="card"><h3>Order #${o.id} <span class="ok">${esc(o.order_status)}</span></h3><small>${esc(o.created_at)}</small>${o.items.map(i => `<p>${esc(i.product_name)} × ${i.quantity} @ ${money(i.unit_price)} = ${money(i.subtotal)}</p>`).join("")}<b>Total: ${money(o.total_amount)}</b></div>`).join("")
      : '<p class="empty">No orders yet.</p><a class="btn" href="/products">Start shopping</a>';
  } catch (e) { toast(e.message, true); }
};
