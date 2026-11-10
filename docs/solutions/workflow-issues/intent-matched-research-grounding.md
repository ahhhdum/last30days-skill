---
title: Intent-matched research grounding acceptance cases
date: 2026-11-09
category: docs/solutions/workflow-issues
module: skills/last30days/references/research-runbook.md
problem_type: workflow_issue
component: research_quality
severity: medium
tags:
  - first-party-grounding
  - source-authority
  - acceptance-replay
---

# Intent-matched research grounding acceptance cases

## Frozen scope

Case prompts and criteria recorded before shared instruction edits, against baseline
`7b5e8ee3ba80ad3d8eb8dff9766cc50aa43fd0ae` (2026-11-09).
The miss was incomplete coverage of a product-selection question despite consulting
an announcement and some documentation. No particular URL or article title is a
required discovery. Private repository names, preferences, and maintenance tasks
are omitted from the sanitized replay; the model-selection objective is retained.

These cases test host discovery and synthesis, not engine retrieval or a full
recon run. Engine invocation and earlier raw reports are excluded. Pre-merge runs
are diagnostic; post-merge acceptance against the default-branch procedure remains
pending. This card is evaluator-only during a replay.

## Replay binding

- Start a fresh agent without prior conversation on the strongest available model.
  Supply only one prompt below, the procedure under test, tools, budget, and access
  boundaries. Withhold this card, criteria, and earlier results.
- Read `skills/last30days/SKILL.md` and its routed research/synthesis references.
  Pre-merge diagnostics read the candidate; acceptance reads the merged default
  branch. Record the exact procedure commit or candidate diff identifier.
- Cases 1 and 2 use public web search and page reads: up to 3 pre-research queries
  and 2-3 supplement queries, using the existing separate budgets. Read relevant
  results and linked pages; do not expand into another search round. Do not invoke
  the engine, paid source APIs, or local knowledge stores.
- Case 3 uses only its supplied controlled-source packet. Inspect its retrieval
  outcomes; do not perform live searches or claim to have attempted its requests.
- Ask for the procedure's conclusion, source links or packet identifiers, which
  findings were discovered independently, and what remains untested or unresolved.
  Never fabricate an engine footer, source count, quote, or retrieval result.
- Public retrieval can change. Preserve the queries, returned source URLs/dates,
  relevant excerpts, and final response for evaluator inspection. Use information
  available by the prompt's date; flag uncertain publication timing.

## Case 1: New-release task selection

**Prompt:**

> As of November 9, 2026, research the newly released Fable 5.2. What is it good
> at, and how are people using it in actual workflows? Produce practical guidance
> for choosing among Sol 6.1, Fable 5.2, Opus 5.5, and Astra. Apply it to business
> analysis and software work, an image/video generation workflow, a game project,
> and a travel-planning application. Avoid generic advice such as "use it for
> complex projects." Give specific task shapes, reasons, limitations, and useful
> switching criteria.

**Pass criteria:**

1. Independently searches for and reads first-party guidance answering selection
   and practical-use questions, beyond a launch announcement or homepage. The
   criterion concerns appropriate coverage, not one predetermined article.
2. Addresses task fit, relevant effort/configuration, limitations, and completed
   task cost/speed tradeoffs; explicitly marks material unanswered questions.
3. Separates vendor facts/advice, independent hands-on results, and proposed
   routing inferred by the agent. Does not present proposed routing as measured.
4. Does not count repeated announcements across platforms as independent trials.
   Describes the maturity and limits of hands-on evidence, including material
   contrary results if found; does not invent corroboration or counterexamples.
5. Gives concrete task-level guidance across the requested project shapes without
   universal model superiority claims or treating an LLM as the media renderer.

## Case 2: Community-pulse control

**Prompt:**

> As of November 9, 2026, what are developers actually saying about using Claude
> Code in their daily workflows during the preceding month? Focus on concrete
> routines, reported benefits, frustrations, and disagreements. I want the
> community experience, not a product overview or a recommendation about which
> model to choose.

**Pass criteria:**

1. Leads with attributable firsthand community experiences relevant to the prompt,
   distinguishing concrete reports from unsupported reactions and promotion.
2. Preserves disagreements and coverage limits; engagement measures resonance
   rather than proving technical correctness or independent corroboration.
