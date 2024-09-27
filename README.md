---

# Gerenciador de Estoque

Este projeto é um **sistema de gerenciamento de estoque** desenvolvido utilizando o framework **Flask** com **Python**, integrando o banco de dados **MySQL**. O projeto oferece funcionalidades para a gestão de produtos e suas categorias, além da exportação de dados de estoque para formatos de planilha.

## Funcionalidades

- **CRUD de produtos**: Adicionar, visualizar, editar e excluir produtos do estoque.
- **CRUD de categorias de produto**: Gerenciar as categorias dos produtos de forma dinâmica.
- **Exportar estoque**: Exportação dos dados do estoque para um arquivo **Excel** (.xlsx). Planejamento para exportação em **CSV** nas futuras versões.

## Tecnologias Utilizadas

### Backend:
- **Python**: Linguagem de programação principal do projeto.
- **Flask**: Framework para construção da aplicação web.
- **MySQL**: Banco de dados utilizado para armazenar informações dos produtos e categorias.

### Extensões Flask e Bibliotecas Python:
- **Flask-Bcrypt**: Utilizado para hashing de senhas.
- **Flask-Login**: Gerenciamento de sessões de usuário.
- **Flask-Mailman**: Envio de e-mails, como confirmação de conta e notificações.
- **Flask-Migrate**: Migrações do banco de dados.
- **Flask-SQLAlchemy**: Integração do banco de dados com SQLAlchemy.
- **Flask-WTF**: Validação e gerenciamento de formulários.
- **PyJWT**: Utilizado para gerar tokens JWT para autenticação e autorização.
- **Pandas**: Utilizado para manipulação de dados e exportação para Excel.

## Requisitos

Para rodar o projeto, é necessário ter o seguinte instalado:

- Python 3.x
- MySQL
- Virtualenv (opcional, mas recomendado)

### Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/gerenciador-de-estoque.git
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure o banco de dados MySQL e as variáveis de ambiente, como as credenciais de banco e a chave secreta do Flask.

5. Execute as migrações do banco de dados:

   ```bash
   flask db upgrade
   ```

6. Inicie a aplicação:

   ```bash
   flask run
   ```

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para enviar issues e pull requests para melhorias ou novas funcionalidades.

## Futuras Funcionalidades

- Exportação de estoque para **CSV**.
- Implementação de relatórios e gráficos de desempenho do estoque.
- Sistema de notificações por e-mail para itens com estoque baixo.

## Licença

Este projeto é licenciado sob a [MIT License](LICENSE.txt).

---
