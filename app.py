import streamlit as st
import psycopg2
import pandas as pd
from psycopg2 import OperationalError, errorcodes

# --- 1. CONFIGURAÇÃO DA CONEXÃO ---
def get_connection():
    """Tenta estabelecer a conexão com o banco de dados PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="admin",
            port="5432",
            client_encoding='utf8'
        )
        return conn
    except OperationalError as e:
        st.error(
            f"❌ Erro ao conectar no PostgreSQL. Verifique se o serviço está rodando e as credenciais (Database, Usuário, Senha). Detalhes: {e}")
        return None


# --- 2. FUNÇÕES DE ACESSO A DADOS (CRUD) ---

# Função genérica para buscar todos os dados de uma tabela
def fetch_data(table_name, columns="*", order_by=""):
    """Busca todos os dados de uma tabela."""
    conn = get_connection()
    if conn:
        try:
            order_clause = f" ORDER BY {order_by}" if order_by else ""
            query = f"SELECT {columns} FROM {table_name}{order_clause};"
            df = pd.read_sql_query(query, conn)
            return df
        except Exception as e:
            st.error(f"Erro ao buscar dados da tabela {table_name}: {e}")
            return pd.DataFrame()
        finally:
            conn.close()
    return pd.DataFrame()


# --- FUNÇÕES DE PRATOS ---

def criar_prato(nome, preco, categoria):
    """Cria um novo prato."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO prato (nome, preco, categoria) VALUES (%s, %s, %s);"
            cursor.execute(query, (nome, preco, categoria))
            conn.commit()
            st.success(f"Prato '{nome}' criado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao criar prato: {e}")
        finally:
            conn.close()


def buscar_pratos(termo_busca=""):
    """Busca pratos por nome (case insensitive)."""
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        query = "SELECT id_prato, nome, preco, categoria FROM prato WHERE nome ILIKE %s ORDER BY id_prato DESC;"
        cursor.execute(query, (f'%{termo_busca}%',))
        dados = cursor.fetchall()
        df = pd.DataFrame(dados, columns=['ID', 'Nome', 'Preço', 'Categoria'])
        conn.close()
        return df
    return pd.DataFrame()


def atualizar_preco_prato(id_prato, novo_preco):
    """Atualiza apenas o preço de um prato."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "UPDATE prato SET preco = %s WHERE id_prato = %s;"
            cursor.execute(query, (novo_preco, id_prato))
            conn.commit()
            if cursor.rowcount > 0:
                st.success("Preço atualizado!")
            else:
                st.warning("Prato não encontrado.")
        except Exception as e:
            st.error(f"Erro ao atualizar: {e}")
        finally:
            conn.close()


def atualizar_prato_nome_categoria(id_prato, novo_nome, nova_categoria):
    """Atualiza nome e categoria de um prato."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "UPDATE prato SET nome = %s, categoria = %s WHERE id_prato = %s;"
            cursor.execute(query, (novo_nome, nova_categoria, id_prato))
            conn.commit()
            if cursor.rowcount > 0:
                st.success(f"Prato ID {id_prato} atualizado para '{novo_nome}'!")
            else:
                st.warning("Prato não encontrado.")
        except Exception as e:
            st.error(f"Erro ao atualizar: {e}")
        finally:
            conn.close()


def deletar_prato(id_prato):
    """Deleta um prato pelo ID."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM prato WHERE id_prato = %s;"
            cursor.execute(query, (id_prato,))
            conn.commit()
            if cursor.rowcount > 0:
                st.success(f"Prato ID {id_prato} deletado com sucesso!")
            else:
                st.warning(f"Prato ID {id_prato} não encontrado.")
        except Exception as e:
            st.error(f"Erro ao deletar prato: {e}")
        finally:
            conn.close()


# --- FUNÇÕES DE CLIENTES ---

def adicionar_cliente(nome, email, telefone):
    """Cria um novo cliente."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO cliente (nome, email, telefone) VALUES (%s, %s, %s);"
            cursor.execute(query, (nome, email, telefone))
            conn.commit()
            st.success(f"Cliente {nome} cadastrado com sucesso!")
        except psycopg2.IntegrityError as e:
            if errorcodes.lookup(e.pgcode) == 'UNIQUE_VIOLATION':
                st.error("Erro: Email já cadastrado. O email deve ser único.")
            else:
                st.error(f"Erro de integridade ao inserir: {e}")
        except Exception as e:
            st.error(f"Erro ao inserir: {e}")
        finally:
            conn.close()


def deletar_cliente(id_cliente):
    """Deleta um cliente pelo ID e dados relacionados (se configurado CASCADE)."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM cliente WHERE id_cliente = %s;"
            cursor.execute(query, (id_cliente,))
            conn.commit()
            if cursor.rowcount > 0:
                st.success(f"Cliente ID {id_cliente} e todos os dados relacionados deletados com sucesso!")
            else:
                st.warning(f"Cliente ID {id_cliente} não encontrado.")
        except Exception as e:
            st.error(f"Erro ao deletar cliente: {e}")
        finally:
            conn.close()


# --- FUNÇÕES DE PEDIDOS (NOVA ÁREA) ---

def fetch_all_pedidos_completos():
    """Busca pedidos com nomes de cliente, mesa e garçom."""
    conn = get_connection()
    if conn:
        try:
            # Query ajustada para o esquema atual da tabela 'pedido'
            query = """
                SELECT 
                    p.id_pedido, 
                    p.data_pedido, 
                    p.valor_total, 
                    c.nome AS nome_cliente, 
                    m.numero AS numero_mesa, 
                    g.nome AS nome_garcom,
                    p.id_cliente,
                    p.id_mesa,
                    p.id_funcionario
                FROM pedido p
                JOIN cliente c ON p.id_cliente = c.id_cliente
                JOIN mesa m ON p.id_mesa = m.id_mesa
                JOIN garcom g ON p.id_funcionario = g.id_funcionario
                ORDER BY p.id_pedido DESC;
            """
            df = pd.read_sql_query(query, conn)
            return df
        except Exception as e:
            st.error(f"Erro ao buscar lista de pedidos: {e}")
            return pd.DataFrame()
        finally:
            conn.close()
    return pd.DataFrame()


def get_pedido_valor_total(id_pedido):
    """Busca o valor total de um pedido."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT valor_total FROM pedido WHERE id_pedido = %s;"
            cursor.execute(query, (id_pedido,))
            result = cursor.fetchone()
            return result[0] if result else 0.00
        except Exception as e:
            print(f"Erro ao buscar valor total do pedido {id_pedido}: {e}")
            return 0.00
        finally:
            conn.close()


