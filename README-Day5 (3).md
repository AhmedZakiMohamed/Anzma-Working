# Building Assistant: Data-Grounded Conversational AI

**Anzma Tech Smart Inspection Systems, Day 5: Conversational AI & Individual Demonstration**

A natural-language interface for the building operations database. Operators ask questions in English or Arabic
("What is the camera status?", "إيه متوسط الحرارة امبارح؟") and receive an answer built **only from facts read from the
real database**. A local LLM (Ollama) phrases the answer; a validator then checks every number, time, date, device
name and citation against those facts. If the model is unavailable or fails validation, the assistant falls back to a
deterministic answer made of the facts themselves. When the data cannot answer a question, the assistant says so
instead of guessing.

---

## Highlights

| Requirement | How it is met |
|---|---|
| Complete individual application | `POST /chat` API + floating chat widget embedded in the dashboard + standalone `chat.html` page |
| Data-grounded conversational AI | SQL collectors produce numbered facts (`F1`, `F2`, ...); the LLM may only use those facts |
| Six mandatory questions | Building status, recent faults, CCTV availability, network issues, repair priorities, energy change |
| KPIs and historical readings | Dedicated `kpi` and `history` intents (availability %, asset health, average temperature, access-denied counts) |
| Acknowledge insufficient data | `data_sufficient: false`, low confidence, and an explicit statement of what is missing |
| Bilingual | Arabic and English questions; the answer follows the language of the question (RTL handled in the UI) |
| Verifiable | Every answer carries `[F#]` citations, an evidence panel, and grounding results |
| Tested | 20 end-to-end questions against the real API and database, results saved in the repo |

---

## Architecture

```
 question
    |
    v
 1. classify   keywords first (AR/EN), LLM only as a fallback  -> intent
    |
    v
 2. gather     SQL collectors read the DB and write numbered FACTS (F1, F2, ...)
    |            in the user's language, plus data_sufficient true/false
    v
 3. compose    local LLM (Ollama) phrases an answer from the facts only
    |
    v
 4. validate   every number / time / date / asset name / [F#] citation
    |            must exist in the facts the answer cites
    v
 5. fallback   LLM down, or rejected twice -> the facts themselves are the answer
```

Design decisions:

- **The database does the math, the model does the wording.** All counts, percentages and averages are computed in SQL
  or Python and handed to the model as text. The model is told not to calculate.
- **Validation instead of trust.** Answers are rejected if they contain a number, time, date or device name that is not
  in the cited facts, if a citation does not exist, or if a required current-state fact is not cited. The model gets one
  retry with the exact violations; after that the deterministic fallback is returned.
- **Cheap, predictable routing.** Intent classification uses Arabic-normalised keyword matching; Ollama is called for
  classification only when no keyword matches. Questions outside the building domain return a fixed out-of-scope reply
  without touching the database.
- **Connection hygiene.** The database cursor is released before any LLM call.
- **Honest coverage checks.** If a system (e.g. CCTV or NETWORK) sent no events in the window, a caveat fact is added
  and `data_sufficient` becomes `false`, because the absence of incidents does not prove the devices are healthy.

---

## Supported questions (intents)

| Intent | Example (EN) | Example (AR) | What it answers from |
|---|---|---|---|
| `status` | What is the building status right now? | إيه حالة المبنى دلوقتي؟ | Asset health per system, active fire alarms, open incidents, open alerts |
| `faults` | What are the recent faults? | إيه الأعطال الأخيرة؟ | Fault events grouped by asset and type, open incidents, alerts |
| `cameras` | What is the CCTV camera availability? | إيه حالة الكاميرات؟ | Cameras online/offline, **availability %**, offline incidents |
| `network` | Are there any network issues? | في مشاكل في الشبكة؟ | Network availability %, downtime, `LINK_DOWN` incidents, bandwidth |
| `repair` | What should we fix first? | إيه أولويات الإصلاح؟ | Ranked assets with a transparent scoring rule |
| `energy` | How did the energy consumption change? | إيه التغير في استهلاك الطاقة؟ | Energy readings, change versus the previous window of equal length |
| `kpi` | What are the building KPIs? | إيه مؤشرات الأداء للمبنى؟ | Asset health %, camera and network availability, fault counts, open incidents |
| `history` | What was the average temperature yesterday? | إيه متوسط الحرارة امبارح؟ | Historical readings (temperature, humidity, bandwidth) and event counts (access denied, door events) |
| `out_of_scope` | Tell me a joke | مين كسب الماتش امبارح؟ | Fixed reply listing what the assistant can answer |

Time windows: the default is the last 72 hours, ending at the **latest recorded event** (not the wall clock). The
question can override it ("last 12 hours", "past week", "اخر 3 ايام"), and so can the `hours` field of the API
(1 to 168). "Yesterday" / "امبارح" means the previous full UTC day relative to the latest event.

