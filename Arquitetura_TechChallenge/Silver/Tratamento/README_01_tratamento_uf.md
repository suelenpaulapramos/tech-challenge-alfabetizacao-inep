# Notebook: `01_tratamento_uf`

## Camada
**Silver** | Tratamento e padronização

## Localização
`Silver/Tratamento/01_tratamento_uf`

## Descrição
Notebook responsável pelo tratamento e padronização dos dados de alfabetização por Unidade Federativa (UF), previamente ingeridos na camada Bronze. Realiza a conversão de tipos, limpeza de espaços, padronização de nomes de colunas e desduplicação dos registros.

## Origem
* **Tabela Bronze**: `workspace.bronze.uf_raw`

## Destino
* **Tabela Silver**: `workspace.silver.uf`
* **Modo**: `CREATE OR REPLACE TABLE`

## Chave de Negócio
`ano + sigla_uf + serie + rede_codigo`

## Tratamentos Realizados
* Cast de tipos: `ano` (INT), `serie` (INT), `taxa_alfabetizacao` (DOUBLE), `media_portugues` (DOUBLE) e proporções por nível (0 a 8) (DOUBLE)
* `TRIM` na coluna `sigla_uf`
* Renomeação de `rede` para `rede_codigo`
* Preservação das colunas de controle: `data_ingestao` e `fonte`
* Filtro de registros nulos: `ano`, `sigla_uf`, `serie` e `rede` não nulos
* Desduplicação via `QUALIFY ROW_NUMBER()` — mantém apenas o registro mais recente por chave

## Tabela de Destino: `workspace.silver.uf`

| Item | Valor |
|---|---|
| **Volume (out/2026)** | 145 linhas |
| **Período coberto** | 2023 a 2024 |
| **Modo** | `CREATE OR REPLACE TABLE` |

### Dicionário de colunas

| Coluna | Tipo | Descrição |
|---|---|---|
| `ano` | INT | Ano de referência da avaliação |
| `sigla_uf` | STRING | Sigla da UF (TRIM aplicado) |
| `serie` | INT | Série avaliada |
| `rede_codigo` | STRING | Código da rede (origem: `rede` com TRIM) |
| `taxa_alfabetizacao` | DOUBLE | Taxa de alfabetização observada |
| `media_portugues` | DOUBLE | Média de proficiência em português |
| `proporcao_aluno_nivel_0` a `proporcao_aluno_nivel_8` | DOUBLE | Proporção de alunos por nível (0 a 8) |
| `data_ingestao` | TIMESTAMP | Data e hora da ingestão ( Bronze) |
| `fonte` | STRING | Origem dos dados |
| `lote_id` | STRING | Identificador do lote |

### Regras de qualidade (DQ Silver)

| Regra | Severidade | Descrição |
|---|---|---|
| `CHAVE_NULA` | BLOQUEANTE | `ano`, `sigla_uf`, `serie`, `rede_codigo` não nulos |
| `CHAVE_DUPLICADA` | BLOQUEANTE | Sem duplicidade na chave de negócio |

## Pré-requisitos
* Notebook `Bronze/Ingestão/01_ingestao_uf` executado
* Notebook `Bronze/Qualidade_dados/01_validar_qualidade_bronze` executado

## Relacionamento
* **Origem**: `workspace.bronze.uf_raw`
* **Validação downstream**: Notebook `Silver/Qualidade_dados/01_validar_qualidade_silver`
* **Uso no Gold**: Notebook `Gold/Fato/01_construir_fatos` (ft_resultado_uf) e `Gold/Dimensoes/01_construir_dimensoes` (dim_uf)