async function carregarMinhasAdocoes() {
  const tbody = document.getElementById("tabela-minhas-adocoes");
  if (!tbody) return;

  tbody.innerHTML = "<tr><td colspan='5'>Carregando...</td></tr>";

  try {
    const adocoes = await apiRequest("/adocoes/minhas");
    tbody.innerHTML = "";

    if (!adocoes.length) {
      tbody.innerHTML =
        "<tr><td colspan='5'>Você ainda não fez pedidos de adoção.</td></tr>";
      return;
    }

    for (const a of adocoes) {
      const animal = await apiRequest(`/animais/${a.id_animal}`);
      let anuncianteNome = "-";
      if (animal.id_anunciante) {
        try {
          const anunciante = await apiRequest(
            `/usuarios/${animal.id_anunciante}`
          );
          anuncianteNome = anunciante.nome;
        } catch {
          // silencioso; se der 403/404 só mostra "-"
        }
      }

      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${a.id_adocao}</td>
        <td>${animal.nome}</td>
        <td>${anuncianteNome}</td>
        <td>${a.mensagem_anunciante || "-"}</td>
        <td>${a.status}</td>
      `;
      tbody.appendChild(tr);
    }
  } catch (e) {
    tbody.innerHTML = `<tr><td colspan="5">${e.message}</td></tr>`;
  }
}

function carregarPerfilUsuario() {
  const user = getUser();
  const el = document.getElementById("perfil-usuario");
  if (!user || !el) return;

  el.innerHTML = `
    <p><strong>Nome:</strong> ${user.nome}</p>
    <p><strong>E-mail:</strong> ${user.email}</p>
    <p><strong>Telefone:</strong> ${user.telefone || "-"}</p>
    <p><strong>Tipo:</strong> ${user.tipo}</p>
  `;
}

document.addEventListener("DOMContentLoaded", () => {
  const user = getUser();
  if (!user || user.tipo !== "usuario") {
    window.location.href = "login.html";
    return;
  }

  const page = document.body.dataset.page || "";

  if (page === "mural-usuario") {
    registrarFiltro("lista-animais-usuario", "form-filtro-usuario");
    carregarPerfilUsuario();
  } else if (page === "minhas-adocoes") {
    carregarMinhasAdocoes();
  }
});
