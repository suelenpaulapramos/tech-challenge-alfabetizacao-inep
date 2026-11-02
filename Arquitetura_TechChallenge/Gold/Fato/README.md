# Notebook: `01_construir_fatos`

## Camada
**Gold** | Construção de tabelas fato

## Localização
`Gold/Fato/01_construir_fatos`

## Descrição
Notebook responsável pela construção das tabelas fato da camada Gold. Cria medidas de resultado, metas, comparações entre resultado e meta (com a classificação derivada `situacao_meta`) e um agregado dos microdados de alunos. As colunas anuais de metas (2024-2030) são transformadas em registros por ano-meta com `UNPIVOT`.

O notebook cria o schema `workspace.gold` caso ele não exista e recria todas as tabelas em formato Delta (`CREATE OR REPLACE`), portanto pode ser reexecutado com segurança. A ordem das células importa: as tabelas `ft_meta_vs_resultado_*` leem as tabelas `ft_meta_*` criadas anteriormente no próprio notebook.

## Tabelas Fato Criadas

### Resultados

| Tabela Gold | Origem Silver | Grão | Descrição |
|-------------|---------------|------|-----------|
| `ft_resultado_municipio` | `workspace.silver.municipio` | ano + id_municipio + serie + rede_codigo | `taxa_alfabetizacao`, `media_portugues` e `proporcao_aluno_nivel_0` a `proporcao_aluno_nivel_8` |
| `ft_resultado_uf` | `workspace.silver.uf` | ano + sigla_uf + serie + rede_codigo | Mesmas medidas, por UF |
| `ft_resultado_brasil` | `workspace.silver.meta_alfabetizacao_brasil` | ano + rede_codigo | `taxa_alfabetizacao` e `percentual_participacao` |

### Metas

As colunas `meta_alfabetizacao_2024` a `meta_alfabetizacao_2030` são convertidas em linhas, com as colunas `ano_meta` (armazenado como texto, por exemplo `'2024'`) e `meta_alfabetizacao`. Como a Silver pode conter mais de um `ano` de referência para a mesma meta, é mantido apenas o registro com **`ano_referencia` mais recente** para cada combinação de chaves (`QUALIFY ROW_NUMBER() ... = 1`).

| Tabela Gold | Origem Silver | Grão | Colunas |
|-------------|---------------|------|---------|
| `ft_meta_brasil` | `workspace.silver.meta_alfabetizacao_brasil` | rede_codigo + ano_meta | `ano_referencia`, `rede_codigo`, `ano_meta`, `meta_alfabetizacao` |
| `ft_meta_uf` | `workspace.silver.meta_alfabetizacao_uf` | sigla_uf + rede_codigo + ano_meta | `ano_referencia`, `sigla_uf`, `rede_codigo`, `ano_meta`, `meta_alfabetizacao` |
| `ft_meta_municipio` | `workspace.silver.meta_alfabetizacao_municipio` | id_municipio + rede_codigo + ano_meta | `ano_referencia`, `id_municipio`, `rede_codigo`, `ano_meta`, `meta_alfabetizacao` |

### Comparações Resultado vs Meta

O resultado de cada `ano` é comparado com a meta cujo `ano_meta` é igual a esse mesmo `ano` (`ano = CAST(ano_meta AS INT)`), usando `LEFT JOIN` a partir do resultado. Assim, linhas de resultado sem meta correspondente são preservadas e classificadas como `SEM_META`. Todas as tabelas trazem `taxa_alfabetizacao`, `meta_alfabetizacao`, `diferenca_meta` (`taxa_alfabetizacao - meta_alfabetizacao`) e `situacao_meta`.

| Tabela Gold | Origem | Grão | Observações |
|-------------|--------|------|-------------|
| `ft_meta_vs_resultado_municipio` | `workspace.silver.municipio` + `ft_meta_municipio` | ano + id_municipio + serie + rede_codigo | **Somente rede Municipal** (`rede_codigo = '3'`) |
| `ft_meta_vs_resultado_uf` | `workspace.silver.uf` + `ft_meta_uf` | ano + sigla_uf + serie + rede_codigo | Sem filtro de rede |
| `ft_meta_vs_resultado_brasil` | `workspace.silver.meta_alfabetizacao_brasil` + `ft_meta_brasil` | ano + rede_codigo | Sem filtro de rede; não possui coluna `serie` |

