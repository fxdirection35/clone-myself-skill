---
name: persona-interview
description: >-
  Build a personalized skill that captures a user's professional persona by
  interviewing them or extracting from info they provide upfront. Records
  industry, role, skills, tools, work habits, decision-making patterns, and
  communication style — then generates a complete SKILL.md that embodies that
  persona.
  You MUST trigger this skill whenever the user asks to: create or build a skill
  or AI persona ("帮我创建skill", "clone me as a skill", "build my persona",
  "根据我的资料生成skill", "生成一个能代表我的skill", "make an AI version of me",
  "我想搞一个跟我风格一样的AI", "来采访我吧然后生成skill"), generate a
  personalized skill from their professional background, or make an AI that
  mimics their work style. Also trigger when the user provides profile details
  like industry, role, and skills and asks you to turn that into a skill.
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

Examine the user's first message. There are two modes.

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

- If user provided a name → auto-generate: `<name>-persona` or `<name>-<role>`
- Ask user: "请问给这个 skill 取什么名字？(英文短名称)"
- In non-interactive context or no reply → auto-generate from their name or role

### Step 2: Generate skill content

Write a `SKILL.md` (and optionally a `README.md`) to `<pwd>/<skill-name>/`. The generated skill must include these sections:

```yaml
---
name: <name>
description: >-
  Embody <user>'s professional persona...
---
```

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

**Section 1: Persona Overview** — Who they are, industry, role, experience

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

**Section 3: Communication Style** — How they speak/write

**Section 4: Decision-Making Patterns** — How they approach problems

**Section 5: Workflow & Process** — How they organize work

**Section 6: Interaction Guidelines** — Do/Don't for interacting with/as this person

**Section 7: Example Scenarios** — 2-3 concrete examples

### Step 3: Generate a README.md (always)

Alongside SKILL.md, generate a `README.md` that briefly explains the skill:

```markdown
# <skill-name>

A persona skill for **<user's name/role>**.

## Usage

This skill is invoked when you need to respond or act as this person.
It captures their professional background, communication style, decision-making
patterns, and workflow preferences.

## Customization

Edit `SKILL.md` to add more details or adjust the persona.

## Generated

This skill was auto-generated by the persona-interview skill on <date>.
```

### Step 4: Save

Write both files to `D:\clone-myself-skill\<skill-name>\`:
- `SKILL.md`
- `README.md`

### Step 5: Confirm

Tell the user the skill was created. If there are gaps, mention they can edit the file to add more details.

---

## Limitations & Edge Cases

- **User refuses to answer** → mark as "not disclosed", don't press, move on or proceed to generation
- **Very little info** (user stops after 1-2 answers) → generate bare-bones skill with the "Missing Info" section filled out comprehensively
- **User asks to restart** → discard current profile, start fresh
- **Non-interactive context** (no response possible) → never wait; extract what you have, auto-generate, save the file
- **Inferred content** → ALWAYS label it as inferred vs user-provided in the generated skill
- **No user name provided** → use their role as identifier (e.g., `frontend-dev`, `product-manager`)
