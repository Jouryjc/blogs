# Research Notes: Claude + Obsidian AI Second Brain

Created: 2026-05-31

## Source

- X article by Khairallah AL-Awady
  - URL: https://x.com/eng_khairallah1/status/2060652660773314833
  - Captured files:
    - `raw/source-fxtwitter-full.json`
    - `raw/source-normalized.md`
    - `raw/source-cover.jpg`
  - Main claim: Obsidian becomes more useful when Claude can read, search, reason over, and maintain a connected vault.
  - Original suggested structure: Inbox, Projects, Areas, Resources, Archive; then connect Claude through Projects, direct vault access, or MCP servers.

## Supplemental Sources

- Obsidian Help: data storage
  - URL: https://help.obsidian.md/data-storage
  - Key facts:
    - Obsidian stores notes as Markdown-formatted plain text files in a vault.
    - A vault is a folder on the local file system, including subfolders.
    - Plain text files can be edited by other editors and managed by file managers.
    - Vaults can sync with Obsidian Sync, Dropbox, iCloud, OneDrive, Git, and third-party services.

- Obsidian Help: internal links
  - URL: https://help.obsidian.md/links
  - Key facts:
    - Internal links connect notes and files into a network of knowledge.
    - Obsidian supports wikilinks like `[[Three laws of motion]]` and Markdown links.
    - If interoperability matters, wikilinks can be disabled in favor of Markdown links.
    - Block references are Obsidian-specific and do not work outside Obsidian.

- Claude Support: Projects
  - URL: https://support.claude.com/en/articles/9517075-what-are-projects
  - Key facts:
    - Projects are self-contained workspaces with their own chat histories and knowledge bases.
    - Users can upload documents, text, code, or other files to project knowledge.
    - Paid plans can automatically use RAG when project knowledge approaches context limits.
    - This is the easiest path, but not an automatically synced vault workflow.

- kepano/obsidian-skills
  - URL: https://github.com/kepano/obsidian-skills
  - Key facts:
    - Agent skills for Obsidian, covering Markdown, Bases, JSON Canvas, CLI, and Defuddle.
    - The README says these skills follow the Agent Skills specification and can be used by skills-compatible agents, including Claude Code and Codex CLI.
    - GitHub API on 2026-05-31: 33,664 stars, 2,370 forks.

- coddingtonbear/obsidian-local-rest-api
  - URL: https://github.com/coddingtonbear/obsidian-local-rest-api
  - Key facts:
    - Secure REST API and MCP server for an Obsidian vault.
    - GitHub API on 2026-05-31: 2,354 stars, 282 forks.

- MarkusPfundstein/mcp-obsidian
  - URL: https://github.com/MarkusPfundstein/mcp-obsidian
  - Key facts:
    - MCP server that interacts with Obsidian through the Obsidian Local REST API community plugin.
    - GitHub API on 2026-05-31: 3,809 stars, 451 forks.

## 5 Title Candidates

1. 推荐标题：别再囤笔记了：让 Claude 读懂你的 Obsidian
2. 稳妥标题：Claude + Obsidian：把 Markdown 笔记变成可用知识库
3. 大众标题：笔记越记越乱？用 Claude 把它变成工作流
4. 专家标题：Claude + Obsidian 工作流：Markdown、双链和 MCP 怎么选
5. 反差标题：第二大脑不是文件夹，真正有用的是可检索工作流

Chosen: 别再囤笔记了：让 Claude 读懂你的 Obsidian

## Article Promise

Explain why AI second brain systems fail when they only collect notes, then give a concrete Obsidian + Claude setup path for developers: file structure, note format, connection options, first workflows, and maintenance checks.

## Practical Asset

- A minimum vault structure.
- AI-friendly note template.
- Connection decision table.
- Five starter prompts for Claude + Obsidian.
- A weekly maintenance checklist.
