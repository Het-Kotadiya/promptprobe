import argparse

from promptprobe.client import OllamaClient
from promptprobe.runner import load_prompts, run_tests, save_results
from promptprobe.reporter import generate_markdown, save_report, print_console_summary


def main():
    """Entry point: read command-line options and run the full PromptProbe pipeline."""
    parser = argparse.ArgumentParser(
        description="PromptProbe - a small LLM prompt-testing and red-teaming tool."
    )

    parser.add_argument(
        "--model",
        default="llama3.2:3b",
        help="Ollama model to test (default: llama3.2:3b)",
    )
    parser.add_argument(
        "--tests",
        default="data/test_prompts.yaml",
        help="Path to the YAML test file (default: data/test_prompts.yaml)",
    )
    parser.add_argument(
        "--json-out",
        default="reports/results.json",
        help="Where to save the JSON results log (default: reports/results.json)",
    )
    parser.add_argument(
        "--report-out",
        default="reports/report.md",
        help="Where to save the Markdown report (default: reports/report.md)",
    )

    args = parser.parse_args()

    # Build the pipeline using the user's chosen options
    print(f"Testing model: {args.model}")
    print(f"Loading tests from: {args.tests}\n")

    try:
        prompts = load_prompts(args.tests)
        client = OllamaClient(model=args.model)
        results = run_tests(prompts, client)
    except FileNotFoundError:
        print(f"ERROR: Could not find the test file '{args.tests}'. Check the path and try again.")
        return
    except RuntimeError as error:
        print(f"ERROR: {error}")
        return

    save_results(results, args.json_out)
    report = generate_markdown(results)
    save_report(report, args.report_out)

    print()
    print_console_summary(results)


if __name__ == "__main__":
    main()