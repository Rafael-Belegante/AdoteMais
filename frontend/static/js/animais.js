async function carregarAnimais(containerId, filtros = {}) {
  const container = document.getElementById(containerId);
  if (!container) return;

  container.innerHTML = "<p>Carregando animais...</p>";

  try {
    const qs = buildQuery(filtros);
    const animais = await apiRequest(`/animais/${qs}`);
    container.innerHTML = "";

    if (!animais.length) {
      container.innerHTML = "<p>Nenhum animal encontrado.</p>";
      return;
    }

    animais.forEach((a) => {
      const card = document.createElement("div");
      card.className = "card";

      const img = document.createElement("img");
      if (a.foto_url) {
        const url =
          a.foto_url.startsWith("http") ? a.foto_url : `${API_BASE}${a.foto_url}`;
        img.src = url;
      } else {
        img.src = "https://placehold.co/600x400?text=ADOTE+";
      }
      img.alt = a.nome;
      card.appendChild(img);

      const h3 = document.createElement("h3");
      h3.textContent = a.nome;
      card.appendChild(h3);

      const meta = document.createElement("div");
      meta.className = "card-meta";
      const partes = [];
      if (a.especie) partes.push(a.especie);
      if (a.raca) partes.push(a.raca);
      if (a.porte) partes.push("Porte " + a.porte);
      if (a.sexo) partes.push(a.sexo);
      meta.textContent = partes.join(" • ");
      card.appendChild(meta);

      const p = document.createElement("p");
      p.textContent = a.descricao || "Sem descrição.";
      card.appendChild(p);

      const actions = document.createElement("div");
      actions.className = "card-actions";

      const btnDetalhes = document.createElement("button");
      btnDetalhes.className = "btn-secondary";
      btnDetalhes.textContent = "Ver detalhes";
      btnDetalhes.addEventListener("click", () => {
        window.location.href = `animal.html?id=${a.id_animal}`;
      });
      actions.appendChild(btnDetalhes);

      const btnAdotar = document.createElement("button");
      btnAdotar.textContent = "Quero adotar";
      btnAdotar.addEventListener("click", () => solicitarAdocao(a.id_animal));
      actions.appendChild(btnAdotar);

      card.appendChild(actions);
      container.appendChild(card);
    });
  } catch (e) {
    container.innerHTML = `<p>${e.message}</p>`;
  }
}

function registrarFiltro(containerId, formId) {
  const form = document.getElementById(formId);
  if (!form) return;

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const data = new FormData(form);

    const filtros = {};
    const q = (data.get("q") || "").trim();
    const especie = (data.get("especie") || "").trim();
    const porte = (data.get("porte") || "").trim();
    const sexo = (data.get("sexo") || "").trim();

    if (q) filtros.q = q;
    if (especie) filtros.especie = especie;
    if (porte) filtros.porte = porte;
    if (sexo) filtros.sexo = sexo;

    carregarAnimais(containerId, filtros);
  });

  // carga inicial sem filtros
  carregarAnimais(containerId, {});
}
