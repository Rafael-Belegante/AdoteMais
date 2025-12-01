async function carregarDetalheAnimal() {
  const params = new URLSearchParams(window.location.search);
  const id = params.get("id");
  const container = document.getElementById("animal-detalhe");
  if (!id || !container) {
    if (container) container.innerHTML = "<p>Animal não encontrado.</p>";
    return;
  }

  try {
    const a = await apiRequest(`/animais/${id}`);
    container.innerHTML = "";

    const layout = document.createElement("div");
    layout.className = "detail-layout";

    const colImg = document.createElement("div");
    const img = document.createElement("img");
    if (a.foto_url) {
      const url =
        a.foto_url.startsWith("http") ? a.foto_url : `${API_BASE}${a.foto_url}`;
      img.src = url;
    } else {
      img.src = "https://placehold.co/800x500?text=ADOTE+";
    }
    img.alt = a.nome;
    colImg.appendChild(img);


    const colInfo = document.createElement("div");
    const h2 = document.createElement("h2");
    h2.textContent = a.nome;
    colInfo.appendChild(h2);

    const meta = document.createElement("div");
    meta.className = "card-meta";
    const partes = [];
    if (a.especie) partes.push(a.especie);
    if (a.raca) partes.push(a.raca);
    if (a.porte) partes.push("Porte " + a.porte);
    if (a.sexo) partes.push(a.sexo);
    meta.textContent = partes.join(" • ");
    colInfo.appendChild(meta);

    const p = document.createElement("p");
    p.textContent = a.descricao || "Sem descrição disponível.";
    colInfo.appendChild(p);

    const actions = document.createElement("div");
    actions.className = "card-actions";

    const btnAdotar = document.createElement("button");
    btnAdotar.textContent = "Quero adotar";
    btnAdotar.addEventListener("click", () => solicitarAdocao(a.id_animal));
    actions.appendChild(btnAdotar);

    colInfo.appendChild(actions);

    layout.appendChild(colImg);
    layout.appendChild(colInfo);
    container.appendChild(layout);
  } catch (e) {
    container.innerHTML = `<p>${e.message}</p>`;
  }
}

document.addEventListener("DOMContentLoaded", carregarDetalheAnimal);
