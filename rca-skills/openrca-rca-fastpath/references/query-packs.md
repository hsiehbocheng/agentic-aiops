# Query Packs

## Usage

1. Replace `<COMPONENT>` and `<WINDOW>` before execution.
2. Use range queries for timeline, instant queries for summary.
3. Always include at least one counter-evidence pack.

---

## Pack: `jvm_oom_heap`

Target example: `MG02`

Evidence queries:

1. `JVM_Memory_7779_JVM_Memory_HeapMemoryUsage{cmdb_id="<COMPONENT>"}`
2. `JVM_Memory_7779_JVM_Memory_HeapMemoryUsed{cmdb_id="<COMPONENT>"}`
3. `JVM_Operating_System_7779_JVM_JVM_CPULoad{cmdb_id="<COMPONENT>"}`
4. `JVM_Threads_7779_JVM_ThreadCount_Threads{cmdb_id="<COMPONENT>"}`

Supporting query:

1. `resets(JVM_Runtime_7779_JVM_JVM_Uptime{cmdb_id="<COMPONENT>"}[<WINDOW>])`

Decision rule:

1. Heap usage has sharp pressure pattern (sawtooth/high oscillation).
2. JVM CPU load and/or thread count spikes versus peer component.
3. Uptime reset is optional (absence does not automatically reject OOM-like event).

---

## Pack: `high_disk_io_read_usage`

Target example: `Tomcat03`

Evidence queries:

1. `OSLinux_OSLinux_LOCALDISK_LOCALDISK_sdb_DSKRead{cmdb_id="<COMPONENT>"}`
2. `OSLinux_OSLinux_LOCALDISK_LOCALDISK_sdb_DSKReadWrite{cmdb_id="<COMPONENT>"}`
3. `OSLinux_OSLinux_LOCALDISK_LOCALDISK_sdb_DSKWrite{cmdb_id="<COMPONENT>"}`
4. `OSLinux_OSLinux_LOCALDISK_LOCALDISK_sdb_DSKTps{cmdb_id="<COMPONENT>"}`
5. `OSLinux_OSLinux_LOCALDISK_LOCALDISK_sdb_DSKPercentBusy{cmdb_id="<COMPONENT>"}`

Decision rule:

1. Do not rely on `DSKRead` only.
2. If `ReadWrite/Tps/Busy` spikes significantly versus baseline/peers, treat as disk I/O incident.
3. In this dataset, write-dominant spikes may still map to disk I/O root cause labels used by tasks.

---

## Pack: `cpu_fault`

Evidence queries:

1. `OSLinux_CPU_CPU_CPUCpuUtil{cmdb_id="<COMPONENT>"}`
2. `OSLinux_CPU_CPU_CPULoad{cmdb_id="<COMPONENT>"}`

Decision rule:

1. Sustained CPU utilization jump in incident window.
2. Peer comparison confirms outlier behavior.

---

## Pack: `network_loss_or_delay`

Evidence queries:

1. `increase(OSLinux_OSLinux_NETWORK_ens160_NETInErr{cmdb_id="<COMPONENT>"}[<WINDOW>])`
2. `increase(OSLinux_OSLinux_NETWORK_ens160_NETOutErr{cmdb_id="<COMPONENT>"}[<WINDOW>])`
3. `OSLinux_OSLinux_NETWORK_ens160_NETBandwidthUtil{cmdb_id="<COMPONENT>"}`

Decision rule:

1. Non-zero error increments or severe utilization anomalies aligned with failure window.

---

## Pack: `db_connection_limit`

Evidence queries:

1. `Mysql_MySQL_3306_Max_Used_Connections{cmdb_id="<COMPONENT>"}`
2. `Mysql_MySQL_3306_MaxConnections{cmdb_id="<COMPONENT>"}`
3. `Mysql_MySQL_3306_ThreadsConnected{cmdb_id="<COMPONENT>"}`

Summary query:

1. `max_over_time(Mysql_MySQL_3306_Max_Used_Connections{cmdb_id="<COMPONENT>"}[<WINDOW>]) / max_over_time(Mysql_MySQL_3306_MaxConnections{cmdb_id="<COMPONENT>"}[<WINDOW>])`

Decision rule:

1. Ratio near saturation and connection/thread signals align with app failure.

---

## Pack: `db_close`

Evidence query:

1. `min_over_time(Mysql_MySQL_3306_GetConnectedStateOfMysqld{cmdb_id="<COMPONENT>"}[<WINDOW>])`

Decision rule:

1. If value drops below `1` during incident window, db close candidate is strong.
