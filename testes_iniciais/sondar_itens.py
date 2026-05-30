# sondar_itens.py
import zipfile
import os

PASTA_BRUTA = "dados_brutos"

def sondar_arquivos_do_zip():
    arquivos = [f for f in os.listdir(PASTA_BRUTA) if f.endswith('.zip')]
    
    if not arquivos:
        print(f"❌ Nenhum arquivo .zip encontrado na pasta '{PASTA_BRUTA}'.")
        return
    
    nome_zip = arquivos[0]
    caminho_zip = os.path.join(PASTA_BRUTA, nome_zip)
    print(f"📦 Arquivo ZIP detectado: {nome_zip}\n")
    
    with zipfile.ZipFile(caminho_zip, 'r') as z:
        lista_interna = z.namelist()
        print(f"🗂️ Encontrados {len(lista_interna)} arquivos dentro do seu ZIP:")
        for nome in lista_interna:
            print(f"  - {nome}")
        print("=" * 60)
        
        # Procura por arquivos que possam conter os itens/produtos
        # Geralmente têm 'Item' ou 'Produto' no nome
        for nome_arquivo_interno in lista_interna:
            if "item" in nome_arquivo_interno.lower() or "produto" in nome_arquivo_interno.lower():
                print(f"\n🔍 Analisando Estrutura de Itens: {nome_arquivo_interno}")
                
                with z.open(nome_arquivo_interno, 'r') as f:
                    try:
                        # Lê o cabeçalho
                        primeira_linha = f.readline().decode('iso-8859-1').strip()
                        separador = ';' if ';' in primeira_linha else ','
                        colunas = primeira_linha.split(separador)
                        
                        print(f"  📊 Total de colunas: {len(colunas)} (Separador: '{separador}')")
                        print("  📋 Primeiras 10 colunas encontradas:")
                        
                        for i, coluna in enumerate(colunas[:10]):
                            coluna_limpa = coluna.replace('"', '').strip()
                            print(f"    [{i:02d}] -> {coluna_limpa}")
                            
                        if len(colunas) > 10:
                            print(f"    ... e mais {len(colunas) - 10} colunas.")
                            
                    except Exception as e:
                        print(f"  ❌ Erro ao ler este arquivo: {e}")
                print("-" * 60)

if __name__ == "__main__":
    sondar_arquivos_do_zip()