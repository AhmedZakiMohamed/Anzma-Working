"""
alerts_api.py
REST endpoints for the alert engine and AI explanations.
"""
from collections import Counter
from datetime import datetime, timedelta
from typing import Literal, Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from psycopg2.extras import Json

import ai_explainer
import alert_config as cfg
import alert_engine

SystemType = Literal["HVAC", "NETWORK", "ACCESS", "CCTV", "FIRE_ALARM"]
Severity = Literal["INFO", "WARNING", "CRITICAL"]
Method = Literal["THRESHOLD", "ANOMALY", "COMPOUND"]

ALERT_SELECT = """
    SELECT al.id, al.rule_id, al.detection_method, al.severity, al.title, al.summary,
           al.first_ts, al.last_ts, al.detected_ts, al.status, al.explanation_source,
           a.id AS asset_id, a.name AS asset_name, s.type AS system_type, l.zone
    FROM alerts al
    JOIN assets a    ON a.id = al.asset_id
    JOIN systems s   ON s.id = a.system_id
    JOIN locations l ON l.id = a.location_id
"""


def create_alerts_router(db, push_alert=None):
    router = APIRouter(prefix="/alerts", tags=["Alerts"])

    def fetch_alert(cur, alert_id):
        cur.execute(ALERT_SELECT.replace("al.explanation_source,", "al.explanation_source, al.evidence, "
                                         "al.explanation, al.explained_at,") + " WHERE al.id = %s", (alert_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(404, "alert not found")
        return row

    @router.post("/run", summary="Run the alert engine over a time window")
    async def run_engine(hours: int = Query(24, ge=1, le=168)):
        """Evaluates all rules and the anomaly detector. The window ends at the latest event
        timestamp. Alerts already stored for the window are replaced. Only alerts that were
        not present before the run are pushed to connected clients."""
        with db() as cur:
            cur.execute("SELECT MAX(ts) AS m FROM events")
            end = cur.fetchone()["m"]
            if end is None:
                raise HTTPException(404, "no events in the database")
            start = end - timedelta(hours=hours)

            cur.execute("SELECT rule_id, asset_id, first_ts FROM alerts "
                        "WHERE first_ts > %s AND first_ts <= %s", (start, end))
            before = {(r["rule_id"], r["asset_id"], r["first_ts"]) for r in cur.fetchall()}

            alerts = alert_engine.run_engine(cur, start, end)
            alert_engine.store_alerts(cur, alerts, start, end)

            cur.execute(ALERT_SELECT + " WHERE al.first_ts > %s AND al.first_ts <= %s "
                        "ORDER BY al.first_ts, al.id", (start, end))
            stored = cur.fetchall()

        new = [a for a in stored if (a["rule_id"], a["asset_id"], a["first_ts"]) not in before]
        if push_alert:
            for a in new:
                await push_alert(jsonable_encoder(a))

        return {"window": {"from": start, "to": end, "hours": hours},
                "alerts_created": len(alerts), "pushed": len(new),
                "by_severity": dict(Counter(a["severity"] for a in alerts)),
                "by_rule": dict(Counter(a["rule_id"] for a in alerts)),
                "by_method": dict(Counter(a["detection_method"] for a in alerts))}

    @router.get("", summary="List alerts")
    def list_alerts(
        severity: Optional[Severity] = None,
        asset_id: Optional[int] = None,
        system_type: Optional[SystemType] = None,
        rule_id: Optional[str] = None,
        method: Optional[Method] = None,
        ts_from: Optional[datetime] = Query(None, alias="from"),
        ts_to: Optional[datetime] = Query(None, alias="to"),
        limit: int = Query(100, ge=1, le=500),
        offset: int = Query(0, ge=0),
    ):
        where, params = [], []
        for cond, val in [("al.severity = %s", severity), ("a.id = %s", asset_id), ("s.type = %s", system_type),
                          ("al.rule_id = %s", rule_id), ("al.detection_method = %s", method),
                          ("al.first_ts >= %s", ts_from), ("al.first_ts <= %s", ts_to)]:
            if val is not None:
                where.append(cond)
                params.append(val)
        w = (" WHERE " + " AND ".join(where)) if where else ""
        with db() as cur:
            cur.execute("SELECT COUNT(*) AS n FROM alerts al JOIN assets a ON a.id = al.asset_id "
                        "JOIN systems s ON s.id = a.system_id" + w, params)
            total = cur.fetchone()["n"]
            cur.execute(ALERT_SELECT + w + " ORDER BY al.first_ts DESC, al.id LIMIT %s OFFSET %s",
                        params + [limit, offset])
            items = cur.fetchall()
        return {"total": total, "limit": limit, "offset": offset, "items": items}

    @router.get("/{alert_id}", summary="Alert with evidence, explanation and recommendations")
    def get_alert(alert_id: int):
        with db() as cur:
            return fetch_alert(cur, alert_id)

    @router.get("/{alert_id}/explain", summary="Get stored explanation for an alert")
    def get_alert_explanation(alert_id: int):
        with db() as cur:
            row = fetch_alert(cur, alert_id)   # بترمي 404 لو مش موجود

        val = row.get("explanation")
        if isinstance(val, dict):
            text = val.get("explanation") or val.get("text") or str(val)
        else:
            text = val or row.get("summary") or f"Alert {alert_id} details and telemetry review."
        return {"explanation": text, "source": row.get("explanation_source")}

    @router.post("/{alert_id}/explain", summary="Generate the AI explanation for an alert")
    def explain_alert(alert_id: int, use_llm: bool = True):
        """Uses the local Ollama model when use_llm is true. The answer is validated against the
        alert's evidence; if the model is unavailable or fails validation, a deterministic
        explanation built from the same evidence and playbook is stored instead."""
        with db() as cur:
            row = fetch_alert(cur, alert_id)
            asset = {"name": row["asset_name"], "system_type": row["system_type"], "zone": row["zone"]}
            result = ai_explainer.explain(row, asset, use_llm=use_llm)
            cur.execute("UPDATE alerts SET explanation = %s, explanation_source = %s, explained_at = now() "
                        "WHERE id = %s", (Json(result), result["source"], alert_id))
            row = fetch_alert(cur, alert_id)
        return row

    return router