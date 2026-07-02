from collections import Counter, defaultdict


def generate_markdown(results):
    """Turn a list of results into a structured Markdown report (as a single string)."""
    lines = []

    lines.append("# PromptProbe Report")
    lines.append("")

    # --- Summary section: count how many of each verdict ---
    verdict_counts = Counter(result["verdict"] for result in results)

    lines.append("## Summary")
    lines.append(f"- **Total tests:** {len(results)}")
    for verdict, count in verdict_counts.items():
        lines.append(f"- **{verdict}:** {count}")
    lines.append("")

    # --- Group the results by their category ---
    grouped = defaultdict(list)
    for result in results:
        category = result.get("category", "uncategorized")
        grouped[category].append(result)

    # --- Write a section for each category ---
    for category, items in grouped.items():
        lines.append(f"## Category: {category}")
        lines.append("")

        for result in items:
            owasp = result.get("owasp", "N/A")
            lines.append(f"### {result['id']}")
            lines.append(f"- **Verdict:** {result['verdict']}")
            lines.append(f"- **OWASP:** {owasp}")
            lines.append(f"- **Prompt:** {result['prompt']}")
            lines.append(f"- **Response:** {result['response']}")
            lines.append("")

    return "\n".join(lines)


def save_report(report_text, filepath):
    """Write the report text to a file."""
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(report_text)
    print(f"Saved report to {filepath}")