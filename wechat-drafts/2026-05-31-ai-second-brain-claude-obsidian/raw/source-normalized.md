# How to Build an AI Second Brain With Claude and Obsidian (Full Course)

Source: https://x.com/eng_khairallah1/status/2060652660773314833
Author: Khairallah AL-Awady (@eng_khairallah1)
Created: Sat May 30 09:20:54 +0000 2026
Article ID: 2060512029065269248

Most people take notes. Almost nobody uses them.

Save this :)

You highlight articles. You save bookmarks. You write meeting notes. You jot down ideas. And then those notes sit in folders you never open again, slowly becoming a digital graveyard of forgotten thoughts.

Obsidian just crossed 1.5 million users. And the reason is not the note-taking.

It is the AI integration.

When you connect Claude to an Obsidian vault, something different happens. Your notes stop being passive text on a screen. They become a knowledge base that Claude can read, search, reason over, and build on.

You ask Claude a question and it answers using your own notes. Not generic internet knowledge. Your notes. Your research. Your ideas. Your context.

That is a second brain. Not a folder full of files you forgot about. A system that actually thinks with you.

Here is exactly how to build one from scratch, even if you have never used Obsidian or Claude before.

Why Obsidian and Not Notion, Apple Notes, or Google Docs

This is the first question most people ask and the answer is simple.

Obsidian stores your notes as plain markdown files on your device. That is it. No proprietary format. No cloud lock-in. No subscription required for core features. Just folders of .md files sitting on your computer.

Why does that matter?

Because any AI tool can read a markdown file. You can point Claude Code at your vault and it reads every note without exporting, converting, or uploading anything. You can run local AI models and keep everything entirely on your machine. You can switch AI providers anytime without migrating your notes. You can version control your vault with Git.

Notion locks your notes in a proprietary database. Apple Notes locks them in iCloud. Google Docs locks them in Google's format. Every one of those creates friction when you try to connect AI.

Obsidian has zero friction. Your notes are files. AI reads files. Done.

The other critical advantage: Obsidian uses bidirectional links. When you write [[project name]] in one note, it automatically connects to every other note that mentions that project. Over time, these links create a web of connected knowledge — not a flat list of isolated documents.

Claude can follow those links. It can trace connections between your notes that you did not make yourself. It finds patterns across hundreds of notes that you would never find manually.

That is the superpower. Not just AI plus notes. AI plus connected notes.

## Step 1: Set Up Your Vault

Download Obsidian from obsidian.md. It is free. Install it. Create a new vault — this is just a folder on your computer where all your notes will live.

Create this folder structure inside your vault:

Inbox/ — where new notes land before they are organized. Every idea, capture, and quick note goes here first.

Projects/ — active projects with dedicated notes. One folder per project.

Areas/ — ongoing areas of responsibility. Things like "Marketing," "Finance," "Health," "Career" — whatever categories matter to your life or work.

Resources/ — reference material. Research, articles you have read, book notes, course notes, templates.

Archive/ — completed projects and outdated material. Still searchable but out of your active view.

This structure comes from Tiago Forte's PARA method and it works extremely well with AI because it gives Claude clear categories to reason about.

Do not overthink this. The structure can evolve. The worst thing you can do is spend three days designing the perfect folder system instead of actually putting notes in it.

## Step 2: Start Taking Notes the Right Way

Here is where most Obsidian guides go wrong. They teach you the tool before teaching you the habit.

The habit is simple: capture everything that might be useful later.

When you read an article and find a useful insight, open Obsidian and write a quick note about it. Not a copy-paste of the article. A few sentences in your own words about why it matters.

When you have an idea in the shower, open Obsidian on your phone and type it into the Inbox folder.

When you finish a meeting, spend two minutes writing the key decisions and action items.

When you learn something new about your field, write it down with a link to where you learned it.

The formatting does not matter at first. The consistency does.

Here is what makes a note AI-friendly:

Use a clear title. "Meeting Notes 2026-05-30 — Product Roadmap Review" not "notes."

Use frontmatter. At the top of every note, add tags and metadata:

---
tags: [meeting-notes, product, q2-2026]
date: 2026-05-30
project: "[[Product Roadmap]]"
---

Use wikilinks. When you mention a person, project, or concept that has its own note, link to it: [[Sarah Chen]], [[Q2 Launch Plan]], [[Customer Retention Strategy]]. These links are what build the connected web that makes your vault powerful.

Write for your future self (and for Claude). Assume you will forget the context in three months. Include enough detail that the note makes sense on its own.

## Step 3: Connect Claude to Your Vault

This is where the magic starts. There are multiple ways to connect Claude to your Obsidian vault, depending on your technical comfort level.

Option A: Claude.ai Projects (Easiest - No Technical Setup)

Create a Project in Claude.ai. Upload your most important notes as project knowledge files. Every conversation within that project now has access to those notes.

Limitations: you need to manually upload files, there is a knowledge file size limit, and it does not automatically sync when you update your notes.

Best for: beginners who want to test the concept before committing to a deeper setup.

Option B: Claude Code + Direct Vault Access (Most Powerful)

If you use Claude Code, point it directly at your Obsidian vault folder. Claude can read, search, and even write to your vault files.

In your CLAUDE.md file, add:

"My Obsidian vault is located at ~/Documents/MyVault. Use it as a persistent knowledge base. When I ask questions, search relevant notes first. When I generate research or summaries, save them as new notes in the appropriate folder following the existing naming and formatting conventions."

