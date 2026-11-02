# Notebook: `01_validar_qualidade_silver`

## Camada
**Silver** | Qualidade de dados e integridade referencial

## Localização
`Silver/Qualidade_dados/01_validar_qualidade_silver`

## Descrição
Notebook de validação de qualidade de dados da camada Silver. Deve ser executado depois dos seis notebooks de tratamento. Verifica chaves nulas, duplicidades e integridade referencial entre as tabelas Silver.

## Tabelas Validadas

| Tabela Silver | Chave de Negócio |
|---------------|-----------------|
| `workspace.silver.uf` | `ano`, `sigla_uf`, `serie`, `rede_codigo` |
| `workspace.silver.meta_alfabetizacao_brasil` | `ano`, `rede_codigo` |
| `workspace.silver.meta_alfabetizacao_uf` | `ano`, `sigla_uf`, `rede_codigo` |
| `workspace.silver.meta_alfabetizacao_municipio` | `ano`, `id_municipio` |
| `workspace.silver.municipio` | `ano`, `id_municipio`, `serie`, `rede_codigo` |
| `workspace.silver.alunos` | `ano`, `id_municipio`, `id_escola`, `id_aluno` |

## Processo de validacao

1. Gera um `execution_id` (UUID) unico para a execucao.
2. Para cada uma das 6 tabelas Silver, valida CHAVE_NULA e CHAVE_DUPLICADA (regras bloqueantes).
3. Verifica relacionamentos entre tabelas (regras informativas).
4. Persiste cada resultado individual em `workspace.monitoring.qualidade_resultados`.
5. Se qualquer regra bloqueante falhar, o notebook interrompe com `raise RuntimeError` apos persistir todas as evidencias.

## Regras de Qualidade

| Regra | Severidade | Descrição |
|------|------------|-----------|
| `CHAVE_NULA` | **BLOQUEANTE** | Verifica se há registros com chaves de negócio nulas |
| `CHAVE_DUPLICADA` | **BLOQUEANTE** | Verifica se há duplicidade de chaves de negócio |
| `RELACIONAMENTO_SEM_META_REDE_MUNICIPAL` | **INFORMATIVA** | Resultados da rede municipal (rede_codigo = '3') em `municipio` sem correspondência em `meta_alfabetizacao_municipio` (join por ano + id_municipio + rede_codigo). 242 registros em out/2026 |
| `RELACIONAMENTO_SEM_MUNICIPIO` | **INFORMATIVA** | Alunos em `alunos` sem município correspondente em `municipio` (join por ano + id_municipio). 3.209 registros em out/2026 |

## Tabela de monitoramento: `workspace.monitoring.qualidade_resultados`

| Coluna | Tipo | Descrição |
|---|---|---|
| `execution_id` | STRING | UUID único da execução de DQ |
| `layer` | STRING | Camada validada (SILVER) |
| `table_name` | STRING | Nome completo da tabela validada |
| `rule_name` | STRING | Nome da regra executada |
| `severity` | STRING | Severidade da regra (BLOQUEANTE ou INFORMATIVA) |
| `checked_at` | TIMESTAMP | Momento da verificação |
| `failed_rows` | BIGINT | Quantidade de registros com falha |
| `status` | STRING | PASSOU ou FALHOU |
| `details` | STRING | Detalhes: chave verificada e distribuicao por ano |

* Os resultados são gravados em modo `append`, preservando o histórico de execuções
* Cada execução recebe um `execution_id` (UUID) único
* Em caso de falha bloqueante, o erro é lançado após persistir todas as evidências

## Pré-requisitos
* Todos os notebooks de tratamento (01 a 06) da Silver devem ter sido executados

## Relacionamento
* **Executar após**: Notebooks `Silver/Tratamento/01` a `06` e `Silver/Dimensoes/01_dicionario_oficial`
* **Próxima etapa**: Notebooks da camada Gold