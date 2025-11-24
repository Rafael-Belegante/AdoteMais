async function carregarUsuarios() {
    const tbody = document.getElementById("tabela-usuarios");
    if (!tbody) return;

    try {
        const usuarios = await apiRequest("/usuarios/");
        tbody.innerHTML = "";

        if (!usuarios.length) {
            tbody.innerHTML = "<tr><td colspan='5'>Nenhum usuário cadastrado.</td></tr>";
            return;
        }

        usuarios.forEach(u => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${u.id_usuario}</td>
                <td>${u.nome}</td>
                <td>${u.email}</td>
                <td>${u.telefone || ""}</td>
                <td>${u.tipo}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        tbody.innerHTML = `<tr><td colspan="5">${e.message}</td></tr>`;
    }
}

document.addEventListener("DOMContentLoaded", carregarUsuarios);