def criar_pedido(id_cliente, id_mesa, id_funcionario):
    """Cria um novo pedido."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # INSERT ajustado para o esquema atual (sem status_pedido)
            query = """
                INSERT INTO pedido (id_cliente, id_mesa, id_funcionario, valor_total) 
                VALUES (%s, %s, %s, 0.00);
            """
            cursor.execute(query, (id_cliente, id_mesa, id_funcionario))
            conn.commit()
            st.success("Pedido criado com sucesso! Valor Total inicializado em R$ 0.00.")
        except Exception as e:
            st.error(f"Erro ao criar pedido: {e}")
        finally:
            conn.close()


def atualizar_cabecalho_pedido(id_pedido, id_cliente, id_mesa, id_funcionario):
    """Atualiza apenas os dados de cabeçalho do pedido (cliente, mesa, garçom)."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # UPDATE ajustado para o esquema atual (sem status_pedido)
            query = """
                UPDATE pedido 
                SET id_cliente = %s, id_mesa = %s, id_funcionario = %s
                WHERE id_pedido = %s;
            """
            cursor.execute(query, (id_cliente, id_mesa, id_funcionario, id_pedido))
            conn.commit()
            if cursor.rowcount > 0:
                st.success(f"Cabeçalho do Pedido {id_pedido} atualizado!")
            else:
                st.warning("Pedido não encontrado para atualização.")
        except Exception as e:
            st.error(f"Erro ao atualizar pedido: {e}")
        finally:
            conn.close()


def deletar_pedido(id_pedido):
    """Deleta um pedido."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM pedido WHERE id_pedido = %s;"
            cursor.execute(query, (id_pedido,))
            conn.commit()
            if cursor.rowcount > 0:
                st.success(f"Pedido {id_pedido} deletado com sucesso!")
            else:
                st.warning("Pedido não encontrado.")
        except Exception as e:
            st.error(f"Erro ao deletar pedido: {e}")
        finally:
            conn.close()


# --- FUNÇÕES DE ITENS DO PEDIDO (LÓGICA DE VALOR TOTAL) ---

def recalcular_total_pedido(conn, id_pedido):
    """
    Recalcula o valor total do pedido somando (preço * quantidade) dos itens.
    Esta função deve ser chamada dentro de uma transação ou conexão aberta.
    """
    try:
        cursor = conn.cursor()
        # Atualiza o valor_total na tabela pedido baseado na soma dos itens
        query_update = """
            UPDATE pedido
            SET valor_total = (
                SELECT COALESCE(SUM(p.preco * ip.quantidade), 0)
                FROM item_pedido ip
                JOIN prato p ON ip.id_prato = p.id_prato
                WHERE ip.id_pedido = %s
            )
            WHERE id_pedido = %s;
        """
        cursor.execute(query_update, (id_pedido, id_pedido))
        conn.commit()
    except Exception as e:
        st.error(f"Erro ao recalcular total: {e}")


def buscar_itens_pedido(id_pedido):
    """Busca os itens de um pedido específico."""
    conn = get_connection()
    if conn:
        try:
            query = """
                SELECT ip.id_item_pedido, p.nome, p.preco, ip.quantidade, ip.observacao, (p.preco * ip.quantidade) as subtotal
                FROM item_pedido ip
                JOIN prato p ON ip.id_prato = p.id_prato
                WHERE ip.id_pedido = %s;
            """
            df = pd.read_sql_query(query, conn, params=(id_pedido,))
            return df
        except Exception as e:
            st.error(f"Erro ao buscar itens do pedido: {e}")
            return pd.DataFrame()
        finally:
            conn.close()
    return pd.DataFrame()


def adicionar_item_pedido(id_pedido, id_prato, quantidade, observacao):
    """Adiciona um item ao pedido e atualiza o total."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO item_pedido (id_pedido, id_prato, quantidade, observacao) VALUES (%s, %s, %s, %s);"
            cursor.execute(query, (id_pedido, id_prato, quantidade, observacao))
            recalcular_total_pedido(conn, id_pedido)  # Atualiza o valor total
            st.success("Item adicionado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao adicionar item: {e}")
        finally:
            conn.close()


