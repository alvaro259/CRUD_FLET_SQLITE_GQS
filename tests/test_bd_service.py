import pytest
import sqlite3
import os

from src.bd_service import (
    criar_tabela,
    inserir_produto,
    ler_produtos,
    atualizar_produto,
    deletar_produto
)

TEST_DB = "test_crud.db" 

@pytest.fixture(autouse=True)
def setup_teardown():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    
    criar_tabela(TEST_DB) 
    
    yield
    
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


# Teste 1: Criação da tabela
def test_tabela_existe():
    conexao = sqlite3.connect(TEST_DB)
    cursor = conexao.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tabeladeprodutos';")
    assert cursor.fetchone() is not None
    
    conexao.close()

# Teste 2: Inserção de um produto (CREATE)
def test_inserir_produto():
    nome = "Produto Teste"
    valor = 10.50
    quantidade = 5
    
    inserir_produto(TEST_DB, nome, valor, quantidade)
    
    produtos = ler_produtos(TEST_DB)
    
    assert len(produtos) == 1
    assert produtos[0]['nome'] == nome
    assert produtos[0]['valor'] == valor
    assert produtos[0]['quantidade'] == quantidade

# Teste 3: Leitura de todos os produtos (READ)
def test_ler_produtos_retorna_lista_completa():
    inserir_produto(TEST_DB, "A", 10.00, 1)
    inserir_produto(TEST_DB, "B", 20.00, 2)
    inserir_produto(TEST_DB, "C", 30.00, 3)
    
    produtos = ler_produtos(TEST_DB)
    
    assert isinstance(produtos, list)
    assert len(produtos) == 3 
    assert isinstance(produtos[0], dict)

# Teste 4: Atualização de um produto (UPDATE)
def test_atualizar_produto_altera_dados():
    inserir_produto(TEST_DB, "Original", 100.00, 5)
    
    produto_id = 1
    nome_novo = "Atualizado"
    valor_novo = 150.00
    quantidade_nova = 10
    
    atualizar_produto(TEST_DB, produto_id, nome_novo, valor_novo, quantidade_nova)
    
    produto_atualizado = ler_produtos(TEST_DB, produto_id=produto_id)[0]
    
    assert produto_atualizado['nome'] == nome_novo
    assert produto_atualizado['valor'] == valor_novo
    assert produto_atualizado['quantidade'] == quantidade_nova

# Teste 5: Deleção de um produto (DELETE)
def test_deletar_produto_remove_item():
    inserir_produto(TEST_DB, "Para deletar", 50.00, 1)
    
    deletar_produto(TEST_DB, 1)
    
    produtos = ler_produtos(TEST_DB)
    
    assert len(produtos) == 0