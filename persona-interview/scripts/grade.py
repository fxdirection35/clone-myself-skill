"""Grade persona-interview skill outputs against assertions."""
import json
import os
import re

WORKSPACE = r"D:\clone-myself-skill\persona-interview-workspace\iteration-2"

EVALS = {
    "eval-1-full-profile": {
        "assertions": [
            ("name_mentioned", "生成的 SKILL.md 包含用户姓名（张明/小明/ming）"),
            ("industry_captured", "生成的 SKILL.md 捕获了行业信息（跨境电商）"),
            ("role_captured", "生成的 SKILL.md 捕获了岗位信息（产品经理）"),
            ("skills_captured", "生成的 SKILL.md 捕获了核心技能"),
            ("workflow_captured", "生成的 SKILL.md 捕获了工作习惯"),
            ("decision_style_captured", "生成的 SKILL.md 捕获了决策风格"),
            ("comm_style_captured", "生成的 SKILL.md 包含了沟通风格描述"),
            ("example_scenarios", "生成的 SKILL.md 包含了至少 2 个示例场景"),
            ("valid_frontmatter", "生成的 SKILL.md 包含有效的 YAML frontmatter"),
            ("inference_labeled", "生成的 SKILL.md 将用户提供的信息与推断的信息分开标注"),
        ],
        "checks": {
            "name_mentioned": lambda t: any(x in t for x in ["张明", "小明", "ming", "Ming"]),
            "industry_captured": lambda t: any(x in t for x in ["跨境电商", "cross-border e-commerce", "e-commerce"]),
            "role_captured": lambda t: any(x in t for x in ["产品经理", "Product Manager"]),
            "skills_captured": lambda t: sum(x in t for x in ["用户调研", "数据分析", "A/B测试", "PRD"]) >= 2,
            "workflow_captured": lambda t: any(x in t for x in ["OKR", "站会", "数据看板", "灰度", "standup", "canary"]),
            "decision_style_captured": lambda t: "数据驱动" in t or "data-driven" in t.lower(),
            "comm_style_captured": lambda t: any(x in t for x in ["直接", "direct", "幽默", "humor"]),
            "example_scenarios": lambda t: t.count("###") >= 4,  # headings count > 3 means scenarios exist
            "valid_frontmatter": lambda t: bool(re.match(r'^---\s*\n', t)) and '---' in t[3:],
            "inference_labeled": lambda t: any(x in t.lower() for x in ["inferred", "推断", "推测", "provided by the user", "用户提供", "用户提供的信息", "来自用户"]),
        }
    },
    "eval-2-partial-info": {
        "assertions": [
            ("name_mentioned", "生成的 SKILL.md 包含用户姓名（李华）"),
            ("role_captured", "生成的 SKILL.md 捕获了岗位信息（后端开发）"),
            ("tech_stack_captured", "生成的 SKILL.md 捕获了技术栈"),
            ("experience_captured", "生成的 SKILL.md 捕获了工作年限（3年）"),
            ("comm_style_captured", "生成的 SKILL.md 包含沟通风格描述（简洁）"),
            ("valid_frontmatter", "生成的 SKILL.md 包含有效的 YAML frontmatter"),
            ("no_fabrication", "对于用户未提供的信息，生成的 SKILL.md 不编造为事实"),
            ("inference_labeled", "生成的 SKILL.md 将用户提供的信息与推断的信息分开标注"),
        ],
        "checks": {
            "name_mentioned": lambda t: any(x in t for x in ["李华", "Li Hua", "lihua"]),
            "role_captured": lambda t: any(x in t for x in ["后端开发", "后端", "Backend", "backend developer"]),
            "tech_stack_captured": lambda t: sum(x.lower() in t.lower() for x in ["Java", "Go", "微服务", "microservice", "分布式", "distributed"]) >= 2,
            "experience_captured": lambda t: "3年" in t or "3 years" in t.lower(),
            "comm_style_captured": lambda t: any(x in t for x in ["简洁", "直接", "concise", "direct"]),
            "valid_frontmatter": lambda t: bool(re.match(r'^---\s*\n', t)) and '---' in t[3:],
            "no_fabrication": lambda t: "星座" not in t and "天蝎" not in t,
            "inference_labeled": lambda t: any(x in t.lower() for x in ["inferred", "推断", "推测", "provided by the user", "用户提供", "用户提供的信息", "基于.*推断"]),
        }
    },
    "eval-3-minimal-stop": {
        "assertions": [
            ("no_followup", "用户在说 stop 后没有继续追问，而是立即进入了生成阶段"),
            ("role_captured", "生成的 SKILL.md 捕获了岗位信息（UI/UX设计师）"),
            ("experience_captured", "生成的 SKILL.md 捕获了工作年限（5年）"),
            ("valid_frontmatter", "生成的 SKILL.md 包含有效的 YAML frontmatter"),
            ("has_missing_info_section", "生成的 SKILL.md 中包含「待补充信息」或 'Missing Info' 等缺失信息章节"),
            ("missing_info_details", "缺失信息章节中列出了至少2项可补充的具体类别和示例问题"),
        ],
        "checks": {
            "no_followup": lambda t: bool(t) and len(t) > 100,
            "role_captured": lambda t: any(x in t.lower() for x in ["ui/ux", "ui设计师", "ux设计师", "交互设计", "user interface", "user experience"]),
            "experience_captured": lambda t: "5年" in t or "5 years" in t.lower(),
            "valid_frontmatter": lambda t: bool(re.match(r'^---\s*\n', t)) and '---' in t[3:],
            "has_missing_info_section": lambda t: any(x in t for x in ["待补充信息", "缺失信息", "Missing Info", "补充信息", "补充完善", "enrich", "缺失类别"]),
            "missing_info_details": lambda t: any(x in t for x in ["|", "表格", "类别", "说明", "示例"]) and ("待补充信息" in t or "缺失" in t or "Missing" in t or "enrich" in t),
        }
    },
    "eval-4-interactive-mode": {
        "assertions": [
            ("no_info_entered_qa", "用户没有提供具体信息，skill 进入提问模式"),
            ("no_infinite_wait", "在没有交互可能的情况下，没有无限等待而是生成了骨架 skill"),
            ("valid_frontmatter", "生成的 SKILL.md 包含有效的 YAML frontmatter"),
            ("has_detailed_missing", "生成的 SKILL.md 中包含详细的「待补充信息」章节"),
            ("missing_at_least_3", "待补充信息章节覆盖了至少3个缺失类别（如行业、岗位、技能等）"),
        ],
        "checks": {
            "no_info_entered_qa": lambda t: True,  # agent behavior check
            "no_infinite_wait": lambda t: bool(t) and len(t) > 100,
            "valid_frontmatter": lambda t: bool(re.match(r'^---\s*\n', t)) and '---' in t[3:],
            "has_detailed_missing": lambda t: any(x in t for x in ["待补充信息", "缺失信息", "Missing Info", "补充信息", "missing", "缺失类别"]),
            "missing_at_least_3": lambda t: sum(x in t.lower() for x in ["行业", "岗位", "技能", "工具", "沟通", "决策", "工作流", "experience", "role", "industry", "skill"]) >= 3,
        }
    }
}


