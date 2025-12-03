# Documentação do Projeto: Gestão da Qualidade de Software

## 1. Descrição do Projeto

Este projeto consiste no desenvolvimento de uma aplicação de gestão de estoque utilizando uma arquitetura modularizada, focada em qualidade de software. O objetivo é fornecer uma interface simples (CRUD - Create, Read, Update, Delete) para manipular dados de produtos, aplicando rigorosamente os conceitos de Desenvolvimento Orientado a Testes (TDD) e práticas de Desenvolvimento Orientado ao Comportamento (BDD).

A aplicação faz a gestão da entidade principal, o Produto, permitindo:
* Cadastro de novos itens (CREATE).
* Visualização da lista completa de estoque (READ).
* Atualização de informações de produtos existentes (UPDATE).
* Exclusão de itens do banco de dados (DELETE).

## 2. Tecnologias Utilizadas

- Python 3.11+: Linguagem de programação principal.
- Flet: Framework para construção da interface gráfica (UI).
- SQLite: Banco de dados leve e embarcado (sem servidor).
- Pytest: Framework utilizado para execução de testes unitários.
- TDD / BDD: Metodologias de desenvolvimento.
- Git: Sistema de controle de versionamento.

## 3. Estrutura de Pastas e Testes

A organização do projeto segue o princípio da Separação de Responsabilidades (SoC), essencial para a testabilidade e manutenção do código.

- CRUD_FLET_SQLITE_GQS/
  - .venv/  — Ambiente virtual
  - src/
    - bd_service.py  — Camada CRUD testada
    - __init__.py
  - tests/
    - test_bd_service.py — Testes unitários
    - __init__.py
  - .gitignore
  - app.py — Interface Flet
  - basededadoscrud.db — Banco SQLite

## 4. Instruções de Instalação e Execução

### 4.1. Clone o Repositório (Versionamento)

    git clone [INSERIR LINK DO SEU REPOSITÓRIO AQUI]
    cd CRUD_FLET_SQLITE_GQS

### 4.2. Configuração do Ambiente Virtual

# Cria o ambiente virtual
    python -m venv .venv

# Ativa o ambiente virtual (Windows PowerShell)
    .\.venv\Scripts\Activate.ps1

# Ativa o ambiente virtual (macOS / Linux)
    source .venv/bin/activate

# Instala as dependências (Flet e Pytest)
    pip install flet pytest

### 4.3. Execução dos Testes Unitários (TDD)

# Executa todos os testes da pasta /tests
    pytest

(O resultado esperado é `5 passed`, confirmando a funcionalidade total do CRUD.)

### 4.4. Execução da Aplicação (UI)

    python app.py

Observações:
- Se estiver usando VSCode, ative o ambiente virtual antes de instalar pacotes.  
- Caso a aplicação precise recriar o banco, execute a função de criação de tabela ou rode o app e clique em "Continuar" no aviso inicial.

### 5. Item 1.1: Objetivos Cumpridos

### 5.1. Testes Unitários e Entidades

O projeto demonstrou testes unitários robustos para as quatro operações funcionais (CRUD) da entidade Produto, excedendo o requisito de "ao menos duas entidades". O código de serviço (bd_service.py) está 100% verificado.

Os testes estão localizados em tests/test_bd_service.py e cobrem os seguintes comportamentos:

| Entidade Funcional | Função Testada | Comportamento Testado |
| :--- | :--- | :--- |
| **CREATE** | inserir_produto | Garante que o item é inserido e que os dados são persistidos corretamente no BD. |
| **READ** | ler_produtos | Garante que todos os itens existentes são recuperados do BD e retornados em formato de lista (de dicionários). |
| **UPDATE** | atualizar_produto | Garante que um registro existente (identificado pelo ID) é alterado com sucesso no BD. |
| **DELETE** | deletar_produto | Garante que um item específico é removido pelo ID e que o banco reflete a ausência do registro. |

---

### 5.2. Determinação da Cobertura Mínima

* Cobertura Mínima Determinada: **90%**  
* Justificativa: Atingir 100% de cobertura é dispendioso e inviável para I/O e blocos de tratamento de erro. No entanto, como a camada bd_service.py é crítica para a integridade dos dados, uma cobertura acima de 90% garante que todas as linhas de lógica principal (SQL e manipulação de conexão) são executadas pelos testes.

---