def remover_item_pedido(id_item_pedido, id_pedido):
    """Remove um item do pedido e atualiza o total."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM item_pedido WHERE id_item_pedido = %s;"
            cursor.execute(query, (id_item_pedido,))
            recalcular_total_pedido(conn, id_pedido)  # Atualiza o valor total
            st.success("Item removido com sucesso!")
        except Exception as e:
            st.error(f"Erro ao remover item: {e}")
        finally:
            conn.close()


# --- FUNÇÕES DE AVALIAÇÕES ---

def fetch_pedidos():
    """Tenta buscar IDs de pedidos e suas datas. Usado para criar Avaliação."""
    return fetch_data('pedido', columns='id_pedido, data_pedido', order_by='id_pedido DESC')


def visualizar_avaliacoes():
    """Busca todas as avaliações com nome do cliente e prato."""
    conn = get_connection()
    if conn:
        query = """
            SELECT
                a.id_avaliacao,
                c.nome AS cliente,
                p.nome AS prato_avaliado,
                a.nota,
                a.comentario,
                a.data_avaliacao,
                c.id_cliente,
                p.id_prato,
                a.id_pedido
            FROM avaliacao a
            JOIN cliente c ON a.id_cliente = c.id_cliente
            JOIN prato p ON a.id_prato = p.id_prato
            ORDER BY a.data_avaliacao DESC;
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    return pd.DataFrame()


def criar_avaliacao(id_cliente, id_prato, nota, comentario, id_pedido):
    """Cria uma nova avaliação."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO avaliacao (id_cliente, id_prato, nota, comentario, id_pedido) VALUES (%s, %s, %s, %s, %s);"
            cursor.execute(query, (id_cliente, id_prato, nota, comentario, id_pedido))
            conn.commit()
            st.success("Avaliação registrada com sucesso!")
        except Exception as e:
            st.error(f"Erro ao registrar avaliação: {e}")
            if "id_pedido" in str(e):
                st.error(
                    "DETALHE: O ID do Pedido é obrigatório (NOT NULL) na tabela 'avaliacao'. Verifique se o ID selecionado é válido.")
        finally:
            conn.close()


def atualizar_avaliacao(id_avaliacao, nova_nota, novo_comentario):
    """Atualiza a nota e o comentário de uma avaliação."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "UPDATE avaliacao SET nota = %s, comentario = %s WHERE id_avaliacao = %s;"
            cursor.execute(query, (nova_nota, novo_comentario, id_avaliacao))
            conn.commit()
            if cursor.rowcount > 0:
                st.success(f"Avaliação ID {id_avaliacao} atualizada!")
            else:
                st.warning(f"Avaliação ID {id_avaliacao} não encontrada.")
        except Exception as e:
            st.error(f"Erro ao atualizar avaliação: {e}")
        finally:
            conn.close()


def deletar_avaliacao(id_avaliacao):
    """Deleta uma avaliação pelo ID."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM avaliacao WHERE id_avaliacao = %s;"
            cursor.execute(query, (id_avaliacao,))
            conn.commit()
            if cursor.rowcount > 0:
                st.success(f"Avaliação ID {id_avaliacao} deletada com sucesso!")
            else:
                st.warning(f"Avaliação ID {id_avaliacao} não encontrada.")
        except Exception as e:
            st.error(f"Erro ao deletar avaliação: {e}")
        finally:
            conn.close()


# --- FUNÇÕES DE FUNCIONÁRIOS (Garçom e Cozinheiro) ---

def criar_funcionario(nome, table_name):
    """Cria um novo funcionário (Garçom ou Cozinheiro)."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = f"INSERT INTO {table_name} (nome) VALUES (%s);"
            cursor.execute(query, (nome,))
            conn.commit()
            st.success(f"Novo(a) {table_name.capitalize()} '{nome}' cadastrado(a) com sucesso!")
        except Exception as e:
            st.error(f"Erro ao cadastrar {table_name}: {e}")
        finally:
            conn.close()


def atualizar_funcionario(id_func, novo_nome, table_name, id_column):
    """Atualiza o nome de um funcionário."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = f"UPDATE {table_name} SET nome = %s WHERE {id_column} = %s;"
            cursor.execute(query, (novo_nome, id_func))
            conn.commit()
            if cursor.rowcount > 0:
                st.success(f"Nome do(a) {table_name.capitalize()} ID {id_func} atualizado para '{novo_nome}'!")
            else:
                st.warning(f"{table_name.capitalize()} ID {id_func} não encontrado.")
        except Exception as e:
            st.error(f"Erro ao atualizar {table_name}: {e}")
        finally:
            conn.close()


def deletar_funcionario(id_func, table_name, id_column):
    """Deleta um funcionário pelo ID."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = f"DELETE FROM {table_name} WHERE {id_column} = %s;"
            cursor.execute(query, (id_func,))
            conn.commit()
            if cursor.rowcount > 0:
                st.success(f"{table_name.capitalize()} ID {id_func} deletado com sucesso!")
            else:
                st.warning(f"{table_name.capitalize()} ID {id_func} não encontrado.")
        except Exception as e:
            st.error(f"Erro ao deletar {table_name}: {e}")
        finally:
            conn.close()


# --- 3. INTERFACE GRÁFICA (STREAMLIT) ---

st.set_page_config(layout="wide", page_title="Sistema Restaurante BD")
st.title("🍽️ Gerenciamento de Dados do Restaurante")

# Menu lateral com a nova opção Pedidos
menu = st.sidebar.selectbox("Escolha a Área", ["Pedidos", "Pratos", "Clientes", "Funcionários"])

