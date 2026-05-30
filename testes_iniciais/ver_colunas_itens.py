import zipfile
import os

PASTA_BRUTA = "dados_brutos"
ARQUIVO_ITENS = "202601_NFe_NotaFiscalItem.csv"

def listar_todas_colunas():
    arquivos = [f for f in os.listdir(PASTA_BRUTA) if f.endswith('.zip')]
    with zipfile.ZipFile(os.path.join(PASTA_BRUTA, arquivos[0]), 'r') as z:
        with z.open(ARQUIVO_ITENS, 'r') as f:
            header = f.readline().decode('iso-8859-1').strip().split(';')
            print(f"📋 Colunas de {ARQUIVO_ITENS}:")
            for i, col in enumerate(header):
                print(f"[{i:02d}] -> {col}")

listar_todas_colunas()