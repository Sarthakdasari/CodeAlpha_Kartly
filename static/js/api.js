let _csrf = null;
async function api(method, url, body) {
  const o = { method, credentials: "same-origin", headers: {} };
  if (method !== "GET") {
    if (!_csrf) _csrf = (await (await fetch("/api/csrf", { credentials: "same-origin" })).json()).csrf;
    o.headers["X-CSRF-Token"] = _csrf;
  }
  if (body !== undefined) { o.headers["Content-Type"] = "application/json"; o.body = JSON.stringify(body); }
  const r = await fetch(url, o); let d = {};
  try { d = await r.json(); } catch (e) {}
  if (!r.ok) { const e = new Error(d.error || "Request failed"); e.status = r.status; throw e; }
  return d;
}
const get = u => api("GET", u), post = (u, b) => api("POST", u, b || {}), put = (u, b) => api("PUT", u, b), del = u => api("DELETE", u);
