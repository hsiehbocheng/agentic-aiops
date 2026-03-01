# Output Template (zh-TW)

Use this exact structure for final RCA output.

## 結論

1. `rank`: 1
2. `root_cause_component`:
3. `root_cause_reason`:
4. `exact_time_range`:
5. `evidence`:
- metric/query:
- key values:
- time alignment:
6. `why_not_others`:
- reason A excluded by:
- reason B excluded by:

## 第二順位

1. `rank`: 2
2. `root_cause_component`:
3. `root_cause_reason`:
4. `exact_time_range`:
5. `evidence`:
- metric/query:
- key values:
- time alignment:
6. `why_not_others`:
- reason A excluded by:
- reason B excluded by:

## 附註

1. Always include both local timezone and UTC timestamp in evidence.
2. If confidence is not high, mark confidence and missing evidence explicitly.
