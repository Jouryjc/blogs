# Default Image Prompt: 蒸馏小余 Sketchnote

本仓库所有微信公众号封面和正文插图，除非用户明确指定其他风格，默认使用 Sketchnote / 蒸馏小余知识图解风格。

Core visual direction:

- Deep Research Sketchnote, hand-drawn technical explainer infographic.
- Chinese AI engineering / agent workflow education article, optimized for mobile WeChat reading.
- Prefer the reference style from 蒸馏小余 article https://mp.weixin.qq.com/s/GaEdNZRgPV4ofNXvJsJQjQ.
- Warm off-white / cream paper texture as the default background. Use low-saturation blue, mint, yellow, and pink sticky-note blocks.
- Deep navy thin hand-drawn outlines, rounded sticky-note panels, marker-like arrows, small corner doodle icons.
- Centered title, compact but readable information density, 3-5 concept blocks, arrows or comparison lanes, compact Chinese labels, bottom takeaway strip.
- Technical but friendly: explain architecture, workflow, trade-offs, failure modes, and mental models through sketches.
- Keep text short and readable in Chinese. Prefer labels such as "计划", "执行", "检查", "回滚", "自动化", "上下文", "子代理", "人工确认".

Avoid:

- Clean corporate PPT templates.
- Generic flat vector flowcharts.
- Photorealistic, 3D, cyberpunk, neon, glossy SaaS marketing poster, or stock illustration style.
- Dense unreadable text, tiny labels, cluttered diagrams, random English filler.
- Overly bright blue/orange full-background posters, excessive clouds/gears, loose decorative composition.

Only use a local reference image when the user explicitly asks for it or the current article prompt explicitly names it. Do not default to `raw/640.jpeg`. When a reference is used, borrow only the visual language; do not copy exact composition, text, branding, or protected visual details.
