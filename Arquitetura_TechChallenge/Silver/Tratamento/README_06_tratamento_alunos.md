# Notebook: `06_tratamento_alunos`

## Camada
**Silver** | Tratamento e padronização

## Localização
`Silver/Tratamento/06_tratamento_alunos`

## Descrição
Notebook responsável pelo tratamento e padronização dos microdados de alunos da Avaliação Nacional de Alfabetização, previamente ingeridos na camada Bronze. Realiza a conversão de tipos, normalização de chaves, padronização de colunas e desduplicação dos registros.

## Origem
* **Tabela Bronze**: `workspace.bronze.alunos_raw`

## Destino
* **Tabela Silver**: `workspace.silver.alunos`
* **Modo**: `CREATE OR REPLACE TABLE`

## Chave de Negócio
`ano + id_municipio + id_escola + id_aluno`

## Tratamentos Realizados
* Cast de tipos: `ano` (INT), `proficiencia` (DOUBLE), `peso_aluno` (DOUBLE)
* `TRIM` em `id_municipio`, `id_escola`, `id_aluno`, `caderno`, `serie`, `rede` (renomeado para `rede_codigo`), `presenca`, `preenchimento_caderno` e `alfabetizado`
* Preservação das colunas de controle: `data_ingestao` e `fonte`
* Filtro de registros nulos: `ano`, `id_municipio`, `id_escola` e `id_aluno` não nulos
* Desduplicação via `QUALIFY ROW_NUMBER()` — mantém apenas o registro mais recente por chave

## Tabela de Destino: `workspace.silver.alunos`

| Item | Valor |
|---|---|
| **Volume (out/2026)** | 3.867.999 linhas |
| **Período coberto** | 2023 a 2024 |
| **Modo** | `CREATE OR REPLACE TABLE` |

### Dicionário de colunas

| Coluna | Tipo | Descrição |
|---|---|---|
| `ano` | INT | Ano da avaliação |
| `id_municipio` | STRING | ID do município (TRIM aplicado) |
| `id_escola` | STRING | ID da escola (TRIM aplicado) |
| `id_aluno` | STRING | ID do aluno (TRIM aplicado) |
| `caderno` | STRING | Tipo de caderno (TRIM aplicado) |
| `serie` | STRING | Série avaliada (TRIM aplicado) |
| `rede_codigo` | STRING | Código da rede (origem: `rede` com TRIM) |
| `presenca` | STRING | Indicador de presença (TRIM aplicado) |
| `preenchimento_caderno` | STRING | Status de preenchimento (TRIM aplicado) |
| `alfabetizado` | STRING | Indicador de alfabetização (TRIM aplicado) |
| `proficiencia` | DOUBLE | Proficiência do aluno |
| `peso_aluno` | DOUBLE | Peso amostral do aluno |
| `data_ingestao` | TIMESTAMP | Data e hora da ingestão (Bronze) |
| `fonte` | STRING | Origem dos dados |
| `lote_id` | STRING | Identificador do lote |

### Regras de qualidade (DQ Silver)

| Regra | Severidade | Descrição |
|---|---|---|
| `CHAVE_NULA` | BLOQUEANTE | `ano`, `id_municipio`, `id_escola`, `id_aluno` não nulos |
| `CHAVE_DUPLICADA` | BLOQUEANTE | Sem duplicidade na chave de negócio |
| `RELACIONAMENTO_SEM_MUNICIPIO` | INFORMATIVA | Alunos sem município correspondente |

## Pré-requisitos
* Notebook `Bronze/Ingestão/06_ingestao_alunos` executado
* Notebook `Bronze/Qualidade_dados/01_validar_qualidade_bronze` executado

## Relacionamento
* **Origem**: `workspace.bronze.alunos_raw`
* **Validação downstream**: Notebook `Silver/Qualidade_dados/01_validar_qualidade_silver`
* **Uso no Gold**: Notebook `Gold/Fato/01_construir_fatos` (ft_resultado_aluno_municipio)