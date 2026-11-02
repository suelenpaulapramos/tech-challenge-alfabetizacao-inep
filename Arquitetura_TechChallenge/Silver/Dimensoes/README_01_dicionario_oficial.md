# Notebook: `01_dicionario_oficial`

## Camada
**Silver** | Dimensões | Dicionário de referência

## Localização
`Silver/Dimensoes/01_dicionario_oficial`

## Descrição
Notebook responsável pela criação da tabela de dicionário oficial de referência a partir dos dados ingeridos na camada Bronze. Esta é uma fonte complementar da Base dos Dados e não substitui as seis entidades obrigatórias do projeto.

## Origem
* **Tabela Bronze**: `workspace.bronze.dicionario_raw`

## Destino
* **Tabela Silver**: `workspace.silver.dicionario`
* **Modo**: `CREATE OR REPLACE TABLE`

## Tratamentos Realizados
* Cast de tipos: `id_tabela` (STRING), `chave` (STRING)
* `TRIM` em `nome_coluna` e `valor`
* Preservação da coluna `cobertura_temporal`

## Tabela de Destino: `workspace.silver.dicionario`

| Item | Valor |
|---|---|
| **Volume (out/2026)** | 54 linhas |
| **Modo** | `CREATE OR REPLACE TABLE` |

> Nota: esta tabela nao e validada pelo DQ Silver (nao esta na lista de tabelas validadas). E uma fonte de referencia complementar.

## Estrutura da Tabela

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id_tabela` | STRING | Identificador da tabela de referência |
| `nome_coluna` | STRING | Nome da coluna no dataset original |
| `chave` | STRING | Chave/código do valor |
| `valor` | STRING | Descrição do valor |
| `cobertura_temporal` | STRING | Período de cobertura temporal |

## Pré-requisitos
* Notebook `Bronze/Ingestão/07_ingestao_dicionario` executado
* Notebook `Bronze/Qualidade_dados/01_validar_qualidade_bronze` executado

## Relacionamento
* **Origem**: `workspace.bronze.dicionario_raw`
* **Uso no Gold**: Notebook `Gold/Dimensoes/01_construir_dimensoes` (dim_rede e dim_serie utilizam o dicionário para obter descrições)