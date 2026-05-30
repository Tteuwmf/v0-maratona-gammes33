import zipfile
import csv
import os

PASTA_BRUTA = "dados_brutos"
ARQUIVO_TARGET = "202601_NFe_NotaFiscal.csv"

def mapear_cabecalhos_reais(registro_bruto):
    """
    Usa os nomes exatos que descobrimos no terminal para traduzir
    o arquivo do governo para o nosso padrão limpo.
    """
    mapa = {
        "CHAVE DE ACESSO": "chave_nota",
        "DATA EMISSÃO": "data_emissao",
        "CPF/CNPJ Emitente": "cnpj_fornecedor",
        "RAZÃO SOCIAL EMITENTE": "nome_fornecedor",
        "ÓRGÃO DESTINATÁRIO": "orgao_destinatario",
        "VALOR NOTA FISCAL": "valor_nota"
    }
    
    registro_mapeado = {}
    for chave_governo, nova_chave in mapa.items():
        registro_mapeado[nova_chave] = registro_bruto.get(chave_governo, "Sem informação").strip()
        
    return registro_mapeado

def testar_ingestao_real():
    # Encontra o zip na pasta
    arquivos = [f for f in os.listdir(PASTA_BRUTA) if f.endswith('.zip')]
    if not arquivos:
        print("❌ Nenhum arquivo .zip encontrado.")
        return
        
    caminho_zip = os.path.join(PASTA_BRUTA, arquivos[0])
    print(f"📦 Lendo dados reais de: {arquivos[0]}")
    
    contador = 0
    
    with zipfile.ZipFile(caminho_zip, 'r') as z:
        with z.open(ARQUIVO_TARGET, 'r') as f:
            # Transforma em generator para não pesar a memória
            linhas_decodificadas = (linha.decode('iso-8859-1') for linha in f)
            leitor = csv.DictReader(linhas_decodificadas, delimiter=';')
            
            print("🚀 Convertendo os primeiros registros do portal...\n")
            
            for linha_bruta in leitor:
                contador += 1
                
                # Aplica o nosso mapeamento com os nomes certos
                nota_limpa = mapear_cabecalhos_reais(linha_bruta)
                
                print(f"--- Registro Real Mapeado [{contador}] ---")
                for chave, valor in nota_limpa.items():
                    print(f"  {chave}: {valor}")
                print()
                
                # Para o teste inicial com calma, lemos apenas 3 linhas
                if contador >= 3:
                    break

if __name__ == "__main__":
    testar_ingestao_real()