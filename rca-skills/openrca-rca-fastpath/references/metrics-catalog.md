# Metrics Catalog

## App Metrics (`__name__=~"app_.*"`)

`tc` in domain language maps to Prometheus label `service`.

| Metric | Full Name | Meaning | Unit | Better Direction | Required Label |
|---|---|---|---|---|---|
| `app_rr` | Response Rate | 回應率 | `%` | higher | `service` |
| `app_sr` | Success Rate | 成功率 | `%` | higher | `service` |
| `app_cnt` | Count | 請求數量 | count | context-dependent | `service` |
| `app_mrt` | Mean Response Time | 平均回應時間 | ms | lower | `service` |

## MG02 JVM Metrics (OOM Heap candidate)

1. `JVM_Memory_7779_JVM_Memory_HeapMemoryUsage`
2. `JVM_Memory_7779_JVM_Memory_HeapMemoryUsed`
3. `JVM_Memory_7779_JVM_Memory_HeapMemoryMax`
4. `JVM_Operating_System_7779_JVM_JVM_CPULoad`
5. `JVM_Threads_7779_JVM_ThreadCount_Threads`
6. `JVM_Runtime_7779_JVM_JVM_Uptime`

## Tomcat03 Disk Metrics (high disk I/O candidate)

Primary device in current dataset: `sdb`

1. `OSLinux_OSLinux_LOCALDISK_LOCALDISK_sdb_DSKRead`
2. `OSLinux_OSLinux_LOCALDISK_LOCALDISK_sdb_DSKReadWrite`
3. `OSLinux_OSLinux_LOCALDISK_LOCALDISK_sdb_DSKWrite`
4. `OSLinux_OSLinux_LOCALDISK_LOCALDISK_sdb_DSKTps`
5. `OSLinux_OSLinux_LOCALDISK_LOCALDISK_sdb_DSKPercentBusy`

## Cross-check Metrics (counter evidence)

1. Network error/loss:
- `OSLinux_OSLinux_NETWORK_ens160_NETInErr`
- `OSLinux_OSLinux_NETWORK_ens160_NETOutErr`

2. DB state/limit:
- `Mysql_MySQL_3306_GetConnectedStateOfMysqld`
- `Mysql_MySQL_3306_Max_Used_Connections`
- `Mysql_MySQL_3306_MaxConnections`
