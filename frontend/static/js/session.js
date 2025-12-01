function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  window.location.href = "index.html";
}

function ensureNavElement() {
  let nav = document.getElementById("main-nav");
  if (!nav) {
    const header = document.querySelector(".topbar");
    if (!header) return null;

    nav = document.createElement("nav");
    nav.id = "main-nav";
    header.appendChild(nav);
  }
  return nav;
}

function buildNav() {
  const nav = ensureNavElement();
  if (!nav) return;

  const user = getUser();
  const page = document.body.dataset.page || "";

  nav.innerHTML = "";

  const addLink = (label, href, activePages = []) => {
    const a = document.createElement("a");
    a.href = href;
    a.textContent = label;
    a.classList.add("nav-item");
    if (activePages.includes(page)) {
      a.classList.add("active");
    }
    nav.appendChild(a);
  };

  const addButton = (label, onClick) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = label;
    btn.classList.add("nav-item", "nav-logout");
    btn.style.fontWeight = "bold"; // garante negrito para o Sair
    btn.addEventListener("click", onClick);
    nav.appendChild(btn);
  };

  // link fixo pro mural
  addLink("Mural", "index.html", ["mural-publico"]);

  if (!user) {
    addLink("Entrar", "login.html", ["auth"]);
    return;
  }

  if (user.tipo === "usuario") {
    addLink("Minhas Adoções", "minhas_adocoes.html", ["minhas-adocoes"]);
    addLink("Perfil", "perfil_usuario.html", ["perfil-usuario"]);
  } else if (user.tipo === "anunciante") {
    addLink("Animais", "painel_anunciante.html", ["painel-anunciante"]);
    addLink("Pedidos", "painel_anunciante_pedidos.html", ["pedidos-anunciante"]);
    addLink("Perfil", "perfil_anunciante.html", ["perfil-anunciante"]);
  } else if (user.tipo === "admin") {
    addLink("Admin", "painel_admin.html", ["painel-admin"]);
  }

  addButton("Sair", logout);
}

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const token = getToken();
    if (token && !localStorage.getItem("user")) {
      try {
        const me = await apiRequest("/auth/me");
        localStorage.setItem("user", JSON.stringify(me));
      } catch (e) {
        console.warn("Token inválido:", e.message);
        localStorage.removeItem("token");
        localStorage.removeItem("user");
      }
    }
  } catch (e) {
    console.error("Erro ao inicializar sessão:", e);
  }

  buildNav();
});
