document.addEventListener('DOMContentLoaded', function () {
    const selectTanque = document.getElementById('id_tanque');
    const infoCombustivel = document.getElementById('id_info_combustivel');

    function atualizarInfoCombustivel() {
        const opcao = selectTanque.options[selectTanque.selectedIndex];
        const combustivel = opcao.dataset.combustivel;
        const situacao = opcao.dataset.situacao;

        console.log(combustivel)
        console.log(situacao)



        if(combustivel != null){

            infoCombustivel.innerHTML = `<p>Tipo de combustível: ${combustivel}</p>`;

            if(situacao != 'False'){
                infoCombustivel.innerHTML += `<p/>Situação do tanque: <strong class="status status-ativo">Ativo</strong></p>`
            }
            
            else{
                infoCombustivel.innerHTML += `<p/>Situação do tanque: <strong class="status status-desativado">Desativado</strong></p>`
            }
        }
        else {
            infoCombustivel.textContent = ``

        }
    }
        selectTanque.addEventListener('change', atualizarInfoCombustivel);

        atualizarInfoCombustivel();
});