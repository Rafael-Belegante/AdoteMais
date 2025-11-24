document.addEventListener("DOMContentLoaded", async () => {
    const btnSair = document.getElementById("btn-sair");
    if (btnSair) {
        btnSair.addEventListener("click", () => {
            localStorage.removeItem("token");
            localStorage.removeItem("user");
            window.location.href = "index.html";
        });
    }

    const token = getToken();
    if (token && !localStorage.getItem("user")) {
        try {
            const me = await apiRequest("/auth/me");
            localStorage.setItem("user", JSON.stringify(me));
        } catch (e) {
            console.warn("Token inválido, limpando sessão.");
            localStorage.removeItem("token");
            localStorage.removeItem("user");
        }
    }
});
