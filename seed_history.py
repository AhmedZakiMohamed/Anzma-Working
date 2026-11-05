"""
seed_history.py - backfills 7 days of hourly temperature + energy readings so the chat can answer
"average temperature yesterday" and "energy consumption change". Run it AFTER your live seed script.
Only INFO readings are added (no faults), so the other answers do not change.
"""
import math
import random
import requests
from datetime import datetime, timedelta, timezone

BASE = "http://127.0.0.1:8000"
random.seed(7)
now = (datetime.now(timezone.utc) - timedelta(hours=2)).replace(minute=0, second=0, microsecond=0)

assets = requests.get(f"{BASE}/assets").json()
by_sys = {}
for a in assets:
    by_sys.setdefault(a["system_type"], []).append(a["name"])
HVAC = by_sys["HVAC"][0]
METER = (by_sys.get("ENERGY") or by_sys.get("POWER") or [HVAC])[0]   # falls back to the HVAC asset

ev = []
for h in range(7 * 24, 2, -1):                                   # hourly, oldest first
    ts = now - timedelta(hours=h)
    hour = ts.hour
    temp = 23 + 3.5 * math.sin((hour - 9) / 24 * 2 * math.pi) + random.uniform(-0.4, 0.4)
    ev.append({"asset_name": HVAC, "ts": ts.isoformat(), "event_type": "TEMPERATURE_READING",
               "severity": "INFO", "value": round(temp, 1), "unit": "C", "details": {}})
    base = 38 + 14 * max(0.0, math.sin((hour - 6) / 24 * 2 * math.pi))       # day/night load curve
    kwh = base * (1.12 if h <= 72 else 1.0) + random.uniform(-1.5, 1.5)       # last 72 h are ~12% higher
    ev.append({"asset_name": METER, "ts": ts.isoformat(), "event_type": "ENERGY_READING",
               "severity": "INFO", "value": round(kwh, 1), "unit": "kWh", "details": {}})

r = requests.post(f"{BASE}/ingest", json={"events": ev})
print(r.status_code, r.text[:400])
