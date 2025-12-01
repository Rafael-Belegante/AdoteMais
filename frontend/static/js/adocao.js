async function solicitarAdocao(id_animal) {
  const user = getUser();
  if (!user || user.tipo !== "usuario") {
    alert("Você precisa estar logado como USUÁRIO para solicitar adoção.");
    window.location.href = "login.html";
    return;
  }

  const confirmar = confirm("Confirmar pedido de adoção para este animal?");
  if (!confirmar) return;

  try {
    await apiRequest("/adocoes/", {
      method: "POST",
      body: JSON.stringify({ id_animal }),
    });
    alert(
      "Pedido de adoção enviado com sucesso! Acompanhe o status em 'Minhas Adoções'."
    );
  } catch (e) {
    alert(e.message);
  }
}
