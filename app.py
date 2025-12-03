import flet as ft
import sqlite3

from src.bd_service import (
    criar_tabela,
    inserir_produto,
    ler_produtos,
    atualizar_produto as bd_atualizar_produto,
    deletar_produto
)

DB_NAME = "basededadoscrud.db"

RED_COLOR = "red600"
GREEN_COLOR = "green700"
WHITE_COLOR = "white"

def main(page: ft.Page):
    
    page.title = "CRUD TABLE"
    page.window.width = 780
    page.window.height = 520
    page.window.always_on_top = True

    page.snack_bar = ft.SnackBar(
        content=ft.Text(""),
        bgcolor=GREEN_COLOR,
        duration=ft.Duration(seconds=2)
    )
    page.overlay.append(page.snack_bar)

    def show_snack(msg: str, color=GREEN_COLOR, seconds: int = 2):
        page.snack_bar.bgcolor = color
        page.snack_bar.content = ft.Text(msg, color=WHITE_COLOR)
        page.snack_bar.duration = ft.Duration(seconds=seconds)
        page.snack_bar.open = True
        page.update()
    
    def criar_bd():
        """Chama a função de criação de tabela do serviço de BD."""
        try:
            criar_tabela(DB_NAME) 
        except Exception as err:
            show_snack(f"Erro ao criar banco de dados: {err}", RED_COLOR, seconds=3)
    
    def create(e):

        def replace(ev):
            preco.value = preco.value.replace(",",".")
            page.update()
            
        def salvar(ev):
            try:
                nome = produto.value
                estoque_val = int(estoque.value)
                preco_val = float(preco.value)
                
                inserir_produto(DB_NAME, nome, preco_val, estoque_val)
                
                tela.open = False
                page.update()
                show_snack("Produto cadastrado com sucesso!", GREEN_COLOR, seconds=2)
                atualizar_page(1)
                
            except ValueError:
                try:
                    tela.open = False
                except Exception:
                    pass
                page.update()
                show_snack("Erro de Validação! Estoque e Preço devem ser números válidos.", RED_COLOR, seconds=3)
                
            except Exception as err:
                try:
                    tela.open = False
                except Exception:
                    pass
                page.update()
                show_snack(f"Erro no Banco de Dados: {err}", RED_COLOR, seconds=3)
                atualizar_page(1)
                
        produto = ft.TextField(label="Nome do produto", autofocus=True)
        estoque = ft.TextField(label="Estoque")
        preco = ft.TextField(label="Preço", on_change=replace)
        
        tela = ft.AlertDialog(
            title = ft.Text("Cadastrar novo produto"),
            content= ft.Column([
                ft.Text("Preencha as informações do novo produto:"),
                produto,
                estoque,
                preco
            ]),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda ev:[setattr(tela, "open", False), page.update()]),
                ft.TextButton("Salvar", on_click= salvar)
            ],
            open=True
        )
        page.overlay.append(tela)
        page.update()
        
    def delete(e):

        def excluir(ev):
            try:
                id_val = int(id_field.value)

                produtos_encontrados = ler_produtos(DB_NAME, id_val)
                if not produtos_encontrados:
                    # Fecha diálogos antes de mostrar erro
                    try:
                        confirmacao.open = False
                    except Exception:
                        pass
                    try:
                        tela.open = False
                    except Exception:
                        pass
                    page.update()
                    show_snack(f"Nenhum produto com ID {id_val} foi encontrado.", RED_COLOR, seconds=3)
                    return

                deletar_produto(DB_NAME, id_val)

                try:
                    confirmacao.open = False
                except Exception:
                    pass
                try:
                    tela.open = False
                except Exception:
                    pass
                page.update()
                show_snack(f"Produto ID {id_val} excluído com sucesso!", GREEN_COLOR, seconds=2)
                
            except ValueError:
                try:
                    confirmacao.open = False
                except Exception:
                    pass
                try:
                    tela.open = False
                except Exception:
                    pass
                page.update()
                show_snack("Erro de Validação! O ID deve ser um número inteiro.", RED_COLOR, seconds=3)
                
            except Exception as err:
                try:
                    confirmacao.open = False
                except Exception:
                    pass
                try:
                    tela.open = False
                except Exception:
                    pass
                page.update()
                show_snack(f"Erro ao excluir produto: {err}", RED_COLOR, seconds=3)
            finally:
                atualizar_page(1)
        
        id_field = ft.TextField(label="ID:", autofocus=True)
        
        tela = ft.AlertDialog(
            title= ft.Text("Excluir produto"),
            content= ft.Column([
                ft.Text("Insira o ID do produto que deseja apagar:"),
                id_field
            ]),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda ev:[setattr(tela, "open", False), page.update()]),
                ft.TextButton("Excluir", on_click= lambda ev: [
                    setattr(tela, "open", False), # Fecha o primeiro diálogo para abrir a confirmação
                    setattr(confirmacao, "open", True), 
                    page.update()
                ])
            ],
            open=True
        )
        page.overlay.append(tela)
        
        confirmacao = ft.AlertDialog(
            title= ft.Text("Tem certeza que deseja excluir esse produto?"),
            content= ft.Text("Essa ação resultará na exclusão definitiva do produto!"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda ev:[setattr(confirmacao, "open", False), page.update()]),
                ft.TextButton("Sim", on_click=excluir)
            ],
            open=False
        )
        page.overlay.append(confirmacao)
        page.update()

        
    def update(e):
        
        def replace(ev):
            preco.value = preco.value.replace(",",".")
            page.update()

        def buscar_produto(ev):
            try:
                id_val = int(id_field.value)
                produtos_encontrados = ler_produtos(DB_NAME, id_val)
                
                if produtos_encontrados:
                    resultado = produtos_encontrados[0]
                    produto.value = resultado['nome']
                    estoque.value = str(resultado['quantidade'])
                    preco.value = f"{resultado['valor']:.2f}"
                    page.update()
                else:
                    try:
                        tela.open = False
                    except Exception:
                        pass
                    page.update()
                    show_snack("Produto não encontrado. Verifique o ID!", RED_COLOR, seconds=2)
            except Exception as err:
                try:
                    tela.open = False
                except Exception:
                    pass
                page.update()
                show_snack(f"Erro ao buscar produto: {err}", RED_COLOR, seconds=2)
                
        def atualizar_produto(ev):
            try:
                id_val = int(id_field.value)
                nome = produto.value
                estoque_val = int(estoque.value)
                preco_val = float(preco.value)
                
                bd_atualizar_produto(DB_NAME, id_val, nome, preco_val, estoque_val)
                
                tela.open = False
                page.update()
                show_snack("Produto atualizado com sucesso!", GREEN_COLOR, seconds=2)
                atualizar_page(1)
                
            except ValueError:
                try:
                    tela.open = False
                except Exception:
                    pass
                page.update()
                show_snack("Erro de Validação! ID, Estoque e Preço devem ser números válidos.", RED_COLOR, seconds=3)
                
            except Exception as err:
                try:
                    tela.open = False
                except Exception:
                    pass
                page.update()
                show_snack(f"Erro no Banco de Dados: {err}", RED_COLOR, seconds=3)
                atualizar_page(1)
                
        id_field = ft.TextField(label="ID", autofocus=True, width=100)
        produto = ft.TextField(label="Nome do produto")
        estoque = ft.TextField(label="Estoque")
        preco = ft.TextField(label="Preço", on_change=replace)
        tela = ft.AlertDialog(
            title = ft.Text("Atualizar produto"),
            content= ft.Column([
                ft.Text("Insira o id e clique em Buscar:"),
                ft.Row([id_field,ft.TextButton("Buscar", on_click=buscar_produto)]),
                ft.Column([produto, estoque, preco])
            ]),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda ev:[setattr(tela, "open", False), page.update()]),
                ft.TextButton("Salvar", on_click=atualizar_produto)
            ],
            open=True
        )
        page.overlay.append(tela)
        page.update()
        
    def read():
        """Chama a função de leitura do serviço de BD e formata para a UI."""
        try:
            produtos = ler_produtos(DB_NAME) 
            
            dados_formatados = [
                (p['id'], p['nome'], p['quantidade'], p['valor']) 
                for p in produtos
            ]
            return dados_formatados
        except Exception as err:
            show_snack(f"Erro ao ler banco de dados: {err}", RED_COLOR, seconds=3)
            return[]
        
    def truncate(e):
        
        def excluir_tabela(ev):
            conexao = None
            try:
                conexao = sqlite3.connect(DB_NAME)
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM tabeladeprodutos;")
                conexao.commit()
                
                try:
                    confirmacao.open = False
                except Exception:
                    pass
                page.update()
                show_snack("Tabela limpa com sucesso!", GREEN_COLOR, seconds=2)
                
            except Exception as err:
                try:
                    confirmacao.open = False
                except Exception:
                    pass
                page.update()
                show_snack(f"Erro ao limpar tabela: {err}", RED_COLOR, seconds=3)
            finally:
                if conexao:
                    conexao.close()
                atualizar_page(1)
        
        confirmacao = ft.AlertDialog(
            title= ft.Text("Tem certeza que deseja excluir os dados da tabela?"),
            content= ft.Text("Essa ação resultará na exclusão definitiva de todos os produto cadastrados na tabela!"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda ev:[setattr(confirmacao, "open", False), page.update()]),
                ft.TextButton("Sim", on_click=excluir_tabela)
            ],
            open=True
        )
        page.overlay.append(confirmacao)
        page.update()
        
    def atualizar_page(selected_index):

        paginas.controls.clear()
        if selected_index == 0:
            paginas.controls.extend([
                ft.Column([
                    ft.Text("Descrição do software", size=25, font_family='Verdana', weight=ft.FontWeight.BOLD),
                    ft.Text("Este software permite ao usuário realizar operações CRUD em uma tabela SQLite (pré-definida) com as seguintes colunas:"),
                    ft.Text('    • ID - O ID (integer, primary key) é preenchido automaticamente;', size=18, font_family='Times New Roman'),
                    ft.Text('    • Produto - O nome (text) do produto é fornecido pelo usuário;', size=18, font_family='Times New Roman'),
                    ft.Text('    • Estoque - A quantidade (integer) em estoque do produto é fornecida pelo usuário;', size=18, font_family='Times New Roman'),
                    ft.Text('    • Preço - O preço (real) do produto é fornecido pelo usuário;', size=18, font_family='Times New Roman'),
                    ft.Text("Assim, o usuário pode realizar ações simples como: cadastrar um produto (Create), visualizar os produtos cadastrados (Read), atualizar as informações de um produto (Update) e apagar produtos da tabela (Delete). O principal objetivo deste software é demonstrar o uso das operações CRUD."),
                ])
            ])
        elif selected_index == 1:
            dados = read()
            
            tabela = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("ID")),
                    ft.DataColumn(ft.Text("Produto")),
                    ft.DataColumn(ft.Text("Estoque")),
                    ft.DataColumn(ft.Text("Preço")),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(linha[0]))),
                            ft.DataCell(ft.Text(linha[1])),
                            ft.DataCell(ft.Text(str(linha[2]))),
                            ft.DataCell(ft.Text(f"R$ {linha[3]:.2f}")),
                        ]
                    ) for linha in dados
                ]
            )
            
            tabela_scroll = ft.Container(
                content=ft.Column(
                    controls=[tabela],
                    scroll=ft.ScrollMode.ALWAYS,
                ),
                    height=415,
            )
            
            paginas.controls.extend([
                tabela_scroll,
                ft.Row([
                    ft.TextButton("Adicionar produto", on_click=create),
                    ft.TextButton("Atualizar produto", on_click=update),
                    ft.TextButton("Remover produto", on_click=delete),
                    ft.TextButton("Limpar tabela", on_click=truncate, style=ft.ButtonStyle(bgcolor=RED_COLOR, color=WHITE_COLOR)),
                ])
            ])
        
        page.update()
    
    def fechar_app(e):
        aviso.open = False
        page.update()
        page.window_close()
        
    aviso = ft.AlertDialog(
        title= ft.Text("Criar BD SQLite3"),
        content=ft.Container(
            content=ft.Column([
                ft.Text("Clique em continuar para criar o banco de dados local (caso ele não exista)!,"),
            ]),
            width=90,
            height=45,
            alignment=ft.alignment.center,
        ),
        actions=[
            ft.TextButton(
                "Cancelar",
                on_click= fechar_app
            ),
            ft.TextButton(
                "Continuar", 
                on_click=lambda ev: [
                    setattr(aviso, "open", False),
                    criar_bd(),
                    page.update()
                ]
            ),
        ],
        actions_alignment="end",
        open=True
    )
    page.overlay.append(aviso)
    
    lateral = ft.NavigationRail(
        selected_index=0,
        destinations=[
            ft.NavigationRailDestination(
                icon="home", selected_icon="home", label= "Home"
            ),
            ft.NavigationRailDestination(
                icon="table_rows", selected_icon="table_rows", label= "Tabela"
            ),
        ],
        on_change=lambda ev: atualizar_page(ev.control.selected_index),
        )  
    
    paginas = ft.Column(expand=True)
    
    page.add(
        ft.Row(
            [
                lateral,
                ft.VerticalDivider(width=1),
                paginas,
            ],
            expand= True
        )
    )
    atualizar_page(0)

ft.app(target=main)
