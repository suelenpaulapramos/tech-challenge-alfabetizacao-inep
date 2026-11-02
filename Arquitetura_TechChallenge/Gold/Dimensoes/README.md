# Notebook: `01_construir_dimensoes`

## Camada
**Gold** | Construção de dimensões

## Localização
`Gold/Dimensoes/01_construir_dimensoes`

## Descrição
Notebook responsável pela construção das tabelas de dimensão da camada Gold, derivadas dos dados tratados na Silver, do dicionário oficial e do arquivo oficial de diretórios de UF. As dimensões são descritivas e servem de apoio às análises (por exemplo, no modelo dimensional consumido por dashboards), relacionando-se às tabelas fato pelas chaves de negócio.

O notebook cria o schema `workspace.gold` caso ele não exista e recria todas as tabelas em formato Delta (`CREATE OR REPLACE`), portanto pode ser reexecutado com segurança.

## Tabelas Criadas

| Tabela Gold | Origem | Colunas | Descrição |
|-------------|--------|---------|-----------|
| `workspace.gold.dim_tempo` | `workspace.silver.municipio` | `ano`, `data_referencia`, `ano_calendario` | Dimensão temporal. `data_referencia` é 01/01 do `ano`; `ano_calendario` é o ano extraído dessa data. Considera apenas anos não nulos |
| `workspace.gold.dim_rede` | `workspace.silver.dicionario` | `rede_codigo`, `descricao_rede` | Dimensão de rede de ensino. Filtra `id_tabela = 'municipio'` e `nome_coluna = 'rede'`; `rede_codigo` é texto (STRING) |
| `workspace.gold.dim_serie` | `workspace.silver.dicionario` | `serie_codigo`, `serie_descricao` | Dimensão de série. Filtra `id_tabela = 'municipio'` e `nome_coluna = 'serie'`; `serie_codigo` é inteiro (INT) |
| `workspace.gold.dim_municipio` | `workspace.silver.municipio` | `id_municipio` | Dimensão de município com `id_municipio` distinto e não nulo (sem atributos descritivos) |
| `workspace.gold.dim_uf` | CSV oficial `br_bd_diretorios_brasil_uf.csv` | `id_uf`, `sigla_uf`, `nome_uf`, `regiao` | Dimensão de UF (ver detalhes abaixo) |
| `workspace.gold.dim_situacao_meta` | Valores fixos | `situacao_meta` | Domínio da classificação de meta: `ATINGIU_OU_SUPEROU`, `ABAIXO_DA_META`, `SEM_META`, `SEM_RESULTADO` |

### Detalhes da `dim_uf`
A tabela é criada em **duas etapas** dentro do notebook:

1. **Versão inicial (SQL)**: criada a partir de `workspace.silver.uf`, contendo apenas `sigla_uf` distinto.
2. **Versão final (PySpark)**: o notebook lê o arquivo oficial `/Volumes/workspace/default/my_files/tech_challenge_fase_2/br_bd_diretorios_brasil_uf.csv`, padroniza os campos (`id_uf` como INT, `sigla_uf` em maiúsculas e sem espaços, `nome_uf` e `regiao` sem espaços), remove duplicidades por `sigla_uf` e **sobrescreve** a tabela com `overwriteSchema = true`.

A versão válida para consumo é, portanto, a final (com `id_uf`, `sigla_uf`, `nome_uf` e `regiao`). Caso o CSV não esteja disponível no Volume, a leitura falha e a tabela permanece apenas com a versão inicial (somente `sigla_uf`).

## Volume e dicionário por dimensão

### `workspace.gold.dim_tempo`

| Item | Valor |
|---|---|
| **Volume (out/2026)** | 2 linhas |
| **Origem** | `workspace.silver.municipio` (anos distintos e não nulos) |

| Coluna | Tipo | Descrição |
|---|---|---|
| `ano` | INT | Ano de referência |
| `data_referencia` | DATE | Data de referência (01/01 do ano) |
| `ano_calendario` | INT | Ano extraído de `data_referencia` |

