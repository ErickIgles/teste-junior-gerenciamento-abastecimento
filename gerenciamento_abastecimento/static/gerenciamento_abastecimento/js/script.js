document.addEventListener('DOMContentLoaded', () => {
  const botoes = document.querySelectorAll('.button');
  
  for (const botao of botoes) {
    botao.onclick = () => {

      const submenu = botao.nextElementSibling;
      if (submenu.style.display === 'block') {
        submenu.style.display = 'none';
      } else{
          submenu.style.display = 'block';
      }
    };
  }


  const asidebar = document.querySelector('.asidebar');
  const hamburguerBtn = document.getElementById('hamburguer-btn');
  const layout = document.querySelector('.layout');

  hamburguerBtn.addEventListener('click', () => {
    asidebar.classList.toggle('hidden');
    layout.classList.toggle('hidden');
  });

})
