# main.py
import zipfile
import csv
import os

# Importando todos os nossos submódulos organizados
from etl import limpar_e_transformar_nota
from gatekeeper import executar_gatekeeper
from database import inicializar_banco, salvar_nota

PASTA_BRUTA = "dados_brutos"
ARQUIVO_TARGET = "202601_NFe_NotaFiscal.csv"

def rodar_pipeline_completo():
    # 1. Garante que o banco de dados e as tabelas estejam criados antes de começar
    inicializar_banco()
    
    arquivos = [f for f in os.listdir(PASTA_BRUTA) if f.endswith('.zip')]
    if not arquivos:
        print("❌ Arquivo ZIP não encontrado.")
        return
        
    caminho_zip = os.path.join(PASTA_BRUTA, arquivos[0])
    contador = 0
    aprovadas = 0
    
    with zipfile.ZipFile(caminho_zip, 'r') as z:
        with z.open(ARQUIVO_TARGET, 'r') as f:
            linhas_decodificadas = (linha.decode('iso-8859-1') for linha in f)
            leitor = csv.DictReader(linhas_decodificadas, delimiter=';')
            
            print("\n🚀 Iniciando Processamento de Fluxo Contínuo...\n")
            
            for linha_bruta in leitor:
                contador += 1
                
                # Passo A: Extração e Transformação (ETL)
                nota_limpa = limpar_e_transformar_nota(linha_bruta)
                
                # Passo B: Validação de Segurança (Gatekeeper)
                if executar_gatekeeper(nota_limpa):
                    aprovadas += 1
                    
                    # Passo C: Persistência (Banco de Dados)
                    salvar_nota(nota_limpa)
                    print(f"💾 Nota #{contador} gravada com sucesso no SQLite.")
                
                # Trava provisória de segurança para teste local
                if contador >= 10:
                    break
                    
    print(f"\n📊 RESUMO FINAL: {contador} processadas | {aprovadas} salvas no banco de dados.")

if __name__ == "__main__":
    rodar_pipeline_completo()