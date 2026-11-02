# Bronze | Ingestão batch

A camada Bronze recebe snapshots das seis entidades obrigatórias da Base dos Dados e preserva o **histórico técnico das cargas**. Cada execução gera um `lote_id` único e adiciona o snapshot em modo `append`.

## Entidades obrigatórias

| Notebook | Origem | Destino |
|---|---|---|
| `01_ingestao_uf` | `...uf` | `workspace.bronze.uf_raw` |
| `02_ingestao_meta_brasil` | `...meta_alfabetizacao_brasil` | `workspace.bronze.meta_alfabetizacao_brasil_raw` |
| `03_ingestao_meta_uf` | `...meta_alfabetizacao_uf` | `workspace.bronze.meta_alfabetizacao_uf_raw` |
| `04_ingestao_meta_municipio` | `...meta_alfabetizacao_municipio` | `workspace.bronze.meta_alfabetizacao_municipio_raw` |
| `05_ingestao_municipio` | `...municipio` | `workspace.bronze.municipio_raw` |
| `06_ingestao_alunos` | `...alunos` | `workspace.bronze.alunos_raw` |

O `07_ingestao_dicionario` é uma fonte auxiliar de referência e não substitui nenhuma das seis entidades obrigatórias.

## Estratégia de histórico

A Bronze não sobrescreve cargas anteriores. Cada lote recebe: `lote_id`, `data_ingestao` e `fonte`. A duplicidade de chaves de negócio é avaliada no último lote pelo DQ Bronze, para não confundir histórico técnico de cargas com duplicidade de negócio.

## Ordem

1. Executar os notebooks 01 a 07.
2. Executar `Qualidade_dados/01_validar_qualidade_bronze`.
3. Somente após o DQ passar, liberar o tratamento Silver.

## Tabelas de monitoramento criadas

O helper cria (se não existirem) duas tabelas no esquema `workspace.monitoring`:

### `workspace.monitoring.pipeline_runs`

| Coluna | Tipo | Descrição |
|---|---|---|
| `run_id` | STRING | UUID único da execução (mesmo valor de `lote_id`) |
| `layer` | STRING | Camada executada (sempre "BRONZE") |
| `entity` | STRING | Nome da entidade ingerida (ex: "uf", "alunos") |
| `started_at` | TIMESTAMP | Início da execução |
| `finished_at` | TIMESTAMP | Fim da execução |
| `duration_seconds` | DOUBLE | Duração total em segundos |
| `status` | STRING | "SUCESSO" ou "FALHA" |
| `row_count` | BIGINT | Quantidade de registros ingeridos |
| `error_message` | STRING | Mensagem de erro (se falha) |

### `workspace.monitoring.finops_ingestion`

| Coluna | Tipo | Descrição |
|---|---|---|
| `run_id` | STRING | UUID único da execução |
| `entity` | STRING | Nome da entidade ingerida |
| `source_table` | STRING | Tabela de origem no BigQuery |
| `bytes_processed` | BIGINT | Bytes processados pelo BigQuery |
| `bytes_billed` | BIGINT | Bytes faturados pelo BigQuery |
| `row_count` | BIGINT | Quantidade de registros ingeridos |
| `recorded_at` | TIMESTAMP | Momento do registro |

## Observação de segurança

O código utiliza atualmente um caminho de credencial do ambiente Databricks para manter compatibilidade com a execução existente. A versão final do repositório deve substituir esse mecanismo por Secret Scope/credencial segura e não versionar arquivos JSON de serviço.
