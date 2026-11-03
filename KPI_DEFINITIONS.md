# KPI Definitions and Calculation Methods

All indicators are calculated from the `events` table (joined with `assets`, `systems` and `locations`) at request time by the endpoints in `dashboard_api.py`. Nothing is hardcoded or pre-computed.

## Reference time and window

- **Reference time ("now"):** the latest event timestamp in the database (`SELECT MAX(ts) FROM events`). This keeps the dashboard meaningful whenever the data was generated.
- **Window:** `(reference - hours, reference]`, where `hours` is chosen on the dashboard (6, 12, 24 or 48).
- **System filter:** limits Total events, Critical alerts, the event trend and the equipment table to one system. KPIs that belong to a specific system are shown only when that system (or "All") is selected.

## KPIs

| # | KPI | System | Definition | Formula | Source fields |
|---|---|---|---|---|---|
| 1 | Total events | All | Events recorded in the window | `COUNT(events)` | `events.ts` |
| 2 | Critical alerts | All | Events with the highest severity | `COUNT(events WHERE severity = 'CRITICAL')` | `events.severity` |
| 3 | Network availability (%) | NETWORK | Share of time the network links were up | `100 x (1 - total_downtime_sec / (window_sec x network_assets))` | `LINK_UP.details.downtime_sec` |
| 4 | Avg bandwidth (Mbps) | NETWORK | Mean traffic; the peak is shown under it | `AVG(value)` over `BANDWIDTH_USAGE` | `events.value` |
| 5 | Access denial rate (%) | ACCESS | Denied badge attempts as a share of all attempts | `100 x DENIED / (GRANTED + DENIED)` | `ACCESS_DENIED`, `ACCESS_GRANTED` |
| 6 | Avg HVAC temperature (°C) | HVAC | Mean measured temperature; the number of high-temperature events is shown under it | `AVG(value)` over `TEMPERATURE_READING` and `HIGH_TEMPERATURE` | `events.value` |
| 7 | Camera offline incidents | CCTV | Times a camera dropped offline | `COUNT(CAMERA_OFFLINE)` | `events.event_type` |
| 8 | Active fire alarms | FIRE_ALARM | Panels currently in alarm (state at reference time, not limited to the window) | assets whose latest `SMOKE_DETECTED` / `ALARM_RESET` event is `SMOKE_DETECTED` | `events.event_type`, `events.ts` |

Notes:
- Availability counts a link outage when its `LINK_UP` (recovery) event falls inside the window. An outage still in progress shows up as an open incident in equipment health, not in availability.
- Averages are weighted by event count, so grouping by severity does not distort them.
- If a KPI has no underlying data in the window (for example no access events), it is shown as "n/a".

## Trends

Bucket size is 15 minutes for the 6-hour window and 1 hour otherwise. Empty buckets are returned as zero (counts) or null (averages).

| Chart | Calculation per bucket |
|---|---|
| Events by system | `COUNT(events)` per system |
| HVAC temperature | weighted average of temperature values |
| Bandwidth | weighted average and maximum of `BANDWIDTH_USAGE` |
| Access control | `ACCESS_GRANTED` and `ACCESS_DENIED` counts |

## Equipment health and system status

Per asset, over the selected window: total events, warnings, criticals, fault events and last-seen time.

**Fault events** are the events that indicate a device or environment problem (user behavior such as `ACCESS_DENIED` is deliberately not counted as a fault):

| System | Fault event types |
|---|---|
| HVAC | `HIGH_TEMPERATURE`, `FILTER_FAULT` |
| NETWORK | `LINK_DOWN` |
| ACCESS | `DOOR_FORCED`, `DOOR_HELD_OPEN` |
| CCTV | `CAMERA_OFFLINE` |
| FIRE_ALARM | `SMOKE_DETECTED`, `BATTERY_LOW` |

**Open incident:** the asset's latest event in a start/end pair is the start event.

| Start event | End event | Status while open |
|---|---|---|
| `LINK_DOWN` | `LINK_UP` | CRITICAL |
| `SMOKE_DETECTED` | `ALARM_RESET` | CRITICAL |
| `CAMERA_OFFLINE` | `CAMERA_ONLINE` | WARNING |

**Asset status** (evaluated at the reference time):

1. **CRITICAL / WARNING:** an open incident, as in the table above.
2. **WARNING:** otherwise, at least one fault event in the last 60 minutes.
3. **OK:** otherwise.

**System status** is the worst status among the assets of that system (CRITICAL > WARNING > OK).

The 60-minute status window is a fixed parameter (`STATUS_WINDOW_MIN` in `dashboard_api.py`).

## API endpoints

| Endpoint | Returns |
|---|---|
| `GET /dashboard/summary?hours=&system_type=` | KPIs (with definitions) and system status indicators |
| `GET /dashboard/trends?hours=&system_type=` | Time series for the charts |
| `GET /dashboard/equipment-health?hours=&system_type=` | Per-asset health table |

All three are documented in Swagger UI at `/docs` under the **Dashboard** tag.
