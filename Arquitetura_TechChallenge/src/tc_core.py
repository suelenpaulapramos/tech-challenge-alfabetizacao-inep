"""Funções de transformação testáveis do pipeline (sem dependência de Databricks).

Usadas pelo notebook de streaming e cobertas por tests/test_tc_core.py.
"""
from pyspark.sql import Column, functions as F

# Estados de situação da meta. Ausência de meta NÃO é "abaixo da meta".
ATINGIU = "ATINGIU_OU_SUPEROU"
ABAIXO = "ABAIXO_DA_META"
SEM_META = "SEM_META"
SEM_RESULTADO = "SEM_RESULTADO"
SEM_COMPARACAO = "SEM_META_DISPONIVEL_PARA_COMPARACAO"


def situacao_meta(taxa: Column, meta: Column) -> Column:
    """Classifica resultado x meta com terceiro estado para meta ausente.

    Ordem importa: comparar com NULL é falso, então o NULL precisa ser tratado antes.
    """
    return (
        F.when(taxa.isNull(), F.lit(SEM_RESULTADO))
        .when(meta.isNull(), F.lit(SEM_META))
        .when(taxa >= meta, F.lit(ATINGIU))
        .otherwise(F.lit(ABAIXO))
    )


def motivo_invalido(taxa: Column, sigla_uf: Column, rede_codigo: Column, event_id: Column,
                    ufs_validas, redes_validas) -> Column:
    """Retorna o motivo de rejeição do evento, ou NULL se o evento é válido.

    Código de rede/UF desconhecido é rejeitado de forma explícita (sem fallback silencioso).
    """
    return (
        F.when(event_id.isNull(), F.lit("event_id nulo"))
        .when(taxa.isNull(), F.lit("taxa_alfabetizacao nula"))
        .when(taxa < 0, F.lit("taxa_alfabetizacao negativa"))
        .when(taxa > 100, F.lit("taxa_alfabetizacao > 100"))
        .when(sigla_uf.isNull(), F.lit("sigla_uf nula"))
        .when(~sigla_uf.isin(list(ufs_validas)), F.lit("sigla_uf desconhecida"))
        .when(rede_codigo.isNull() | ~rede_codigo.isin(list(redes_validas)),
              F.lit("rede_codigo desconhecido"))
    )


def latencia_segundos(event_time: Column, processing_time: Column) -> Column:
    """Latência real em segundos com fração (cast para double preserva micros).

    NÃO usar unix_timestamp(): ele trunca para segundos inteiros.
    """
    return processing_time.cast("double") - event_time.cast("double")


def taxa_correspondencia(total: int, sem_par: int, limiar: float = 95.0):
    """Retorna (taxa_pct, aprovado). Tabela vazia reprova (não há o que comparar)."""
    if total <= 0:
        return 0.0, False
    taxa = (total - sem_par) / total * 100.0
    return taxa, taxa >= limiar


def taxa_alfabetizacao_ponderada(df, col_alfabetizado="alfabetizado", col_peso="peso_aluno",
                                 col_avaliado="avaliado", grupo=None):
    """Taxa = soma(peso dos alfabetizados) / soma(peso dos AVALIADOS).

    Denominador é só o universo avaliado (não o total de registros). Linhas sem peso
    ou sem resultado ficam fora tanto do numerador quanto do denominador.
    `col_alfabetizado` deve ser booleano (True/False/NULL).
    """
    valido = F.col(col_avaliado) & F.col(col_alfabetizado).isNotNull() & F.col(col_peso).isNotNull()
    num = F.sum(F.when(valido & F.col(col_alfabetizado), F.col(col_peso)).otherwise(0.0))
    den = F.sum(F.when(valido, F.col(col_peso)).otherwise(0.0))
    agg = (df.groupBy(*grupo) if grupo else df.groupBy()).agg(
        (F.when(den > 0, num / den * 100.0)).alias("taxa_recalculada_pct"),
        den.alias("peso_avaliados"),
        F.sum(F.when(valido, 1).otherwise(0)).alias("n_avaliados"),
    )
    return agg
