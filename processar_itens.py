# processar_itens.py
import csv
import zipfile
import os
from database import salvar_item

def limpar_numero(valor):
    try:
        return float(valor.replace(".", "").replace(",", "."))
    except:
        return 0.0

# Adicionamos o argumento 'chaves_aprovadas'
def processar_arquivo_itens(caminho_zip, nome_arquivo_csv, chaves_aprovadas):
    print(f"\n📦 Iniciando filtragem de itens: {nome_arquivo_csv}")
    itens_salvos = 0
    
    with zipfile.ZipFile(caminho_zip, 'r') as z:
        with z.open(nome_arquivo_csv, 'r') as f:
            linhas = (l.decode('iso-8859-1') for l in f)
            leitor = csv.DictReader(linhas, delimiter=';')
            
            for linha in leitor:
                chave_item = linha["CHAVE DE ACESSO"].strip()
                
                # O FILTRO ACONTECE AQUI:
                if chave_item in chaves_aprovadas:
                    item = {
                        "chave_nota": chave_item,
                        "n_produto": linha["NÚMERO PRODUTO"],
                        "descricao": linha["DESCRIÇÃO DO PRODUTO/SERVIÇO"].strip(),
                        "ncm": linha["CÓDIGO NCM/SH"],
                        "cfop": linha["CFOP"],
                        "quantidade": limpar_numero(linha["QUANTIDADE"]),
                        "unidade": linha["UNIDADE"].strip(),
                        "valor_unitario": limpar_numero(linha["VALOR UNITÁRIO"]),
                        "valor_total": limpar_numero(linha["VALOR TOTAL"])
                    }
                    salvar_item(item)
                    itens_salvos += 1
                
    print(f"✅ Filtro concluído! {itens_salvos} itens de notas aprovadas foram salvos.")