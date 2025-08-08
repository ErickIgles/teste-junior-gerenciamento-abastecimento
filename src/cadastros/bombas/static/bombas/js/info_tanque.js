document.addEventListener('DOMContentLoaded', () => {
    const selectTanque = document.getElementById('id_tanque');
    const infoCombustivel = document.getElementById('id_info_combustivel');
    
    function amostrarCombustivel(){
        const identificadorSelecionado = selectTanque.options[selectTanque.selectedIndex];
        const tipoCombustivel = identificadorSelecionado.getAttribute('data-combustivel');

        if (tipoCombustivel != null){
            infoCombustivel.textContent = `Tipo de Combustível: ${tipoCombustivel}`;
        }

    }

    selectTanque.addEventListener('change', amostrarCombustivel);
})