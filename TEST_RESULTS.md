# Test results (2026-11-05 11:05 UTC)

**41/41 passed** against `http://127.0.0.1:8000` (energy expected: present).

LLM mode: 15 answers validated from Ollama, 5 fell back to the deterministic answer.

| Mode | ID | Intent | Source | Sufficient | Result | Failed checks |
|---|---|---|---|---|---|---|
| - | meta-questions | - | - | None | PASS | - |
| deterministic | Q1-en | status | FALLBACK | True | PASS | - |
| deterministic | Q1-ar | status | FALLBACK | True | PASS | - |
| deterministic | Q2-en | faults | FALLBACK | True | PASS | - |
| deterministic | Q2-ar | faults | FALLBACK | True | PASS | - |
| deterministic | Q3-en | cameras | FALLBACK | True | PASS | - |
| deterministic | Q3-ar | cameras | FALLBACK | True | PASS | - |
| deterministic | Q4-en | network | FALLBACK | True | PASS | - |
| deterministic | Q4-ar | network | FALLBACK | True | PASS | - |
| deterministic | Q5-en | repair | FALLBACK | True | PASS | - |
| deterministic | Q5-ar | repair | FALLBACK | True | PASS | - |
| deterministic | Q6-en | energy | FALLBACK | True | PASS | - |
| deterministic | Q6-ar | energy | FALLBACK | True | PASS | - |
| deterministic | K1-en | kpi | FALLBACK | True | PASS | - |
| deterministic | K1-ar | kpi | FALLBACK | True | PASS | - |
| deterministic | H1-en | history | FALLBACK | True | PASS | - |
| deterministic | H1-ar | history | FALLBACK | True | PASS | - |
| deterministic | H2-en | history | FALLBACK | True | PASS | - |
| deterministic | H2-ar | history | FALLBACK | True | PASS | - |
| deterministic | OOS-en | out_of_scope | RULES | False | PASS | - |
| deterministic | OOS-ar | out_of_scope | RULES | False | PASS | - |
| llm | Q1-en | status | OLLAMA | True | PASS | - |
| llm | Q1-ar | status | FALLBACK | True | PASS | - |
| llm | Q2-en | faults | OLLAMA | True | PASS | - |
| llm | Q2-ar | faults | OLLAMA | True | PASS | - |
| llm | Q3-en | cameras | OLLAMA | True | PASS | - |
| llm | Q3-ar | cameras | OLLAMA | True | PASS | - |
| llm | Q4-en | network | OLLAMA | True | PASS | - |
| llm | Q4-ar | network | OLLAMA | True | PASS | - |
| llm | Q5-en | repair | OLLAMA | True | PASS | - |
| llm | Q5-ar | repair | OLLAMA | True | PASS | - |
| llm | Q6-en | energy | FALLBACK | True | PASS | - |
| llm | Q6-ar | energy | OLLAMA | True | PASS | - |
| llm | K1-en | kpi | OLLAMA | True | PASS | - |
| llm | K1-ar | kpi | OLLAMA | True | PASS | - |
| llm | H1-en | history | FALLBACK | True | PASS | - |
| llm | H1-ar | history | FALLBACK | True | PASS | - |
| llm | H2-en | history | FALLBACK | True | PASS | - |
| llm | H2-ar | history | OLLAMA | True | PASS | - |
| llm | OOS-en | out_of_scope | RULES | False | PASS | - |
| llm | OOS-ar | out_of_scope | RULES | False | PASS | - |

## Sample answers (deterministic mode)

**Q1-en** - What is the building status right now?