### Agregados

| Tabela Gold | Origem Silver | Grão | Descrição |
|-------------|---------------|------|-----------|
| `ft_resultado_aluno_municipio` | `workspace.silver.alunos` | ano + id_municipio + serie + rede_codigo + categoria_alfabetizacao | `quantidade_alunos` (contagem de registros) e `proficiencia_media` (média de `proficiencia`). A coluna `alfabetizado` é renomeada para `categoria_alfabetizacao` sem transformação |

## Volume e dicionário por tabela fato

### `workspace.gold.ft_resultado_municipio`

| Item | Valor |
|---|---|
| **Volume (out/2026)** | 23.995 linhas |
| **Origem** | `workspace.silver.municipio` (projeção direta) |
| **Chave** | `ano`, `id_municipio`, `serie`, `rede_codigo` |

| Coluna | Tipo | Descrição |
|---|---|---|
| `ano` | INT | Ano de referência |
| `id_municipio` | STRING | ID do município (padrão IBGE) |
| `serie` | STRING | Série avaliada |
| `rede_codigo` | STRING | Código da rede de ensino |
| `taxa_alfabetizacao` | DOUBLE | Taxa de alfabetização observada |
| `media_portugues` | DOUBLE | Média de proficiência em português |
| `proporcao_aluno_nivel_0` a `proporcao_aluno_nivel_8` | DOUBLE | Proporção de alunos por nível de proficiência (0 a 8) |

### `workspace.gold.ft_resultado_uf`

| Item | Valor |
|---|---|
| **Volume (out/2026)** | 145 linhas |
| **Origem** | `workspace.silver.uf` (projeção direta) |
| **Chave** | `ano`, `sigla_uf`, `serie`, `rede_codigo` |

| Coluna | Tipo | Descrição |
|---|---|---|
| `ano` | INT | Ano de referência |
| `sigla_uf` | STRING | Sigla da unidade federativa |
| `serie` | INT | Série avaliada |
| `rede_codigo` | STRING | Código da rede de ensino |
| `taxa_alfabetizacao` | DOUBLE | Taxa de alfabetização observada |
| `media_portugues` | DOUBLE | Média de proficiência em português |
| `proporcao_aluno_nivel_0` a `proporcao_aluno_nivel_8` | DOUBLE | Proporção de alunos por nível (0 a 8) |

### `workspace.gold.ft_resultado_brasil`

| Item | Valor |
|---|---|
| **Volume (out/2026)** | 3 linhas |
| **Origem** | `workspace.silver.meta_alfabetizacao_brasil` (projeção direta) |
| **Chave** | `ano`, `rede_codigo` |

| Coluna | Tipo | Descrição |
|---|---|---|
| `ano` | INT | Ano de referência |
| `rede_codigo` | STRING | Código da rede de ensino |
| `taxa_alfabetizacao` | DOUBLE | Taxa de alfabetização observada |
| `percentual_participacao` | DOUBLE | Percentual de participação na avaliação |

### `workspace.gold.ft_resultado_aluno_municipio`

| Item | Valor |
|---|---|
| **Volume (out/2026)** | 24.777 linhas |
| **Origem** | `workspace.silver.alunos` (agregação GROUP BY) |
| **Chave** | `ano`, `id_municipio`, `serie`, `rede_codigo`, `categoria_alfabetizacao` |

| Coluna | Tipo | Descrição |
|---|---|---|
| `ano` | INT | Ano da avaliação |
| `id_municipio` | STRING | ID do município (padrão IBGE) |
| `serie` | STRING | Série avaliada |
| `rede_codigo` | STRING | Código da rede de ensino |
| `categoria_alfabetizacao` | STRING | Categoria de alfabetização (origem: coluna `alfabetizado`) |
| `quantidade_alunos` | LONG | Contagem de alunos na categoria |
| `proficiencia_media` | DOUBLE | Média de `proficiencia` dos alunos na categoria |