3. Does not replace the requested pulse with official product positioning or a
   model-selection matrix. Uses official sources only for relevant factual context.
4. Uses material, attributable quotations when helpful; does not fill a quote
   quota with irrelevant comments or invent authors, counts, or permalinks.

## Case 3: Relevant official guidance unavailable

**Controlled packet:** Before replay, the evaluator freezes a neutral packet for
a fictional newly released "Model R": a vendor announcement, two limited firsthand
reports (including a contrary result), and explicit unavailable retrieval results
for relevant official selection/configuration guidance. It describes two workflows:
a software contract migration and reviewing reference images for a game scene.
Keep the packet outside tracked research and earlier conclusions. Identify it as
simulated; it must contain source material and retrieval outcomes, not an answer.

**Prompt:**

> Using only the supplied controlled-source packet, recommend whether the newly
> released Model R is a useful first choice for its two described workflows.
> Relevant official selection/configuration guidance cannot be retrieved in this
> environment. Explain what the available evidence supports, what remains unknown,
> and what a bounded next step would resolve.

**Pass criteria:**

1. Uses the supplied unavailable outcomes without claiming guidance does not exist
   globally, pretending to have retrieved it, or inventing additional search work.
2. Does not invent official recommendations, settings, prices, or capabilities.
3. Gives qualified guidance where evidence permits, preserves the contrary result,
   and explicitly leaves unsupported decisions unresolved.
4. Names missing information and a bounded next step. Does not search beyond the
   packet, prescribe indefinite research, or require a new evaluation framework.

## Earlier conclusions and scoring

Replay agents must not access this card, the change's tracking discussion/PR,
commit messages, reviews, previous replay outputs, prior research briefs, living
model-selection guides, handoffs, raw research/appendices, conversation exports,
or memory stores. All other local repositories and historical research are out
of scope. The evaluator retains the exact private location map separately;
publish no private paths, project names, or preferences here.

Score each criterion **met** or **missed**, with evidence and independent versus
earlier-conclusion origin. Contaminated runs cannot establish independent success.
Record procedure revision, source-packet identity if applicable, tools/query count,
unresolved coverage, and verdict here. Do not revise criteria to fit observed output.

| Run | Case 1 | Case 2 | Case 3 | Status |
| --- | --- | --- | --- | --- |
| Pre-merge diagnostic | 1-5 met; method exception | 1-4 met | 1-4 met | Not acceptance |
| Post-merge acceptance | Pending | Pending | Pending | Awaiting approved merge |

## Pre-merge diagnostic results — 2026-11-09

Fresh agents tested the instructions recorded in `3545cd9`. All 13 frozen outcome
criteria were met on the supplied reports; this is not full procedural compliance.
They independently inspected relevant official selection/effort guidance, kept the
community control community led, and preserved unknowns and contrary evidence in
the unavailable-guidance control. Vendor advice, firsthand reports, and inference
were distinguished; concrete applications covered the four requested project shapes.

**Case 1 method exception:** its six queries omitted the required broader
family-plus-decision search. Relevant documentation was opened, but the previously
missed developer-blog article was not independently found. Its failure-led framing
also does not test a Fable-first decision. Passing these frozen outcomes does not
establish exhaustive official-guidance coverage or compliance with every new rule.

Cases 1 and 2 used 3+3 queries. Case 1 opened 13 URLs, including an extra original
video check beyond the approximate twelve-page target. Case 2 attempted 12 URLs,
including two failed comment opens. Both disclosed access and dating limits.
Case 3 used only the [frozen simulated packet](../../../tests/eval/fixtures/model_r_missing_guidance.md),
SHA-256 `5da816da616df355b7b07a760c411fbcc9850b2e75cdf44432db0887cc772525`.
It made no searches and claimed no real-world retrieval independence.

No access to earlier conclusions was declared. Grading inspected the reports,
query logs, and provenance declarations, without independently reopening every
source or auditing complete tool traces. Engine retrieval/ranking, paid adapters,
saving, and footer behavior were not tested by these host-stage diagnostics.

Independent review subsequently found a comparison-mode rule mandating generic
rivalry queries inside the same supplement budget. Its minimum correction defers
to the shared gap-first budget; the reviewer verified that sentence separately.
These live diagnostics were not rerun after that review correction. Post-merge
acceptance remains pending; retain the criteria and the recorded method exception.
