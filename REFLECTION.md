# Reflection: what must improve before production

**Anzma Tech, Day 5 (Conversational AI). Ahmed**

## What I built and what the evidence says

The assistant answers building questions from the real database: SQL collectors build numbered facts, a local model
phrases the answer, and a validator rejects anything whose numbers, times, dates, device names or citations are not in
the facts. The end-to-end suite (20 questions, English and Arabic, both modes) passes 41/41 against the live API.

The honest picture comes from reading the answers, not the pass count:

- **Model phrasing is the weak point.** Of 18 in-scope questions, 13 answers came from the model (8 first try, 5 after
  one corrective retry) and 5 fell back to the deterministic fact list. The validator rejected 15 attempts in total.
- **The validator catches facts, not meaning.** Accepted answers still included a network described as "operating
  without issues" despite 6 critical events, `DOOR_FORCED` rendered in Arabic as "door opened", a fault list that
  skipped the top network fault, and a garbled citation placement. I added a judgment-phrase guard and prompt rules
  after this run, but that only covers known phrases.
- **Data is synthetic.** Energy and temperature history come from `seed_history.py`; the 12% energy change is seeded.

## Improvements needed before production

1. **Verify meaning, not only numbers.** Check that every critical or open item in the facts is mentioned, enforce
   per-sentence citations, and use a second pass (rules or a small verifier model) to flag unsupported qualitative
   claims. Track the validator rejection rate and first-attempt acceptance rate as quality metrics.
2. **Stronger or tuned model.** A 7B local model needs two attempts or a fallback too often. Evaluate a larger or
   fine-tuned model, and constrain output with a structured format (JSON items each bound to a fact) so wording cannot
   drift from the data.
3. **Real data sources.** Ingest real energy and power meters (and use deltas for cumulative counters), and compute
   time-weighted availability for cameras and network instead of the current-state ratio.
4. **Alert lifecycle.** Alerts are not closed when an asset recovers, which inflates "open alerts" (16 critical in
   the latest run). Auto-close on recovery events and expose alert age.
5. **Conversation memory.** Each question is independent today; follow-ups such as "and yesterday?" or "which one is
   the worst?" are not understood. Keep the last intent, window and entities per session.
6. **Security and operations.** `/chat` has no authentication, authorisation, rate limiting or audit log. Add
   per-user auth, rate limits, request logging with the facts used, and secrets management.
7. **Resilience and performance.** Cache collector results for short windows, set model timeouts with a visible
   degraded mode, and add load and failure tests (Ollama down, slow database).
8. **Routing robustness.** Keyword routing is fast and predictable but brittle to unusual phrasing; add an evaluation
   set of real operator questions and measure intent accuracy, with the model classifier as a measured fallback.
9. **Freshness guarantees.** Windows end at the latest recorded event. In production the answer should warn when that
   event is older than a threshold, so a stalled feed is never mistaken for a calm building.
10. **CI.** Run `tests/test_chat.py` against a seeded database on every change, and keep the results file in the repo.

## What I would tell the team

The architecture (facts first, model second, validate, fall back) is the right foundation and it fails safe. The
remaining risk is subtle wording that is numerically correct but misleading, so the next investment should be semantic
verification and a better model, not more intents.
