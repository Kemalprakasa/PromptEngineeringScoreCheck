
import re, yaml
from typing import Dict, Any, List

def load_rubric(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def _match_any(text: str, patterns: List[str]) -> bool:
    text_low = text.lower()
    return any(p.lower() in text_low for p in patterns)

def evaluate_prompt(prompt: str, rubric: Dict[str, Any]) -> Dict[str, Any]:
    weights = rubric["weights"]
    rules = rubric["rules"]
    tips = rubric.get("tips", {})
    scores = {}
    details = {}

    for k, rule in rules.items():
        ok = _match_any(prompt, rule.get("any_of", []))
        scores[k] = weights.get(k, 0) if ok else 0
        details[k] = {
            "ok": ok,
            "weight": weights.get(k, 0),
            "tip": tips.get(k, "")
        }

    total = sum(scores.values())
    max_total = rubric["weights"]["total"]
    passed = total >= rubric["thresholds"]["pass_score"]

    # Extra heuristic: check presence of table/JSON markers
    format_bonus = 0
    if ("[" in prompt and "]" in prompt and "tabel" in prompt.lower()) or "{" in prompt:
        format_bonus = 0.5
        total += format_bonus

    return {
        "total": round(total, 2),
        "max_total": max_total + format_bonus,
        "passed": passed,
        "scores": scores,
        "details": details,
        "format_bonus": format_bonus
    }
