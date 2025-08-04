const botoes = document.querySelectorAll('.menu-alternativo');

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