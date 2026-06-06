# Codex remote control source notes

Created: 2026-05-15 Asia/Shanghai

## Official OpenAI sources

- OpenAI product post, "Work with Codex from anywhere", published 2026-05-14:
  https://openai.com/index/work-with-codex-from-anywhere/
  - Codex is now in the ChatGPT mobile app, in preview.
  - Users can connect to machines where Codex is running, including a laptop, Mac mini, or managed remote environment.
  - Mobile can work across threads, review outputs, approve commands, change models, or start new work.
  - Files, credentials, permissions, and local setup remain on the host machine.
  - Updates stream back to phone, including screenshots, terminal output, diffs, test results, and approvals.
  - OpenAI says Codex uses a secure relay layer and does not expose trusted machines directly to the public internet.
  - Remote SSH is generally available; Codex desktop can detect hosts from SSH config and run threads in remote machines.
  - Availability: preview on iOS and Android across all plans including Free and Go in supported regions. Windows host connection support is coming soon.
  - Remote SSH and Hooks are available on all plans. Programmatic access tokens are available on Enterprise and Business plans. HIPAA-compliant use is for eligible ChatGPT Enterprise workspaces only in local environments.

- OpenAI Developers, "Remote connections":
  https://developers.openai.com/codex/remote-connections
  - Remote connections let users use Codex away from the machine running it, or when a project lives on another machine.
  - Remote access uses the connected host's projects, threads, files, credentials, permissions, plugins, Computer Use, browser setup, and local tools.
  - Users can start or continue threads, send follow-up instructions, approve actions, review outputs/diffs/test results/terminal output/screenshots, get notifications, and switch hosts.
  - Setup currently requires a Mac host running the Codex App; setup flow is not available from CLI or IDE extension.
  - Admins may need to enable Remote Control for ChatGPT workspaces.
  - SSH remote project threads run commands, read files, and write changes on the remote host.
  - Security guidance: use trusted SSH keys, least-privilege accounts, avoid unauthenticated public listeners, and use VPN/mesh networking for remote reachability instead of exposing the app server.

- OpenAI Developers, Codex changelog:
  https://developers.openai.com/codex/changelog
  - 2026-05-13: Codex mobile documentation added, including setup, connected-host behavior, security requirements, and troubleshooting.
  - 2026-05-05: Access token docs updated for trusted, non-interactive local workflows.

- OpenAI Help Center, "Using Codex with your ChatGPT plan":
  https://help.openai.com/en/articles/11369540
  - Codex is included with ChatGPT Plus, Pro, Business, Enterprise/Edu; for a limited time also included with Free and Go.
  - Remote Control may need workspace admin enablement or RBAC permission.

## X / Twitter primary posts

- OpenAI, 2026-05-14:
  https://x.com/openai/status/2055016850849993072
  - Announced Codex in the ChatGPT mobile app preview.
  - Says users can start new work, review outputs, steer execution, and approve next steps from ChatGPT mobile while Codex keeps running on laptop, Mac mini, or devbox.

- OpenAI Developers, 2026-05-14:
  https://x.com/openaidevs/status/2055016926213181608
  - Emphasizes phone access while Codex keeps working on the user's computer with files and project context in place.

- OpenAI, 2026-05-14:
  https://x.com/openai/status/2055016852133417389
  - Says preview is rolling out on iOS and Android in supported regions.
  - Says Windows host connection support is coming soon.

- Greg Brockman, 2026-05-14:
  https://x.com/gdb/status/2055034165968384099
  - Frames the update as using Codex from the ChatGPT app wherever Codex is running.

