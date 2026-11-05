"""
tests/test_chat.py - end-to-end tests of POST /chat against the REAL running API and database.

    python tests/test_chat.py                       # deterministic mode (use_llm=false) + LLM mode
    python tests/test_chat.py --no-llm              # deterministic only (fast, no Ollama)
    python tests/test_chat.py --energy missing      # expect "not enough data" for energy (before seed_history.py)
    python tests/test_chat.py --base http://host:8000

Checks per question: expected intent, language of the answer, grounding.passed, every [F#] citation exists in
sources, data_sufficient as expected, and (for insufficient data) low confidence. Results are written to
tests/test_results.json and tests/TEST_RESULTS.md. Exit code 1 if any check fails.
"""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

HERE = Path(__file__).parent
ARABIC = re.compile(r"[\u0600-\u06FF]")
CITE = re.compile(r"\[(F\d+)\]")

# (id, question, expected intent, expected data_sufficient or None = don't care)
CASES = [
    ("Q1-en", "What is the building status right now?", "status", True),
    ("Q1-ar", "إيه حالة المبنى دلوقتي؟", "status", True),
    ("Q2-en", "What are the recent faults?", "faults", True),
    ("Q2-ar", "إيه الأعطال الأخيرة؟", "faults", True),
    ("Q3-en", "What is the CCTV camera availability?", "cameras", None),
    ("Q3-ar", "إيه حالة الكاميرات؟", "cameras", None),
    ("Q4-en", "Are there any network issues?", "network", None),
    ("Q4-ar", "في مشاكل في الشبكة؟", "network", None),
    ("Q5-en", "What should we fix first? Give me the repair priorities.", "repair", True),
    ("Q5-ar", "إيه أولويات الإصلاح؟", "repair", True),
    ("Q6-en", "How did the energy consumption change?", "energy", "ENERGY"),
    ("Q6-ar", "إيه التغير في استهلاك الطاقة؟", "energy", "ENERGY"),
    ("K1-en", "What are the building KPIs?", "kpi", None),
    ("K1-ar", "إيه مؤشرات الأداء للمبنى؟", "kpi", None),
    ("H1-en", "What was the average temperature yesterday?", "history", True),
    ("H1-ar", "إيه متوسط الحرارة امبارح؟", "history", True),
    ("H2-en", "How many times was access denied in the last 3 days?", "history", True),
    ("H2-ar", "كام مرة اتمنع حد من الدخول؟", "history", True),
    ("OOS-en", "Tell me a joke about cats", "out_of_scope", False),
    ("OOS-ar", "مين كسب الماتش امبارح؟", "out_of_scope", False),
]


