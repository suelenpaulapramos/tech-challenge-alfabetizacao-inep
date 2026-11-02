# Notebook: `02_ingestao_meta_brasil`

## Camada
**Bronze** | Ingestão batch

## Localização
`Bronze/Ingestão/02_ingestao_meta_brasil`

## Descrição
Notebook responsável pela ingestão batch dos dados de metas de alfabetização em nível Brasil, provenientes da Base dos Dados (BigQuery). Cada execução acrescenta um novo lote imutável à tabela Bronze.

## Origem dos Dados
* **BigQuery**: `basedosdados.br_inep_avaliacao_alfabetizacao.meta_alfabetizacao_brasil`

## Destino
* **Tabela Delta**: `workspace.bronze.meta_alfabetizacao_brasil_raw`
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
3. `ingest_bq_table("meta_brasil", ...)` para realizar a ingestão

## Tabela de Destino: `workspace.bronze.meta_alfabetizacao_brasil_raw`

| Item | Valor |
|---|---|
| **Volume (out/2026)** | 6 linhas (2 lotes) |
| **Chave de negócio** | `ano`, `rede` |
| **Período coberto** | 2023 a 2025 |
| **Metas anuais** | 2024 a 2030 |
| **Modo de gravação** | `append` (lotes imutáveis) |

### Dicionário de colunas

| Coluna | Tipo | Descrição |
|---|---|---|
| `ano` | LONG | Ano de referência |
| `rede` | STRING | Código/ nome da rede de ensino |
| `taxa_alfabetizacao` | DOUBLE | Taxa de alfabetização observada |
| `meta_alfabetizacao_2024` | DOUBLE | Meta de alfabetização para 2024 |
| `meta_alfabetizacao_2025` | DOUBLE | Meta de alfabetização para 2025 |
| `meta_alfabetizacao_2026` | DOUBLE | Meta de alfabetização para 2026 |
| `meta_alfabetizacao_2027` | DOUBLE | Meta de alfabetização para 2027 |
| `meta_alfabetizacao_2028` | DOUBLE | Meta de alfabetização para 2028 |
| `meta_alfabetizacao_2029` | DOUBLE | Meta de alfabetização para 2029 |
| `meta_alfabetizacao_2030` | DOUBLE | Meta de alfabetização para 2030 |
| `percentual_participacao` | DOUBLE | Percentual de participação na avaliação |
| `data_ingestao` | TIMESTAMP | Data e hora da ingestão |
| `fonte` | STRING | Origem dos dados ("Base dos Dados - BigQuery") |
| `lote_id` | STRING | Identificador único do lote de ingestão |

### Regras de qualidade (DQ Bronze)

| Regra | Severidade | Descrição |
|---|---|---|
| `LOTE_VAZIO` | BLOQUEANTE | Último lote não pode ter zero registros |
| `METADADOS_NULOS` | BLOQUEANTE | `lote_id`, `data_ingestao` e `fonte` não nulos |
| `CHAVE_NULA` | BLOQUEANTE | `ano`, `rede` não nulos |
| `CHAVE_DUPLICADA` | INFORMATIVA | Verifica duplicidade da chave no lote |

## Relacionamento
* **Próxima etapa**: Notebook `Bronze/Qualidade_dados/01_validar_qualidade_bronze`
* **Tratamento downstream**: Notebook `Silver/Tratamento/02_tratamento_meta_brasil`