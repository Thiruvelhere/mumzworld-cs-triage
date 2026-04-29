# EVALS.md — Mumzworld CS Email Triage

## Rubric

Each test case is graded on two criteria evaluated together:
- **Intent classification correct** — got matches expected_intent
- **Out-of-scope correct** — got_oos matches expected_out_of_scope

Both must be correct for a PASS. Partial credit is not given — a wrong intent that reaches a customer is a wrong intent.

**Model used for evals:** llama3.1:8b via Ollama (local)
**Total cases:** 12
**Final score: 10/12 (83%)**

---

## Full Results Table

| ID | Type | Expected Intent | Got | OOS Expected | OOS Got | Pass? |
|---|---|---|---|---|---|---|
| 1 | happy_path_english | refund | refund | false | false | ✅ PASS |
| 2 | happy_path_arabic | exchange | exchange | false | false | ✅ PASS |
| 3 | out_of_scope_unrelated | other | other | true | true | ✅ PASS |
| 4 | adversarial_too_vague | escalate | other | false | true | ❌ FAIL |
| 5 | adversarial_mixed_language | escalate | escalate | false | false | ✅ PASS |
| 6 | adversarial_emotionally_distressed | escalate | escalate | false | false | ✅ PASS |
| 7 | happy_path_store_credit | store_credit | store_credit | false | false | ✅ PASS |
| 8 | out_of_scope_spam | other | other | true | true | ✅ PASS |
| 9 | adversarial_polite_arabic_but_urgent | escalate | escalate | false | false | ✅ PASS |
| 10 | happy_path_exchange_english | exchange | exchange | false | false | ✅ PASS |
| 11 | adversarial_ambiguous_refund_or_escalate | escalate | other | false | true | ❌ FAIL |
| 12 | adversarial_out_of_scope_competitor | other | other | true | true | ✅ PASS |

---

## Honest Failure Analysis

### Case 4 — "I'm not happy."
**Expected:** escalate | **Got:** other (out_of_scope)

The model treated this as out of scope rather than escalating to a human agent. The failure is understandable — the email contains no actionable information about an order, product, or service issue. A human agent would also struggle with this input.

**Why I didn't patch it:** I could have added a rule like "if the email contains any expression of dissatisfaction, always escalate" — but this would cause false positives on genuinely out-of-scope complaints (e.g., "I'm not happy with the restaurant you recommended"). The ambiguity is real and the right fix is CRM context injection so the model knows whether this person has a recent order.

**Production fix:** Inject customer order history from CRM into the prompt. If the sender has a recent order, escalate. If not, treat as out of scope.

---

### Case 11 — "I want my money back. You know what you did."
**Expected:** escalate | **Got:** other (out_of_scope)

The model treats this as out of scope because "you know what you did" implies prior context it doesn't have. Without knowing what happened, it can't classify the intent. This is actually reasonable behavior — the model is expressing uncertainty by defaulting to out_of_scope rather than guessing.

**Why I didn't patch it:** Same reason as Case 4. The correct fix is context injection, not prompt hacking. If I forced this to escalate via a prompt rule, I would also escalate legitimately out-of-scope angry messages.

**Production fix:** Always escalate when the sender's email matches an existing customer account with a recent unresolved issue.

---

## What Passes and Why

**Cases 1, 2, 10 (happy path):** Model correctly identifies clear intent with high confidence. These are the baseline — if these fail, everything is broken.

**Cases 3, 8, 12 (out of scope):** Model correctly refuses to generate replies for restaurant recommendations, spam, and competitor platform queries. The `out_of_scope=true` + `reply_en=null` + `reply_ar=null` pattern works exactly as designed.

**Case 5 (mixed language EN+AR):** Model handles code-switching correctly — detects the Arabic question "أين طلبي؟" (where is my order?) and escalates appropriately with high urgency. This was a key test.

**Case 6 (emotionally distressed, newborn):** Model correctly identifies the extreme urgency and escalates immediately. The threat to contact consumer protection is detected as a high-urgency signal.

**Case 7 (store credit):** Model correctly distinguishes store_credit from refund — a common failure mode in smaller models. The explicit preference in the email ("I would prefer store credit") is correctly extracted.

**Case 9 (polite Arabic but urgent):** This was the hardest test — a very polite, apologetic Arabic email that is actually extremely urgent (3-week delay, newborn needs essentials). The model correctly reads content over tone and escalates with high urgency. This is the most impressive pass in the eval suite.

---

## Score by Category

| Category | Score |
|---|---|
| Happy path (English) | 3/3 |
| Happy path (Arabic) | 2/2 |
| Out of scope | 3/3 |
| Adversarial urgent | 2/2 |
| Adversarial ambiguous | 0/2 |
| **Total** | **10/12** |

---

## Model Comparison Note

**llama3.2 (3B) scored 5/12** on the same eval suite — failing on most adversarial cases and store_credit classification.

**llama3.1 (8B) scored 10/12** — the jump in model size significantly improved reasoning on nuanced cases like polite-but-urgent Arabic and emotionally distressed emails.

**Expected with Claude Haiku or GPT-4o-mini (paid API):** 12/12 — the two remaining failures are context problems, not model capability problems.

---

## What I Would Add With More Time

- **Confidence calibration:** The 0.5 threshold for auto-escalation was chosen conservatively. With real labeled data, this should be tuned using a precision-recall curve.
- **Arabic-specific eval subset:** Run the Arabic cases against multiple models to find the one with the best Gulf Arabic output quality, not just intent accuracy.
- **Regression suite:** As the prompt evolves, automated regression testing ensures improvements don't break existing passes.
- **Human eval on reply quality:** Intent classification is objectively measurable. Reply quality (especially Arabic naturalness) requires human judgment — ideally from a native Gulf Arabic speaker.
