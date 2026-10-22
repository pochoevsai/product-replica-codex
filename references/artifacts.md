# Product Replica artifact rules

## Evidence record

For each important observation, record:

| Field | Meaning |
|---|---|
| `id` | Stable identifier such as `FLOW-BOOK-01` or `SCREEN-03` |
| `source` | URL, supplied file, screenshot, test run, or user statement |
| `observed` | What is directly visible or reproducible |
| `inferred` | What is hypothesized from the observation |
| `confidence` | `high`, `medium`, or `low` |
| `implication` | Product or implementation consequence |

Do not present inferred behavior as fact. Mark unknowns and state how to verify them.

## Feature matrix

Each feature should include:

`id, capability, actor, priority, source, acceptance_criteria, status, intentional_difference, risk`

Priorities:

- `must`: required for the agreed vertical slice or launch gate;
- `should`: important but can follow the slice;
- `could`: useful optional work;
- `out-of-scope`: deliberately excluded with a reason.

Use `done` only when acceptance criteria are tested. Use `partial` when a meaningful part works but a stated criterion is missing.

## Reports

Every report should end with:

1. verified facts;
2. decisions made;
3. open questions;
4. risks and mitigations;
5. next smallest valuable action;
6. exact verification commands or manual checks.

For review analysis, include source links, dates when relevant, counts, sample limitations, and representative paraphrases. Never fabricate a quote, review, ranking, score, or user complaint.