This is the setup that developers and power users are running right now and it is dramatically more powerful than any other approach.

Option C: MCP Servers (Best Balance of Power and Ease)

There are several MCP servers designed specifically for Obsidian:

mcpvault: zero dependencies, no Obsidian plugin required, works without Obsidian running. Reads raw .md files directly with BM25 search and relevance ranking. 14 MCP methods. This is the cleanest option for most users.

mcp-obsidian: the most established option with 3,000+ stars. Requires the Local REST API community plugin in Obsidian, which means Obsidian must be running. More features but more setup.

Obsidian-Skills by Steph Ango: the CEO of Obsidian published official Claude Skills for Obsidian. 12,900+ GitHub stars. Five skills covering every Obsidian file format. These follow the open Agent Skills spec so they work with Claude Code, Codex, and other agents.

Pick one. Install it. You now have an AI that can reason over your entire knowledge base.

## Step 4: Build Your First AI Workflows

Once Claude can access your vault, start with these five workflows that deliver immediate value:

Workflow 1: The Weekly Digest

"Read all my notes tagged with #meeting-notes from the past week. Create a weekly summary that includes: key decisions made, action items assigned, open questions, and any patterns or themes you notice across multiple meetings. Save it as a new note in Weekly Reviews/."

Claude reads your meeting notes, synthesizes the patterns, and delivers a summary you would never have time to create yourself.

Workflow 2: The Research Synthesizer

"I just saved three new research notes about [topic] in my Resources folder. Read them alongside any existing notes I have on this topic. Create a synthesis note that: identifies the most important insights across all sources, flags any contradictions between sources, highlights gaps in my knowledge, and suggests what I should research next."

This is where the connected nature of Obsidian shines. Claude does not just summarize each note — it finds the connections and contradictions between them.

Workflow 3: The Idea Connector

"Search my entire vault for notes that are related to [[Current Project]] but are not currently linked to it. Look for relevant insights, past research, and ideas that I might have forgotten. List the top 10 connections with a one-sentence explanation of why each is relevant."

This workflow surfaces buried knowledge. That idea you had six months ago that is suddenly relevant to your current project? Claude finds it.

Workflow 4: The Knowledge Gap Finder

"Analyze my notes about [topic]. What subtopics have I not written about? What questions have I explored but not answered? What areas does my vault cover shallowly? Create a list of knowledge gaps ranked by importance."

Instead of figuring out what you do not know by yourself, let Claude audit your knowledge base and tell you.

Workflow 5: The Daily Briefing

"Read my daily notes from the past three days and my current project notes. Create a morning briefing that includes: what I was working on, what I planned to do next, any deadlines approaching in the next week, and suggestions for what to focus on today based on urgency and importance."

You wake up. You read a briefing your AI wrote overnight based on your own notes. You know exactly where you left off and what matters most.

Step 5: The AI-First Note Design Philosophy

There is a concept gaining traction in the Obsidian community called "AI-first note design." The idea: structure your notes so that AI can understand them as easily as you can.

Here is what that looks like in practice:

Every note gets machine-readable frontmatter. Tags, dates, project links, status. This lets Claude filter and search your vault efficiently.

Every note starts with a one-sentence preamble. "This note contains the key findings from our Q2 customer retention analysis." Claude reads this first and decides whether the note is relevant before reading the full content.

Every note uses consistent formatting. Headers for sections. Bold for key terms. Links for relationships. When every note follows the same structure, Claude can parse them reliably.

Sources are captured verbatim. When you save research, include the URL, author, date, and a direct quote. This lets Claude trace claims back to original sources when synthesizing your vault.

This takes slightly more effort when creating notes. But it makes every future AI interaction dramatically more effective.

## Step 6: Let Claude Maintain Your Vault

The reason most knowledge management systems fail is maintenance. People are great at adding notes. They are terrible at organizing, linking, and updating them.

Claude can handle all of that.

"Scan my Inbox folder for any notes that have been there for more than 3 days. For each one, suggest which folder it belongs in, add appropriate tags, and identify any existing notes it should be linked to."

"Check all notes in Projects/ for any that reference completed projects. Move them to Archive/ and update any links that point to them."

"Find notes in my vault that have zero incoming links — no other notes link to them. These are orphan notes. For each one, identify 2-3 existing notes that should link to it and explain why."

You built the vault. Claude maintains it. The system stays organized without you spending hours on housekeeping.

## Step 7: The Compounding Effect

A second brain that you use for one week is a note-taking app.

A second brain that you use for one month is a useful reference system.

A second brain that you use for six months is a knowledge engine that contains insights, connections, and accumulated wisdom that no amount of Googling can replicate.

And when Claude can access all of it, the value of every new note you add increases because it does not just sit in isolation — it connects to everything you have already written.

The person who builds this system now and maintains it for six months will have something that gives them a genuine, unreplicable advantage. Their AI assistant will know their work, their research, their projects, and their thinking in a way that no one else's AI can.

That is the real second brain. Not a note-taking app. A persistent, evolving knowledge system that thinks alongside you every single day.

Start today. Download Obsidian. Create five notes about what you are working on right now. Connect Claude. Ask it a question about your own notes. That first moment, when Claude answers using your own knowledge, changes everything.

Follow me @eng_khairallah1 for more AI courses, tools, and workflows. New content every week.

hope this was useful for you, Khairallah ❤️