if menu == "Pedidos":
    st.header("📝 Gerenciamento de Pedidos")

    # Abas para as operações de Pedido
    tab_view, tab_create, tab_edit, tab_del = st.tabs(["Visualizar", "Criar Pedido", "Editar Pedido", "Deletar Pedido"])

    # Dados auxiliares para dropdowns
    df_clientes = fetch_data('cliente', columns='id_cliente, nome')
    df_mesas = fetch_data('mesa', columns='id_mesa, numero')
    df_garcons = fetch_data('garcom', columns='id_funcionario, nome')
    df_pratos = fetch_data('prato', columns='id_prato, nome, preco')

    with tab_view:
        st.subheader("Lista Detalhada de Pedidos")
        df_pedidos = fetch_all_pedidos_completos()

        if not df_pedidos.empty:

            # Formatação dos dados para exibição na tabela principal
            df_display = df_pedidos.copy()
            df_display['data_pedido'] = df_display['data_pedido'].dt.strftime('%d/%m/%Y %H:%M')
            df_display['valor_total'] = df_display['valor_total'].apply(lambda x: f"R$ {x:.2f}")

            # Define as colunas a serem exibidas na tabela principal
            display_columns = ['id_pedido', 'data_pedido', 'nome_cliente', 'numero_mesa', 'nome_garcom', 'valor_total']

            st.dataframe(
                df_display[display_columns],
                use_container_width=True,
                column_config={
                    "id_pedido": "ID",
                    "data_pedido": "Data/Hora",
                    "nome_cliente": "Cliente",
                    "numero_mesa": "Mesa",
                    "nome_garcom": "Garçom",
                    "valor_total": "Valor Total"
                },
                hide_index=True
            )

            st.markdown("---")
            st.subheader("Detalhes dos Itens (Clique para Expandir)")

            # Itera sobre cada pedido para criar um expansor
            for index, pedido in df_pedidos.iterrows():
                id_pedido = pedido['id_pedido']

                # Cabeçalho do Expansor
                expander_title = f"📋 Pedido #{id_pedido} - Cliente: {pedido['nome_cliente']} (Mesa: {pedido['numero_mesa']})"

                with st.expander(expander_title):

                    df_itens = buscar_itens_pedido(id_pedido)

                    if not df_itens.empty:
                        st.markdown("##### Itens Solicitados")
                        st.dataframe(
                            df_itens[['nome', 'quantidade', 'preco', 'subtotal', 'observacao']],
                            use_container_width=True,
                            column_config={
                                "nome": "Prato",
                                "quantidade": "Qtd",
                                "preco": "Preço Unitário (R$)",
                                "subtotal": "Subtotal (R$)",
                                "observacao": "Obs"
                            },
                            hide_index=True
                        )
                        st.markdown(f"**Valor Total do Pedido: R$ {get_pedido_valor_total(id_pedido):.2f}**")
                    else:
                        st.info("Nenhum item adicionado a este pedido ainda.")
        else:
            st.info("Nenhum pedido encontrado.")

    with tab_create:
        st.subheader("➕ Novo Pedido")
        with st.form("form_criar_pedido"):
            col1, col2, col3 = st.columns(3)

            # Selectbox Cliente
            with col1:
                if not df_clientes.empty:
                    id_cli = st.selectbox("Cliente", df_clientes['id_cliente'].tolist(),
                                          format_func=lambda x:
                                          df_clientes[df_clientes['id_cliente'] == x]['nome'].iloc[0])
                else:
                    st.warning("Cadastre clientes primeiro.")
                    id_cli = None

            # Selectbox Mesa
            with col2:
                if not df_mesas.empty:
                    id_mesa = st.selectbox("Mesa", df_mesas['id_mesa'].tolist(),
                                           format_func=lambda
                                               x: f"Mesa {df_mesas[df_mesas['id_mesa'] == x]['numero'].iloc[0]}")
                else:
                    st.warning("Cadastre mesas primeiro.")
                    id_mesa = None

            # Selectbox Garçom
            with col3:
                if not df_garcons.empty:
                    id_func = st.selectbox("Garçom", df_garcons['id_funcionario'].tolist(),
                                           format_func=lambda x:
                                           df_garcons[df_garcons['id_funcionario'] == x]['nome'].iloc[0])
                else:
                    st.warning("Cadastre garçons primeiro.")
                    id_func = None

            submitted = st.form_submit_button("Abrir Pedido")
            if submitted:
                if id_cli and id_mesa and id_func:
                    criar_pedido(id_cli, id_mesa, id_func)
                else:
                    st.error("Todos os campos de seleção são obrigatórios.")

    with tab_edit:
        st.subheader("✏️ Editar Pedido")
        df_pedidos = fetch_all_pedidos_completos()
        if not df_pedidos.empty:

            # Seleção do pedido a editar
            id_pedido_edit = st.selectbox("Selecione o Pedido para Editar", df_pedidos['id_pedido'].tolist(),
                                          format_func=lambda
                                              x: f"Pedido #{x} - {df_pedidos[df_pedidos['id_pedido'] == x]['nome_cliente'].iloc[0]}")

            # Pega dados atuais do pedido selecionado
            pedido_atual = df_pedidos[df_pedidos['id_pedido'] == id_pedido_edit].iloc[0]

            # --- PARTE 1: Cabeçalho do Pedido ---
            st.markdown("### 1. Dados Principais (Cliente, Mesa, Garçom)")

            with st.form("form_editar_pedido_header"):
                col1, col2 = st.columns(2)

                with col1:
                    # Lógica segura para indexação do Selectbox
                    client_ids = df_clientes['id_cliente'].tolist()
                    mesa_ids = df_mesas['id_mesa'].tolist()
                    garcom_ids = df_garcons['id_funcionario'].tolist()

                    try:
                        idx_cli = client_ids.index(pedido_atual['id_cliente'])
                    except ValueError:
                        idx_cli = 0

                    try:
                        idx_mesa = mesa_ids.index(pedido_atual['id_mesa'])
                    except ValueError:
                        idx_mesa = 0

                    novo_id_cli = st.selectbox("Cliente", client_ids, index=idx_cli,
                                               format_func=lambda x:
                                               df_clientes[df_clientes['id_cliente'] == x]['nome'].iloc[0])

                    novo_id_mesa = st.selectbox("Mesa", mesa_ids, index=idx_mesa,
                                                format_func=lambda
                                                    x: f"Mesa {df_mesas[df_mesas['id_mesa'] == x]['numero'].iloc[0]}")

                with col2:
                    try:
                        idx_garcom = garcom_ids.index(pedido_atual['id_funcionario'])
                    except ValueError:
                        idx_garcom = 0

                    novo_id_func = st.selectbox("Garçom", garcom_ids, index=idx_garcom,
                                                format_func=lambda x:
                                                df_garcons[df_garcons['id_funcionario'] == x]['nome'].iloc[0])

                # Valor Total (Read-Only)
                st.info(f"💰 **Valor Total Atual (Calculado): R$ {get_pedido_valor_total(id_pedido_edit):.2f}**")

                submit_edit_header = st.form_submit_button("Salvar Cabeçalho")
                if submit_edit_header:
                    atualizar_cabecalho_pedido(id_pedido_edit, novo_id_cli, novo_id_mesa, novo_id_func)

            # --- PARTE 2: Gerenciamento de Itens ---
            st.markdown("---")
            st.markdown("### 2. Itens do Pedido")

            df_itens = buscar_itens_pedido(id_pedido_edit)

            if not df_itens.empty:
                st.dataframe(df_itens, use_container_width=True)

                # Botão para deletar item
                with st.expander("Remover Item do Pedido"):
                    with st.form("form_remove_item"):
                        id_item_remove = st.selectbox("Selecione o Item para Remover:",
                                                      df_itens['id_item_pedido'].tolist(),
                                                      format_func=lambda
                                                          x: f"{df_itens[df_itens['id_item_pedido'] == x]['nome'].iloc[0]} (Qtd: {df_itens[df_itens['id_item_pedido'] == x]['quantidade'].iloc[0]})")
                        submit_remove = st.form_submit_button("Remover Item")
                        if submit_remove:
                            remover_item_pedido(id_item_remove, id_pedido_edit)
            else:
                st.info("Nenhum item neste pedido.")

            # Formulário para adicionar item
            with st.expander("Adicionar Novo Item", expanded=True):
                if not df_pratos.empty:
                    with st.form("form_add_item"):
                        col_i1, col_i2 = st.columns([3, 1])
                        with col_i1:
                            id_prato_add = st.selectbox("Prato:", df_pratos['id_prato'].tolist(),
                                                        format_func=lambda
                                                            x: f"{df_pratos[df_pratos['id_prato'] == x]['nome'].iloc[0]} (R$ {df_pratos[df_pratos['id_prato'] == x]['preco'].iloc[0]})")
                        with col_i2:
                            qtd_add = st.number_input("Qtd:", min_value=1, value=1, step=1)

                        obs_add = st.text_input("Observação (Opcional):")

                        submit_add_item = st.form_submit_button("Adicionar Item")
                        if submit_add_item:
                            adicionar_item_pedido(id_pedido_edit, id_prato_add, qtd_add, obs_add)
        else:
            st.info("Sem pedidos para editar.")

    with tab_del:
        st.subheader("🗑️ Deletar Pedido")
        df_pedidos = fetch_all_pedidos_completos()
        if not df_pedidos.empty:
            with st.form("form_del_pedido"):
                id_pedido_del = st.selectbox("Selecione o Pedido", df_pedidos['id_pedido'].tolist(),
                                             format_func=lambda
                                                 x: f"Pedido #{x} - {df_pedidos[df_pedidos['id_pedido'] == x]['nome_cliente'].iloc[0]}")
                submit_del = st.form_submit_button("Deletar Pedido")
                if submit_del:
                    deletar_pedido(id_pedido_del)
        else:
            st.info("Sem pedidos para deletar.")


