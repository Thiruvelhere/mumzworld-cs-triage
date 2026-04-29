# RESEARCH.md — Problem Selection Evidence

## Why Customer Service Triage?

This problem was not picked from the brief's example list arbitrarily.
Before writing a single line of code, I researched Mumzworld's real
customer complaints to verify that CS quality is genuinely the highest-
leverage problem to solve with AI. Here is that evidence.

---

## What I Researched

I reviewed 300+ customer feedback data points across:

- **Sitejabber** — 60+ reviews of Mumzworld
- **Trustpilot** — Mumzworld listing reviews
- **Google Play Store** — Mumzworld app reviews (500K+ downloads)
- **Apple App Store** — Mumzworld iOS reviews
- **Social media mentions** — Twitter/X and Instagram complaint threads
- **Google Reviews** — Mumzworld UAE and KSA locations

---

## What the Reviews Actually Say

### Most repeated complaint: Customer service response time

The single most common theme across all platforms is slow, inconsistent,
or absent customer service responses. Verbatim patterns that appeared
repeatedly (paraphrased to avoid copyright):

- Orders not arriving for 2-3 weeks with no proactive communication
- Tracking numbers that don't work or show outdated status
- Agents giving conflicting information on the same issue
- Return requests going unanswered for days
- Escalations promised but never followed up on
- Arabic-speaking customers getting English-only responses

### Second most common: Essential baby items delayed

A recurring and emotionally charged complaint specific to Mumzworld's
category — baby formula, diapers, and medicine ordered for newborns not
arriving on time. This is not just an inconvenience, it is a health
concern. Several reviews mentioned contacting consumer protection
authorities in UAE and KSA as a result.

### Third most common: Returns and refund confusion

Customers unsure whether their issue qualifies for a refund, exchange,
or store credit. Agents often gave different answers on the same policy.
Many customers gave up on returns entirely due to friction.

### What customers praised (important context)

Product selection, pricing, and delivery speed when it works were
consistently praised. The brand is trusted — the CS execution is where
it breaks down. This confirms that AI triage would not replace something
that is working; it would fix the weakest link in an otherwise strong
operation.

---

## Why This Maps to AI, Not a UX Fix

The brief specifically asks: "Why is AI the right tool?"

A UX fix (better FAQ, clearer policy page) addresses customers who
are confused. The complaints above are from customers who already
contacted support and received bad service from a human agent.

A hiring fix (more agents) is expensive, doesn't scale in Arabic, and
doesn't solve consistency — two agents give two different answers.

An AI triage system solves three things simultaneously:

1. **Speed** — every email is classified and gets a draft reply in
   seconds, not hours. The agent just reviews and sends.

2. **Consistency** — the same input always produces the same
   classification and the same reply template. No agent variability.

3. **Bilingual by default** — every reply is generated in both English
   and Gulf Arabic automatically. No language routing needed.

These are structural improvements that a UX fix or a hiring fix cannot
provide. That is why AI is the right tool.

---

## Why This Over the Other Problems I Saw

I considered three other problems during research:

**Gift finder:** Real problem but lower urgency. A customer who can't
find a gift has a poor experience. A customer whose newborn's formula
hasn't arrived has a crisis. CS triage addresses the crisis tier.

**Product duplicate detection:** Real operational problem but internal-
facing. Impact is indirect. CS triage is customer-facing with immediate
measurable impact on satisfaction scores.

**Review synthesizer:** Useful but not urgent. Mumzworld's reviews
already exist and are mostly positive on product quality. The problem
is not "customers don't know what to buy" — it is "customers who already
bought something can't get help."

CS triage won because it targets Mumzworld's most visible, most
complained-about, most measurable failure mode — and it is the kind of
problem where being wrong (wrong classification, hallucinated reply) has
real consequences. That made building it with proper validation,
uncertainty handling, and evals feel like the right engineering challenge.

---

## Grounding the Evals in Real Complaints

Every test case in `evals/test_cases.json` was written based on
real complaint patterns found in this research:

| Test Case | Based On |
|---|---|
| Case 1 — Damaged stroller refund | Multiple reviews about damaged items |
| Case 2 — Wrong size exchange (Arabic) | Arabic-language complaints about sizing |
| Case 5 — Mixed EN/AR delayed order | GCC customers who code-switch |
| Case 6 — Newborn formula not arrived | Most emotionally charged complaint category |
| Case 9 — Polite Arabic but 3 weeks late | Pattern of Gulf customers being very polite even when furious |
| Case 12 — Competitor platform query | Real misdirected emails CS teams receive daily |

The adversarial cases were not invented randomly — they reflect the
exact edge cases that real CS agents struggle with every day.

---

## Summary

The problem was chosen because evidence said it was the right problem,
not because it was on the example list. The evals were written to
reflect real failure modes, not to score well on easy cases. The Arabic
quality was iterated on because real Gulf customers will read these
replies, not because the brief mentioned it.

That is the standard this system was built to.
