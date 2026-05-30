# etl.py
from datetime import datetime

def limpar_e_transformar_nota(registro_bruto):
    """
    Recebe um dicionário bruto do CSV do governo e retorna um dicionário tipado e limpo.
    """
    chave = registro_bruto.get("CHAVE DE ACESSO", "").strip()
    data_bruta = registro_bruto.get("DATA EMISSÃO", "").strip()
    cnpj_bruto = registro_bruto.get("CPF/CNPJ Emitente", "").strip()
    nome = registro_bruto.get("RAZÃO SOCIAL EMITENTE", "").strip()
    orgao = registro_bruto.get("ÓRGÃO DESTINATÁRIO", "").strip()
    valor_bruto = registro_bruto.get("VALOR NOTA FISCAL", "").strip()

    try:
        valor_float = float(valor_bruto.replace(".", "").replace(",", "."))
    except ValueError:
        valor_float = 0.0

    try:
        data_dt = datetime.strptime(data_bruta, "%d/%m/%Y %H:%M:%S")
        data_iso = data_dt.strftime("%Y-%m-%d")
        mes_ref = data_dt.strftime("%Y-%m")
    except ValueError:
        data_iso = "1900-01-01"
        mes_ref = "1900-01"

    return {
        "chave_nota": chave,
        "data_emissao": data_iso,
        "mes_referencia": mes_ref,
        "cnpj_fornecedor": cnpj_bruto,
        "nome_fornecedor": nome,
        "orgao_destinatario": orgao,
        "valor_nota": valor_float
    }