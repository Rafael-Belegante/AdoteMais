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
                    body
                });
                if (!res.ok) {
                    const err = await res.json();
                    throw new Error(err.detail || "Erro ao logar");
                }
                const tokenData = await res.json();
                localStorage.setItem("token", tokenData.access_token);

                // Busca dados do usuário logado
                const me = await apiRequest("/auth/me");
                localStorage.setItem("user", JSON.stringify(me));

                alert("Login realizado com sucesso!");

                if (me.tipo === "ong") {
                    window.location.href = "painel_ong.html";
                } else if (me.tipo === "admin") {
                    window.location.href = "painel_admin.html";
                } else {
                    window.location.href = "painel_usuario.html";
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
                tipo: data.get("tipo") || "usuario"   // 👈 lê o select
            };

            try {
                const user = await apiRequest("/auth/register", {
                    method: "POST",
                    body: JSON.stringify(payload)
                });
                localStorage.setItem("user", JSON.stringify(user));
                alert("Cadastro realizado! Agora faça login.");
            } catch (e) {
                alert(e.message);
            }
        });
    }
});
