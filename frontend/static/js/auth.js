document.addEventListener("DOMContentLoaded", () => {
  const formLogin = document.getElementById("form-login");
  const formRegister = document.getElementById("form-register");

  if (formLogin) {
    formLogin.addEventListener("submit", async (e) => {
      e.preventDefault();
      const data = new FormData(formLogin);
      const email = data.get("email");
      const senha = data.get("senha");

      const body = new URLSearchParams();
      body.append("username", email);
      body.append("password", senha);

      try {
        const res = await fetch(`${API_BASE}/auth/login`, {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body,
        });
        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.detail || "Erro ao realizar login");
        }
        const tokenData = await res.json();
        localStorage.setItem("token", tokenData.access_token);

        const me = await apiRequest("/auth/me");
        localStorage.setItem("user", JSON.stringify(me));

        if (me.tipo === "anunciante") {
          window.location.href = "painel_anunciante.html";
        } else if (me.tipo === "admin") {
          window.location.href = "painel_admin.html";
        } else {
          window.location.href = "index.html";
        }
      } catch (e) {
        alert(e.message);
      }
    });
  }

  if (formRegister) {
    formRegister.addEventListener("submit", async (e) => {
      e.preventDefault();
      const data = new FormData(formRegister);
      const payload = {
        nome: data.get("nome"),
        email: data.get("email"),
        telefone: data.get("telefone"),
        senha: data.get("senha"),
        tipo: data.get("tipo") || "usuario",
      };

      try {
        await apiRequest("/auth/register", {
          method: "POST",
          body: JSON.stringify(payload),
        });
        alert("Cadastro realizado! Agora faça login.");
      } catch (e) {
        alert(e.message);
      }
    });
  }
});