Repair-priority scoring: open CRITICAL incident 100 points, open WARNING incident 50, each open critical alert 20, each
open warning alert 8, each fault in the last 60 minutes 3 points. The rule is itself returned as a fact so the answer
can explain the ranking.

---

## API

### `POST /chat`

```json
{ "message": "What is the camera status?", "hours": 72, "use_llm": true }
```

| Field | Type | Notes |
|---|---|---|
| `message` | string, 2 to 500 chars | Required. English or Arabic |
| `hours` | int, 1 to 168 | Optional. Default: parsed from the question, otherwise 72 |
| `use_llm` | bool | `false` returns the deterministic answer only (no Ollama call) |

Response (abridged):

```json
{
  "intent": "cameras",
  "language": "en",
  "answer": "- Total cameras: 3, of which 0 are offline now. [F2]\n- Current camera availability: 100.0% (3 of 3 online). [F3]",
  "source": "OLLAMA",
  "model": "<model name>",
  "data_sufficient": true,
  "confidence": "high",
  "window": { "from": "...", "to": "...", "hours": 72 },
  "sources": [ { "ref": "F1", "text": "Window: ...", "data": { } } ],
  "grounding": { "passed": true, "violations": [], "attempts": 1, "rejected_answers": [] }
}
```

- `source`: `OLLAMA` (validated model answer), `FALLBACK` (deterministic facts), `RULES` (out-of-scope reply).
- `grounding.rejected_answers` records why a model answer was rejected, which is useful for debugging and evaluation.
- `404` is returned if the database has no events at all.

### `GET /chat/questions`

Returns `questions` (the six mandatory questions, used as UI buttons), `extra` (KPI and history examples) and the list
of `intents`.

---

## Chat widget

`chat-widget.js` and `chat-widget.css` add a floating assistant to the dashboard with one line before `</body>`:

```html
<script src="/static/chat-widget.js" defer></script>
```

The widget loads its own stylesheet and follows the dashboard's light/dark CSS variables. Features:

- Suggested-question chips loaded from `/chat/questions`
- Clickable `[F#]` citation chips that open and highlight the supporting evidence
- Trust indicators: "Verified against data", "AI answer" / "Data summary", "Limited data", window and confidence
- Validation notes (rejected model attempts) inside the evidence panel
- Time-window selector, RTL layout for Arabic answers, keyboard support (Enter to send, Esc to close), retry on error
- Conversation kept in `sessionStorage` for the browser session only

`chat.html` is a minimal standalone page with the same API calls, handy for demos and debugging.

---

## Installation

### Prerequisites

