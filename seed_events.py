import requests
from datetime import datetime, timedelta, timezone

BASE = "http://127.0.0.1:8000"
now = datetime.now(timezone.utc) - timedelta(minutes=2)      # لازم ما يبقاش مستقبل
T = lambda mins_ago: (now - timedelta(minutes=mins_ago)).isoformat()

assets = requests.get(f"{BASE}/assets").json()
by_sys = {}
for a in assets:
    by_sys.setdefault(a["system_type"], []).append(a["name"])
pick = lambda s, i=0: by_sys[s][min(i, len(by_sys[s]) - 1)]

HVAC, NET, ACC, CAM, FIRE = (pick(s) for s in ["HVAC", "NETWORK", "ACCESS", "CCTV", "FIRE_ALARM"])
ev = []
def add(asset, mins_ago, etype, sev="INFO", value=None, unit=None, **details):
    ev.append({"asset_name": asset, "ts": T(mins_ago), "event_type": etype,
               "severity": sev, "value": value, "unit": unit, "details": details})

# ---- HVAC: ارتفاع تدريجي ثم HIGH_TEMP + فلتر ----
for i, t in enumerate([23, 24, 25.5, 27, 29, 31]):
    add(HVAC, 55 - i * 5, "TEMPERATURE_READING", "INFO", t, "C")
add(HVAC, 20, "HIGH_TEMPERATURE", "CRITICAL", 34.5, "C")
add(HVAC, 18, "HIGH_TEMPERATURE", "CRITICAL", 36.0, "C")
add(HVAC, 15, "FILTER_FAULT", "WARNING", None, None, pressure_drop_pa=310)

# ---- NETWORK: bandwidth عالي + packet loss + link down + flapping ----
for i in range(4):
    add(NET, 50 - i * 3, "BANDWIDTH_USAGE", "WARNING", 940 + i * 10, "Mbps")
add(NET, 45, "PACKET_LOSS", "WARNING", 7.5, "%")
add(NET, 44, "PACKET_LOSS", "WARNING", 9.2, "%")
add(NET, 40, "LINK_DOWN", "CRITICAL")
add(NET, 38, "LINK_UP", "INFO", None, None, downtime_sec=120)
for i in range(4):                                            # flapping
    add(NET, 30 - i * 4, "LINK_DOWN", "WARNING")
    add(NET, 29 - i * 4, "LINK_UP", "INFO", None, None, downtime_sec=45)

# ---- ACCESS: brute force + door forced + door held open ----
for i in range(8):
    add(ACC, 35 - i, "ACCESS_DENIED", "WARNING", None, None, badge=f"B-{900+i}")
add(ACC, 25, "ACCESS_GRANTED", "INFO", None, None, badge="B-100")
add(ACC, 22, "DOOR_FORCED", "CRITICAL")
add(ACC, 18, "DOOR_HELD_OPEN", "WARNING", 240, "s")

# ---- CCTV: كاميرا offline + نشاط باب أثناءها (compound) ----
add(CAM, 40, "CAMERA_OFFLINE", "WARNING")
add(ACC, 28, "DOOR_HELD_OPEN", "WARNING", 300, "s")
add(CAM, 10, "CAMERA_ONLINE", "INFO")
add(CAM, 33, "MOTION_DETECTED", "INFO", 12, "events")

# ---- FIRE: بطارية + دخان + reset ----
add(FIRE, 50, "PANEL_HEARTBEAT", "INFO", None, None, battery_pct=35, mains_ok=False)
add(FIRE, 45, "PANEL_HEARTBEAT", "WARNING", None, None, battery_pct=18, mains_ok=False)
add(FIRE, 40, "BATTERY_LOW", "WARNING", 12, "%", battery_pct=12, mains_ok=False)
add(FIRE, 12, "SMOKE_DETECTED", "CRITICAL", None, None, detector="SD-31")
add(FIRE, 8, "ALARM_RESET", "INFO")

r = requests.post(f"{BASE}/ingest", json={"events": ev})
print(r.status_code, r.text[:400])
if r.ok:
    print(requests.post(f"{BASE}/alerts/run?hours=24").json())