elif menu == "Pratos":
    st.header("🍴 Gerenciar Cardápio e Preços")

    # Abas de navegação dentro da seção Pratos
    tab1, tab2, tab3 = st.tabs(["Listar/Buscar", "Criar/Atualizar", "Deletar"])

    with tab1:
        st.subheader("Lista Completa e Busca")
        termo = st.text_input("Buscar Prato por Nome:", "")
        df_pratos = buscar_pratos(termo)
        if not df_pratos.empty:
            st.dataframe(df_pratos, use_container_width=True)
        else:
            st.info("Nenhum prato encontrado ou não há pratos cadastrados.")

    with tab2:
        col_c, col_u_p, col_u_nc = st.columns(3)

        with col_c:
            st.subheader("➕ Criar Novo Prato")
            with st.form("form_criar_prato"):
                nome_c = st.text_input("Nome do Prato")
                preco_c = st.number_input("Preço (R$)", min_value=0.01, step=1.00)
                categoria_c = st.text_input("Categoria")
                submit_c = st.form_submit_button("Criar Prato")
                if submit_c and nome_c and preco_c and categoria_c:
                    criar_prato(nome_c, preco_c, categoria_c)

        with col_u_p:
            st.subheader("🔄 Atualizar Preço")
            with st.form("form_atualizar_preco"):
                pratos_existentes = fetch_data('prato', columns='id_prato, nome, preco')

                if not pratos_existentes.empty:
                    prato_map = pratos_existentes.set_index('id_prato')['nome'].to_dict()
                    id_prato_selecionado = st.selectbox(
                        "Selecione o Prato para Atualizar o Preço:",
                        options=list(prato_map.keys()),
                        format_func=lambda
                            x: f"ID {x}: {prato_map[x]} (R$ {pratos_existentes[pratos_existentes['id_prato'] == x]['preco'].iloc[0]})",
                        key='select_prato_preco'
                    )

                    novo_valor = st.number_input(
                        "Novo Preço (R$)", min_value=0.01, step=1.00, key='novo_preco_prato'
                    )

                    submit_u = st.form_submit_button("Salvar Novo Preço")
                    if submit_u and id_prato_selecionado and novo_valor:
                        atualizar_preco_prato(id_prato_selecionado, novo_valor)
                else:
                    st.warning("Não há pratos para atualizar preços.")

        with col_u_nc:
            st.subheader("✏️ Editar Nome e Categoria")
            with st.form("form_atualizar_nome_categoria"):
                pratos_existentes = fetch_data('prato', columns='id_prato, nome, categoria')

                if not pratos_existentes.empty:
                    prato_map = pratos_existentes.set_index('id_prato')['nome'].to_dict()
                    id_prato_selecionado_nc = st.selectbox(
                        "Selecione o Prato para Editar:",
                        options=list(prato_map.keys()),
                        format_func=lambda x: f"ID {x}: {prato_map[x]}",
                        key='select_prato_nc'
                    )

                    prato_atual = pratos_existentes[pratos_existentes['id_prato'] == id_prato_selecionado_nc].iloc[0]
                    novo_nome = st.text_input("Novo Nome", value=prato_atual['nome'])
                    nova_categoria = st.text_input("Nova Categoria", value=prato_atual['categoria'])

                    submit_nc = st.form_submit_button("Salvar Nome e Categoria")
                    if submit_nc and id_prato_selecionado_nc and novo_nome and nova_categoria:
                        atualizar_prato_nome_categoria(id_prato_selecionado_nc, novo_nome, nova_categoria)
                else:
                    st.warning("Não há pratos para editar nome/categoria.")

    with tab3:
        st.subheader("🗑️ Deletar Prato")
        df_pratos_del = fetch_data('prato', columns='id_prato, nome, preco')
        if not df_pratos_del.empty:
            ids_pratos = df_pratos_del['id_prato'].tolist()

            with st.form("form_deletar_prato"):
                id_prato_del = st.selectbox(
                    "Selecione o ID do Prato a Deletar:",
                    options=ids_pratos,
                    format_func=lambda x: f"ID {x}: {df_pratos_del[df_pratos_del['id_prato'] == x]['nome'].iloc[0]}",
                    key='select_prato_del'
                )

                st.warning(
                    f"Ao deletar o ID {id_prato_del}, os itens_pedido e avaliações relacionadas serão removidos (se configurado CASCADE no banco).")

                submit_del = st.form_submit_button("DELETAR PRATO PERMANENTEMENTE")
                if submit_del and id_prato_del:
                    deletar_prato(id_prato_del)
        else:
            st.info("Nenhum prato para deletar.")


