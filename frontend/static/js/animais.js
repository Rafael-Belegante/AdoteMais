async function carregarAnimais() {
    const container = document.getElementById("lista-animais");
    if (!container) return;

    try {
        const animais = await apiRequest("/animais/");
        container.innerHTML = "";

        if (!animais.length) {
            container.innerHTML = "<p>Nenhum animal disponível no momento.</p>";
            return;
        }

        animais.forEach(a => {
            const card = document.createElement("div");
            card.className = "card";

            const img = document.createElement("img");
            img.src = a.foto_url || "img/placeholder.jpg";
            img.alt = a.nome;
            card.appendChild(img);

            const h3 = document.createElement("h3");
            h3.textContent = a.nome;
            card.appendChild(h3);

            const p = document.createElement("p");
            p.textContent = a.descricao || "Sem descrição.";
            card.appendChild(p);

            const btn = document.createElement("button");
            btn.textContent = "Quero adotar";
            btn.onclick = () => solicitarAdocao(a.id_animal);
            card.appendChild(btn);

            container.appendChild(card);
        });
    } catch (e) {
        console.error(e);
    }
}

async function solicitarAdocao(id_animal) {
    const userId = getUserId();
    if (!userId) {
        alert("Você precisa estar logado como usuário para solicitar adoção.");
        window.location.href = "login.html";
        return;
    }

    try {
        await apiRequest("/adocoes/", {
            method: "POST",
            body: JSON.stringify({ id_usuario: userId, id_animal })
        });
        alert("Solicitação de adoção enviada com sucesso!");
    } catch (e) {
        alert(e.message);
    }
}

document.addEventListener("DOMContentLoaded", carregarAnimais);
