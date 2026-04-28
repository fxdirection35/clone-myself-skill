# persona-interview

A Claude Code skill that interviews you to build a detailed professional persona, then generates a personalized skill that embodies that persona. Also supports updating existing skills without restarting from scratch.

## How it works

1. **Tell it what you want** — Say something like "帮我创建一个skill" or "采访我生成一个skill"
2. **Provide your info** — Either upfront ("我是XX行业的YY岗位，有Z年经验...") or through one-at-a-time questions
3. **Get your persona skill** — A `SKILL.md` is generated in your working directory with Core Behavioral Principles, Communication Style, Decision Patterns, Example Scenarios, and more

You can stop the interview anytime by saying **"结束"**, **"停止"**, or **"stop"**.

## Installation

```bash
/plugin persona-interview
```

Or install the `.skill` file:

```bash
/plugin persona-interview.skill
```

## Features

### Creation Modes
- **Single-Shot Mode** — Provide all your info upfront (name, industry, role, skills, etc.) and get a complete persona skill immediately, no questions asked
- **Interactive Mode** — Claude asks one question at a time across 6 dimensions: basic info, career, skills, workflow, decision-making, communication style

### Update Mode — Update existing skills incrementally
- **Single-Shot Update** — Say "更新小明那个 skill，技能改成 ...，沟通风格改成 ..." and the skill is updated directly, no follow-up questions
- **Interactive Update** — Specify which skill and what categories to change; Claude asks targeted questions per category
- Backup file (`SKILL.md.bak`) is created before any update
- Before/after diff table shows what changed

### Generated Skill Quality
- **Core Behavioral Principles** — 3-5 actionable rules distilled from the persona (e.g., "Data over opinion", "Conservative rollout")
- **Coverage Summary** — Visual indicator showing what % is user-provided vs inferred vs missing (`🟢 4/6 类别 | 🟡 推断 2 项 | ⚪ 待补充: ...`)
- **Inference Labeling** — Clearly split between "Provided by the user" vs "Inferred from context" with confidence levels (high/medium/low)
- **Interaction Guidelines** — Persona-specific DO/DON'T derived from their actual work patterns
- **Example Scenarios** — 2-3 concrete scenarios in context→approach→output format
- **Missing Info Section** — If info is limited, includes a checklist of what to add, plus a tip to use update mode to fill gaps
- **Language Adaptation** — Generates in Chinese, English, or mixed — matching your input style

### Edge Case Handling
- Early termination ("stop") with minimum coverage check
- Non-interactive context fallback (never waits indefinitely)
- User refuses to answer — marked as "not disclosed", no pressure
- Very little info — generates bare-bones skill with detailed Missing Info section
- Frontmatter graceful degradation: no "Not specified with Not specified experience" anti-pattern
- Skill name auto-normalization (lowercase, hyphens, no special characters)

## Output

The skill saves to your current directory:

```
<your-skill-name>/
├── SKILL.md       # The persona skill — installable with /plugin
└── README.md      # Quick start guide
```

## Generated skill structure

Each generated `SKILL.md` includes (in order):
- **📋 待补充信息** (only if gaps exist) — Checklist of missing categories with update mode tip
- **Persona Overview** — Name, industry, role, experience + coverage summary
- **Core Behavioral Principles** — 3-5 prioritized rules for how to act as this person
- **Core Expertise** — User-provided vs inferred (confidence-labeled)
- **Communication Style** — How they speak and write
- **Decision-Making Patterns** — Risk posture, approach to trade-offs
- **Workflow & Process** — Daily/weekly rhythms, tools, project management
- **Interaction Guidelines** — Persona-specific DO/DON'T
- **Example Scenarios** — 2-3 context→approach→output examples

## Update workflow

```
User: "更新小明的 skill，技能加 SQL 和 Python"
  → Single-Shot Update detects: name + categories + values
  → Searches for 小明-product-manager/SKILL.md
  → Creates SKILL.md.bak backup
  → Shows diff table:
    | 类别 | 变更前 | 变更后 |
    | 技能 | Java, Go | Java, Go, SQL, Python |
  → Writes updated SKILL.md
  → Confirms changes
```

## Development

```
persona-interview/
├── SKILL.md              # The skill definition
├── evals/
│   └── evals.json        # Test cases (5 evals: full, partial, minimal, interactive, update)
├── scripts/
│   └── grade.py          # Evaluation grading script
└── workspace/            # Test run artifacts
```

Built with the [skill-creator](https://github.com/anthropics/claude-code/skills/skill-creator).
