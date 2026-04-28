# EVALS.md

## Evaluation Rubric

A case is marked **PASS** when:

* predicted `intent` matches expected intent
* predicted `out_of_scope` matches expected scope status

12 total test cases covering:

* happy path requests
* Arabic inputs
* mixed-language inputs
* vague complaints
* urgent delivery failures
* spam / unrelated queries
* competitor misroutes

---

## Final Results

**Score: 10 / 12**

| Category                | Result |
| ----------------------- | ------ |
| Happy Path              | 4 / 4  |
| Arabic & Mixed Language | 4 / 4  |
| Out of Scope            | 3 / 3  |
| Ambiguous / Adversarial | 2 / 4  |

---

## Failed Cases

### Case 4 — “I'm not happy.”

Predicted: `other`
Expected: `escalate`

The message expresses dissatisfaction but lacks actionable context.
The model treated it as vague rather than unresolved complaint.

**Production mitigation:** Route short negative sentiment messages to manual review.

---

### Case 11 — “I want my money back. You know what you did.”

Predicted: `other`
Expected: `escalate`

The customer requests refund but provides no context.
The safer production behavior is escalation due to implied unresolved issue.

**Production mitigation:** Add business rule for refund demand + missing context.

---

## Key Findings

* The model performs strongly on explicit requests and multilingual inputs.
* Out-of-scope detection was reliable across spam and competitor cases.
* Weakness appears mainly on intentionally vague emotional complaints.

---

## What I Would Improve With More Time

* Hybrid rules layer for vague dissatisfaction detection
* Confidence threshold calibration using labeled data
* Compare Ollama Llama 3.1 8B vs OpenRouter larger models
* Human feedback loop from support agents

---

## Model Note

Primary evaluation was run locally using **Ollama llama3.1:8b** for speed and reproducibility.
Larger hosted models may improve ambiguous-case accuracy but were not required to validate the prototype.
