# Environment Baseline (OpenRCA)

Last verified: 2026-02-28

## Datasources

1. Prometheus (VictoriaMetrics)
- `uid`: `cfe4jhy1ca0aoe`

2. Loki
- `uid`: `afeli6qsodnggf`

3. Tempo
- `uid`: `cfe4jhy5i3x1cb`

## Prometheus Labels

Label names:

1. `__name__`
2. `cmdb_id`
3. `service`

`cmdb_id` values:

1. `IG01`, `IG02`
2. `MG01`, `MG02`
3. `Mysql01`, `Mysql02`
4. `Redis01`, `Redis02`
5. `Tomcat01`, `Tomcat02`, `Tomcat03`, `Tomcat04`
6. `apache01`, `apache02`
7. `dockerA1`, `dockerA2`, `dockerB1`, `dockerB2`

`service` values:

1. `ServiceTest1` to `ServiceTest11`

## Loki Labels

Label names:

1. `cmdb_id`
2. `job`
3. `log_name`
4. `source`

Known values:

1. `cmdb_id`: `TEST`, `Tomcat01`, `Tomcat02`, `Tomcat03`, `Tomcat04`, `apache01`, `apache02`
2. `job`: `openrca`, `openrca-test`
3. `log_name`: `apache_access_log`, `gc`, `localhost_access_log`, `test_log`
4. `source`: `log_service`, `manual`

Notes:

1. Loki currently has no `service` label.
2. For service-like grouping in logs, use `cmdb_id` and/or `job`.