```
- Window: last 72 h ending 2026-11-05 06:00 UTC (latest recorded event). [F1]
- HVAC: 3 assets (2 OK, 0 WARNING, 1 CRITICAL), 1153 events of which 5 critical. [F2]
- NETWORK: 2 assets (2 OK, 0 WARNING, 0 CRITICAL), 678 events of which 6 critical. [F3]
- ACCESS: 3 assets (3 OK, 0 WARNING, 0 CRITICAL), 351 events of which 1 critical. [F4]
- CCTV: 3 assets (3 OK, 0 WARNING, 0 CRITICAL), 351 events of which 0 critical. [F5]
- FIRE_ALARM: 2 assets (1 OK, 0 WARNING, 1 CRITICAL), 69 events of which 4 critical. [F6]
- Active fire alarms right now: 1. [F7]
- FA-PANEL-02 (Meeting Rooms): CRITICAL - Smoke alarm active (open incident) since 2026-11-04 22:58 UTC. [F8]
- HVAC-AHU-01 (Open Office): CRITICAL - Smoke alarm active (open incident) since 2026-11-04 22:50 UTC. [F9]
- Open alerts: 16 critical, 8 warning, 0 info. [F10]
```

**Q1-ar** - إيه حالة المبنى دلوقتي؟

```
- النافذة الزمنية: آخر 72 ساعة حتى 2026-11-05 06:00 UTC (وقت آخر حدث مسجل). [F1]
- HVAC: 3 أصل (2 OK، 0 WARNING، 1 CRITICAL)، و1153 حدث منها 5 حرج. [F2]
- NETWORK: 2 أصل (2 OK، 0 WARNING، 0 CRITICAL)، و678 حدث منها 6 حرج. [F3]
- ACCESS: 3 أصل (3 OK، 0 WARNING، 0 CRITICAL)، و351 حدث منها 1 حرج. [F4]
- CCTV: 3 أصل (3 OK، 0 WARNING، 0 CRITICAL)، و351 حدث منها 0 حرج. [F5]
- FIRE_ALARM: 2 أصل (1 OK، 0 WARNING، 1 CRITICAL)، و69 حدث منها 4 حرج. [F6]
- إنذارات الحريق النشطة حالياً: 1. [F7]
- FA-PANEL-02 (Meeting Rooms): CRITICAL - Smoke alarm active (open incident) منذ 2026-11-04 22:58 UTC. [F8]
- HVAC-AHU-01 (Open Office): CRITICAL - Smoke alarm active (open incident) منذ 2026-11-04 22:50 UTC. [F9]
- التنبيهات المفتوحة: 16 حرجة، 8 تحذيرية، 0 معلوماتية. [F10]
```

**Q2-en** - What are the recent faults?

```
- Window: last 72 h ending 2026-11-05 06:00 UTC (latest recorded event). [F1]
- Total fault events: 27 across 12 assets. [F2]
- SW-CORE-01 (NETWORK): LINK_DOWN x 5 (5 critical), last 2026-11-03 09:30 UTC. [F3]
- HVAC-CRAC-01 (HVAC): HIGH_TEMPERATURE x 5 (3 critical), last 2026-11-02 13:30 UTC. [F4]
- FA-PANEL-02 (FIRE_ALARM): SMOKE_DETECTED x 4 (3 critical), last 2026-11-04 22:58 UTC. [F5]
- HVAC-AHU-01 (HVAC): SMOKE_DETECTED x 1 (1 critical), last 2026-11-04 22:50 UTC. [F6]
- SW-ACCESS-02 (NETWORK): LINK_DOWN x 1 (1 critical), last 2026-11-03 08:41 UTC. [F7]
- HVAC-AHU-01 (HVAC): HIGH_TEMPERATURE x 1 (1 critical), last 2026-11-03 02:52 UTC. [F8]
- DOOR-LOBBY-01 (ACCESS): DOOR_FORCED x 1 (1 critical), last 2026-11-02 15:44 UTC. [F9]
- FA-PANEL-01 (FIRE_ALARM): SMOKE_DETECTED x 1 (1 critical), last 2026-11-02 08:57 UTC. [F10]
- 7 more fault groups are not listed. [F11]
- Open incidents right now: 2 (HVAC-AHU-01, FA-PANEL-02). [F12]
- Open alerts: 16 critical, 8 warning, 0 info. [F13]
```

**Q2-ar** - إيه الأعطال الأخيرة؟

