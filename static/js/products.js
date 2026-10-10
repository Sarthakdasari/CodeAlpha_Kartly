window.pageInit = async () => {
  const p = new URLSearchParams(location.search);
  $("#f-q").value = p.get("q") || "";
  const cats = (await get("/api/categories")).categories;
  $("#f-cat").innerHTML += cats.map(c => `<option ${p.get("category") === c ? "selected" : ""}>${esc(c)}</option>`).join("");
  async function load() {
    $("#grid").innerHTML = '<p class="empty">Loading…</p>';
    const qs = new URLSearchParams({ q: $("#f-q").value, category: $("#f-cat").value, sort: $("#f-sort").value });
    try { showGrid($("#grid"), (await get("/api/products?" + qs)).products); } catch (e) { $("#grid").innerHTML = '<p class="error">Could not load products.</p>'; }
  }
  let t; $("#f-q").oninput = () => { clearTimeout(t); t = setTimeout(load, 250); };
  $("#f-cat").onchange = $("#f-sort").onchange = load; load();
};
