# Notebook: `01_validar_qualidade_bronze`

## Camada
**Bronze** | Qualidade de dados

## Localização
`Bronze/Qualidade_dados/01_validar_qualidade_bronze`

## Descrição
Notebook de validação de qualidade de dados da camada Bronze. Deve ser executado após os sete notebooks de ingestão. Aplica regras de qualidade sobre o lote mais recente de cada tabela Bronze e persiste os resultados na tabela de monitoramento antes de interromper a execução caso haja falhas bloqueantes.

## Tabelas Envolvidas

| Tabela Bronze | Chave de Negócio |
|---------------|-----------------|
| `workspace.bronze.uf_raw` | `ano`, `sigla_uf`, `serie`, `rede` |
| `workspace.bronze.meta_alfabetizacao_brasil_raw` | `ano`, `rede` |
| `workspace.bronze.meta_alfabetizacao_uf_raw` | `ano`, `sigla_uf`, `rede` |
| `workspace.bronze.meta_alfabetizacao_municipio_raw` | `ano`, `id_municipio` |
| `workspace.bronze.municipio_raw` | `ano`, `id_municipio`, `serie`, `rede` |
| `workspace.bronze.alunos_raw` | `ano`, `id_municipio`, `id_escola`, `id_aluno` |
| `workspace.bronze.dicionario_raw` | `id_tabela`, `nome_coluna`, `chave` |

## Processo de validação

1. Para cada tabela Bronze, seleciona o último lote válido (`lote_id` mais recente com `data_ingestao` não nula).
2. Aplica as 4 regras sobre os registros daquele lote.
3. Persiste cada resultado individual em `workspace.monitoring.qualidade_resultados`.
4. Se qualquer regra bloqueante falhar, o notebook interrompe com `raise RuntimeError` após persistir todas as evidências.

## Regras de Qualidade

| Regra | Severidade | Descrição |
|------|------------|-----------|
| `LOTE_VAZIO` | **BLOQUEANTE** | Último lote não pode ter zero registros |
| `METADADOS_NULOS` | **BLOQUEANTE** | `lote_id`, `data_ingestao` e `fonte` não podem ser nulos |
| `CHAVE_NULA` | **BLOQUEANTE** | Verifica se há registros com chaves de negócio nulas no lote mais recente |
| `CHAVE_DUPLICADA` | **INFORMATIVA** | Verifica se há duplicidade de chaves de negócio no lote mais recente |

## Tabela de monitoramento: `workspace.monitoring.qualidade_resultados`

| Coluna | Tipo | Descrição |
|---|---|---|
| `execution_id` | STRING | UUID único da execução de DQ |
| `layer` | STRING | Camada validada (BRONZE) |
| `table_name` | STRING | Nome completo da tabela validada |
| `rule_name` | STRING | Nome da regra executada |
| `severity` | STRING | Severidade da regra (BLOQUEANTE ou INFORMATIVA) |
| `checked_at` | TIMESTAMP | Momento da verificação |
| `failed_rows` | BIGINT | Quantidade de registros com falha |
| `status` | STRING | PASSOU ou FALHOU |
| `details` | STRING | Detalhes: lote_id, chave e registros afetados |

## Persistência dos Resultados
* Os resultados são gravados na tabela `workspace.monitoring.qualidade_resultados`
* Cada execução recebe um `execution_id` (UUID) único
* Em caso de falha bloqueante, o erro é lançado após persistir todas as evidências

## Pré-requisitos
* Todos os notebooks de ingestão (01 a 07) devem ter sido executados previamente
* As tabelas Bronze devem existir no catálogo `workspace.bronze`

## Relacionamento
* **Executar após**: Notebooks `Bronze/Ingestão/01` a `07`
* **Próxima etapa**: Notebooks de tratamento da camada Silver