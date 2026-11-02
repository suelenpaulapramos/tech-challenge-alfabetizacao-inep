# Notebook: `04_ingestao_meta_municipio`

## Camada
**Bronze** | Ingestão batch

## Localização
`Bronze/Ingestão/04_ingestao_meta_municipio`

## Descrição
Notebook responsável pela ingestão batch dos dados de metas de alfabetização por município, provenientes da Base dos Dados (BigQuery). Cada execução acrescenta um novo lote imutável à tabela Bronze.

## Origem dos Dados
* **BigQuery**: `basedosdados.br_inep_avaliacao_alfabetizacao.meta_alfabetizacao_municipio`

## Destino
* **Tabela Delta**: `workspace.bronze.meta_alfabetizacao_municipio_raw`
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
3. `ingest_bq_table("meta_municipio", ...)` para realizar a ingestão

## Tabela de Destino: `workspace.bronze.meta_alfabetizacao_municipio_raw`

| Item | Valor |
|---|---|
| **Volume (out/2026)** | 21.408 linhas (2 lotes) |
| **Chave de negócio** | `ano`, `id_municipio` |
| **Período coberto** | 2023 a 2024 |
| **Metas anuais** | 2024 a 2030 |
| **Modo de gravação** | `append` (lotes imutáveis) |

### Dicionário de colunas

| Coluna | Tipo | Descrição |
|---|---|---|
| `ano` | LONG | Ano de referência |
| `id_municipio` | STRING | ID do município (padrão IBGE) |
| `rede` | STRING | Código/ nome da rede de ensino |
| `taxa_alfabetizacao` | DOUBLE | Taxa de alfabetização observada |
| `meta_alfabetizacao_2024` | DOUBLE | Meta de alfabetização para 2024 |
| `meta_alfabetizacao_2025` | DOUBLE | Meta de alfabetização para 2025 |
| `meta_alfabetizacao_2026` | DOUBLE | Meta de alfabetização para 2026 |
| `meta_alfabetizacao_2027` | DOUBLE | Meta de alfabetização para 2027 |
| `meta_alfabetizacao_2028` | DOUBLE | Meta de alfabetização para 2028 |
| `meta_alfabetizacao_2029` | DOUBLE | Meta de alfabetização para 2029 |
| `meta_alfabetizacao_2030` | DOUBLE | Meta de alfabetização para 2030 |
| `nivel_alfabetizacao` | LONG | Nível de alfabetização |
| `percentual_participacao` | DOUBLE | Percentual de participação na avaliação |
| `data_ingestao` | TIMESTAMP | Data e hora da ingestão |
| `fonte` | STRING | Origem dos dados ("Base dos Dados - BigQuery") |
| `lote_id` | STRING | Identificador único do lote de ingestão |

### Regras de qualidade (DQ Bronze)

| Regra | Severidade | Descrição |
|---|---|---|
| `LOTE_VAZIO` | BLOQUEANTE | Último lote não pode ter zero registros |
| `METADADOS_NULOS` | BLOQUEANTE | `lote_id`, `data_ingestao` e `fonte` não nulos |
| `CHAVE_NULA` | BLOQUEANTE | `ano`, `id_municipio` não nulos |
| `CHAVE_DUPLICADA` | INFORMATIVA | Verifica duplicidade da chave no lote |

## Relacionamento
* **Próxima etapa**: Notebook `Bronze/Qualidade_dados/01_validar_qualidade_bronze`
* **Tratamento downstream**: Notebook `Silver/Tratamento/04_tratamento_meta_municipio`