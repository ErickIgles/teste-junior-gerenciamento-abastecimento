SOFTWARE PARA GERENCIAR OS ABASTECIMENTOS E TANQUES DE COMBUSTÍVEIS



### Passos para rodar

1. Clone este repositório:
    git clone https://github.com/ErickIgles/teste-junior-gerenciamento-abastecimento.git

2 entre no repositorio:
    cd gerencimento-abastecimento

2 crie um ambiente virtual
    python -m venv venv

3 ative o ambiente virtual
    venv\Scripts\activate     # Windows

4 Instale as dependências:
    pip install -r requirements.txt

5 Execute as migrations
    python manage.py migrate


6 Rode o servidor de desenvolvimento:
    python manage.py runserver

7 Acesse no navegador:

    http://127.0.0.1:8000/


8 Acesse o menu/ cadastros/ Tanque/ Cadastrar Tanque -> e realize o cadastro
9 Acesse o menu/ cadastro/ Listagem de Tanque e visualize as listagens

10 Acesse o menu/ cadastros/ Bomba/ Cadastrar Bomba -> e realize o cadastro
11 Acesso o menu/ cadastros/ Listagem Bomba e visualize as listagens

12 acesse o menu/ Abastecimentos/ Cadastrar Abastecimento -> e realize o cadastro
13 acesse o menu/ Abastecimentos/ Listagem de Abastecimentos e visualize as listagens

14 Cada listagem possui um formulário de pesquisa por nome e data

15 No momento a opção de relatórios não está em funcionalidade
