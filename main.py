# main.py
import zipfile
import csv
import os

# Importando todos os nossos submódulos
from etl import limpar_e_transformar_nota
from gatekeeper import executar_gatekeeper
# Importações atualizadas para incluir o banco de itens e o processador de itens
from database import inicializar_banco, salvar_nota, inicializar_tabela_itens
from processar_itens import processar_arquivo_itens

PASTA_BRUTA = "dados_brutos"
ARQUIVO_NOTAS = "202601_NFe_NotaFiscal.csv"
ARQUIVO_ITENS = "202601_NFe_NotaFiscalItem.csv"

def rodar_pipeline_completo():
    # 1. Inicializa todas as tabelas no banco de dados
    inicializar_banco()
    inicializar_tabela_itens()
    
    arquivos = [f for f in os.listdir(PASTA_BRUTA) if f.endswith('.zip')]
    if not arquivos:
        print("❌ Arquivo ZIP não encontrado.")
        return
        
    caminho_zip = os.path.join(PASTA_BRUTA, arquivos[0])
    
    # Este 'set' vai guardar apenas as chaves das notas que passarem no Gatekeeper
    chaves_aprovadas = set() 
    
    contador = 0
    aprovadas = 0
    
    with zipfile.ZipFile(caminho_zip, 'r') as z:
        # --- PASSO 1: Processar Notas (Cabeçalhos) ---
        print("\n🚀 Iniciando Processamento de Notas...")
        with z.open(ARQUIVO_NOTAS, 'r') as f:
            linhas_decodificadas = (linha.decode('iso-8859-1') for linha in f)
            leitor = csv.DictReader(linhas_decodificadas, delimiter=';')
            
            for linha_bruta in leitor:
                contador += 1
                
                nota_limpa = limpar_e_transformar_nota(linha_bruta)
                
                # O Gatekeeper filtra e nós guardamos a chave apenas se aprovar
                if executar_gatekeeper(nota_limpa):
                    aprovadas += 1
                    salvar_nota(nota_limpa)
                    
                    # A MÁGICA: Adicionamos a chave ao nosso conjunto de "aprovadas"
                    chaves_aprovadas.add(nota_limpa["chave_nota"])
                    print(f"💾 Nota #{contador} aprovada e gravada.")
                
                # Trava de segurança para não processar o arquivo inteiro agora
                if contador >= 10:
                    break
        
        # --- PASSO 2: Processar Itens (Produtos) usando o filtro ---
        # Agora passamos o nosso "set" de chaves aprovadas para a função
        processar_arquivo_itens(caminho_zip, ARQUIVO_ITENS, chaves_aprovadas)
                    
    print(f"\n📊 RESUMO FINAL: {contador} notas processadas | {aprovadas} aprovadas e itens extraídos.")

if __name__ == "__main__":
    rodar_pipeline_completo()