elif menu == "Clientes":
    st.header("👤 Gerenciar Clientes e Avaliações")

    cliente_menu = st.tabs(["Cadastro Cliente", "Criar Avaliação", "Visualizar Avaliações", "Editar Avaliação",
                            "Deletar Cliente/Avaliação"])

    with cliente_menu[0]:  # Cadastro Cliente
        st.subheader("➕ Cadastrar Novo Cliente")
        with st.form("form_cliente"):
            nome = st.text_input("Nome Completo")
            email = st.text_input("E-mail")
            phone = st.text_input("Telefone")

            submit = st.form_submit_button("Cadastrar Cliente")
            if submit and nome and email:
                adicionar_cliente(nome, email, phone if phone else None)

        st.subheader("Lista de Clientes")
        st.dataframe(fetch_data('cliente', order_by='id_cliente DESC'), use_container_width=True)

    with cliente_menu[1]:  # Criar Avaliação
        st.subheader("⭐ Criar Nova Avaliação")
        df_clientes = fetch_data('cliente', columns='id_cliente, nome')
        df_pratos = fetch_data('prato', columns='id_prato, nome')

        # Busca dados da tabela 'pedido'
        df_pedidos = fetch_pedidos()

        if not df_clientes.empty and not df_pratos.empty and not df_pedidos.empty:
            col_aval1, col_aval2 = st.columns(2)
            with st.form("form_criar_avaliacao"):
                with col_aval1:
                    id_cliente_aval = st.selectbox(
                        "Cliente:",
                        options=df_clientes['id_cliente'].tolist(),
                        format_func=lambda x: f"ID {x}: {df_clientes[df_clientes['id_cliente'] == x]['nome'].iloc[0]}",
                        key='select_cliente_aval'
                    )
                    id_prato_aval = st.selectbox(
                        "Prato Avaliado:",
                        options=df_pratos['id_prato'].tolist(),
                        format_func=lambda x: f"ID {x}: {df_pratos[df_pratos['id_prato'] == x]['nome'].iloc[0]}",
                        key='select_prato_aval'
                    )

                    # Campo para selecionar o ID do Pedido
                    id_pedido_aval = st.selectbox(
                        "Pedido Relacionado (Obrigatório):",
                        options=df_pedidos['id_pedido'].tolist(),
                        # Exibe ID e Data do Pedido
                        format_func=lambda
                            x: f"ID {x}: Data {df_pedidos[df_pedidos['id_pedido'] == x]['data_pedido'].iloc[0].strftime('%Y-%m-%d %H:%M')}",
                        key='select_pedido_aval'
                    )

                with col_aval2:
                    nota_aval = st.slider("Nota (1 a 5)", 1, 5, 5)
                    comentario_aval = st.text_area("Comentário", max_chars=255)

                submit_aval = st.form_submit_button("Registrar Avaliação")

                if submit_aval and id_cliente_aval and id_prato_aval and id_pedido_aval:
                    criar_avaliacao(id_cliente_aval, id_prato_aval, nota_aval, comentario_aval, id_pedido_aval)
        else:
            st.warning("É necessário ter clientes, pratos e **pedidos** cadastrados para criar uma avaliação.")

    with cliente_menu[2]:  # Visualizar Avaliações
        st.subheader("⭐ Visualizar Clientes e Avaliações")
        df_avaliacoes = visualizar_avaliacoes()

        if not df_avaliacoes.empty:
            st.dataframe(
                df_avaliacoes[
                    ['id_avaliacao', 'cliente', 'prato_avaliado', 'id_pedido', 'nota', 'comentario', 'data_avaliacao']],
                use_container_width=True,
                column_config={
                    "id_avaliacao": "ID Avaliação",
                    "cliente": "Nome do Cliente",
                    "prato_avaliado": "Prato Avaliado",
                    "id_pedido": "ID Pedido",
                    "nota": "Nota (1-5)",
                    "comentario": "Comentário",
                    "data_avaliacao": "Data"
                }
            )
        else:
            st.info("Nenhuma avaliação encontrada.")

    with cliente_menu[3]:  # Editar Avaliação
        st.subheader("✏️ Editar Avaliação Existente")
        df_avaliacoes = visualizar_avaliacoes()

        if not df_avaliacoes.empty:
            aval_map = df_avaliacoes.set_index('id_avaliacao')[
                ['cliente', 'prato_avaliado', 'nota', 'comentario']].to_dict('index')

            with st.form("form_editar_avaliacao"):
                id_aval_edit = st.selectbox(
                    "Selecione a Avaliação para Editar:",
                    options=df_avaliacoes['id_avaliacao'].tolist(),
                    format_func=lambda x: f"ID {x} | {aval_map[x]['cliente']} | {aval_map[x]['prato_avaliado']}",
                    key='select_aval_edit'
                )

                aval_atual = aval_map[id_aval_edit]

                # Certifica que o valor inicial é int para o slider, evitando erros
                nova_nota = st.slider("Nova Nota (1 a 5)", 1, 5, int(aval_atual['nota']), key='nova_nota_aval_edit')
                novo_comentario = st.text_area("Novo Comentário", value=aval_atual['comentario'],
                                               key='novo_comentario_aval_edit', max_chars=255)

                submit_edit_aval = st.form_submit_button("Salvar Edição da Avaliação")
                if submit_edit_aval and id_aval_edit:
                    atualizar_avaliacao(id_aval_edit, nova_nota, novo_comentario)
        else:
            st.info("Nenhuma avaliação para editar.")

    with cliente_menu[4]:  # Deletar Cliente/Avaliação
        st.subheader("🗑️ Deletar Cliente ou Avaliação")
        tab_del_c, tab_del_a = st.tabs(["Deletar Cliente", "Deletar Avaliação"])

        with tab_del_c:
            df_clientes_del = fetch_data('cliente', columns='id_cliente, nome, email')
            if not df_clientes_del.empty:
                ids_clientes = df_clientes_del['id_cliente'].tolist()

                with st.form("form_deletar_cliente"):
                    id_cliente_del = st.selectbox(
                        "Selecione o Cliente a Deletar:",
                        options=ids_clientes,
                        format_func=lambda
                            x: f"ID {x}: {df_clientes_del[df_clientes_del['id_cliente'] == x]['nome'].iloc[0]} ({df_clientes_del[df_clientes_del['id_cliente'] == x]['email'].iloc[0]})",
                        key='select_cliente_del'
                    )

                    st.error(
                        "⚠️ Aviso: Deletar um cliente removerá TODOS os pedidos e avaliações associadas (CASCADE).")

                    submit_del = st.form_submit_button("DELETAR CLIENTE PERMANENTEMENTE")
                    if submit_del and id_cliente_del:
                        deletar_cliente(id_cliente_del)
            else:
                st.info("Nenhum cliente para deletar.")

        with tab_del_a:
            df_aval_del = fetch_data('avaliacao', columns='id_avaliacao, id_cliente, nota')
            df_clientes_del_aval = fetch_data('cliente', columns='id_cliente, nome')

            if not df_aval_del.empty and not df_clientes_del_aval.empty:
                df_merged = pd.merge(df_aval_del, df_clientes_del_aval, on='id_cliente', how='left')
                ids_avaliacoes = df_merged['id_avaliacao'].tolist()

                with st.form("form_deletar_avaliacao"):
                    id_avaliacao_del = st.selectbox(
                        "Selecione a Avaliação a Deletar:",
                        options=ids_avaliacoes,
                        format_func=lambda
                            x: f"ID {x}: Nota {df_merged[df_merged['id_avaliacao'] == x]['nota'].iloc[0]} (Cliente: {df_merged[df_merged['id_avaliacao'] == x]['nome'].iloc[0]})",
                        key='select_aval_del'
                    )

                    submit_del_aval = st.form_submit_button("DELETAR AVALIAÇÃO")
                    if submit_del_aval and id_avaliacao_del:
                        deletar_avaliacao(id_avaliacao_del)
            else:
                st.info("Nenhuma avaliação para deletar.")