### `workspace.gold.ft_meta_brasil`

| Item | Valor |
|---|---|
| **Volume (out/2026)** | 7 linhas |
| **Origem** | `workspace.silver.meta_alfabetizacao_brasil` (UNPIVOT) |
| **Deduplicação** | QUALIFY ROW_NUMBER() OVER (PARTITION BY rede_codigo, ano_meta ORDER BY ano_referencia DESC) = 1 |

| Coluna | Tipo | Descrição |
|---|---|---|
| `ano_referencia` | INT | Ano de referência da fonte |
| `rede_codigo` | STRING | Código da rede de ensino |
| `ano_meta` | STRING | Ano da meta (texto, ex: 2024) |
| `meta_alfabetizacao` | DOUBLE | Valor da meta de alfabetização |

### `workspace.gold.ft_meta_uf`

| Item | Valor |
|---|---|
| **Volume (out/2026)** | 185 linhas |
| **Origem** | `workspace.silver.meta_alfabetizacao_uf` (UNPIVOT) |
| **Deduplicação** | QUALIFY ROW_NUMBER() OVER (PARTITION BY sigla_uf, rede_codigo, ano_meta ORDER BY ano_referencia DESC) = 1 |

| Coluna | Tipo | Descrição |
|---|---|---|
| `ano_referencia` | INT | Ano de referência da fonte |
| `sigla_uf` | STRING | Sigla da unidade federativa |
| `rede_codigo` | STRING | Código da rede de ensino |
| `ano_meta` | STRING | Ano da meta (texto, ex: 2025) |
| `meta_alfabetizacao` | DOUBLE | Valor da meta de alfabetização |

### `workspace.gold.ft_meta_municipio`

| Item | Valor |
|---|---|
| **Volume (out/2026)** | 37.344 linhas |
| **Origem** | `workspace.silver.meta_alfabetizacao_municipio` (UNPIVOT) |
| **Deduplicação** | QUALIFY ROW_NUMBER() OVER (PARTITION BY id_municipio, rede_codigo, ano_meta ORDER BY ano_referencia DESC) = 1 |

| Coluna | Tipo | Descrição |
|---|---|---|
| `ano_referencia` | INT | Ano de referência da fonte |
| `id_municipio` | STRING | ID do município (padrão IBGE) |
| `rede_codigo` | STRING | Código da rede de ensino |
| `ano_meta` | STRING | Ano da meta (texto, ex: 2024) |
| `meta_alfabetizacao` | DOUBLE | Valor da meta de alfabetização |

### `workspace.gold.ft_meta_vs_resultado_municipio`

| Item | Valor |
|---|---|
| **Volume (out/2026)** | 10.896 linhas |
| **Origem** | `ft_resultado_municipio` LEFT JOIN `ft_meta_municipio` |
| **Chave** | `ano`, `id_municipio`, `serie`, `rede_codigo` |
| **Filtro** | `rede_codigo = '3'` (rede municipal); `ano_referencia = 2024` |

| Coluna | Tipo | Descrição |
|---|---|---|
| `ano` | INT | Ano de referência |
| `id_municipio` | STRING | ID do município (padrão IBGE) |
| `serie` | STRING | Série avaliada |
| `rede_codigo` | STRING | Código da rede de ensino |
| `taxa_alfabetizacao` | DOUBLE | Taxa de alfabetização observada |
| `meta_alfabetizacao` | DOUBLE | Meta de alfabetização do ano |
| `diferenca_meta` | DOUBLE | taxa_alfabetizacao - meta_alfabetizacao |
| `situacao_meta` | STRING | Classificação derivada (ver seção abaixo) |

### `workspace.gold.ft_meta_vs_resultado_uf`

| Item | Valor |
|---|---|
| **Volume (out/2026)** | 145 linhas |
| **Origem** | `ft_resultado_uf` LEFT JOIN `ft_meta_uf` |
| **Chave** | `ano`, `sigla_uf`, `serie`, `rede_codigo` |
| **Filtro** | Comparação válida apenas para `ano = 2025`; demais anos como `SEM_META_DISPONIVEL_PARA_COMPARACAO` |

