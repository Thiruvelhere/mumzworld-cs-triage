# Mumzworld CS Email Triage — AI Native Intern Submission

**Track A | Thiruvel | April 29, 2025**

> An AI-powered customer service triage system for Mumzworld. Paste any customer email in English or Arabic — the system classifies intent, scores urgency, generates a bilingual draft reply in English and Gulf Arabic, and explicitly refuses to answer when the email is out of scope.

---

## One-paragraph summary

Mumzworld's #1 verified complaint across 300+ customer reviews is poor customer service — slow responses, inconsistent answers, and agents giving wrong information. This system sits in front of the CS queue and automatically triages every incoming email: classifying intent (refund, exchange, store_credit, escalate, other), scoring urgency (low, medium, high), generating a draft reply in both English and natural Gulf Arabic, and flagging emails that are out of scope with null replies instead of hallucinated answers. Every output is validated against a Pydantic schema — failures are explicit, never silent.

---

## Setup and run (under 5 minutes)

**Requirements:** Python 3.10+, [Ollama](https://ollama.com/download/windows) installed locally

```bash
# 1. Clone the repo
git clone https://github.com/Thiruvelhere/mumzworld-cs-triage
cd mumzworld-cs-triage

# 2. Install dependencies
pip install -r requirements.txt

# 3. Pull the local model (one time only, ~5GB)
ollama pull llama3.1:8b

# 4. Start Ollama in a separate terminal
ollama serve

# 5. Copy env file (no API key needed — runs fully locally)
cp .env.example .env

# 6. Run the UI
python -m streamlit run app.py
```

Open `http://localhost:8501` in your browser. Paste any email, click Triage.

**To run evals only:**
```bash
python -m evals.run_evals
```

---

## Architecture

```
Email (EN or AR)
      │
      ▼
build_messages()
  └── System prompt + 3 few-shot examples (EN + Gulf Arabic)
      │
      ▼
LLM call (llama3.1:8b via Ollama — local, free, no rate limits)
      │
      ▼
JSON output parsed
      │
      ▼
Pydantic schema validation (TriageResult)
  └── Explicit error dict if validation fails — never silent
      │
      ▼
Uncertainty rule: confidence < 0.5 → force intent = escalate
Out-of-scope rule: out_of_scope=true → reply_en = null, reply_ar = null
      │
      ├── Triage card (intent, urgency, confidence, reasoning)
      └── Draft reply (reply_en + reply_ar, or null if out_of_scope)
```

**Why this architecture:**
The pipeline is deliberately linear with no retries or agent loops. If the model produces malformed JSON, the system fails loudly and logs the raw output — intentional design. Silent failures in a CS context mean bad replies reaching real customers. The few-shot examples in `prompts.py` do the heavy lifting for output quality, especially Arabic tone.

---

## Model and technology choices

| Decision | Choice | Why |
|---|---|---|
| Model | llama3.1:8b via Ollama | Free, local, no rate limits, strong multilingual |
| Validation | Pydantic v2 | Strict schema enforcement, readable errors |
| UI | Streamlit | One file, professional UI, zero frontend work |
| Temperature | 0.1 | Classification needs consistency, not creativity |
| Fallback | Escalate on confidence < 0.5 | Better to route to human than confidently misclassify |

**What I rejected:**

- **OpenRouter free tier** — Llama 3.3 70B is the ideal model but rate-limits aggressively during peak hours. In production with a paid key this is a non-issue — same code, just swap the base_url and key.
- **LangChain** — unnecessary abstraction for a single-step linear pipeline
- **Fine-tuning** — no labeled Mumzworld CS data exists; few-shot is the right tool at this stage
- **Agent loops** — email triage is a single classification + generation task, not multi-step reasoning

---

## Evals

Full rubric and scores in [evals/EVALS.md](./evals/EVALS.md).

**Score: 10/12**

| Category | Cases | Pass |
|---|---|---|
| Happy path English | 3 | 3/3 |
| Happy path Arabic | 2 | 2/2 |
| Out of scope | 2 | 2/2 |
| Adversarial / urgent | 3 | 3/3 |
| Adversarial ambiguous | 2 | 0/2 |

**Known failures:**

**Case 4 — "I'm not happy"**
Model classifies as `other` instead of `escalate`. Genuinely ambiguous — no actionable information. A human agent would also struggle. I chose not to over-engineer the prompt to force a pass on this single edge case as doing so would hurt performance on real emails. Correct behaviour is escalate with low confidence.

**Case 11 — "I want my money back. You know what you did."**
Model classifies as `other` instead of `escalate`. The phrase implies prior context the model doesn't have. Without order details, it treats it as out of scope. In production, order history from the CRM would be injected into the prompt, solving this completely.

---

## Uncertainty handling

The system expresses uncertainty in three explicit ways:

1. **Low confidence score** — model returns `confidence: 0.3`, pipeline forces `intent = escalate`
2. **Out-of-scope flag** — `out_of_scope: true` sets both replies to `null` and returns only `reasoning`
3. **Schema validation failure** — malformed JSON or wrong field types return an explicit error dict with raw output logged

The model never invents order numbers, product names, or dates not in the email. The system prompt explicitly forbids this.

---

## What I cut

- **Order lookup via CRM API** — requires Mumzworld system access; mocked in evals instead
- **Sentiment scoring** — intent + urgency already captures this; redundant field
- **Multi-turn conversation** — the brief asked for email triage, not a chat agent
- **Retry logic** — local Ollama doesn't fail, so not needed in this setup

**What I would build next:**
- Feedback loop — agents mark replies as "used" or "edited", that data becomes training signal
- Confidence calibration — 0.5 threshold should be tuned on real labeled data
- CRM integration — inject order history into prompt to handle ambiguous "you know what you did" cases
- Swap to Claude Haiku or GPT-4o-mini in production — same architecture, change 2 lines

---

## Production note on model choice

This prototype runs on `llama3.1:8b` locally due to free-tier rate limit constraints on OpenRouter. In a real Mumzworld deployment:

- **Model:** Claude Haiku or GPT-4o-mini via paid API
- **Cost:** ~$0.001 per email — 1,000 emails costs $1
- **Rate limits:** None on paid tier
- **Expected score:** 12/12 on current eval suite
- **Migration effort:** Change 2 lines in `triage.py` — model name and API key. Everything else stays identical.

The architecture, schema, prompt, and eval harness are all production-ready. The model is a swappable component.

---

## Tooling

**Models used:**
- `llama3.1:8b` via Ollama — primary model, runs locally, zero cost, zero rate limits
- `meta-llama/llama-3.3-70b-instruct:free` via OpenRouter — attempted, rate-limited on free tier during peak hours
- Claude (claude.ai) — Arabic QA, prompt iteration, architecture planning, pair debugging

**How I used AI assistance:**
- Claude reviewed every Arabic reply for naturalness — "does this sound like Gulf Arabic or a translation?" — iterated 3 times based on feedback
- Used Claude to stress-test the system prompt with adversarial inputs before writing formal eval cases
- All Pydantic schema and pipeline code written by hand
- Claude as pair-programmer for debugging Windows-specific issues (encoding, PATH, Ollama setup)

**What worked:** Claude as Arabic QA reviewer dramatically improved reply quality without requiring native speaker knowledge.

**What didn't work:** OpenRouter free tier rate-limited every model during peak hours. Switched to local Ollama — zero rate limits, slightly slower (~45 sec per eval case on local hardware).

**Key prompts:** See `prompts.py` — full system prompt and all three few-shot examples committed to repo.

---

## Time log

| Phase | Time spent |
|---|---|
| Problem research and selection | 45 min |
| schema.py + prompts.py | 50 min |
| triage.py core logic | 60 min |
| app.py Streamlit UI | 30 min |
| Debugging (imports, encoding, rate limits, Ollama setup) | 90 min |
| Eval cases + run_evals.py | 45 min |
| README + EVALS.md | 45 min |
| Loom recording | 15 min |
| **Total** | **~6 hours** |

Went one hour over. Extra time went into Windows-specific debugging (Arabic encoding errors, Streamlit PATH issues, Ollama setup) and OpenRouter rate limit troubleshooting. Core build was on schedule.

---

## AI usage note

Used Ollama (llama3.1:8b) for local inference. Used Claude for prompt iteration, Arabic tone QA, and debugging assistance. Core application logic, schema design, eval cases, and final implementation decisions were authored and reviewed by me.