def run_case(base, case, use_llm, energy_mode):
    cid, question, want_intent, want_suff = case
    if want_suff == "ENERGY":
        want_suff = energy_mode == "present"
    r = requests.post(f"{base}/chat", json={"message": question, "use_llm": use_llm}, timeout=180)
    checks = {"http_200": r.status_code == 200}
    out = {}
    if r.ok:
        out = r.json()
        answer, sources = out.get("answer", ""), out.get("sources", [])
        refs = {s["ref"] for s in sources}
        cited = set(CITE.findall(answer))
        is_ar = bool(ARABIC.search(question))
        checks["intent"] = out.get("intent") == want_intent
        checks["language"] = bool(ARABIC.search(answer)) == is_ar
        checks["answer_not_empty"] = len(answer.strip()) > 10
        checks["grounding_passed"] = bool(out.get("grounding", {}).get("passed"))
        if want_intent != "out_of_scope":
            checks["has_citations"] = bool(cited)
            checks["citations_exist"] = cited <= refs
        if want_suff is not None:
            checks["data_sufficient"] = out.get("data_sufficient") is want_suff
        if out.get("data_sufficient") is False and want_intent != "out_of_scope":
            checks["low_confidence_when_insufficient"] = out.get("confidence") == "low"
        if want_intent == "cameras" and out.get("data_sufficient") is not None:
            checks["camera_availability_pct"] = any("availability" in s.get("data", {}) for s in sources)
        if want_intent == "energy" and want_suff is False:
            checks["admits_missing_data"] = any(s.get("data", {}).get("rows") == 0 for s in sources)
    return {"id": cid, "mode": "llm" if use_llm else "deterministic", "question": question,
            "intent": out.get("intent"), "source": out.get("source"), "data_sufficient": out.get("data_sufficient"),
            "confidence": out.get("confidence"), "answer": out.get("answer"),
            "grounding": out.get("grounding"), "checks": checks, "passed": all(checks.values())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://127.0.0.1:8000")
    ap.add_argument("--no-llm", action="store_true", help="skip the Ollama run")
    ap.add_argument("--energy", choices=["present", "missing"], default="present",
                    help="'present' after seed_history.py, 'missing' to verify the honest 'no data' answer")
    a = ap.parse_args()

    results = []
    q = requests.get(f"{a.base}/chat/questions", timeout=30).json()
    results.append({"id": "meta-questions", "mode": "-", "question": "GET /chat/questions",
                    "checks": {"six_mandatory": len(q.get("questions", [])) == 6}, "passed": len(q.get("questions", [])) == 6})
    for use_llm in ([False] if a.no_llm else [False, True]):
        for case in CASES:
            try:
                res = run_case(a.base, case, use_llm, a.energy)
            except Exception as exc:  # connection error, timeout...
                res = {"id": case[0], "mode": "llm" if use_llm else "deterministic", "question": case[1],
                       "checks": {"request": False}, "passed": False, "error": f"{type(exc).__name__}: {exc}"}
            results.append(res)
            print(("PASS" if res["passed"] else "FAIL"), res["mode"][:5].ljust(5), res["id"].ljust(7),
                  res.get("source") or "-", [k for k, v in res["checks"].items() if not v] or "")

    total, ok = len(results), sum(r["passed"] for r in results)
    llm_runs = [r for r in results if r["mode"] == "llm" and r.get("source")]
    fallbacks = sum(r["source"] == "FALLBACK" for r in llm_runs)
    ollama_ok = sum(r["source"] == "OLLAMA" for r in llm_runs)
    rules = sum(r["source"] == "RULES" for r in llm_runs)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    (HERE / "test_results.json").write_text(json.dumps(
        {"run_at": stamp, "base": a.base, "energy_expected": a.energy, "passed": ok, "total": total, "results": results},
        ensure_ascii=False, indent=2, default=str), encoding="utf-8")

    md = [f"# Test results ({stamp})", "", f"**{ok}/{total} passed** against `{a.base}` (energy expected: {a.energy}).", ""]
    if llm_runs:
        md += [f"LLM mode: {ollama_ok} answers accepted from Ollama, {fallbacks} fell back to the deterministic answer, "
               f"{rules} out-of-scope replies (rules). Acceptance rate on in-scope questions: {ollama_ok}/{ollama_ok + fallbacks}.", ""]
    md += ["| Mode | ID | Intent | Source | Sufficient | Result | Failed checks |", "|---|---|---|---|---|---|---|"]
    for r in results:
        failed = ", ".join(k for k, v in r["checks"].items() if not v) or "-"
        md.append(f"| {r['mode']} | {r['id']} | {r.get('intent') or '-'} | {r.get('source') or '-'} | "
                  f"{r.get('data_sufficient')} | {'PASS' if r['passed'] else 'FAIL'} | {failed} |")
    md += ["", "## Sample answers (deterministic mode)", ""]
    for r in results:
        if r["mode"] == "deterministic" and r.get("answer"):
            md += [f"**{r['id']}** - {r['question']}", "", "```", r["answer"], "```", ""]
    (HERE / "TEST_RESULTS.md").write_text("\n".join(md), encoding="utf-8")
    print(f"\n{ok}/{total} passed. Wrote tests/test_results.json and tests/TEST_RESULTS.md")
    sys.exit(0 if ok == total else 1)


if __name__ == "__main__":
    main()