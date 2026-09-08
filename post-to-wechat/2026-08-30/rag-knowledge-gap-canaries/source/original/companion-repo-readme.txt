# Why RAGs Hallucinate

Companion repository for the paper **"Why RAGs Hallucinate: Penalty-Aware
Evaluation of Retrieval-Augmented Generation Systems with Knowledge-Gap
Canaries"** (Do Rosario, Younes, Pires — CustomGPT.ai, 2026).

Every number in the paper can be recomputed from the audit logs in this
repository. arXiv link: coming with submission.

## Headline results

1,000 SimpleQA-Verified questions × 4 systems × 3 repeats, graded blind by a
cross-family three-judge panel (GPT + Claude + Gemini, 98.9% unanimous).
Scoring: correct **+1** · wrong **−4** · abstain **0** (an 80% confidence
threshold).

| System | Penalty-Aware Score (Q) ↑ | Accuracy ↑ | Abstention | Acc. when answering ↑ | Canary violation ↓ |
|---|---|---|---|---|---|
| OpenAI RAG | **+0.862** | 0.948 | 3.3% | **98.0%** | 22.2% |
| Gemini RAG | +0.793 | **0.968** | 0.2% | 97.0% | 98.1% |
| CustomGPT.ai RAG | +0.767 | 0.866 | 11.1% | 97.5% | **16.7%** |
| No-RAG Baseline | −1.933 | 0.286 | 16.0% | 34.0% | exempt |

The three RAG systems are closely clustered in accuracy when they answer.
What separates them, roughly sixfold, is how often they answer questions
their knowledge base cannot support ("knowledge-gap canaries"). Conventional
accuracy ranks the systems in the opposite order from penalty-aware scoring,
and the reordering is stable for penalties from k=1 to k=9.

## What is being measured

- **Penalty-aware scoring** — asymmetric scoring makes abstention rational
  below an explicit confidence threshold; conventional accuracy is the
  degenerate k=0 case that rewards guessing.
- **Knowledge-gap canaries** — 18 questions whose answers are verifiably
  absent from the shared 1,000-document knowledge base. Any answer to a
  canary is a grounding violation sourced from parametric memory, even when
  factually correct.
- **Cross-family judge panel** — every attempted answer is graded
  independently by gpt-5.4, Claude Sonnet 5, and Gemini 3 Flash; the
  majority verdict is final, agreement is reported, and a pre-registered
  policy repairs judge votes lost to API quotas.
- **Failure attribution** — grades are joined with each provider's
  retrieval-evidence signal (citations / grounding chunks) to separate
  retrieval failures, generation failures, and abstention-policy decisions.

## Repository layout

```
paper/                  LaTeX source of the paper (+ figure script output)
src/                    evaluation core: scoring, judge panel, audit logging
sampler/                provider clients (CustomGPT.ai, OpenAI, Gemini) + judges
scripts/benchmark/      campaign runner
scripts/analysis/       statistics, failure attribution, hard-set mining,
                        judge-vote backfill
scripts/reports/        report/figure generation
tests/                  unit tests (scoring, panel voting, backfill)
data/                   dataset (SimpleQA-Verified + KB-coverage flags),
                        canary and hard-set question IDs
results/run_*/          complete audit logs of the three campaign repeats
docs/                   gauntlet + campaign reports, computed statistics
```

## The audit logs

Each `results/run_*/` directory is one full campaign repeat:

| File | Contents |
|---|---|
| `provider_requests.jsonl` | every provider call: prompt, raw response, latency, tokens, cost, retrieval metadata |
| `judge_evaluations.jsonl` | every panel grading: verbatim judge prompts, all three votes with reasoning, tallies |
| `judge_evaluations_backfilled.jsonl` | (repeat 3) panels completed after quota-delayed Gemini votes were re-cast |
| `rejudge_log.jsonl` | (repeat 3) the backfill audit trail, including the 12 grade flips |
| `abstention_classifications.jsonl` | attempt-vs-abstention classification per response |
| `judge_consistency_validation.jsonl` | judge determinism re-grades |
| `quality_benchmark_results.json` | the pipeline's per-run aggregate metrics |

## Reproduce the paper's numbers

No API keys are needed to recompute statistics from the shipped logs:

```bash
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=$PWD

# every table in the paper (validates against the pipeline's own aggregates first)
python scripts/analysis/campaign_statistics.py \
  --runs results/run_20260802_225842_090 results/run_20260803_000008_985 results/run_20260803_172510_141

# failure attribution (the "Why RAG Systems Hallucinate" section)
python scripts/analysis/failure_attribution.py

# figures
python scripts/reports/paper_figures.py

# unit tests
pytest tests/ -k "judge_panel or rejudge or canary" -q
```

To re-run the benchmark itself you need provider API keys (see
`.env.example`) and vendor retrieval stores loaded with the corpus; expect
roughly $190 per 1,000-question repeat across the four systems. Model
versions are pinned in the samplers; commercial systems are moving targets,
so fresh runs measure today's products, not the paper's August 2026
snapshot.

## Conflict of interest

The authors are affiliated with CustomGPT.ai, one of the evaluated vendors.
Mitigations, access-parity details, and disclosures are in the paper
(§Limitations) and in `docs/campaign-report.md`. The affiliated product does
not lead the headline metric; every grading decision is auditable here.

## License

MIT. Portions of the evaluation harness derive from
[openai/simple-evals](https://github.com/openai/simple-evals) (see LICENSE).
SimpleQA-Verified questions are from
[Haas et al., 2025](https://arxiv.org/abs/2509.07968); see `data/DATA.md`
for attribution.
