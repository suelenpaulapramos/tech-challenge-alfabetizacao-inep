# Notebook: `04_tratamento_meta_municipio`

## Camada
**Silver** | Tratamento e padronização

## Localização
`Silver/Tratamento/04_tratamento_meta_municipio`

## Descrição
Notebook responsável pelo tratamento e padronização dos dados de metas de alfabetização por município, previamente ingeridos na camada Bronze. Realiza a conversão de tipos, limpeza de espaços e desduplicação dos registros.

## Origem
* **Tabela Bronze**: `workspace.bronze.meta_alfabetizacao_municipio_raw`

## Destino
* **Tabela Silver**: `workspace.silver.meta_alfabetizacao_municipio`
* **Modo**: `CREATE OR REPLACE TABLE`

## Chave de Negócio
`ano + id_municipio`

## Tratamentos Realizados
* Cast de tipos: `ano` (INT), `taxa_alfabetizacao` (DOUBLE), metas de 2024 a 2030 (DOUBLE), `nivel_alfabetizacao` (INT), `percentual_participacao` (DOUBLE)
* `TRIM` em `id_municipio` e `rede` (renomeado para `rede_codigo`)
* Preservação das colunas de controle: `data_ingestao` e `fonte`
* Filtro de registros nulos: `ano` e `id_municipio` não nulos
* Desduplicação via `QUALIFY ROW_NUMBER()` — mantém apenas o registro mais recente por chave

## Tabela de Destino: `workspace.silver.meta_alfabetizacao_municipio`

| Item | Valor |
|---|---|
| **Volume (out/2026)** | 10.704 linhas |
| **Período coberto** | 2023 a 2024 |
| **Metas anuais** | 2024 a 2030 |
| **Modo** | `CREATE OR REPLACE TABLE` |

> Nota: o SQL de deduplicacao usa `PARTITION BY ano, id_municipio` (2 colunas). A coluna `rede_codigo` e derivada via CASE WHEN (rede municipal = '3', demais = NULL) e nao participa da chave de deduplicacao.

### Dicionário de colunas

| Coluna | Tipo | Descrição |
|---|---|---|
| `ano` | INT | Ano de referência |
| `id_municipio` | STRING | ID do município (TRIM aplicado) |
| `rede` | STRING | Nome original da rede (TRIM aplicado) |
| `rede_codigo` | STRING | Código derivado: '3' se rede municipal, NULL caso contrário |
| `taxa_alfabetizacao` | DOUBLE | Taxa de alfabetização observada |
| `meta_alfabetizacao_2024` a `meta_alfabetizacao_2030` | DOUBLE | Metas anuais de 2024 a 2030 |
| `nivel_alfabetizacao` | INT | Nível de alfabetização |
| `percentual_participacao` | DOUBLE | Percentual de participação |
| `data_ingestao` | TIMESTAMP | Data e hora da ingestão (Bronze) |
| `fonte` | STRING | Origem dos dados |
| `lote_id` | STRING | Identificador do lote |

### Regras de qualidade (DQ Silver)

| Regra | Severidade | Descrição |
|---|---|---|
| `CHAVE_NULA` | BLOQUEANTE | `ano`, `id_municipio` não nulos |
| `CHAVE_DUPLICADA` | BLOQUEANTE | Sem duplicidade na chave de negócio |
| `RELACIONAMENTO_SEM_META_REDE_MUNICIPAL` | INFORMATIVA | Resultados da rede municipal sem meta correspondente |

## Pré-requisitos
* Notebook `Bronze/Ingestão/04_ingestao_meta_municipio` executado
* Notebook `Bronze/Qualidade_dados/01_validar_qualidade_bronze` executado

## Relacionamento
* **Origem**: `workspace.bronze.meta_alfabetizacao_municipio_raw`
* **Validação downstream**: Notebook `Silver/Qualidade_dados/01_validar_qualidade_silver` (verifica integridade referencial com `municipio`)
* **Uso no Gold**: Notebook `Gold/Fato/01_construir_fatos` (ft_meta_municipio e ft_meta_vs_resultado_municipio)