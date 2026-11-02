# Notebook: `06_ingestao_alunos`

## Camada
**Bronze** | Ingestão batch

## Localização
`Bronze/Ingestão/06_ingestao_alunos`

## Descrição
Notebook responsável pela ingestão batch dos microdados de alunos da Avaliação Nacional de Alfabetização, provenientes da Base dos Dados (BigQuery). Esta fonte pode ser volumosa, por isso utiliza um limite de bytes faturáveis maior (50 GB) em comparação com os demais notebooks de ingestão.

## Origem dos Dados
* **BigQuery**: `basedosdados.br_inep_avaliacao_alfabetizacao.alunos`

## Destino
* **Tabela Delta**: `workspace.bronze.alunos_raw`
* **Modo de gravação**: `append` (lotes imutáveis)

## Colunas de Controle Adicionadas
* `data_ingestao` — timestamp da carga
* `fonte` — "Base dos Dados - BigQuery"
* `lote_id` — UUID único do lote

## Configuração Especial
* `max_bytes_billed = 50_000_000_000` (50 GB) — limite elevado para acomodar o volume de microdados

## Pré-requisitos
* Executar o notebook `_common_ingestao` (incluído via `%run`)
* Credencial do ambiente Databricks disponível no caminho configurado no helper
* Bibliotecas BigQuery instaladas

## Ordem de Execução
1. `%pip install` das dependências
2. `%run ./_common_ingestao` para carregar o helper
3. `ingest_bq_table("alunos", ..., max_bytes_billed=50_000_000_000)` para realizar a ingestão

## Tabela de Destino: `workspace.bronze.alunos_raw`

| Item | Valor |
|---|---|
| **Volume (out/2026)** | 7.735.998 linhas (2 lotes) |
| **Chave de negócio** | `ano`, `id_municipio`, `id_escola`, `id_aluno` |
| **Período coberto** | 2023 a 2024 |
| **Modo de gravação** | `append` (lotes imutáveis) |
| **Limite de bytes** | 50 GB (`max_bytes_billed`) |

### Dicionário de colunas

| Coluna | Tipo | Descrição |
|---|---|---|
| `ano` | LONG | Ano da avaliação |
| `id_municipio` | STRING | ID do município (padrão IBGE) |
| `id_escola` | STRING | ID da escola |
| `id_aluno` | STRING | ID do aluno |
| `caderno` | STRING | Tipo de caderno aplicado |
| `serie` | STRING | Série avaliada |
| `rede` | STRING | Código/ nome da rede de ensino |
| `presenca` | STRING | Indicador de presença na avaliação |
| `preenchimento_caderno` | STRING | Status de preenchimento do caderno |
| `alfabetizado` | STRING | Indicador de alfabetização (sim/ não) |
| `proficiencia` | DOUBLE | Proficiência do aluno |
| `peso_aluno` | DOUBLE | Peso amostral do aluno |
| `data_ingestao` | TIMESTAMP | Data e hora da ingestão |
| `fonte` | STRING | Origem dos dados ("Base dos Dados - BigQuery") |
| `lote_id` | STRING | Identificador único do lote de ingestão |

### Regras de qualidade (DQ Bronze)

| Regra | Severidade | Descrição |
|---|---|---|
| `LOTE_VAZIO` | BLOQUEANTE | Último lote não pode ter zero registros |
| `METADADOS_NULOS` | BLOQUEANTE | `lote_id`, `data_ingestao` e `fonte` não nulos |
| `CHAVE_NULA` | BLOQUEANTE | `ano`, `id_municipio`, `id_escola`, `id_aluno` não nulos |
| `CHAVE_DUPLICADA` | INFORMATIVA | Verifica duplicidade da chave no lote |

## Relacionamento
* **Próxima etapa**: Notebook `Bronze/Qualidade_dados/01_validar_qualidade_bronze`
* **Tratamento downstream**: Notebook `Silver/Tratamento/06_tratamento_alunos`
* **Streaming relacionado**: Notebooks `Bronze/Streaming/01_preparar_eventos_demo` e `Bronze/Streaming/02_streaming_alunos`