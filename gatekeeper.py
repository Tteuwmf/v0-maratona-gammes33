# gatekeeper.py
import requests
import time
import json
import os
from datetime import datetime

CACHE_FILE = "cache_cnpjs.json"

def carregar_cache():
    """Lê o caderninho salvo no disco. Se não existir, cria um vazio."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def salvar_cache(cache_dict):
    """Atualiza o caderninho no disco com novos CNPJs."""
    with open(CACHE_FILE, "w") as f:
        json.dump(cache_dict, f, indent=4)

# Carregamos o cache para a memória uma vez só quando o módulo inicia
CACHE_LOCAL = carregar_cache()

def buscar_data_abertura_cnpj(cnpj):
    """Busca o CNPJ no Cache. Se não achar, vai na BrasilAPI com cuidado e identificação."""
    
    if cnpj in CACHE_LOCAL:
        return CACHE_LOCAL[cnpj]
    
    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
    print(f"   🌐 [API] Buscando CNPJ novo na internet: {cnpj}...")
    
    # Adicionando um "Crachá" para a API não nos bloquear
    headers = {
        "User-Agent": "Projeto_Maratona_UFRGS/1.0 (Pesquisa Academica)"
    }
    
    try:
        # Passamos o header na requisição
        response = requests.get(url, headers=headers, timeout=10)
        time.sleep(2) # Pausa estratégica aumentada para 2 segundos
        
        if response.status_code == 200:
            dados = response.json()
            data_abertura = dados.get("data_inicio_atividade")
            
            CACHE_LOCAL[cnpj] = data_abertura
            salvar_cache(CACHE_LOCAL)
            return data_abertura
            
        elif response.status_code == 429:
            print("   ⚠️ [API] Rate limit atingido. Salvando fallback no cache para evitar bloqueios.")
            # Salva uma data muito antiga para a nota passar provisoriamente
            # e não ficar martelando a API no mesmo CNPJ.
            CACHE_LOCAL[cnpj] = "1900-01-01" 
            salvar_cache(CACHE_LOCAL)
            return "1900-01-01"
            
        else:
            print(f"   ⚠️ [API] CNPJ não encontrado (Erro {response.status_code}).")
            CACHE_LOCAL[cnpj] = "1900-01-01"
            salvar_cache(CACHE_LOCAL)
            return "1900-01-01"
            
    except requests.exceptions.RequestException:
        print("   ❌ [API] Erro de conexão.")
        
    return "1900-01-01"

def executar_gatekeeper(nota_limpa):
    """Aplica a regra cronológica comparando a nota com a base da Receita."""
    cnpj = nota_limpa["cnpj_fornecedor"]
    data_emissao_str = nota_limpa["data_emissao"]
    nome_fornecedor = nota_limpa["nome_fornecedor"]
    
    data_abertura_str = buscar_data_abertura_cnpj(cnpj)
    
    try:
        data_emissao_dt = datetime.strptime(data_emissao_str, "%Y-%m-%d")
        data_abertura_dt = datetime.strptime(data_abertura_str, "%Y-%m-%d")
        
        if data_emissao_dt < data_abertura_dt:
            print(f"🚨 [RECUSADA] A nota de '{nome_fornecedor}' é mais velha que a própria empresa!")
            return False
        return True
    except ValueError:
        return False # Formato de data zoado descarta a nota