```
- النافذة الزمنية: آخر 72 ساعة حتى 2026-11-05 06:00 UTC (وقت آخر حدث مسجل). [F1]
- إجمالي أحداث الأعطال: 27 على 12 أصل. [F2]
- SW-CORE-01 (NETWORK): LINK_DOWN × 5 (منها 5 حرج)، آخرها 2026-11-03 09:30 UTC. [F3]
- HVAC-CRAC-01 (HVAC): HIGH_TEMPERATURE × 5 (منها 3 حرج)، آخرها 2026-11-02 13:30 UTC. [F4]
- FA-PANEL-02 (FIRE_ALARM): SMOKE_DETECTED × 4 (منها 3 حرج)، آخرها 2026-11-04 22:58 UTC. [F5]
- HVAC-AHU-01 (HVAC): SMOKE_DETECTED × 1 (منها 1 حرج)، آخرها 2026-11-04 22:50 UTC. [F6]
- SW-ACCESS-02 (NETWORK): LINK_DOWN × 1 (منها 1 حرج)، آخرها 2026-11-03 08:41 UTC. [F7]
- HVAC-AHU-01 (HVAC): HIGH_TEMPERATURE × 1 (منها 1 حرج)، آخرها 2026-11-03 02:52 UTC. [F8]
- DOOR-LOBBY-01 (ACCESS): DOOR_FORCED × 1 (منها 1 حرج)، آخرها 2026-11-02 15:44 UTC. [F9]
- FA-PANEL-01 (FIRE_ALARM): SMOKE_DETECTED × 1 (منها 1 حرج)، آخرها 2026-11-02 08:57 UTC. [F10]
- وفيه 7 مجموعات أعطال أخرى لم تُعرض. [F11]
- حوادث مفتوحة حالياً: 2 (HVAC-AHU-01، FA-PANEL-02). [F12]
- التنبيهات المفتوحة: 16 حرجة، 8 تحذيرية، 0 معلوماتية. [F13]
```

**Q3-en** - What is the CCTV camera availability?

```
- Window: last 72 h ending 2026-11-05 06:00 UTC (latest recorded event). [F1]
- Total cameras: 3, of which 0 are offline now. [F2]
- Current camera availability: 100.0% (3 of 3 online). [F3]
- Camera-offline incidents in the window: 4. [F4]
```

**Q3-ar** - إيه حالة الكاميرات؟

```
- النافذة الزمنية: آخر 72 ساعة حتى 2026-11-05 06:00 UTC (وقت آخر حدث مسجل). [F1]
- إجمالي الكاميرات: 3، منها 0 غير متصلة حالياً. [F2]
- توافر الكاميرات الحالي: 100.0% (3 من 3 متصلة). [F3]
- حوادث انقطاع الكاميرات في النافذة: 4. [F4]
```

**Q4-en** - Are there any network issues?

```
- Window: last 72 h ending 2026-11-05 06:00 UTC (latest recorded event). [F1]
- Network availability: 99.706% across 2 network assets, total downtime 1525 s. [F2]
- LINK_DOWN incidents in the window: 6. [F3]
- Bandwidth: average 529.5 Mbps, peak 1008.6 Mbps. [F4]
```

**Q4-ar** - في مشاكل في الشبكة؟

```
- النافذة الزمنية: آخر 72 ساعة حتى 2026-11-05 06:00 UTC (وقت آخر حدث مسجل). [F1]
- توافر الشبكة: 99.706% على 2 أصل شبكة، وإجمالي زمن الانقطاع 1525 ثانية. [F2]
- حوادث LINK_DOWN في النافذة: 6. [F3]
- استهلاك النطاق: متوسط 529.5 Mbps وذروة 1008.6 Mbps. [F4]
```

**Q5-en** - What should we fix first? Give me the repair priorities.