### `workspace.gold.dim_rede`

| Item | Valor |
|---|---|
| **Volume (out/2026)** | 7 linhas |
| **Origem** | `workspace.silver.dicionario` (filtro: `id_tabela = 'municipio'` e `nome_coluna = 'rede'`) |

| Coluna | Tipo | Descrição |
|---|---|---|
| `rede_codigo` | STRING | Código da rede de ensino |
| `descricao_rede` | STRING | Descrição/ nome da rede |

### `workspace.gold.dim_serie`

| Item | Valor |
|---|---|
| **Volume (out/2026)** | 1 linha |
| **Origem** | `workspace.silver.dicionario` (filtro: `id_tabela = 'municipio'` e `nome_coluna = 'serie'`) |

| Coluna | Tipo | Descrição |
|---|---|---|
| `serie_codigo` | INT | Código da série |
| `serie_descricao` | STRING | Descrição/ nome da série |

### `workspace.gold.dim_municipio`

| Item | Valor |
|---|---|
| **Volume (out/2026)** | 5.550 linhas |
| **Origem** | `workspace.silver.municipio` (IDs distintos e não nulos) |

| Coluna | Tipo | Descrição |
|---|---|---|
| `id_municipio` | STRING | ID do município (padrão IBGE) |

> TODO: preencher — incluir nome do município e UF (join com diretório de municípios do IBGE).

### `workspace.gold.dim_uf`

| Item | Valor |
|---|---|
| **Volume (out/2026)** | 27 linhas |
| **Origem** | CSV oficial `br_bd_diretorios_brasil_uf.csv` no Volume `/Volumes/workspace/default/my_files/tech_challenge_fase_2/` |

| Coluna | Tipo | Descrição |
|---|---|---|
| `id_uf` | INT | Código IBGE da UF |
| `sigla_uf` | STRING | Sigla da unidade federativa (maiúscula, sem espaços) |
| `nome_uf` | STRING | Nome do estado |
| `regiao` | STRING | Região do Brasil (Norte, Nordeste, Sudeste, Sul, Centro-Oeste) |

### `workspace.gold.dim_situacao_meta`

| Item | Valor |
|---|---|
| **Volume (out/2026)** | 4 linhas |
| **Origem** | Valores fixos (cláusula `VALUES`) |

| Coluna | Tipo | Descrição |
|---|---|---|
| `situacao_meta` | STRING | Categoria de cumprimento da meta |

Valores possíveis:

| Valor | Descrição |
|---|---|
| `ATINGIU_OU_SUPEROU` | Taxa observada maior ou igual à meta |
| `ABAIXO_DA_META` | Taxa observada abaixo da meta |
| `SEM_META` | Meta não disponível para comparação |
| `SEM_RESULTADO` | Resultado não disponível para comparação |

## Pré-requisitos
* Todos os notebooks de tratamento da Silver executados (01 a 06)
* Notebook `Silver/Dimensoes/01_dicionario_oficial` executado (gera `workspace.silver.dicionario`)
* Notebook `Silver/Qualidade_dados/01_validar_qualidade_silver` executado
* Arquivo `br_bd_diretorios_brasil_uf.csv` disponível no Volume `/Volumes/workspace/default/my_files/tech_challenge_fase_2/`

## Relacionamento
* **Origens**: `workspace.silver.municipio`, `workspace.silver.uf`, `workspace.silver.dicionario` e o CSV oficial de UF
* **Relação com os fatos**: as dimensões não são lidas pelo notebook `Gold/Fato/01_construir_fatos`; os dois notebooks são independentes entre si e podem ser executados em qualquer ordem. A ligação entre dimensões e fatos ocorre nas consultas e modelos analíticos, por meio de `ano`, `id_municipio`, `sigla_uf`, `rede_codigo` e `serie`
* **Validação**: as dimensões **não** são cobertas pelo notebook `Gold/Qualidade_dados/01_validar_qualidade_gold`, que valida somente tabelas fato
