---
title: "Self-hosted Deep Research 原文(规范化)"
tags:
  - type/source
  - topic/rag
moc:
  - "[[rag]]"
related:
  - "[[wechat-drafts/2026-05-25-self-hosted-deep-research/article]]"
---

# How to build a Deep Researcher

Source: https://x.com/akshay_pachaar/status/2047395420935229724
Article URL: http://x.com/i/article/2047308282273189889
Author: Akshay 🚀 (@akshay_pachaar)
Published: Thu Apr 23 19:21:21 +0000 2026
Cover: https://pbs.twimg.com/media/HGnOzZ5aMAA79RI.jpg

---

A 100% open-source, self-hostable Deep Research Stack That Beat OpenAI, Gemini, and Perplexity

---

If you need AI to do research for you today, you're probably using ChatGPT Deep Research, Claude, or Perplexity. All three are genuinely capable. All three are also closed-source SaaS running in someone else's cloud.

Every query you send and every internal document you connect sits on their servers, not yours.

For most teams, that's been the trade-off: accept it, or don't use AI for serious research.

In this article, you'll see a third option: a fully open-source deep research stack that runs on your own infrastructure.

Three tools, all open source: **Onyx** for retrieval, **CrewAI** for orchestration, **Voxtral** for voice. (https://github.com/onyx-dot-app/onyx)

Here's the full system running end-to-end, from voice query to narrated research report:

![source-media-2047309825919582208](https://pbs.twimg.com/amplify_video_thumb/2047309825919582208/img/guEMMBsb2cyEoJ-T.jpg)

The rest of this article breaks down how it works and walks you through building the same stack yourself. Before any of that, though, it's worth being clear about why this is worth building at all.

# Why self-hosting actually matters

Every major AI research tool is a closed cloud service. That has real consequences:

- **Your queries go to their servers.** The questions you ask reveal what you're working on.

- **Your connected data gets indexed on their infrastructure.** Integration is convenient, but the index lives on their side.

- **Retention, logging, and audit are their call, not yours.** Enterprise tiers soften this but don't eliminate it.

- **Quotas and pricing change on their timeline.** The tool you depend on today can reprice or rate-limit tomorrow.

For regulated industries, teams with IP-sensitive work, or anyone working under data residency rules, that list isn't theoretical. It's the reason AI-assisted research still feels out of reach for a lot of serious work.

Unless you can run the whole stack yourself, with no compromise on quality.

![source-media-2047376961442635776](https://pbs.twimg.com/media/HGm-f7wbYAAexfG.jpg)

# Why Existing Research Tools Break

Most research tools do one pass. They search, collect whatever comes back, and hand it to the LLM to write something up.

That works for shallow queries. It breaks the moment you ask something that requires synthesis across sources, contradiction detection, or reasoning across multiple hops.

Here's what that failure looks like in practice:

- The agent finds a source and a contradicting source. It picks one and moves on. The contradiction never surfaces.

- Two sources say the same thing in different words. The report cites both as independent evidence.

- A critical connecting fact lives in a document that wasn't retrieved, because keyword matching doesn't understand that "cloud migration" and "moving our PostgreSQL cluster to AWS" are the same thing.

These aren't edge cases. They're the normal shape of real research questions.

And they all share the same root cause: **research isn't one task.**

![source-media-2047378310955724801](https://pbs.twimg.com/media/HGm_ufFa8AExGtP.jpg)

# What good deep research actually requires

Five things, regardless of tools:

**1. Separation of stages.** Hard walls between gathering, analysis, and writing. Each stage gets only the clean output from the one before.

**2. Retrieval that reasons.** Keyword search is brittle. Vector similarity breaks on multi-hop. You need parallel query variants, intelligent recombination, and an LLM selection step before synthesis. Skip that last step and hallucinations enter.

**3. Reflection in the loop.** Static plans don't survive contact with findings. The system should pivot when something unexpected surfaces, while tracking coverage of the original plan.

**4. Unified search across public and internal sources.** A research layer needs to query the open web and internal knowledge in one pipeline, with permissions enforced per-document. Whether the indexing runs on your infrastructure or a vendor's is what determines who owns the data.

**5. A voice layer.** Speaking beats typing for queries. Listening beats reading for long reports. Makes a tool reachable, not just usable.

![source-media-2047377686033756160](https://pbs.twimg.com/media/HGm_KHEacAAo35h.jpg)

## Onyx: an open-source retrieval layer that beats the benchmarks (https://github.com/onyx-dot-app/onyx)

Onyx is an open-source AI platform built around these principles. It gives any model RAG, web search, code execution, deep research, and custom agents out of the box. 

Fully self-hostable, so your data never leaves your infrastructure.

And it's not a compromise on capability.

Onyx submitted to **DeepResearch Bench**, an independent academic benchmark covering 100 PhD-level research tasks across 22 fields, evaluated on report quality and citation accuracy.

**It placed #1**, ahead of OpenAI Deep Research, Gemini 2.5 Pro, and Perplexity Deep Research.

The team recently shared their lessons from that submission. Their prompt philosophy in one line: "Prefer being thorough in research over being helpful."

Here's how that philosophy translates to architecture.

## Three phases, not one loop

**Phase 1: Clarification.** Up to 5 targeted questions for short or ambiguous queries. Skipped automatically for detailed ones.

**Phase 2: Planning.** Decomposes the query into up to 6 exploration directions. Critical choice: the planner has no tool access, so it produces a plan, not answers.

**Phase 3: Iterative execution.** Orchestrator and research agents alternate up to 8 cycles, each dispatching up to 3 agents in parallel.

![source-media-2047378785163726849](https://pbs.twimg.com/media/HGnAKFpa0AE3uWs.jpg)

## **Two separations that matter:**

- The orchestrator never searches directly.

- Research agents never see the full query or plan.

This forces self-contained task briefs and prevents context leakage.

## Adaptive strategy

Onyx deviates from the original plan based on what it finds. Between every dispatch, a mandatory reflection step produces structured output:

- What's covered

- What gaps remain

- What new directions emerged

- Whether more cycles will yield new info

Runs every time. The result behaves like a researcher, not a retrieval engine.

## The 6-stage retrieval pipeline

Each agent runs this before the LLM synthesises anything:

**Query generation.** Parallel queries: semantic rephrasing, keyword variants, broad searches. Multi-part questions split automatically.

**Search and recombination.** Hybrid index (vector + BM-25), results combined via Reciprocal Rank Fusion, adjacent chunks merged.

**LLM selection.** The LLM reviews all chunks and keeps only the relevant ones. Skipping this is where hallucinations enter.

**Context expansion.** For each selected doc, the LLM reads surrounding chunks to decide context size. Parallel per document.

**Prompt building.** Selected sections assembled with citations and chat history.

**Answer synthesis.** Grounded answer with inline citations linking to sources.

![source-media-2047381972503408640](https://pbs.twimg.com/media/HGnDDnaasAAN3dz.jpg)

## Citation integrity 

- Agents cite inline as they write intermediate reports.

- Citations from parallel agents get merged and renumbered into one unified set.

- Every final claim traces back to a specific source document.

## Internal sources, indexed on your infrastructure

Onyx connects to **40+ enterprise data sources**: Slack, Confluence, Jira, GitHub, Salesforce, Google Drive, SharePoint, Notion, Zendesk, HubSpot, Gong, and more.

![source-media-2047382681403723776](https://pbs.twimg.com/media/HGnDs4RbEAAL7zC.jpg)

The difference from proprietary tools isn't whether it can connect. It's where the indexing happens. Onyx pre-indexes everything continuously on your own infrastructure, syncing content, metadata, and permissions in near real time.

**What that gets you:**

- One query spans the open web and every internal source at once.

- Users only see results from documents they're authorised to view.

- Permissions sync automatically from each source.

- No internal data leaves your network to be indexed or stored by a vendor.

![source-media-2047382937096908801](https://pbs.twimg.com/media/HGnD7wzbcAEQGAQ.jpg)

# CrewAI: the orchestration layer

Onyx handles retrieval. CrewAI handles coordination.

The default pattern most developers reach for is one agent with three sequential tasks sharing a growing context window:

- The writer starts before the analyst finishes.

- Raw search noise bleeds into the final report.

- Source material gets reinterpreted twice before output.

**CrewAI solves this with three primitives:**

- **Flows** wire independent Crews together, each receiving only clean output from the stage before. No accumulated context.

- **Skills** inject domain-specific instructions into an agent's prompt at runtime via SKILL.md. Instruction at the point of action.

- **MCP Integration** attaches MCP servers directly to an agent via the mcps field. No adapter, no context manager.

Onyx connects in one declaration:

```python
from crewai import Agent

researcher_agent = Agent(
    role="Senior Research Analyst",
    goal="Gather information on research query with source URLs",
    backstory="You are a disciplined analyst. Record every source URL.",
    mcps=[
        f"{ONYX_MCP_URL}?token={ONYX_TOKEN}"
    ]
)
```

The Researcher agent gets three tools instantly:

- Search the knowledge base

- Search the web

- Fetch full page content from any URL

No manual tool wiring. Schemas cached, connections on-demand, graceful failure if the server is unreachable.

# Voxtral: the voice layer (https://huggingface.co/mistralai/Voxtral-4B-TTS-2603)

Every research workflow has one friction point: the keyboard.

Voice in AI tools is usually a bolt-on: a Whisper wrapper for input, a basic TTS for output, different models per direction with no coherent design.

Voxtral is different. It's Mistral's native audio model family, built for speech understanding and generation from the ground up, with the same family handling both directions:

- Transcription stays accurate across accents, background noise, and domain vocabulary.

- Narration sounds natural, not robotic.

**Two changes to the research experience:**

- **Voice input.** Speak a question instead of typing. The transcript flows straight into the pipeline.

- **Report narration.** The full Markdown report gets read back as expressive speech. Listening beats screen-reading for long reports.

![source-media-2047385500152193024](https://pbs.twimg.com/media/HGnGQ87bYAAPOZv.jpg)

# How it all fits together

**The full flow:**

![source-media-2047385969649999872](https://pbs.twimg.com/tweet_video_thumb/HGnGsR8bYAAa8uL.jpg)

Type, speak, or upload a PDF as your research query.

**Researcher Agent** searches the web and your documents via Onyx MCP.

**Analyst Agent** deduplicates, flags contradictions, and groups findings.

**Report Writer Agent** produces a structured, citation-backed Markdown report.

Click **"Play Report"** for narration via Voxtral TTS.

## Three mini-crews, not one

The natural first design is one Crew with three sequential tasks. Don't do it.

Shared context across stages degrades ground truth. The Onyx team calls this "deep frying":

- Facts get reinterpreted.

- Contradictions smoothed over.

- Source material unrecognisable by the time the Writer sees it.

This system uses a Flow: three separate Crews, each receiving only clean output from the stage before.

![source-media-2047386259732201472](https://pbs.twimg.com/media/HGnG9KlagAA_o4H.jpg)

**Researcher Agent.** Connects to Onyx via CrewAI's MCP integration. Runs web searches, reads full URLs, searches uploaded PDFs. Every finding carries a citation.

**Analyst Agent.** Takes raw findings and:

- Deduplicates overlapping facts

- Merges sources saying the same thing

- Flags explicit contradictions

- Groups into coherent themes

Output is a structured summary, not a pile of search results.

**Report Writer Agent.** Turns the summary into a polished, citation-backed Markdown report. Equipped with a CrewAI Skill (SKILL.md) injected at generation time for consistent structure.

```plaintext
deep-research-report/
├── SKILL.md       # Formatting rules, evidence standards, structure
├── scripts/       # Optional
└── references/    # Optional
```

SKILL.md uses YAML front matter and a Markdown body:

```markdown
---
name: deep-research-report
description: >
  Guidelines for writing high-quality, publication-ready deep research reports.
  Covers structure, tone, evidence standards, and formatting rules.
metadata:
  author: deep-research-agent
  version: "1.0"
---

Instructions for the agent go here.
This markdown is injected into the agent's prompt when the skill is activated.
```

Here's a successful execution of the full flow:

![source-media-2047386667263434752](https://pbs.twimg.com/media/HGnHU4wboAADPRN.jpg)

# Find all the code and try it here

You can find all the code for the project on @LightningAI Studio:

**Get started here →** (https://lightning.ai/lightning-ai/templates/multi-agent-deep-researcher-powered-by-gemma-4?utm_campaign=akshay&utm_medium=twitter)

# What you get by building this

The story here isn't that an open-source tool has finally caught up to the big names.

**Onyx** runs deep research on infrastructure you can inspect, self-host, and modify. Paired with CrewAI's enforced stage separation and Voxtral's native speech layer, you get a research stack with: (https://github.com/onyx-dot-app/onyx)

- **Capability.** Competitive or better research quality, with full citation integrity.

- **Control.** Every byte of your queries and internal data stays on your infrastructure.

- **Transparency.** Open-source code you can read, audit, and extend.

![source-media-2047387722575405056](https://pbs.twimg.com/media/HGnISUGaYAARa9S.jpg)

So here's the question worth starting with: **what would your team's research workflow look like if data sovereignty wasn't the constraint?**

Start there.

---

That's a wrap!

If you enjoyed reading this:

Find me →@akshay_pachaar ✔️ (https://x.com/@akshay_pachaar)

Every day, I share tutorials and insights on AI, Machine Learning, and vibe coding best practices.