```
- Window: last 72 h ending 2026-11-05 06:00 UTC (latest recorded event). [F1]
- Ranking rule: open CRITICAL incident 100 points, open WARNING incident 50, each open critical alert 20, each open warning alert 8, each fault in the last 60 minutes 3 points. [F2]
- Priority 1: FA-PANEL-02 (FIRE_ALARM, Meeting Rooms) - Smoke alarm active (open incident), since 2026-11-04 22:58 UTC; 5 critical and 0 warning open alerts; score 200. [F3]
- Priority 2: HVAC-AHU-01 (HVAC, Open Office) - Smoke alarm active (open incident), since 2026-11-04 22:50 UTC; 1 critical and 0 warning open alerts; score 120. [F4]
- Priority 3: SW-CORE-01 (NETWORK, Server Room) - no recent faults; 4 critical and 0 warning open alerts; score 80. [F5]
- Priority 4: CAM-SERVER-01 (CCTV, Server Room) - no recent faults; 1 critical and 2 warning open alerts; score 36. [F6]
- Priority 5: DOOR-LOBBY-01 (ACCESS, Lobby) - no recent faults; 1 critical and 1 warning open alerts; score 28. [F7]
- 5 more assets have lower priority. [F8]
```

**Q5-ar** - إيه أولويات الإصلاح؟

```
- النافذة الزمنية: آخر 72 ساعة حتى 2026-11-05 06:00 UTC (وقت آخر حدث مسجل). [F1]
- قاعدة الترتيب: حادث مفتوح حرج 100 نقطة، حادث مفتوح تحذيري 50، كل تنبيه حرج مفتوح 20، كل تنبيه تحذيري مفتوح 8، وكل عطل في آخر 60 دقيقة 3 نقاط. [F2]
- الأولوية 1: FA-PANEL-02 (FIRE_ALARM، Meeting Rooms) - Smoke alarm active (open incident)، منذ 2026-11-04 22:58 UTC؛ 5 تنبيه حرج و0 تحذيري مفتوح؛ النقاط 200. [F3]
- الأولوية 2: HVAC-AHU-01 (HVAC، Open Office) - Smoke alarm active (open incident)، منذ 2026-11-04 22:50 UTC؛ 1 تنبيه حرج و0 تحذيري مفتوح؛ النقاط 120. [F4]
- الأولوية 3: SW-CORE-01 (NETWORK، Server Room) - no recent faults؛ 4 تنبيه حرج و0 تحذيري مفتوح؛ النقاط 80. [F5]
- الأولوية 4: CAM-SERVER-01 (CCTV، Server Room) - no recent faults؛ 1 تنبيه حرج و2 تحذيري مفتوح؛ النقاط 36. [F6]
- الأولوية 5: DOOR-LOBBY-01 (ACCESS، Lobby) - no recent faults؛ 1 تنبيه حرج و1 تحذيري مفتوح؛ النقاط 28. [F7]
- وفيه 5 أصول أخرى بأولوية أقل. [F8]
```

**Q6-en** - How did the energy consumption change?

```
- Window: last 72 h ending 2026-11-05 06:00 UTC (latest recorded event). [F1]
- HVAC-AHU-01 (ENERGY_READING): 72 readings, average 47.56 kWh, max 59.5. [F2]
- Consumption change: average reading 47.56 kWh in the current window versus 42.46 kWh in the previous window of equal length, a change of 12.0%. [F3]
```

**Q6-ar** - إيه التغير في استهلاك الطاقة؟

```
- النافذة الزمنية: آخر 72 ساعة حتى 2026-11-05 06:00 UTC (وقت آخر حدث مسجل). [F1]
- HVAC-AHU-01 (ENERGY_READING): 72 قراءة، متوسط 47.56 kWh، أقصى 59.5. [F2]
- التغيّر في الاستهلاك: متوسط القراءة 47.56 kWh في النافذة الحالية مقابل 42.46 kWh في النافذة السابقة بنفس الطول، أي تغيّر بنسبة 12.0%. [F3]
```

**K1-en** - What are the building KPIs?

