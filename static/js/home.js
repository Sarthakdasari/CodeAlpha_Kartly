window.pageInit = async () => {
  $("#featured").innerHTML = $("#popular").innerHTML = '<p class="empty">Loading…</p>';
  try {
    showGrid($("#featured"), (await get("/api/products?featured=1")).products);
    showGrid($("#popular"), (await get("/api/products?sort=popular")).products.slice(0, 4));
    $("#cats").innerHTML = (await get("/api/categories")).categories.map(c => `<a class="cat" href="/products?category=${encodeURIComponent(c)}">${esc(c)}</a>`).join("");
  } catch (e) { toast(e.message, true); }
};