elif menu == "Funcionários":
    st.header("👨‍🍳 Gerenciamento de Funcionários")
    st.markdown(
        "##### As especialidades **Garçom** e **Cozinheiro** são obrigatórias e gerenciadas separadamente por tabela.")

    func_menu = st.tabs(["Garçom (CRUD)", "Cozinheiro (CRUD)"])

    # --- Garçom CRUD ---
    with func_menu[0]:
        st.subheader("Garçom - Gerenciamento")
        table_name = 'garcom'
        id_column = 'id_funcionario'  # Usado id_funcionario para consistência com pedido

        tab_c, tab_u, tab_d = st.tabs(["Criar", "Editar", "Deletar"])

        with tab_c:
            st.markdown("##### ➕ Novo Garçom")
            with st.form("form_criar_garcom"):
                nome_c = st.text_input("Nome do Garçom")
                submit_c = st.form_submit_button("Cadastrar Garçom")
                if submit_c and nome_c:
                    criar_funcionario(nome_c, table_name)

        with tab_u:
            st.markdown("##### ✏️ Editar Nome do Garçom")
            df_funcs = fetch_data(table_name, columns=f'{id_column}, nome', order_by='nome')
            if not df_funcs.empty:
                with st.form("form_editar_garcom"):
                    id_func_edit = st.selectbox(
                        "Garçom para Editar:",
                        options=df_funcs[id_column].tolist(),
                        format_func=lambda x: f"ID {x}: {df_funcs[df_funcs[id_column] == x]['nome'].iloc[0]}",
                        key='select_garcom_edit'
                    )
                    nome_atual = df_funcs[df_funcs[id_column] == id_func_edit]['nome'].iloc[0]
                    novo_nome = st.text_input("Novo Nome", value=nome_atual)
                    submit_u = st.form_submit_button("Atualizar Nome")
                    if submit_u and id_func_edit and novo_nome:
                        atualizar_funcionario(id_func_edit, novo_nome, table_name, id_column)
            else:
                st.info("Nenhum garçom cadastrado para editar.")

        with tab_d:
            st.markdown("##### 🗑️ Deletar Garçom")
            df_funcs = fetch_data(table_name, columns=f'{id_column}, nome', order_by='nome')
            if not df_funcs.empty:
                with st.form("form_deletar_garcom"):
                    id_func_del = st.selectbox(
                        "Garçom para Deletar:",
                        options=df_funcs[id_column].tolist(),
                        format_func=lambda x: f"ID {x}: {df_funcs[df_funcs[id_column] == x]['nome'].iloc[0]}",
                        key='select_garcom_del'
                    )
                    st.warning("Deletar um garçom pode afetar pedidos e outras relações (se configurado CASCADE).")
                    submit_d = st.form_submit_button("DELETAR GARÇOM PERMANENTEMENTE")
                    if submit_d and id_func_del:
                        deletar_funcionario(id_func_del, table_name, id_column)
            else:
                st.info("Nenhum garçom cadastrado para deletar.")

        st.subheader("Lista de Garçons")
        st.dataframe(fetch_data(table_name), use_container_width=True)

    # --- Cozinheiro CRUD ---
    with func_menu[1]:
        st.subheader("Cozinheiro - Gerenciamento")
        table_name = 'cozinheiro'
        id_column = 'id_cozinheiro'  # Mantido id_cozinheiro

        tab_c, tab_u, tab_d = st.tabs(["Criar", "Editar", "Deletar"])

        with tab_c:
            st.markdown("##### ➕ Novo Cozinheiro")
            with st.form("form_criar_cozinheiro"):
                nome_c = st.text_input("Nome do Cozinheiro")
                submit_c = st.form_submit_button("Cadastrar Cozinheiro")
                if submit_c and nome_c:
                    criar_funcionario(nome_c, table_name)

        with tab_u:
            st.markdown("##### ✏️ Editar Nome do Cozinheiro")
            df_funcs = fetch_data(table_name, columns=f'{id_column}, nome', order_by='nome')
            if not df_funcs.empty:
                with st.form("form_editar_cozinheiro"):
                    id_func_edit = st.selectbox(
                        "Cozinheiro para Editar:",
                        options=df_funcs[id_column].tolist(),
                        format_func=lambda x: f"ID {x}: {df_funcs[df_funcs[id_column] == x]['nome'].iloc[0]}",
                        key='select_cozinheiro_edit'
                    )
                    nome_atual = df_funcs[df_funcs[id_column] == id_func_edit]['nome'].iloc[0]
                    novo_nome = st.text_input("Novo Nome", value=nome_atual)
                    submit_u = st.form_submit_button("Atualizar Nome")
                    if submit_u and id_func_edit and novo_nome:
                        atualizar_funcionario(id_func_edit, novo_nome, table_name, id_column)
            else:
                st.info("Nenhum cozinheiro cadastrado para editar.")

        with tab_d:
            st.markdown("##### 🗑️ Deletar Cozinheiro")
            df_funcs = fetch_data(table_name, columns=f'{id_column}, nome', order_by='nome')
            if not df_funcs.empty:
                with st.form("form_deletar_cozinheiro"):
                    id_func_del = st.selectbox(
                        "Cozinheiro para Deletar:",
                        options=df_funcs[id_column].tolist(),
                        format_func=lambda x: f"ID {x}: {df_funcs[df_funcs[id_column] == x]['nome'].iloc[0]}",
                        key='select_cozinheiro_del'
                    )
                    st.warning("Deletar um cozinheiro pode afetar pedidos e outras relações (se configurado CASCADE).")
                    submit_d = st.form_submit_button("DELETAR COZINHEIRO PERMANENTEMENTE")
                    if submit_d and id_func_del:
                        deletar_funcionario(id_func_del, table_name, id_column)
            else:
                st.info("Nenhum cozinheiro cadastrado para deletar.")

        st.subheader("Lista de Cozinheiros")
        st.dataframe(fetch_data(table_name), use_container_width=True)