-- Consultas para SQL Alerts do Databricks (criar uma por bloco; condição: "linhas > 0").

-- 1) Falha bloqueante de DQ na última execução de cada camada
SELECT layer, table_name, rule_name, failed_rows, checked_at
FROM workspace.monitoring.qualidade_resultados q
WHERE severity = 'BLOQUEANTE' AND status = 'FALHOU'
  AND layer NOT LIKE '%DEMO'
  AND checked_at = (SELECT MAX(checked_at) FROM workspace.monitoring.qualidade_resultados WHERE layer = q.layer);

-- 2) Etapa do pipeline com FALHA nas últimas 24 h
SELECT layer, entity, started_at, error_message
FROM workspace.monitoring.pipeline_runs
WHERE status = 'FALHA' AND layer NOT LIKE '%DEMO' AND started_at >= current_timestamp() - INTERVAL 24 HOURS;

-- 3) Variação de volume > 20% vs. execução anterior, por camada E entidade (partição correta)
WITH r AS (
  SELECT layer, entity, started_at, row_count,
         LAG(row_count) OVER (PARTITION BY layer, entity ORDER BY started_at) AS anterior
  FROM workspace.monitoring.pipeline_runs
  WHERE status = 'SUCESSO' AND row_count IS NOT NULL),
u AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY layer, entity ORDER BY started_at DESC) rn FROM r)
SELECT layer, entity, anterior, row_count, ROUND(100.0*(row_count-anterior)/anterior, 1) AS variacao_pct
FROM u WHERE rn = 1 AND anterior > 0 AND ABS(row_count-anterior)/anterior > 0.20;

-- 4) SLA: etapa mais lenta que 2x a mediana histórica
WITH h AS (SELECT layer, entity, percentile_approx(duration_seconds, 0.5) AS mediana
           FROM workspace.monitoring.pipeline_runs WHERE status = 'SUCESSO' GROUP BY layer, entity)
SELECT r.layer, r.entity, r.duration_seconds, h.mediana
FROM workspace.monitoring.pipeline_runs r JOIN h USING (layer, entity)
WHERE r.started_at >= current_timestamp() - INTERVAL 24 HOURS AND r.duration_seconds > 2*h.mediana AND h.mediana > 0;

-- 5) Streaming: latência média do último ciclo acima do limite (ajuste o limite; coluna conforme streaming_runs)
SELECT * FROM workspace.monitoring.streaming_runs
WHERE status = 'FALHA'
   OR (status = 'SUCESSO' AND avg_latency_seconds > 30)
ORDER BY started_at DESC LIMIT 5;
