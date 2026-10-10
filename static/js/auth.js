window.pageInit = () => {
  const f = $("#regform") || $("#loginform"), reg = !!$("#regform");
  if (USER) { location.href = "/account"; return; }
  $("#show").onchange = e => f.querySelectorAll('input[type=password],input[data-pw]').forEach(i => { i.type = e.target.checked ? "text" : "password"; i.dataset.pw = 1; });
  f.onsubmit = async ev => {
    ev.preventDefault(); const d = Object.fromEntries(new FormData(f)), m = $("#msg"); m.textContent = "";
    if (!d.email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.email)) return m.textContent = "Enter a valid email address.";
    if (!d.password) return m.textContent = "Password is required.";
    if (reg) {
      if (!d.name.trim()) return m.textContent = "Name is required.";
      if (d.password.length < 8 || !/\d/.test(d.password) || !/[A-Za-z]/.test(d.password)) return m.textContent = "Password needs 8+ characters with letters and numbers.";
      if (d.password !== d.confirm) return m.textContent = "Passwords do not match.";
    }
    try { await post(reg ? "/api/register" : "/api/login", d); location.href = "/products"; } catch (e) { m.textContent = e.message; }
  };
};