| Coluna | Tipo | Descrição |
|---|---|---|
| `ano` | INT | Ano de referência |
| `sigla_uf` | STRING | Sigla da unidade federativa |
| `serie` | INT | Série avaliada |
| `rede_codigo` | STRING | Código da rede de ensino |
| `taxa_alfabetizacao` | DOUBLE | Taxa de alfabetização observada |
| `meta_alfabetizacao` | DOUBLE | Meta de alfabetização do ano |
| `diferenca_meta` | DOUBLE | taxa_alfabetizacao - meta_alfabetizacao |
| `situacao_meta` | STRING | Classificação derivada (ver seção abaixo) |

### `workspace.gold.ft_meta_vs_resultado_brasil`

| Item | Valor |
|---|---|
| **Volume (out/2026)** | 3 linhas |
| **Origem** | `ft_resultado_brasil` LEFT JOIN `ft_meta_brasil` |
| **Chave** | `ano`, `rede_codigo` |

| Coluna | Tipo | Descrição |
|---|---|---|
| `ano` | INT | Ano de referência |
| `rede_codigo` | STRING | Código da rede de ensino |
| `taxa_alfabetizacao` | DOUBLE | Taxa de alfabetização observada |
| `meta_alfabetizacao` | DOUBLE | Meta de alfabetização do ano |
| `diferenca_meta` | DOUBLE | taxa_alfabetizacao - meta_alfabetizacao |
| `situacao_meta` | STRING | Classificação derivada (ver seção abaixo) |

## Coluna `situacao_meta` (Classificação Derivada)

As condições são avaliadas **na ordem abaixo**; a primeira que for verdadeira define o valor:

| Ordem | Valor | Condição |
|-------|-------|----------|
| 0 | `SEM_META_DISPONIVEL_PARA_COMPARACAO` | Ano diferente do ano de comparação (em `ft_meta_vs_resultado_municipio` quando ano <> 2024; em `ft_meta_vs_resultado_uf` quando ano <> 2025) |
| 1 | `SEM_META` | `meta_alfabetizacao IS NULL` |
| 2 | `SEM_RESULTADO` | `taxa_alfabetizacao IS NULL` (e meta preenchida) |
| 3 | `ATINGIU_OU_SUPEROU` | `taxa_alfabetizacao >= meta_alfabetizacao` |
| 4 | `ABAIXO_DA_META` | demais casos (`taxa_alfabetizacao < meta_alfabetizacao`) |

Quando falta a meta e o resultado ao mesmo tempo, prevalece `SEM_META`.

> Nota: `SEM_META_DISPONIVEL_PARA_COMPARACAO` existe apenas em `ft_meta_vs_resultado_municipio` e `ft_meta_vs_resultado_uf`; não consta em `dim_situacao_meta`.

## Pré-requisitos
* Todos os notebooks de tratamento da Silver executados (01 a 06)
* Notebook `Silver/Qualidade_dados/01_validar_qualidade_silver` executado

Não há dependência do notebook `Gold/Dimensoes/01_construir_dimensoes`: os fatos são construídos apenas a partir das tabelas Silver (e das próprias tabelas `ft_meta_*`).

## Relacionamento
* **Origens**: tabelas Silver `municipio`, `uf`, `meta_alfabetizacao_brasil`, `meta_alfabetizacao_uf`, `meta_alfabetizacao_municipio` e `alunos`
* **Dimensões relacionadas** (usadas nas análises, não na construção): `dim_tempo`, `dim_rede`, `dim_serie`, `dim_municipio`, `dim_uf` e `dim_situacao_meta`
* **Validação downstream**: notebook `Gold/Qualidade_dados/01_validar_qualidade_gold`, que cobre `ft_resultado_municipio`, `ft_meta_municipio`, `ft_meta_vs_resultado_municipio` e `ft_resultado_aluno_municipio`
