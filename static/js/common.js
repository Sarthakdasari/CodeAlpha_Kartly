const $ = s => document.querySelector(s);
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const money = n => new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 }).format(n);
const FALLBACK = "data:image/svg+xml;utf8," + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="600" height="450"><rect fill="#eef0ff" width="100%" height="100%"/><text x="50%" y="50%" fill="#6366f1" font-family="sans-serif" text-anchor="middle">No image</text></svg>');
function toast(msg, bad) {
  const t = document.createElement("div"); t.className = "toast" + (bad ? " bad" : ""); t.textContent = msg;
  $("#toasts").append(t); setTimeout(() => t.remove(), 3500);
}
let USER = null;
async function whoami() { const d = await get("/api/me"); USER = d.user; return USER; }
async function refreshCount() { try { $("#cartcount").textContent = USER ? (await get("/api/cart")).count : 0; } catch (e) {} }
const short = (t, n = 70) => { t = t.replace(/\.$/, ""); if (t.length <= n) return t + "."; const c = t.slice(0, n); return c.slice(0, c.lastIndexOf(" ")) + "…"; };
function card(p) {
  return `<article class="pcard"><a href="/product?id=${p.id}"><img loading="lazy" src="${esc(p.image_url)}" alt="${esc(p.name)}" onerror="this.onerror=null;this.src=FALLBACK"></a>
  <div class="pb"><small>${esc(p.category)}</small><h3>${esc(p.name)}</h3><p>${esc(short(p.description))}</p><div class="row"><b>${money(p.price)}</b>
  <span class="${p.stock ? (p.stock < 5 ? "low" : "ok") : "out"}">${p.stock ? (p.stock < 5 ? "Only " + p.stock + " left" : "In stock") : "Out of stock"}</span></div>
  <div class="row"><a class="btn ghost" href="/product?id=${p.id}">Details</a><button class="btn" data-add="${p.id}" ${p.stock ? "" : "disabled"}>Add to Cart</button></div></div></article>`;
}
async function addToCart(id, q = 1) {
  if (!USER) { location.href = "/login"; return; }
  try { await post("/api/cart/items/" + id, { quantity: q }); toast("Added to cart"); refreshCount(); } catch (e) { toast(e.message, true); }
}
document.addEventListener("click", e => { const b = e.target.closest("[data-add]"); if (b) addToCart(+b.dataset.add); });
function showGrid(el, list) { el.innerHTML = list.length ? list.map(card).join("") : '<p class="empty">No products found.</p>'; }
(async () => {
  try { await whoami(); } catch (e) {}
  if (USER) { const a = $("#authlink"); a.textContent = USER.name.split(" ")[0]; a.href = "/account"; }
  await refreshCount();
  if (window.pageInit) window.pageInit();
})();
