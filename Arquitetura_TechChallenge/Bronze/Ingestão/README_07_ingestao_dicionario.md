# Notebook: `07_ingestao_dicionario`

## Camada
**Bronze** | Ingestão batch

## Localização
`Bronze/Ingestão/07_ingestao_dicionario`

## Descrição
Notebook responsável pela ingestão batch do dicionário de referência da Avaliação Nacional de Alfabetização, proveniente da Base dos Dados (BigQuery). O dicionário contém a descrição das colunas e chaves utilizadas nas demais tabelas do dataset.

## Origem dos Dados
* **BigQuery**: `basedosdados.br_inep_avaliacao_alfabetizacao.dicionario`

## Destino
* **Tabela Delta**: `workspace.bronze.dicionario_raw`
* **Modo de gravação**: `append` (lotes imutáveis)

## Colunas de Controle Adicionadas
* `data_ingestao` — timestamp da carga
* `fonte` — "Base dos Dados - BigQuery"
* `lote_id` — UUID único do lote

## Pré-requisitos
* Executar o notebook `_common_ingestao` (incluído via `%run`)
* Credencial do ambiente Databricks disponível no caminho configurado no helper
* Bibliotecas BigQuery instaladas

## Ordem de Execução
1. `%pip install` das dependências
2. `%run ./_common_ingestao` para carregar o helper
3. `ingest_bq_table("dicionario", ...)` para realizar a ingestão

## Tabela de Destino: `workspace.bronze.dicionario_raw`

| Item | Valor |
|---|---|
| **Volume (out/2026)** | 54 linhas (2 lotes) |
| **Chave de negócio** | `id_tabela`, `nome_coluna`, `chave` |
| **Modo de gravação** | `append` (lotes imutáveis) |

### Dicionário de colunas

| Coluna | Tipo | Descrição |
|---|---|---|
| `id_tabela` | STRING | Nome da tabela de referência no dicionário |
| `nome_coluna` | STRING | Nome da coluna descrita |
| `chave` | STRING | Chave/ código do valor |
| `cobertura_temporal` | STRING | Período de cobertura temporal |
| `valor` | STRING | Descrição/ valor associado à chave |
| `data_ingestao` | TIMESTAMP | Data e hora da ingestão |
| `fonte` | STRING | Origem dos dados ("Base dos Dados - BigQuery") |
| `lote_id` | STRING | Identificador único do lote de ingestão |

### Regras de qualidade (DQ Bronze)

| Regra | Severidade | Descrição |
|---|---|---|
| `LOTE_VAZIO` | BLOQUEANTE | Último lote não pode ter zero registros |
| `METADADOS_NULOS` | BLOQUEANTE | `lote_id`, `data_ingestao` e `fonte` não nulos |
| `CHAVE_NULA` | BLOQUEANTE | `id_tabela`, `nome_coluna`, `chave` não nulos |
| `CHAVE_DUPLICADA` | INFORMATIVA | Verifica duplicidade da chave no lote |

## Relacionamento
* **Próxima etapa**: Notebook `Bronze/Qualidade_dados/01_validar_qualidade_bronze`
* **Tratamento downstream**: Notebook `Silver/Dimensoes/01_dicionario_oficial`