- Python 3.10+
- PostgreSQL with the project schema (`events`, `assets`, `systems`, `locations`, `alerts`)
- [Ollama](https://ollama.com) running locally with the model configured in `ai_explainer.py` (`OLLAMA_MODEL`)
- Python packages: `fastapi`, `uvicorn[standard]`, `pydantic`, `psycopg2-binary`, `python-dotenv`, `python-socketio`

### Wire the router into the API

`chat_api.py` exposes `create_chat_router(db)`, where `db` is the same connection-context helper used by the other
routers. In the main app:

```python
from chat_api import create_chat_router
app.include_router(create_chat_router(db))
```

Place `chat_engine.py` and `chat_api.py` next to `dashboard_api.py` and `ai_explainer.py`; the engine imports the shared
status logic and fault definitions from them. Serve the widget files from the static directory.

### Run

```bash
ollama serve                              # in one terminal
uvicorn App:asgi_app --reload --port 8000     # in another (use your app's module name)
```

Open the dashboard (widget) or `/static/chat.html` (standalone page). Interactive API docs are at `/docs`.

---

## Seed data

| Script | Purpose |
|---|---|
| `seed_events.py` | Realistic last-hour scenarios: HVAC overheating and filter fault, network packet loss and link flapping, access brute-force and forced door, camera outage, fire-panel battery and smoke event. Also triggers `POST /alerts/run` |
| `seed_history.py` | Backfills 7 days of hourly `TEMPERATURE_READING` and `ENERGY_READING` (kWh) events so historical and energy-change questions have data. The most recent 72 hours are about 12% higher than the 72 hours before |

Run `seed_events.py` first, then `seed_history.py`. `ENERGY_READING` must be an event type accepted by `/ingest`.

---

## Testing

`test_chat.py` is an end-to-end test against the **running API and real database** (no stubs). It asks 20
questions (the six mandatory ones, KPI, history and out-of-scope questions, each in English and Arabic), in both
deterministic mode and LLM mode.

```bash
python test_chat.py
python test_chat.py --no-llm missing
python test_chat.py --energy http://host:8000
```

Checks per question: expected intent, answer language matches the question, `grounding.passed`, citations present and
all existing in `sources`, expected `data_sufficient`, low confidence when data is insufficient, camera availability
percentage present, and an explicit admission when energy data is missing. The exit code is 1 if any check fails.

Results are written to `test_results.json` and `TEST_RESULTS.md`.

### Latest run (2026-11-05, `--energy missing`)

| Result | Value |
|---|---|
| Checks passed | **41 / 41** (deterministic and LLM modes, both languages) |
| LLM answers accepted by the validator | 16 of 20 |
| LLM answers that fell back to the deterministic answer | 4 of 20 |

The four fallbacks were rejections by the validator, not crashes: a device name that was not copied exactly, a missing
required citation, and numbers (24.6 and 3) that do not appear in the cited facts. This is the validator doing its job:
unsupported text never reaches the user.

### Sample answers (deterministic mode)

**Repair priorities**

```
- Priority 1: FA-PANEL-02 (FIRE_ALARM, Meeting Rooms) - Smoke alarm active (open incident), since 2026-11-04 22:58 UTC;
  5 critical and 0 warning open alerts; score 206. [F3]
- Priority 2: HVAC-AHU-01 (HVAC, Open Office) - Smoke alarm active (open incident), since 2026-11-04 22:50 UTC;
  1 critical and 1 warning open alerts; score 128. [F4]
- Priority 3: SW-CORE-01 (NETWORK, Server Room) - no recent faults; 4 critical and 0 warning open alerts; score 80. [F5]
```

**Network issues**

```
- Network availability: 99.706% across 2 network assets, total downtime 1525 s. [F2]
- LINK_DOWN incidents in the window: 6. [F3]
- Bandwidth: average 474.7 Mbps, peak 1008.6 Mbps. [F4]
```

**Historical reading (yesterday's average temperature)**

```
- Period: yesterday (2026-11-03) UTC, relative to the day of the latest recorded event. [F1]
- TEMPERATURE_READING: 356 readings, average 23.8 °C, min 18.8, max 28.6. [F2]
```

**Insufficient data (energy)**

```
The database does not contain any energy or power readings, so energy consumption cannot be determined
without guessing. [F2]      (confidence: low, data_sufficient: false)
```

---

## Known limitations

- **Energy.** The energy intent computes the change against the previous window when `ENERGY_READING` events exist.
  In the current database none are stored (the event type is not among those ingested), so the assistant reports
  "insufficient data" with low confidence. This is the intended behaviour for missing data, but it is not a real
  energy answer.
- **Camera availability is a current-state ratio** (cameras online now divided by total cameras), not a time-weighted
  uptime figure.
- **Model wording.** A 7B local model still occasionally produces answers the validator rejects (about 1 in 5 in the
  latest run). The fallback keeps answers correct but less fluent.
- **No conversation memory.** Each question is answered independently; follow-ups such as "and yesterday?" are not
  understood.
- **Keyword routing.** Intent detection is keyword-based with an LLM fallback; unusual phrasings may be routed to
  `out_of_scope`.
- **Windows follow the latest event, not the wall clock.** If the data feed stops, answers describe the last recorded
  moment (the window fact states this explicitly).
- **Stale alerts.** Alerts are not auto-closed when an asset recovers, which can inflate "open alerts".
- **No authentication or rate limiting** on `/chat`, and the widget stores history in `sessionStorage` only.

## Before production

1. Add authentication, per-user rate limiting and audit logging of questions and answers.
2. Ingest real energy and power meter data, and compute time-weighted availability for cameras and network.
3. Auto-close alerts when the underlying asset recovers.
4. Add short conversation memory (resolve follow-up questions against the previous intent and window).
5. Evaluate larger or fine-tuned models, and track the validator rejection rate as a quality metric.
6. Run the end-to-end suite in CI against a seeded database, and add load and failure tests for Ollama downtime.

---

## Repository layout

```
ANZMA-DATABASE/
│
├── App.py                  # Main FastAPI application
├── ai_explainer.py         # Ollama LLM configuration and explanation
├── chat_engine.py          # Intent classification, SQL collectors, fact building, LLM composition, validation and fallback
├── chat_api.py             # FastAPI router: POST /chat and GET /chat/questions
│
├── seed_events.py          # Generates realistic building events and alert scenarios
├── seed_history.py         # Generates 7-day historical temperature and energy readings
│
├── test_chat.py            # End-to-end tests for English and Arabic chat questions
├── test_citations.py       # Citation and evidence validation tests
├── test_results.json       # Machine-readable test results
├── TEST_RESULTS.md         # Human-readable test report
│
├── static/
│   ├── chat-widget.js      # Floating chat widget logic and API integration
│   ├── chat-widget.css     # Chat widget styling and responsive design
│   ├── chat.html           # Standalone chat interface
│   ├── dashboard.html      # Building operations dashboard
│   └── style.css           # Main dashboard styling
│
├── docs/
│   ├── Data-Flow-Diagram.png
│   └── ER-Diagram.png
│
├── requirements.txt
├── schema.sql
├── README.md
└── .gitignore
```

(Adjust paths to match the repository: the widget and HTML files live in the static directory.)
