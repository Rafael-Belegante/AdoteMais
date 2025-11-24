async function carregarAdocoesPendentes() {
    const tbody = document.getElementById("tabela-adocoes");
    if (!tbody) return;

    try {
        const adocoes = await apiRequest("/adocoes/pendentes");
        tbody.innerHTML = "";

        if (!adocoes.length) {
            tbody.innerHTML = "<tr><td colspan='6'>Nenhuma solicitação pendente.</td></tr>";
            return;
        }

        for (const a of adocoes) {
            const [animal, adotante] = await Promise.all([
                apiRequest(`/animais/${a.id_animal}`),
                apiRequest(`/usuarios/${a.id_usuario}`)
            ]);

            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${a.id_adocao}</td>
                <td>${animal.nome}</td>
                <td>${adotante.nome}</td>
                <td>${adotante.email}<br>${adotante.telefone || ""}</td>
                <td>${a.status}</td>
                <td>
                    <button data-id="${a.id_adocao}" data-acao="aprovar">Aprovar</button>
                    <button data-id="${a.id_adocao}" data-acao="negar">Negar</button>
                </td>
            `;
            tbody.appendChild(tr);
        }

        tbody.addEventListener("click", async (e) => {
            const btn = e.target.closest("button");
            if (!btn) return;
            const id = btn.getAttribute("data-id");
            const acao = btn.getAttribute("data-acao");
            if (!id || !acao) return;

            const path = acao === "aprovar" ? `/adocoes/${id}/aprovar` : `/adocoes/${id}/negar`;
            try {
                await apiRequest(path, { method: "PUT" });
                alert(`Adoção ${acao}ada com sucesso!`);
                carregarAdocoesPendentes();
            } catch (err) {
                alert(err.message);
            }
        }, { once: true });
    } catch (e) {
        tbody.innerHTML = `<tr><td colspan="6">${e.message}</td></tr>`;
    }
}

document.addEventListener("DOMContentLoaded", carregarAdocoesPendentes);