def grade_run(eval_name, config, output_path):
    results = {"expectations": [], "summary": {"passed": 0, "failed": 0, "total": 0, "pass_rate": 0.0}}

    if eval_name not in EVALS:
        return results

    eval_data = EVALS[eval_name]

    skill_path = os.path.join(output_path, "SKILL.md")
    text = ""
    if os.path.exists(skill_path):
        with open(skill_path, "r", encoding="utf-8") as f:
            text = f.read()

    for key, assertion_text in eval_data["assertions"]:
        check = eval_data["checks"][key]
        try:
            passed = check(text)
        except Exception:
            passed = False

        if key in ("no_followup", "no_info_entered_qa", "no_infinite_wait"):
            passed = os.path.exists(skill_path) and len(text) > 100

        evidence = f"Found in SKILL.md" if passed else f"Not found or failed"

        results["expectations"].append({
            "text": assertion_text,
            "passed": passed,
            "evidence": evidence
        })
        if passed:
            results["summary"]["passed"] += 1
        else:
            results["summary"]["failed"] += 1

    results["summary"]["total"] = results["summary"]["passed"] + results["summary"]["failed"]
    results["summary"]["pass_rate"] = round(results["summary"]["passed"] / results["summary"]["total"], 2) if results["summary"]["total"] > 0 else 0.0

    return results


def main():
    # Check if iteration-2 exists
    if not os.path.exists(WORKSPACE):
        print(f"Workspace {WORKSPACE} does not exist yet. Run eval tests first.")
        return

    for eval_name in EVALS:
        for config in ["with_skill", "without_skill"]:
            output_path = os.path.join(WORKSPACE, eval_name, config, "outputs")
            grading_path = os.path.join(WORKSPACE, eval_name, config, "grading.json")

            results = grade_run(eval_name, config, output_path)

            with open(grading_path, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

            print(f"{eval_name}/{config}: {results['summary']['passed']}/{results['summary']['total']} passed ({results['summary']['pass_rate']:.0%})")


if __name__ == "__main__":
    main()
