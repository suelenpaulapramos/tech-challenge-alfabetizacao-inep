# Notebook: `05_ingestao_municipio`

## Camada
**Bronze** | Ingestão batch

## Localização
`Bronze/Ingestão/05_ingestao_municipio`

## Descrição
Notebook responsável pela ingestão batch dos dados de resultados municipais de alfabetização, provenientes da Base dos Dados (BigQuery). Cada execução acrescenta um novo lote imutável à tabela Bronze.

## Origem dos Dados
* **BigQuery**: `basedosdados.br_inep_avaliacao_alfabetizacao.municipio`

## Destino
* **Tabela Delta**: `workspace.bronze.municipio_raw`
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
3. `ingest_bq_table("municipio", ...)` para realizar a ingestão

## Tabela de Destino: `workspace.bronze.municipio_raw`

| Item | Valor |
|---|---|
| **Volume (out/2026)** | 47.990 linhas (2 lotes) |
| **Chave de negócio** | `ano`, `id_municipio`, `serie`, `rede` |
| **Período coberto** | 2023 a 2024 |
| **Modo de gravação** | `append` (lotes imutáveis) |

### Dicionário de colunas

| Coluna | Tipo | Descrição |
|---|---|---|
| `ano` | LONG | Ano de referência da avaliação |
| `id_municipio` | STRING | ID do município (padrão IBGE) |
| `serie` | STRING | Série avaliada |
| `rede` | STRING | Código/ nome da rede de ensino |
| `taxa_alfabetizacao` | DOUBLE | Taxa de alfabetização observada |
| `media_portugues` | DOUBLE | Média de proficiência em português |
| `proporcao_aluno_nivel_0` | DOUBLE | Proporção de alunos no nível 0 de proficiência |
| `proporcao_aluno_nivel_1` | DOUBLE | Proporção de alunos no nível 1 |
| `proporcao_aluno_nivel_2` | DOUBLE | Proporção de alunos no nível 2 |
| `proporcao_aluno_nivel_3` | DOUBLE | Proporção de alunos no nível 3 |
| `proporcao_aluno_nivel_4` | DOUBLE | Proporção de alunos no nível 4 |
| `proporcao_aluno_nivel_5` | DOUBLE | Proporção de alunos no nível 5 |
| `proporcao_aluno_nivel_6` | DOUBLE | Proporção de alunos no nível 6 |
| `proporcao_aluno_nivel_7` | DOUBLE | Proporção de alunos no nível 7 |
| `proporcao_aluno_nivel_8` | DOUBLE | Proporção de alunos no nível 8 |
| `data_ingestao` | TIMESTAMP | Data e hora da ingestão |
| `fonte` | STRING | Origem dos dados ("Base dos Dados - BigQuery") |
| `lote_id` | STRING | Identificador único do lote de ingestão |

### Regras de qualidade (DQ Bronze)

| Regra | Severidade | Descrição |
|---|---|---|
| `LOTE_VAZIO` | BLOQUEANTE | Último lote não pode ter zero registros |
| `METADADOS_NULOS` | BLOQUEANTE | `lote_id`, `data_ingestao` e `fonte` não nulos |
| `CHAVE_NULA` | BLOQUEANTE | `ano`, `id_municipio`, `serie`, `rede` não nulos |
| `CHAVE_DUPLICADA` | INFORMATIVA | Verifica duplicidade da chave no lote |

## Relacionamento
* **Próxima etapa**: Notebook `Bronze/Qualidade_dados/01_validar_qualidade_bronze`
* **Tratamento downstream**: Notebook `Silver/Tratamento/05_tratamento_municipio`