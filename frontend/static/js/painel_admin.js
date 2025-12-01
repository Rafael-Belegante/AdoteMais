async function carregarUsuarios() {
  const tbody = document.getElementById("tabela-usuarios");
  if (!tbody) return;

  tbody.innerHTML = "<tr><td colspan='6'>Carregando...</td></tr>";

  try {
    const usuarios = await apiRequest("/usuarios/");
    tbody.innerHTML = "";

    if (!usuarios.length) {
      tbody.innerHTML = "<tr><td colspan='6'>Nenhum usuário cadastrado.</td></tr>";
      return;
    }

    usuarios.forEach((u) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${u.id_usuario}</td>
        <td>${u.nome}</td>
        <td>${u.email}</td>
        <td>${u.telefone || ""}</td>
        <td>${u.tipo}</td>
        <td>
          <button class="btn-secondary" data-acao="editar" data-id="${u.id_usuario}">Editar</button>
          <button data-acao="excluir" data-id="${u.id_usuario}">Excluir</button>
        </td>
      `;
      tbody.appendChild(tr);
    });

    tbody.addEventListener("click", async (e) => {
      const btn = e.target.closest("button");
      if (!btn) return;
      const id = btn.getAttribute("data-id");
      const acao = btn.getAttribute("data-acao");
      if (!id || !acao) return;

      if (acao === "excluir") {
        if (!confirm("Confirma excluir este usuário?")) return;
        try {
          await apiRequest(`/usuarios/${id}`, { method: "DELETE" });
          carregarUsuarios();
        } catch (err) {
          alert(err.message);
        }
      } else if (acao === "editar") {
        const novoNome = prompt("Novo nome (deixe em branco para manter):");
        const novoEmail = prompt("Novo e-mail (deixe em branco para manter):");
        const novoTelefone = prompt("Novo telefone (deixe em branco para manter):");
        const novoTipo = prompt("Novo tipo (usuario, anunciante, admin ou vazio):");
        const novaSenha = prompt("Nova senha (deixe em branco para manter):");

        const payload = {};
        if (novoNome) payload.nome = novoNome;
        if (novoEmail) payload.email = novoEmail;
        if (novoTelefone) payload.telefone = novoTelefone;
        if (novoTipo) payload.tipo = novoTipo;
        if (novaSenha) payload.senha = novaSenha;

        try {
          await apiRequest(`/usuarios/${id}`, {
            method: "PUT",
            body: JSON.stringify(payload),
          });
          carregarUsuarios();
        } catch (err) {
          alert(err.message);
        }
      }
    }, { once: true });
  } catch (e) {
    tbody.innerHTML = `<tr><td colspan="6">${e.message}</td></tr>`;
  }
}

async function criarUsuario(e) {
  e.preventDefault();
  const form = e.target;
  const data = new FormData(form);
  const payload = {
    nome: data.get("nome"),
    email: data.get("email"),
    telefone: data.get("telefone"),
    senha: data.get("senha"),
    tipo: data.get("tipo"),
  };

  try {
    await apiRequest("/usuarios/", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    alert("Usuário criado com sucesso!");
    form.reset();
    carregarUsuarios();
  } catch (e) {
    alert(e.message);
  }
}

async function carregarLogs() {
  const tbody = document.getElementById("tabela-logs");
  if (!tbody) return;

  tbody.innerHTML = "<tr><td colspan='4'>Carregando...</td></tr>";

  try {
    const formFiltro = document.getElementById("form-filtro-logs");
    let qs = "";
    if (formFiltro) {
      const data = new FormData(formFiltro);
      const id_usuario = data.get("id_usuario");
      if (id_usuario) {
        qs = buildQuery({ id_usuario });
      }
    }

    const logs = await apiRequest(`/logs/${qs}`);
    tbody.innerHTML = "";

    if (!logs.length) {
      tbody.innerHTML = "<tr><td colspan='4'>Nenhum log encontrado.</td></tr>";
      return;
    }

    logs.forEach((l) => {
      const dt = new Date(l.data_hora);
      const dia = dt.toLocaleDateString("pt-BR");
      const hora = dt.toLocaleTimeString("pt-BR", {
        hour: "2-digit",
        minute: "2-digit",
      });
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${l.id_log}</td>
        <td>${dia} ${hora}</td>
        <td>${l.id_usuario || "-"}</td>
        <td><strong>${l.acao}</strong> - ${l.detalhe || ""}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (e) {
    tbody.innerHTML = `<tr><td colspan="4">${e.message}</td></tr>`;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const user = getUser();
  if (!user || user.tipo !== "admin") {
    window.location.href = "login.html";
    return;
  }

  const formCriar = document.getElementById("form-criar-usuario");
  if (formCriar) {
    formCriar.addEventListener("submit", criarUsuario);
  }

  const formFiltroLogs = document.getElementById("form-filtro-logs");
  if (formFiltroLogs) {
    formFiltroLogs.addEventListener("submit", (e) => {
      e.preventDefault();
      carregarLogs();
    });
  }

  carregarUsuarios();
  carregarLogs();
});
