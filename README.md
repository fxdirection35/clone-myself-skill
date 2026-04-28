# persona-interview

A Claude Code skill that interviews you to build a detailed professional persona, then generates a personalized skill that embeds that persona.

## How it works

1. **Tell it what you want** — Say something like "帮我创建一个skill" or "采访我生成一个skill"
2. **Provide your info** — Either upfront ("我是XX行业的YY岗位，有Z年经验...") or through one-at-a-time questions
3. **Get your persona skill** — A `SKILL.md` is generated in your working directory, ready to use

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

- **Two modes**: Single-shot (you provide info upfront) or interactive (Claude asks questions one at a time)
- **6 dimensions**: Industry, role, skills, workflow, decision-making, communication style
- **Inference labeling**: Generated skill clearly marks what you said vs what was inferred from context
- **Missing info section**: If info is limited, the generated skill includes a checklist of what to add
- **Language adaptation**: Generates in Chinese, English, or mixed — matching your input style
- **Early termination**: Say "stop" anytime; minimum coverage check ensures useful output

## Output

The skill saves to your current directory:

```
<your-skill-name>/
├── SKILL.md       # The persona skill — installable with /plugin
└── README.md      # Quick start guide
```

## Generated skill structure

Each generated `SKILL.md` includes:
- Persona Overview
- Core Expertise (user-provided vs inferred, clearly labeled)
- Communication Style
- Decision-Making Patterns
- Workflow & Process
- Interaction Guidelines
- Example Scenarios (2-3 role-specific examples)
- Missing Info (checklist for enriching the persona)

## Development

```
persona-interview/
├── SKILL.md              # The skill definition
├── evals/
│   └── evals.json        # Test cases
├── scripts/
│   └── grade.py          # Evaluation grading script
└── workspace/            # Trigger eval set for description tuning
```

Built with the [skill-creator](https://github.com/anthropics/claude-code/skills/skill-creator).
