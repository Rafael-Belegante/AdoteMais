// ====== LISTAGEM E CRUD DE ANIMAIS ======

async function carregarMeusAnimais() {
  const tbody = document.getElementById("tabela-meus-animais");
  if (!tbody) return;

  tbody.innerHTML = "<tr><td colspan='6'>Carregando...</td></tr>";

  try {
    const animais = await apiRequest("/animais/meus");
    tbody.innerHTML = "";

    if (!animais.length) {
      tbody.innerHTML =
        "<tr><td colspan='6'>Nenhum animal cadastrado.</td></tr>";
      return;
    }

    animais.forEach((a) => {
      const meta = [];
      if (a.especie) meta.push(a.especie);
      if (a.raca) meta.push(a.raca);
      if (a.porte) meta.push("Porte " + a.porte);
      if (a.sexo) meta.push(a.sexo);

      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${a.id_animal}</td>
        <td>${a.nome}</td>
        <td>${meta.join(" • ")}</td>
        <td>${a.status}</td>
        <td>${a.descricao || ""}</td>
        <td>
          <button class="btn-secondary" data-acao="editar" data-id="${a.id_animal}">Editar</button>
          <button data-acao="excluir" data-id="${a.id_animal}">Excluir</button>
        </td>
      `;
      tbody.appendChild(tr);
    });
  } catch (e) {
    tbody.innerHTML = `<tr><td colspan="6">${e.message}</td></tr>`;
  }
}

// Delegação de eventos para cliques na tabela
async function onTabelaAnimaisClick(e) {
  const btn = e.target.closest("button");
  if (!btn) return;

  const id = btn.getAttribute("data-id");
  const acao = btn.getAttribute("data-acao");
  if (!id || !acao) return;

  if (acao === "excluir") {
    await excluirAnimal(id);
  } else if (acao === "editar") {
    await editarAnimal(id);
  }
}

async function excluirAnimal(id) {
  const confirmar = confirm("Confirma excluir este animal?");
  if (!confirmar) return;

  try {
    await apiRequest(`/animais/${id}`, { method: "DELETE" });
    await carregarMeusAnimais();
  } catch (err) {
    alert(err.message);
  }
}

async function editarAnimal(id) {
  try {
    const animal = await apiRequest(`/animais/${id}`);

    const novoNome = prompt(
      "Novo nome (deixe em branco para manter):",
      animal.nome
    );
    const novaDescricao = prompt(
      "Nova descrição (deixe em branco para manter):",
      animal.descricao || ""
    );
    const novoStatus = prompt(
      "Novo status (disponivel, aguardando_aprovacao, adotado ou vazio para manter):",
      animal.status
    );

    const payload = {};

    if (novoNome && novoNome.trim() && novoNome !== animal.nome) {
      payload.nome = novoNome.trim();
    }
    if (
      novaDescricao &&
      novaDescricao.trim() &&
      novaDescricao !== animal.descricao
    ) {
      payload.descricao = novaDescricao.trim();
    }
    if (novoStatus && novoStatus.trim() && novoStatus !== animal.status) {
      payload.status = novoStatus.trim();
    }

    if (!Object.keys(payload).length) {
      return;
    }

    await apiRequest(`/animais/${id}`, {
      method: "PUT",
      body: JSON.stringify(payload),
    });
    await carregarMeusAnimais();
  } catch (err) {
    alert(err.message);
  }
}

async function cadastrarAnimal(e) {
  e.preventDefault();
  const form = e.target;
  const data = new FormData(form);

  const payload = {
    nome: data.get("nome"),
    descricao: data.get("descricao"),
    especie: data.get("especie"),
    raca: data.get("raca"),
    porte: data.get("porte"),
    sexo: data.get("sexo"),
    idade: data.get("idade") ? Number(data.get("idade")) : null,
    foto_url: data.get("foto_url") || null,
  };

  // upload de arquivo se tiver
  const file = data.get("foto");
  if (file && file.size > 0) {
    try {
      const fd = new FormData();
      fd.append("file", file);

      const res = await apiRequest("/upload/foto-animal", {
        method: "POST",
        body: fd,
      });

      if (res && res.url) {
        payload.foto_url = res.url;
      }
    } catch (e) {
      alert("Erro ao enviar imagem: " + e.message);
      return;
    }
  }

  try {
    await apiRequest("/animais/", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    alert("Animal cadastrado com sucesso!");
    form.reset();
    await carregarMeusAnimais();
  } catch (e) {
    alert(e.message);
  }
}

// ====== PEDIDOS DE ADOÇÃO ======

async function carregarPedidosPendentes() {
  const lista = document.getElementById("lista-pedidos");
  if (!lista) return;

  lista.innerHTML = "<p>Carregando pedidos...</p>";

  try {
    const adocoes = await apiRequest("/adocoes/pendentes");
    lista.innerHTML = "";

    if (!adocoes.length) {
      lista.innerHTML = "<p>Não há pedidos de adoção pendentes.</p>";
      return;
    }

    for (const a of adocoes) {
      const [animal, adotante] = await Promise.all([
        apiRequest(`/animais/${a.id_animal}`),
        apiRequest(`/usuarios/${a.id_usuario}`),
      ]);

      const card = document.createElement("div");
      card.className = "card";

      const h3 = document.createElement("h3");
      h3.textContent = `Pedido #${a.id_adocao} - ${animal.nome}`;
      card.appendChild(h3);

      const meta = document.createElement("div");
      meta.className = "card-meta";
      meta.textContent = `Adotante: ${adotante.nome} (${adotante.email})`;
      card.appendChild(meta);

      const p = document.createElement("p");
      p.textContent = `Status: ${a.status}`;
      card.appendChild(p);

      const actions = document.createElement("div");
      actions.className = "card-actions";

      const btnAprovar = document.createElement("button");
      btnAprovar.className = "btn-secondary";
      btnAprovar.textContent = "Aprovar";
      btnAprovar.addEventListener("click", async () => {
        // mensagem obrigatória
        let mensagem = null;
        while (true) {
          mensagem = prompt("Mensagem para o adotante (obrigatória):");
          if (mensagem === null) {
            // usuário cancelou -> não faz nada
            return;
          }
          mensagem = mensagem.trim();
          if (mensagem) break;
          alert("A mensagem é obrigatória para aprovar o pedido.");
        }

        try {
          await apiRequest(`/adocoes/${a.id_adocao}/aprovar`, {
            method: "PUT",
            body: JSON.stringify({ mensagem_anunciante: mensagem }),
          });
          await carregarPedidosPendentes();
          await carregarMeusAnimais();
        } catch (err) {
          alert(err.message);
        }
      });
      actions.appendChild(btnAprovar);

      const btnNegar = document.createElement("button");
      btnNegar.textContent = "Negar";
      btnNegar.addEventListener("click", async () => {
        // mensagem obrigatória
        let mensagem = null;
        while (true) {
          mensagem = prompt("Mensagem para o adotante (obrigatória):");
          if (mensagem === null) {
            return;
          }
          mensagem = mensagem.trim();
          if (mensagem) break;
          alert("A mensagem é obrigatória para negar o pedido.");
        }

        try {
          await apiRequest(`/adocoes/${a.id_adocao}/negar`, {
            method: "PUT",
            body: JSON.stringify({ mensagem_anunciante: mensagem }),
          });
          await carregarPedidosPendentes();
          await carregarMeusAnimais();
        } catch (err) {
          alert(err.message);
        }
      });
      actions.appendChild(btnNegar);

      card.appendChild(actions);
      lista.appendChild(card);
    }
  } catch (e) {
    lista.innerHTML = `<p>${e.message}</p>`;
  }
}

// ====== PERFIL (LEITURA SIMPLES) ======

function carregarPerfilAnunciante() {
  const user = getUser();
  const el = document.getElementById("perfil-anunciante");
  if (!user || !el) return;

  el.innerHTML = `
    <p><strong>Nome:</strong> ${user.nome}</p>
    <p><strong>E-mail:</strong> ${user.email}</p>
    <p><strong>Telefone:</strong> ${user.telefone || "-"}</p>
    <p><strong>Tipo:</strong> ${user.tipo}</p>
  `;
}

// ====== INICIALIZAÇÃO POR PÁGINA ======

document.addEventListener("DOMContentLoaded", () => {
  const user = getUser();
  if (!user || user.tipo !== "anunciante") {
    window.location.href = "login.html";
    return;
  }

  const page = document.body.dataset.page || "";

  // Página de animais (cadastro/gerência)
  if (page === "painel-anunciante") {
    const formAnimal = document.getElementById("form-animal-anunciante");
    if (formAnimal) {
      formAnimal.addEventListener("submit", cadastrarAnimal);
    }

    const tbody = document.getElementById("tabela-meus-animais");
    if (tbody) {
      // listener único, sem { once: true }
      tbody.addEventListener("click", onTabelaAnimaisClick);
    }

    carregarMeusAnimais();
    carregarPerfilAnunciante();
  }

  // Página de pedidos
  if (page === "pedidos-anunciante") {
    carregarPedidosPendentes();
    carregarPerfilAnunciante();
  }
});
