# 🏛️ Pipeline de Auditoria de Notas Fiscais Públicas — MaratonaColab 2026

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57.svg?style=flat-square&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![SBSC 2026](https://img.shields.io/badge/Hackathon-SBSC_2026-orange.svg?style=flat-square)](https://sbsc.ufba.br)
[![UFRGS](https://img.shields.io/badge/INF-UFRGS-004A8F.svg?style=flat-square)](https://www.inf.ufrgs.br)

Projeto desenvolvido durante a **MaratonaColab 2026**, realizada no âmbito do **XXI Simpósio Brasileiro de Sistemas Colaborativos (SBSC 2026)**, sediado no **Instituto de Informática da UFRGS**.

O sistema consiste em um pipeline de Engenharia de Dados (ETL) e auditoria automatizada para ingestão, filtragem e persistência estruturada de notas fiscais eletrônicas governamentais extraídas do Portal da Transparência.

---

## 🎯 Desafio & Proposta de Valor

Arquivos brutos de compras públicas governamentais possuem dimensões na ordem de gigabytes compactados em `.zip`, contendo milhões de registros e inconsistências de codificação (`ISO-8859-1`). Carregar esses arquivos por completo em memória provoca falhas de execução (*OutOfMemory*).

Esta solução implementa um pipeline em lotes com **leitura em streaming com geradores Python**, descompactação *in-memory* e um mecanismo de regras de negócio (**Gatekeeper**) que audita, limpa e persiste apenas registros relevantes e validados.

---

## ⚙️ Arquitetura do Pipeline

```text
[Arquivo ZIP Bruto] ──(Streaming via ZipFile)──> [Gerador de Linhas]
                                                        │
                                                        ▼
                                              [etl.py: Limpeza & Cast]
                                                        │
                                                        ▼
                                              [gatekeeper.py: Validação de Regras]
                                                        │
                                   ┌────────────────────┴────────────────────┐
                                   ▼                                         ▼
                            [Reprovada: Ignora]                     [Aprovada: Persiste]
                                                                             │
                                                                             ▼
                                                                 [database.py: SQLite DB]
```

### Principais Componentes Técnicos:
* **`etl.py`:** Limpeza de caracteres, conversão de tipos de dados (datas, valores monetários) e normalização de chaves de acesso.
* **`gatekeeper.py`:** Mecanismo de regras de auditoria que filtra notas atípicas, limites orçamentários e inconsistências de CNPJs.
* **`database.py`:** Modelagem relacional e operações transacionais para gravação de cabeçalhos de notas e itens de produtos.
* **`processar_itens.py`:** Processamento correlacionado entre o cabeçalho fiscal e seus respectivos itens de licitação.
* **`main.py`:** Orquestrador principal do pipeline.

---

## 🚀 Como Executar Localmente

### 1. Clonar o repositório
```bash
git clone https://github.com/Tteuwmf/v0-maratona-gammes33.git
cd v0-maratona-gammes33
```

### 2. Estrutura de dados esperada
Certifique-se de posicionar o arquivo `.zip` de notas fiscais dentro do diretório `dados_brutos/`.

### 3. Executar o pipeline de ingestão
```bash
python main.py
```

O banco relacional `auditoria_ufrgs.db` será gerado automaticamente com os dados auditados.

---

## 👥 Autores
* **Matheus Dagostini Faccini** ([GitHub](https://github.com/Tteuwmf) · [LinkedIn](https://www.linkedin.com/in/matheus-faccini-48459142a/))
* Desenvolvido para a MaratonaColab / SBSC 2026 (INF/UFRGS).
