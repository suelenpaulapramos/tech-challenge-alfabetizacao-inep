# Notebook: `02_tratamento_meta_brasil`

## Camada
**Silver** | Tratamento e padronização

## Localização
`Silver/Tratamento/02_tratamento_meta_brasil`

## Descrição
Notebook responsável pelo tratamento e padronização dos dados de metas de alfabetização em nível Brasil, previamente ingeridos na camada Bronze. Realiza a conversão de tipos, limpeza de espaços e desduplicação dos registros.

## Origem
* **Tabela Bronze**: `workspace.bronze.meta_alfabetizacao_brasil_raw`

## Destino
* **Tabela Silver**: `workspace.silver.meta_alfabetizacao_brasil`
* **Modo**: `CREATE OR REPLACE TABLE`

## Chave de Negócio
`ano + rede_codigo`

## Tratamentos Realizados
* Cast de tipos: `ano` (INT), `taxa_alfabetizacao` (DOUBLE), metas de 2024 a 2030 (DOUBLE), `percentual_participacao` (DOUBLE)
* `TRIM` na coluna `rede` e renomeação para `rede_codigo`
* Preservação das colunas de controle: `data_ingestao` e `fonte`
* Filtro de registros nulos: `ano` e `rede` não nulos
* Desduplicação via `QUALIFY ROW_NUMBER()` — mantém apenas o registro mais recente por chave

## Tabela de Destino: `workspace.silver.meta_alfabetizacao_brasil`

| Item | Valor |
|---|---|
| **Volume (out/2026)** | 3 linhas |
| **Período coberto** | 2023 a 2025 |
| **Metas anuais** | 2024 a 2030 |
| **Modo** | `CREATE OR REPLACE TABLE` |

### Dicionário de colunas

| Coluna | Tipo | Descrição |
|---|---|---|
| `ano` | INT | Ano de referência |
| `rede_codigo` | STRING | Código da rede (origem: `rede` com TRIM) |
| `taxa_alfabetizacao` | DOUBLE | Taxa de alfabetização observada |
| `meta_alfabetizacao_2024` a `meta_alfabetizacao_2030` | DOUBLE | Metas anuais de 2024 a 2030 |
| `percentual_participacao` | DOUBLE | Percentual de participação |
| `data_ingestao` | TIMESTAMP | Data e hora da ingestão (Bronze) |
| `fonte` | STRING | Origem dos dados |
| `lote_id` | STRING | Identificador do lote |

### Regras de qualidade (DQ Silver)

| Regra | Severidade | Descrição |
|---|---|---|
| `CHAVE_NULA` | BLOQUEANTE | `ano`, `rede_codigo` não nulos |
| `CHAVE_DUPLICADA` | BLOQUEANTE | Sem duplicidade na chave de negócio |

## Pré-requisitos
* Notebook `Bronze/Ingestão/02_ingestao_meta_brasil` executado
* Notebook `Bronze/Qualidade_dados/01_validar_qualidade_bronze` executado

## Relacionamento
* **Origem**: `workspace.bronze.meta_alfabetizacao_brasil_raw`
* **Validação downstream**: Notebook `Silver/Qualidade_dados/01_validar_qualidade_silver`
* **Uso no Gold**: Notebook `Gold/Fato/01_construir_fatos` (ft_resultado_brasil e ft_meta_brasil)