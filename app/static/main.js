
const API_BASE = "";

function setToken(token) { localStorage.setItem("token", token); }
function getToken() { return localStorage.getItem("token") || ""; }
function logout() { localStorage.removeItem("token"); alert("Sesión cerrada."); window.location.href = "/login"; }

document.addEventListener("DOMContentLoaded", () => {
  const logoutLink = document.getElementById("logoutLink");
  if (logoutLink) logoutLink.addEventListener("click", (e) => { e.preventDefault(); logout(); });

  // LOGIN
  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;

      const form = new URLSearchParams();
      form.append("username", username);
      form.append("password", password);
      form.append("grant_type", "");

      const res = await fetch(`${API_BASE}/auth/token`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: form.toString()
      });
      const data = await res.json();
      if (res.ok) {
        setToken(data.access_token);
        document.getElementById("loginMsg").textContent = "Login exitoso.";
        setTimeout(() => window.location.href = "/", 400);
      } else {
        document.getElementById("loginMsg").textContent = data.detail || "Error de login";
      }
    });
  }

  // CLIENTE: REGISTER
  const registerForm = document.getElementById("registerForm");
  if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const nombre = document.getElementById("nombre").value;
      const telefono = document.getElementById("telefono").value;
      const form = new FormData();
      form.append("nombre", nombre);
      form.append("telefono", telefono);

      const res = await fetch(`${API_BASE}/clients/register`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${getToken()}` },
        body: form
      });
      const data = await res.json();
      document.getElementById("registerMsg").textContent = JSON.stringify(data, null, 2);
    });
  }

  // CLIENTE: UPLOAD
  const uploadForm = document.getElementById("uploadForm");
  if (uploadForm) {
    uploadForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const clientId = document.getElementById("clientId").value;
      const fileInput = document.getElementById("fileInput");
      const form = new FormData();
      form.append("file", fileInput.files[0]);

      const res = await fetch(`${API_BASE}/clients/${clientId}/upload`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${getToken()}` },
        body: form
      });
      const data = await res.json();
      document.getElementById("uploadMsg").textContent = JSON.stringify(data, null, 2);
    });
  }

  // ADMIN1: documents
  const docsForm = document.getElementById("docsForm");
  if (docsForm) {
    docsForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const id = document.getElementById("docsClientId").value;
      const res = await fetch(`${API_BASE}/clients/${id}/documents`, {
        headers: { "Authorization": `Bearer ${getToken()}` }
      });
      const data = await res.json();
      document.getElementById("docsOut").textContent = JSON.stringify(data, null, 2);
    });
  }

  // ADMIN1: report
  const reportForm = document.getElementById("reportForm");
  if (reportForm) {
    reportForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const id = document.getElementById("reportClientId").value;
      const res = await fetch(`${API_BASE}/reports/client/${id}`, {
        headers: { "Authorization": `Bearer ${getToken()}` }
      });
      const data = await res.json();
      document.getElementById("reportOut").textContent = JSON.stringify(data, null, 2);
    });
  }

  // ADMIN2: KPIs + Chart
  const kbtn = document.getElementById("loadKpisBtn");
  if (kbtn) {
    kbtn.addEventListener("click", async () => {
      const res = await fetch(`${API_BASE}/dashboard/kpis`, {
        headers: { "Authorization": `Bearer ${getToken()}` }
      });
      const data = await res.json();
      document.getElementById("kpisOut").textContent = JSON.stringify(data, null, 2);
      const ctx = document.getElementById("chart").getContext("2d");
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['Clientes', 'Documentos'],
          datasets: [{ label: 'KPIs', data: [data.total_clients || 0, data.total_documents || 0] }]
        }
      });
    });
  }
});
