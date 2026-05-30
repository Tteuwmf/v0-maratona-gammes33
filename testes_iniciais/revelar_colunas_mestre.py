import zipfile
import os

PASTA_BRUTA = "dados_brutos"
# Nome exato do arquivo que o seu terminal detectou
ARQUIVO_TARGET = "202601_NFe_NotaFiscal.csv" 

def revelar_todas_colunas():
    arquivos = [f for f in os.listdir(PASTA_BRUTA) if f.endswith('.zip')]
    if not arquivos:
        print("❌ Nenhum arquivo .zip na pasta.")
        return
        
    caminho_zip = os.path.join(PASTA_BRUTA, arquivos[0])
    
    with zipfile.ZipFile(caminho_zip, 'r') as z:
        # Abrindo especificamente a tabela mestre de Notas Fiscais
        with z.open(ARQUIVO_TARGET, 'r') as f:
            primeira_linha = f.readline().decode('iso-8859-1').strip()
            separador = ';' if ';' in primeira_linha else ','
            colunas = primeira_linha.split(separador)
            
            print(f"📋 Lista completa das 25 colunas de: {ARQUIVO_TARGET}\n")
            print("-" * 50)
            for indice, coluna in enumerate(colunas):
                coluna_limpa = coluna.replace('"', '').strip()
                print(f" Coluna [{indice:02d}]: {coluna_limpa}")
            print("-" * 50)

if __name__ == "__main__":
    revelar_todas_colunas()