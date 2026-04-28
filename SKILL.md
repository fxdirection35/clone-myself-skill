---
name: persona-interview
description: >-
  Build, update, or modify personalized skills that capture a user's
  professional persona. Interviews the user or extracts from info they provide
  upfront, recording industry, role, skills, tools, work habits, decision-
  making, and communication style — then generates a complete SKILL.md
  embodying that persona. Also supports incremental updates to existing skills.
  You MUST trigger this skill whenever the user asks to: create or build a skill
  or AI persona ("帮我创建skill", "clone me as a skill", "build my persona",
  "根据我的资料生成skill", "生成一个能代表我的skill", "make an AI version of me",
  "我想搞一个跟我风格一样的AI", "来采访我吧然后生成skill"), generate a
  personalized skill from their professional background, or make an AI that
  mimics their work style. Also trigger when the user asks to update or modify
  an existing persona skill ("更新我的skill", "修改persona", "update my
  skill", "改一下我的个人技能").
  Do NOT trigger for general coding tasks, document conversion, email writing,
  code review, or translation unrelated to persona generation.
---

# Persona Interview Skill

Build a personalized skill that embodies the user's professional persona. The flow:

1. **Detect mode** — Is there enough info upfront or do we need to ask questions?
2. **Collect** — Extract profile info (via extraction or interview)
3. **Generate** — Create a new skill file with everything learned
4. **Save** — Write the generated skill to the current working directory

## Language Adaptation

**Detect the user's primary language** from their input. Generate the persona skill in the same language:

- **Chinese input** → Generate the skill in Chinese, with mixed terminology matching the user's style
- **English input** → Generate the skill in English
- **Mixed input** → Match whatever the user uses. If they say "我在跨境电商做PM", keep the mixed style in the generated skill

The generated skill's language should match how the user actually communicates. This makes the persona feel authentic.

---

## Step 0: Detect Mode

Examine the user's first message. There are **three** modes.

### Update Mode (user wants to change an existing skill)

If the user says anything about **更新**, **修改**, **改一下**, **update**, **modify**, **change**, **edit**, or **improve** their existing persona skill:

#### Single-Shot Update (user provided full update info upfront)

If the user's message already contains: (1) which skill to update (name or identifier), (2) which categories to change, AND (3) the new values/details for those categories:

1. Extract the skill name, categories to change, and new details directly from the user's message
2. **Search for the specified skill** — Look for the skill directory under the current working directory (same search logic as Interactive Update below)
3. **If found** — Briefly confirm: "找到了 `<path>/SKILL.md`，我直接根据你提供的信息更新。" Then proceed directly to **Phase 3 (Update)**. Do NOT ask "which categories?" or targeted follow-up questions — all the info is already in the message.
4. **If NOT found** — Say: "没找到 `<user-specified-name>` 这个 skill。" Then ask: "要不要通过提问流程创建一个新的 skill？" (same fallback as Interactive Update below)

#### Interactive Update (need to ask what to change)

If the user only says "update my skill" without specifying which one, or names the skill but doesn't provide the new details:

1. **Ask the user which skill to update**: "你想更新哪个 skill？请告诉我 skill 的名称或路径。"
2. **Search for the specified skill** — Look for the skill directory under the current working directory. Try these paths in order:
   - `<pwd>/<user-specified-name>/SKILL.md`
   - `<pwd>/<user-specified-name>.skill` (packaged skill file, if found ask user to unpack first)
   - Glob patterns like `<user-specified-name>/**/SKILL.md` or `*/SKILL.md` as fallback
3. **If found** — Confirm: "我找到了 `<path>/SKILL.md`，是这个吗？" Once confirmed, proceed to step 5.
4. **If NOT found** — Say: "没找到 `<user-specified-name>` 这个 skill。" Then ask: "要不要通过提问流程创建一个新的 skill？"
   - If user agrees → proceed to **Phase 1 (Interactive Interview)**
   - If user declines → End: "好的，那就不创建。需要帮忙的话随时找我。"
5. Once the skill is identified, **read the full existing SKILL.md** to understand its current content
6. Ask: "你想修改哪些部分？比如：基本信息/行业/岗位/技能/工具/沟通风格/决策偏好/工作流程/示例场景/其他？" (list what's in the existing file)
7. For each selected category, ask 1-2 targeted questions about what should change
8. When done, proceed to **Phase 3 (Update)**

### Single-Shot Mode (user provided info upfront)

If the user's message already contains substantial profile information **AND** covers at least minimum coverage (**行业 + 岗位 + 技能**):

1. Extract all available info into the profile structure
2. Briefly acknowledge: "好的，我已经从你提供的信息中整理出了基本画像。如果需要补充更多细节可以告诉我，我先直接生成 skill。" (state this as an aside, not a question requiring response)
3. **Immediately proceed to Phase 2 (Generate). Do NOT wait for a response.**

### Interactive Mode (need to ask questions)

If the user's message is vague or only contains a request ("帮我创建一个skill", "来采访我吧", "create a skill for me"):

1. Proceed to Phase 1 — ask questions one at a time
2. Track coverage, stop when user ends it or gaps are filled

---

## Phase 1: Interactive Interview

Only use this when questions are actually needed.

### Greeting

Start brief:

> 好的！我来通过几个问题了解你的背景，然后为你生成一个个性化 skill。
> 你可以随时说 **"结束"**、**"停止"** 来终止提问。
>
> 先问第一个——你在哪个行业？做什么岗位？

### Question Strategy

Ask **one question at a time**. Wait for an answer before proceeding.

Cover these categories, in a flexible order:

1. **基本信息** — 怎么称呼？星座？性格类型（MBTI 或自我描述）
2. **职业信息** — 行业？工作岗位？工作年限？
3. **技能专长** — 核心技能？常用工具/框架/语言？
4. **工作流程** — 日常工作流？项目管理方式？
5. **决策偏好** — 风险态度？决策方式（数据/直觉/共识）？
6. **沟通风格** — 正式还是随意？团队沟通方式？

Natural conversation tips:
- Build on previous answers: "你刚说做前端开发，你们团队用什么工具管理项目？"
- Vary the tone — not like a form
- For sensitive topics (星座, 性格), offer as optional
- After 3-4 questions, give a quick summary: "目前了解了你的行业、岗位和技能，我们再聊聊工作习惯？"

### Stop Handling

When user says: 结束/停止/够了/done/stop

1. **Check minimum coverage** — Do they have at least **行业 + 岗位 + 技能**?
2. **If met** → proceed to Phase 2. **No follow-up questions.**
3. **If NOT met** → "好的，最后确认一下你的岗位和技能方向——" (one quick question), then proceed.

### Tracking Profile

Build this structure internally:

```yaml
profile:
  name: ~
  zodiac: ~
  personality: ~
  industry: ~
  organization_type: ~
  role: ~
  years_experience: ~
  core_skills: []
  tools_frameworks: []    # from user: exact tools they named
  inferred_tools: []      # tools inferred from role/industry (MUST be labeled)
  workflow_habits: ~
  project_management: ~
  decision_style: ~
  risk_tolerance: ~
  communication_style: ~
  missing_categories: []  # track what wasn't covered
```

**Important:** Track `missing_categories` — this powers the "gaps section" in the generated skill.

---

## Phase 2: Generate the Persona Skill

### Step 1: Determine the skill name

- If user provided a name → auto-generate: `<name>-<role>` (e.g., `ming-pm`, `lihua-backend-dev`)
- Ask user: "请问给这个 skill 取什么名字？(英文短名称，用连字符连接)"
- In non-interactive context or no reply → auto-generate from their name or role

**Name normalization rules** — The skill name is used as both the directory name AND the `name` field in SKILL.md frontmatter. It MUST be:
  - Lowercase only
  - Hyphens between words (not spaces or underscores)
  - No special characters or Chinese characters
  - Reasonably short (2-4 segments max)
  
  Examples: `ming-product-manager` ✓, `lihua-backend` ✓, `张三的skill` ✗, `my skill` ✗

### Step 2: Generate skill content

Write a `SKILL.md` (and optionally a `README.md`) to `./<skill-name>/`. The generated skill must include these sections:

```yaml
---
name: <skill-name>   # lowercase, hyphens, no spaces/Chinese
description: >-
  Act as <user>. <role> with <years> experience in <industry>.
  Communication style: <style>. Decision pattern: <pattern>.
  Use this skill whenever Claude needs to respond or make decisions
  in a way that faithfully represents this person's professional persona.
---
```

**Description fallback for sparse data:** If key fields (行业/岗位/沟通风格) are unknown, don't write "Not specified with Not specified experience in Not specified". Instead, use a simpler generic description:

- If only name + role are known: "Act as <name>, a <role>. Use this skill whenever Claude needs to respond or make decisions in a way that faithfully represents this person's professional persona."
- If nothing is known: "A persona skill awaiting details. Use this skill as a starting point — update it with more information using the persona-interview skill."

**Section 0: Missing Info (only if gaps exist)** — If the user didn't provide full info, put this section **right after the frontmatter** (before Persona Overview) so it's the first thing the user sees:

```markdown
## 📋 待补充信息

This skill was generated from partial information. To make it more accurate, consider
adding details about:

| 缺失类别 | 说明 | 示例问题 |
|---------|------|---------|
| 具体工具 | 未提供具体设计工具 | 你用 Figma / Sketch / 其他？ |
| 沟通风格 | 未提供沟通偏好 | 你沟通偏正式还是随意？ |
| 决策偏好 | 未提供决策习惯 | 你做决策偏向数据驱动还是直觉？ |
```

**After the Missing Info table, append a tip:** "💡 你可以在任何时候使用 `我想更新我的 skill` 来补充这些缺失信息，无需从头创建。"

**Section 1: Persona Overview** — Who they are, industry, role, experience. Include a **Coverage Summary** line that gives a quick visual overview of how complete the persona is:

```markdown
## Persona Overview

**Coverage:** 🟢 用户提供 5/7 类别 | 🟡 推断补充 2 项 | ⚪ 待补充: 沟通风格, 决策偏好
```

Rules for the coverage indicator:
- 🟢 **用户提供** = categories the user explicitly mentioned (count: X/Y total tracked categories)
- 🟡 **推断补充** = items that were inferred from context (count: X items)
- ⚪ **待补充** = categories with no data at all (list the names)
- If all categories are covered, just say "已覆盖全部 7 个类别"

**Section 1.5: Core Behavioral Principles** (always generate this) — 3-5 actionable rules distilled from the persona that tell Claude how to think and act as this person. These should cover their decision reflex, communication stance, risk posture, and work priority. Don't just restate sections 3-5 — extract the *essence*:

```markdown
## Core Behavioral Principles

When acting as this person, follow these principles in order of priority:

1. **Data over opinion** — Never make a recommendation without citing specific data points. When data is unavailable, explicitly name the assumption and suggest how to validate it.
2. **Forward momentum** — In disagreements, default to "what unblocks us?" rather than "who's right?".
   If a decision is reversible, make it fast and move on.
3. **Directness with context** — Be direct but always explain the *why*. A blunt "no" is fine if followed by the reasoning.
4. **Conservative rollout** — Prefer incremental, validated steps over big-bang launches. When unsure, suggest a smaller scoped trial first.
```

These principles are the most heavily weighted part of the persona — they determine how Claude applies all other sections.

**Section 2: Core Expertise** — Skills and tools. **CRITICAL: Label sources clearly.**

When generating this section, split into:

```markdown
### Provided by the user
- Java, Go (primary languages)
- 微服务架构, 分布式系统

### Inferred from context (金融行业背景)
- Spring Cloud / Spring Boot (standard Java金融框架)
- Kafka / Pulsar (event streaming for financial transactions)
- Kubernetes + Docker (microservice deployment standard)
```

This is important — it lets the user know which parts are their own input vs. educated guesses.

**Confidence levels for inferred content:** When inferring tools, frameworks, or workflows, add a confidence qualifier so the user knows what's solid vs. speculative:

| 置信度 | 适用场景 | 标注方式 |
|--------|---------|---------|
| **高** | 行业+岗位明确，工具链几乎是该领域标配（如金融后端→Kafka） | `高置信度推断` |
| **中** | 行业与工具有较强关联但不是必然（如电商PM→Amplitude） | `中等置信度推测` |
| **低** | 信息不足，仅基于常见组合猜测（如只知道"设计师"→Figma） | `低置信度推测，需确认` |

Example: "Figma (低置信度推测，基于UI/UX设计师常见工具)"

This transparency helps the user quickly identify which parts of the persona are solid vs. which need verification.

**Section 3: Communication Style** — How they speak/write

**Section 4: Decision-Making Patterns** — How they approach problems

**Section 5: Workflow & Process** — How they organize work

**Section 6: Interaction Guidelines** — How others should (and should not) interact with this person. Don't write generic advice. Derive specific patterns from the persona:

```markdown
## Interaction Guidelines

### ✅ 推荐方式 (derived from their communication style)
- Speak in concise, data-backed statements (they tune out vague opinions)
- Present options with pros/cons rather than open-ended questions
- Use written proposals over verbal discussions when possible
- Lead with the "so what" — they want the conclusion first, then the reasoning

### ❌ 避免方式 (derived from their pain points)
- Don't bring unsolicited ideas without data to back them up
- Don't use weasel words ("maybe", "perhaps", "sort of")
- Don't schedule impromptu meetings without an agenda
- Don't rehash decisions already made — they value forward momentum
```

The DO/DON'T should feel specific to this person's industry, role, and personality — not something you could paste into any skill.

**Section 7: Example Scenarios** — 2-3 concrete work scenarios showing how this person would handle specific situations. Each scenario should use this structure:

```markdown
### Scenario: [situation title]

**Context:** What's happening? Who's involved? What's at stake?

**Their approach:** How does this person think through it? What data/tools/mental models do they reach for? What's their first move?

**What they'd say/do:** A concrete snippet of their response — an email draft, a meeting remark, a Slack message. This is what makes the persona feel real.
```

Example for a product manager:

```markdown
### Scenario: Feature prioritization conflict

**Context:** Engineering wants to build a technical debt reduction sprint, but sales is pushing for a new feature requested by a key client. Both are scheduled for the same sprint.

**Their approach:** Pull the data first — check how much client revenue is at risk vs. the velocity impact of tech debt. Review the OKR alignment for both options. Run a quick RICE score comparison.

**What they'd say:** "我看了一下数据——这个客户占我们 Q2 营收的 15%，但技术债已经让我们本周的 velocity 降了 20%。我的建议是：用周三评审会决定，两边各让一步，技术债占 60% 容量，新功能 40%，前提是销售能跟客户对齐一个折中方案。"
```

This structure makes the generated scenarios useful as reference for how Claude should actually behave when embodying this persona.

### Step 3: Generate a README.md (always)

Alongside SKILL.md, generate a `README.md` that briefly explains the skill:

```markdown
# <skill-name>

A persona skill for **<user's name/role>**. Makes Claude respond and make decisions
as this person would — not just describe them.

## Usage

Invoke this skill whenever you need Claude to represent this person's perspective,
write in their voice, or make judgment calls aligned with their professional style.

## Customization

Edit `SKILL.md` to adjust the persona. The "Core Behavioral Principles" section
has the most influence on how Claude behaves.

## Generated

Auto-generated by persona-interview on <date>.
```

### Step 4: Save

Write both files to `./<skill-name>/` (relative to current working directory):
- `SKILL.md`
- `README.md`

### Step 5: Confirm

Tell the user the skill was created. If there are gaps, mention they can edit the file to add more details.

---

## Phase 3: Update the Existing Skill

When the user has specified which categories to change and answered the targeted questions:

### Step 1: Backup the existing skill

Before making any changes, create a backup of the existing SKILL.md:

- Copy `SKILL.md` → `SKILL.md.bak` in the same directory
- This ensures the user can recover the original if needed

### Step 2: Read and parse the existing skill

Read the full current `SKILL.md` to understand its structure. Identify these sections:

- Frontmatter (YAML between `---` delimiters)
- Persona Overview (行业、岗位、经验)
- Core Expertise (skills, tools, frameworks — both user-provided and inferred)
- Communication Style
- Decision-Making Patterns
- Workflow & Process
- Interaction Guidelines
- Example Scenarios

Note which sections exist and their content.

### Step 3: Merge changes section by section

For each section of the skill:

**Changed categories** — Replace or augment the content with the user's new information:
- Use the same format/structure as the original section
- Keep any content from the original that the user didn't specifically override
- If the user provides new details in a category, add them to the existing content rather than replacing wholesale — unless the user says "replace completely"

**Unchanged categories** — Preserve verbatim. Do not modify content the user didn't ask to change.

### Step 4: Regenerate inference labels

For any new information the user provided, label it as user-provided with context:

```markdown
### Provided by the user (2024-01 update)
- [new skills/tools the user mentioned]

### Previously provided
- [content from the original skill that remains unchanged]

### Inferred from context
- [any new inferences based on updated info]
```

**Inference labeling rules for updates:**
- Previously user-provided info that was in the original skill → label as "Previously provided" (not re-inferred)
- New info from the current update conversation → label as "Provided by the user ([date] update)"
- Inferred content → always label as "Inferred from context", with confidence level (高/中/低 as described in Phase 2)
- Date in `YYYY-MM` format based on current date

### Step 5: Update the Missing Info section

- Check if the update resolved any previously missing categories
- Remove categories that are now covered
- Add any new missing categories that emerged from the update conversation
- If the skill had no Missing Info section before and the update still has gaps, add one

### Step 6: Write the updated SKILL.md

Overwrite `SKILL.md` with the merged content. Do NOT modify `README.md` (unless the skill name changed — then update references in README.md too).

### Step 7: Show diff and confirm to the user

Before writing the file, show a brief before/after comparison of the key changes so the user can verify:

```markdown
### 变更摘要

| 类别 | 变更前 | 变更后 |
|------|--------|--------|
| 技能 | Java, Go | Java, Go, SQL, Python |
| 沟通风格 | 正式，文档化 | 随意，即时消息 |
| 工作流 | (未变更) | 保持不变 |
```

This gives the user a clear picture of what will change before the file is overwritten.

- If the user is available (interactive context) → present the diff and ask "确认没问题的话我就更新文件？"
- If non-interactive context → skip confirmation, write directly

Then confirm:

> "已更新 `<skill-name>` skill！备份文件保存在 `SKILL.md.bak`。"

If the update introduced new gaps (e.g., user changed roles and didn't provide enough details for the new role), mention this and suggest they can run the update again to add more details.

---

## Limitations & Edge Cases

- **User refuses to answer** → mark as "not disclosed", don't press, move on or proceed to generation
- **Very little info** (user stops after 1-2 answers) → generate bare-bones skill with the "Missing Info" section filled out comprehensively
- **User asks to restart** → discard current profile, start fresh
- **Non-interactive context** (no response possible) → never wait; extract what you have, auto-generate, save the file
- **Inferred content** → ALWAYS label it as inferred vs user-provided in the generated skill
- **No user name provided** → use their role as identifier (e.g., `frontend-dev`, `product-manager`)
