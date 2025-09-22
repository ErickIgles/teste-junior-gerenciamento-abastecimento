document.addEventListener('DOMContentLoaded', () => {


  // Abre o modal pelo ID
  window.abrirModal = function(id) {
      const modal = document.getElementById(id);
      if (modal) {
          modal.style.display = "block";
      }
  }

  // Fecha o modal pelo ID
  window.fecharModal = function(id) {
      const modal = document.getElementById(id);
      if (modal) {
          modal.style.display = "none";
      }
  }

  // Fecha ao clicar no X e fora do modal
  document.addEventListener("DOMContentLoaded", () => {
      document.querySelectorAll(".modal .close").forEach(span => {
          span.addEventListener("click", () => {
              const modal = span.closest(".modal");
              if (modal) {
                  modal.style.display = "none";
              }
          });
      });

      window.addEventListener("click", event => {
          if (event.target.classList.contains("modal")) {
              event.target.style.display = "none";
          }
      });
  });






  const asidebar = document.querySelector('.asidebar');
  const hamburguerBtn = document.getElementById('hamburguer-btn');
  const layout = document.querySelector('.layout');

  // Lógica para os botões do submenu
  const botoes = document.querySelectorAll('.button');
  
  for (const botao of botoes) {
    botao.onclick = () => {
      const submenu = botao.nextElementSibling;
      if (submenu.style.display === 'block') {
        submenu.style.display = 'none';
      } else {
        submenu.style.display = 'block';
      }
    };
  }

  // Define um ponto de quebra para o comportamento de clique fora
  const breakpoint = 768;

  // Lógica para o botão de hambúrguer
  hamburguerBtn.addEventListener('click', () => {
    asidebar.classList.toggle('hidden');
    layout.classList.toggle('hidden'); // Sempre alterna a classe 'hidden' no layout

    // Salva o estado no localStorage
    if (asidebar.classList.contains('hidden')) {
      localStorage.setItem('asidebar', 'fechado');
    } else {
      localStorage.setItem('asidebar', 'aberto');
    }
  });

  // Lógica de fechamento ao clicar fora, apenas em telas menores
  if (window.innerWidth <= breakpoint) {
    document.addEventListener('click', (event) => {
      // Se o asidebar está visível e o clique não foi no asidebar ou no botão
      if (!asidebar.contains(event.target) && !hamburguerBtn.contains(event.target) && !asidebar.classList.contains('hidden')) {
        asidebar.classList.add('hidden');
        layout.classList.add('hidden'); // Adiciona a classe 'hidden' também no layout
      }
    });
  }

  // Checa o estado do localStorage ao carregar a página
  // A classe 'hidden' é aplicada em ambos os elementos ao carregar
  if (localStorage.getItem('asidebar') === 'fechado') {
    asidebar.classList.add('hidden');
    layout.classList.add('hidden');
  } else {
      asidebar.classList.remove('hidden');
      layout.classList.remove('hidden');
  }
});