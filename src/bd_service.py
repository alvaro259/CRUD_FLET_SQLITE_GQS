import sqlite3

# Função para criar a tabela se não existir
def criar_tabela(db_name):
    conexao = sqlite3.connect(db_name)
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tabeladeprodutos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            valor REAL NOT NULL,
            quantidade INTEGER NOT NULL
        );
    """)
    conexao.commit()
    conexao.close()

# Função para inserir um novo produto (CREATE)
def inserir_produto(db_name, nome, valor, quantidade):
    conexao = sqlite3.connect(db_name)
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO tabeladeprodutos (nome, valor, quantidade) VALUES (?, ?, ?)",
        (nome, valor, quantidade)
    )
    conexao.commit()
    conexao.close()

# Função para ler produtos (todos ou por ID) - (READ)
def ler_produtos(db_name, produto_id=None):
    conexao = sqlite3.connect(db_name)
    conexao.row_factory = sqlite3.Row 
    cursor = conexao.cursor()
    
    if produto_id:
        cursor.execute("SELECT * FROM tabeladeprodutos WHERE id=?", (produto_id,))
    else:
        cursor.execute("SELECT * FROM tabeladeprodutos")
        
    produtos = [dict(row) for row in cursor.fetchall()]
    conexao.close()
    return produtos

# Função para atualizar um produto (UPDATE)
def atualizar_produto(db_name, produto_id, nome, valor, quantidade):
    conexao = sqlite3.connect(db_name)
    cursor = conexao.cursor()
    # A correção está na instrução SQL abaixo: 'WHERE id=?' repetia 'WHERE id=?'
    cursor.execute(
        "UPDATE tabeladeprodutos SET nome=?, valor=?, quantidade=? WHERE id=?",
        (nome, valor, quantidade, produto_id)
    )
    conexao.commit()
    conexao.close()

# Função para deletar um produto por ID (DELETE)
def deletar_produto(db_name, produto_id):
    conexao = sqlite3.connect(db_name)
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM tabeladeprodutos WHERE id=?", (produto_id,))
    conexao.commit()
    conexao.close()