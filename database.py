# database.py
import sqlite3

DB_NAME = "auditoria_ufrgs.db"

def inicializar_banco():
    """
    Cria o arquivo do banco de dados e a tabela Mestre se eles não existirem.
    Usamos a CHAVE DE ACESSO como Chave Primária para garantir que nenhuma nota 
    seja duplicada se rodarmos o script duas vezes.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Criando a tabela mestre de notas fiscais
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notas_fiscais_mestre (
            chave_nota TEXT PRIMARY KEY,
            data_emissao TEXT,
            mes_referencia TEXT,
            cnpj_fornecedor TEXT,
            nome_fornecedor TEXT,
            orgao_destinatario TEXT,
            valor_nota REAL
        )
    """)
    
    conn.commit()
    conn.close()
    print("🗃️ [BANCO] Banco de dados inicializado e pronto para uso.")

def salvar_nota(nota):
    """
    Insere a nota sanitizada e aprovada no banco de dados.
    Utiliza 'INSERT OR IGNORE' para ignorar silenciosamente caso a nota já exista.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT OR IGNORE INTO notas_fiscais_mestre (
                chave_nota, data_emissao, mes_referencia, cnpj_fornecedor,
                nome_fornecedor, orgao_destinatario, valor_nota
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            nota["chave_nota"],
            nota["data_emissao"],
            nota["mes_referencia"],
            nota["cnpj_fornecedor"],
            nota["nome_fornecedor"],
            nota["orgao_destinatario"],
            nota["valor_nota"]
        ))
        conn.commit()
    except sqlite3.Error as e:
        print(f"❌ [BANCO] Erro ao salvar a nota {nota['chave_nota']}: {e}")
    finally:
        conn.close()

#ITENS

def inicializar_tabela_itens():
    """Cria a tabela de itens se não existir."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_notas_fiscais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chave_nota TEXT,
            n_produto INTEGER,
            descricao TEXT,
            ncm TEXT,
            cfop TEXT,
            quantidade REAL,
            unidade TEXT,
            valor_unitario REAL,
            valor_total REAL,
            FOREIGN KEY (chave_nota) REFERENCES notas_fiscais_mestre (chave_nota)
        )
    """)
    conn.commit()
    conn.close()
    print("🗃️ [BANCO] Tabela de itens inicializada.")

def salvar_item(item):
    """Insere um item no banco de dados."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO itens_notas_fiscais (
            chave_nota, n_produto, descricao, ncm, cfop, 
            quantidade, unidade, valor_unitario, valor_total
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        item["chave_nota"], item["n_produto"], item["descricao"], 
        item["ncm"], item["cfop"], item["quantidade"], 
        item["unidade"], item["valor_unitario"], item["valor_total"]
    ))
    conn.commit()
    conn.close()