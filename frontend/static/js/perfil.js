document.addEventListener("DOMContentLoaded", () => {
  const user = getUser();
  const tipoPagina = document.body.dataset.perfilTipo; // "usuario" ou "anunciante"

  if (!user || (tipoPagina && user.tipo !== tipoPagina)) {
    window.location.href = "login.html";
    return;
  }

  const form = document.getElementById("form-perfil");
  if (!form) return;

  // preencher campos
  form.nome.value = user.nome || "";
  form.email.value = user.email || "";
  form.telefone.value = user.telefone || "";

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = new FormData(form);
    const payload = {
      nome: data.get("nome"),
      telefone: data.get("telefone") || null,
    };

    try {
      const atualizado = await apiRequest("/auth/me", {
        method: "PUT",
        body: JSON.stringify(payload),
      });
      localStorage.setItem("user", JSON.stringify(atualizado));
      alert("Perfil atualizado com sucesso!");
    } catch (err) {
      alert(err.message);
    }
  });
});