```
- Window: last 72 h ending 2026-11-05 06:00 UTC (latest recorded event). [F1]
- Asset health: 84.6% healthy (11 of 13 assets OK). [F2]
- Current camera availability: 100.0% (3 of 3 online). [F3]
- Network availability: 99.706% with total downtime 1525 s. [F4]
- Fault events in the window: 27, of which 16 critical. [F5]
- Open incidents right now: 2. [F6]
- Active fire alarms right now: 1. [F7]
- Open alerts: 16 critical, 8 warning, 0 info. [F8]
```

**K1-ar** - إيه مؤشرات الأداء للمبنى؟

```
- النافذة الزمنية: آخر 72 ساعة حتى 2026-11-05 06:00 UTC (وقت آخر حدث مسجل). [F1]
- صحة الأصول: 84.6% سليمة (11 من 13 أصل بحالة OK). [F2]
- توافر الكاميرات الحالي: 100.0% (3 من 3 متصلة). [F3]
- توافر الشبكة: 99.706% وإجمالي زمن الانقطاع 1525 ثانية. [F4]
- أحداث الأعطال في النافذة: 27 منها 16 حرج. [F5]
- الحوادث المفتوحة حالياً: 2. [F6]
- إنذارات الحريق النشطة حالياً: 1. [F7]
- التنبيهات المفتوحة: 16 حرجة، 8 تحذيرية، 0 معلوماتية. [F8]
```

**H1-en** - What was the average temperature yesterday?

```
- Period: yesterday (2026-11-04) UTC, relative to the day of the latest recorded event. [F1]
- TEMPERATURE_READING: 24 readings, average 23.0 C, min 19.6, max 26.6. [F2]
- HVAC-AHU-01: average 23.0 C over 24 readings. [F3]
```

**H1-ar** - إيه متوسط الحرارة امبارح؟

```
- الفترة: امبارح (2026-11-04) بتوقيت UTC، محسوبة نسبةً ليوم آخر حدث مسجل. [F1]
- TEMPERATURE_READING: 24 قراءة، المتوسط 23.0 C، الأدنى 19.6، الأقصى 26.6. [F2]
- HVAC-AHU-01: متوسط 23.0 C على 24 قراءة. [F3]
```

**H2-en** - How many times was access denied in the last 3 days?

```
- Window: last 72 h ending 2026-11-05 06:00 UTC (latest recorded event). [F1]
- Number of ACCESS_DENIED events in the period: 63 (recorded events only). [F2]
- DOOR-SERVER-01 (ACCESS_DENIED): 23 times, last 2026-11-03 08:11 UTC. [F3]
- DOOR-EXEC-01 (ACCESS_DENIED): 22 times, last 2026-11-03 05:40 UTC. [F4]
- DOOR-LOBBY-01 (ACCESS_DENIED): 18 times, last 2026-11-03 08:36 UTC. [F5]
```

**H2-ar** - كام مرة اتمنع حد من الدخول؟

```
- النافذة الزمنية: آخر 72 ساعة حتى 2026-11-05 06:00 UTC (وقت آخر حدث مسجل). [F1]
- عدد أحداث ACCESS_DENIED في الفترة: 63 (حسب الأحداث المسجلة فقط). [F2]
- DOOR-SERVER-01 (ACCESS_DENIED): 23 مرة، آخرها 2026-11-03 08:11 UTC. [F3]
- DOOR-EXEC-01 (ACCESS_DENIED): 22 مرة، آخرها 2026-11-03 05:40 UTC. [F4]
- DOOR-LOBBY-01 (ACCESS_DENIED): 18 مرة، آخرها 2026-11-03 08:36 UTC. [F5]
```

**OOS-en** - Tell me a joke about cats

```
I can only answer about the building data: building status, faults, cameras, network, repair priorities, energy consumption, KPIs and historical readings (temperature, humidity, access events). Please ask about one of these.
```

**OOS-ar** - مين كسب الماتش امبارح؟

```
أقدر أجاوب فقط عن بيانات المبنى: حالة المبنى، الأعطال، الكاميرات، الشبكة، أولويات الإصلاح، استهلاك الطاقة، مؤشرات الأداء (KPIs)، والقراءات التاريخية (حرارة، رطوبة، محاولات الدخول). اسألني في واحد منهم.
```
