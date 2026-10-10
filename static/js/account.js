window.pageInit = () => {
  if (!USER) { location.href = "/login"; return; }
  $("#account").innerHTML = `<p><b>Name:</b> ${esc(USER.name)}</p><p><b>Email:</b> ${esc(USER.email)}</p><p><b>Member since:</b> ${esc(USER.created_at)}</p><a class="btn ghost" href="/orders">My orders</a> <button class="btn" id="out">Log out</button>`;
  $("#out").onclick = async () => { await post("/api/logout"); location.href = "/"; };
};
