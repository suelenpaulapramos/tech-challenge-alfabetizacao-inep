# Notebook: `01_validar_qualidade_gold`

## Camada
**Gold** | Validação de qualidade das tabelas fato

## Localização
`Gold/Qualidade_dados/01_validar_qualidade_gold`

## Descrição
Notebook de validação de qualidade de dados da camada Gold. Verifica se as tabelas fato principais (nível município e agregado de alunos) possuem chaves de negócio duplicadas ou nulas. Os resultados de todas as verificações são persistidos antes de qualquer interrupção: se alguma regra bloqueante falhar, o notebook lança erro somente ao final, depois de gravar todas as evidências.

## Escopo da Validação
* **Validadas**: 4 tabelas fato (listadas abaixo)
* **Não validadas**: as tabelas de dimensão e as demais tabelas fato (`ft_resultado_uf`, `ft_resultado_brasil`, `ft_meta_brasil`, `ft_meta_uf`, `ft_meta_vs_resultado_uf` e `ft_meta_vs_resultado_brasil`)

## Tabelas Validadas

| Tabela Gold | Chave de Negócio |
|-------------|-----------------|
| `workspace.gold.ft_resultado_municipio` | `ano`, `id_municipio`, `serie`, `rede_codigo` |
| `workspace.gold.ft_meta_municipio` | `id_municipio`, `rede_codigo`, `ano_meta` |
| `workspace.gold.ft_meta_vs_resultado_municipio` | `ano`, `id_municipio`, `serie`, `rede_codigo` |
| `workspace.gold.ft_resultado_aluno_municipio` | `ano`, `id_municipio`, `serie`, `rede_codigo`, `categoria_alfabetizacao` |

## Processo de validação

1. Gera um `execution_id` (UUID) unico para a execucao.
2. Para cada uma das 4 tabelas validadas, aplica as 2 regras (CHAVE_DUPLICADA e CHAVE_NULA).
3. Cada verificacao gera um registro individual em `workspace.monitoring.qualidade_resultados`.
4. Se qualquer regra bloqueante falhar, o notebook interrompe com `raise RuntimeError` listando as tabelas e regras com falha (formato `tabela:REGRA=quantidade`), apos persistir todas as evidencias.

## Regras de Qualidade

Cada regra e aplicada a cada uma das tabelas acima (8 verificacoes por execucao).

| Regra | Severidade | Descrição |
|------|------------|-----------|
| `CHAVE_DUPLICADA` | **BLOQUEANTE** | Conta as combinações de chave de negócio que aparecem mais de uma vez |
| `CHAVE_NULA` | **BLOQUEANTE** | Conta os registros em que ao menos uma coluna da chave de negócio é nula |

## Tabela de monitoramento: `workspace.monitoring.qualidade_resultados`

| Coluna | Tipo | Descrição |
|---|---|---|
| `execution_id` | STRING | UUID único da execução de DQ |
| `layer` | STRING | Camada validada (GOLD) |
| `table_name` | STRING | Nome completo da tabela validada |
| `rule_name` | STRING | Nome da regra executada |
| `severity` | STRING | Severidade da regra (BLOQUEANTE) |
| `checked_at` | TIMESTAMP | Momento da verificação (UTC) |
| `failed_rows` | BIGINT | Quantidade de registros com falha |
| `status` | STRING | PASSOU ou FALHOU |
| `details` | STRING | Colunas da chave verificada |

* O notebook cria o schema `workspace.monitoring` e a tabela `workspace.monitoring.qualidade_resultados` caso não existam
* Os registros são gravados em modo `append`, preservando o histórico de execuções
* Cada execução recebe um `execution_id` (UUID) único, compartilhado por todos os registros daquela execução

## Pré-requisitos
* Notebook `Gold/Fato/01_construir_fatos` executado (as tabelas validadas precisam existir)
* Não depende do notebook `Gold/Dimensoes/01_construir_dimensoes`

## Relacionamento
* **Executar após**: `Gold/Fato/01_construir_fatos`
* **Notebook complementar**: `Gold/Qualidade_dados/99_demo_falha_qualidade_dados` (demonstração didática de falha)
