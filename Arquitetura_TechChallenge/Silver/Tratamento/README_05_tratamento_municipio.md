# Notebook: `05_tratamento_municipio`

## Camada
**Silver** | Tratamento e padronização

## Localização
`Silver/Tratamento/05_tratamento_municipio`

## Descrição
Notebook responsável pelo tratamento e padronização dos dados de resultados municipais de alfabetização, previamente ingeridos na camada Bronze. Realiza a conversão de tipos, normalização de chaves, padronização de colunas e desduplicação dos registros.

## Origem
* **Tabela Bronze**: `workspace.bronze.municipio_raw`

## Destino
* **Tabela Silver**: `workspace.silver.municipio`
* **Modo**: `CREATE OR REPLACE TABLE`

## Chave de Negócio
`ano + id_municipio + serie + rede_codigo`

## Tratamentos Realizados
* Cast de tipos: `ano` (INT), `taxa_alfabetizacao` (DOUBLE), `media_portugues` (DOUBLE) e proporções por nível (0 a 8) (DOUBLE)
* `TRIM` em `id_municipio`, `serie` e `rede` (renomeado para `rede_codigo`)
* Preservação das colunas de controle: `data_ingestao` e `fonte`
* Filtro de registros nulos: `ano`, `id_municipio`, `serie` e `rede` não nulos
* Desduplicação via `QUALIFY ROW_NUMBER()` — mantém apenas o registro mais recente por chave

## Tabela de Destino: `workspace.silver.municipio`

| Item | Valor |
|---|---|
| **Volume (out/2026)** | 23.995 linhas |
| **Período coberto** | 2023 a 2024 |
| **Modo** | `CREATE OR REPLACE TABLE` |

### Dicionário de colunas

| Coluna | Tipo | Descrição |
|---|---|---|
| `ano` | INT | Ano de referência da avaliação |
| `id_municipio` | STRING | ID do município (TRIM aplicado) |
| `serie` | STRING | Série avaliada (TRIM aplicado) |
| `rede_codigo` | STRING | Código da rede (origem: `rede` com TRIM) |
| `taxa_alfabetizacao` | DOUBLE | Taxa de alfabetização observada |
| `media_portugues` | DOUBLE | Média de proficiência em português |
| `proporcao_aluno_nivel_0` a `proporcao_aluno_nivel_8` | DOUBLE | Proporção de alunos por nível (0 a 8) |
| `data_ingestao` | TIMESTAMP | Data e hora da ingestão (Bronze) |
| `fonte` | STRING | Origem dos dados |
| `lote_id` | STRING | Identificador do lote |

### Regras de qualidade (DQ Silver)

| Regra | Severidade | Descrição |
|---|---|---|
| `CHAVE_NULA` | BLOQUEANTE | `ano`, `id_municipio`, `serie`, `rede_codigo` não nulos |
| `CHAVE_DUPLICADA` | BLOQUEANTE | Sem duplicidade na chave de negócio |

## Pré-requisitos
* Notebook `Bronze/Ingestão/05_ingestao_municipio` executado
* Notebook `Bronze/Qualidade_dados/01_validar_qualidade_bronze` executado

## Relacionamento
* **Origem**: `workspace.bronze.municipio_raw`
* **Validação downstream**: Notebook `Silver/Qualidade_dados/01_validar_qualidade_silver` (verifica integridade referencial com `meta_alfabetizacao_municipio`)
* **Uso no Gold**: Notebook `Gold/Fato/01_construir_fatos` (ft_resultado_municipio e ft_meta_vs_resultado_municipio) e `Gold/Dimensoes/01_construir_dimensoes` (dim_tempo e dim_municipio)