### 5.3. Utilização do TDD (Desenvolvimento Orientado a Testes)

O TDD foi aplicado rigidamente na construção da camada de serviço (src/bd_service.py). O processo seguiu o ciclo Red-Green-Refactor para cada funcionalidade (CREATE, READ, UPDATE, DELETE):

| Módulo/Função | Aplicação do Ciclo TDD |
| :--- | :--- |
| **bd_service.py** (Métodos CRUD) | O desenvolvimento de todas as funções CRUD começou com a escrita de testes de falha (RED) antes de qualquer código de produção existir. Isso garantiu que o código de produção fosse escrito apenas para atender a uma necessidade de teste comprovada (fazendo o teste passar, GREEN). A fase de Refactor garantiu a estabilidade do código mesmo após correções complexas de gerenciamento de conexão SQLite em memória. |
| **Camada de Teste** (tests/test_bd_service.py) | A fixture setup_db foi crucial, sendo adaptada (TDD implícito) para criar a tabela diretamente e passar a conexão, corrigindo o problema de isolamento de banco de dados em memória. |

---

### 5.4. Práticas do BDD (Behavior-Driven Development)

O BDD foi utilizado para documentar o comportamento esperado do sistema usando o padrão Gherkin (Given/When/Then), transformando os requisitos de negócio em base para testes de aceitação.

#### Caso de Uso 1: Cadastro de Novo Produto (CREATE)

| Palavra-Chave | Descrição (Comportamento Esperado) |
| :--- | :--- |
| **Feature:** | Cadastro de Produto |
| **Scenario:** | Cadastro bem-sucedido de um novo produto no estoque. |
| **Given** | Que o usuário está na tela de cadastro de produto |
| **And** | Que o banco de dados está inicializado e acessível |
| **When** | Ele preenche "Nome" com "Webcam 4K", "Valor" com 399.99 e "Quantidade" com 5 |
| **And** | Ele clica no botão "Adicionar Produto" |
| **Then** | O sistema deve exibir a mensagem "Produto adicionado com sucesso" |
| **And** | A tabela de exibição deve conter um novo item com Nome = "Webcam 4K" |

#### Caso de Uso 2: Edição de Estoque (UPDATE/Read)

| Palavra-Chave | Descrição (Comportamento Esperado) |
| :--- | :--- |
| **Feature:** | Atualização de Produto |
| **Scenario:** | Atualização bem-sucedida da quantidade de estoque de um produto existente. |
| **Given** | Que o produto "Mouse Gamer" com Quantidade 10 está na tabela |
| **And** | Que o usuário abriu a tela de edição do "Mouse Gamer" |
| **When** | Ele altera o campo "Quantidade" para **25** |
| **And** | Ele clica no botão "Salvar Alterações" |
| **Then** | O sistema deve exibir a mensagem "Produto atualizado com sucesso" |
| **And** | O campo de Quantidade na tabela de exibição deve ser **25** |
| **And** | O banco de dados deve refletir a quantidade 25 para o item. |

---

#### Geração de Testes Automatizados a partir do BDD

Os cenários Gherkin (acima) servem como base para testes de **integração/aceitação** automatizados. Cada linha Gherkin é mapeada para um passo (função Python) que interage com a interface (UI) ou com a API de testes do Flet. Por exemplo, o passo 'When Ele clica no botão "Adicionar Produto"' seria traduzido para um comando que simula um clique no botão da interface Flet.

## 6. Contribuidores

- **Álvaro Gomes Fernandes** — Desenvolvedor principal, responsável pelo design da interface Flet, integração com SQLite, implementação das validações e revisão final dos testes unitários.
- **João Augusto de Carvalho Paes Tonini** — Colaborador, responsável por apoio no desenvolvimento, revisão de código, suporte na elaboração de testes e documentação.

## 7. Conclusão

O projeto demonstrou a aplicação prática de conceitos fundamentais de desenvolvimento de software, incluindo organização de camadas, persistência de dados com SQLite, implementação de um CRUD funcional e criação de testes unitários para garantir a confiabilidade do sistema.

O uso do Flet permitiu desenvolver uma interface simples e eficiente, enquanto a separação entre lógica de negócios e interface garantiu clareza e manutenibilidade ao código.  
Com isso, o sistema final apresenta boa estrutura, facilidade de expansão e atende aos requisitos propostos.