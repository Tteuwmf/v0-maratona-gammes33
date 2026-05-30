import zipfile
import os

PASTA_BRUTA = "dados_brutos"

def sondar_todos_arquivos_zip():
    # Encontra o primeiro arquivo .zip na pasta
    arquivos = [f for f in os.listdir(PASTA_BRUTA) if f.endswith('.zip')]
    
    if not arquivos:
        print(f"❌ Nenhum arquivo .zip encontrado na pasta '{PASTA_BRUTA}'.")
        return
    
    nome_zip = arquivos[0]
    caminho_zip = os.path.join(PASTA_BRUTA, nome_zip)
    print(f"📦 Arquivo ZIP detectado: {nome_zip}\n")
    
    with zipfile.ZipFile(caminho_zip, 'r') as z:
        lista_interna = z.namelist()
        print(f"🗂️ Encontrados {len(lista_interna)} arquivos dentro do seu ZIP.")
        print("=" * 60)
        
        # Passa por cada um dos 3 arquivos para descobrir o que tem dentro
        for indice, nome_arquivo_interno in enumerate(lista_interna):
            print(f"\n📄 [Arquivo {indice}] Nome: {nome_arquivo_interno}")
            
            with z.open(nome_arquivo_interno, 'r') as f:
                try:
                    # Lê apenas a primeira linha (cabeçalho)
                    primeira_linha = f.readline().decode('iso-8859-1').strip()
                    
                    if not primeira_linha:
                        print("  ⚠️ Este arquivo parece estar vazio.")
                        continue
                    
                    # Detecta o separador correto
                    separador = ';' if ';' in primeira_linha else ','
                    colunas = primeira_linha.split(separador)
                    
                    print(f"  📊 Total de colunas: {len(colunas)} (Separador: '{separador}')")
                    print("  🔍 Primeiras colunas para identificação:")
                    
                    # Mostra as primeiras 6 colunas para vocês analisarem
                    for i, coluna in enumerate(colunas[:6]):
                        coluna_limpa = coluna.replace('"', '').strip()
                        print(f"    -> {coluna_limpa}")
                        
                    if len(colunas) > 6:
                        print(f"    ... e mais {len(colunas) - 6} colunas.")
                        
                except Exception as e:
                    print(f"  ❌ Erro ao ler o cabeçalho deste arquivo: {e}")
            print("-" * 60)

if __name__ == "__main__":
    sondar_todos_arquivos_zip()